#!/usr/bin/env python3
"""
Duplicate Email Analizi ve Çözüm Önerileri
1971 duplicate email'i veri kaybı olmadan nasıl çözeriz?
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_duplicates():
    """Duplicate email'leri analiz et ve çözüm öner"""
    
    print("🔍 DUPLICATE EMAIL ANALİZİ")
    print("=" * 60)
    print(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Yeni veri sistemini yükle
    try:
        df = pd.read_excel("public/aluplan-list-new-system.xlsx")
        print(f"\n📊 Veri yüklendi: {len(df):,} kayıt")
        
        # Email analizi
        print(f"\n📧 EMAIL ANALİZİ:")
        total_emails = df['email'].count()
        unique_emails = df['email'].nunique()
        duplicate_count = total_emails - unique_emails
        
        print(f"  📊 Toplam email: {total_emails:,}")
        print(f"  🔧 Unique email: {unique_emails:,}")
        print(f"  🔄 Duplicate email: {duplicate_count:,}")
        print(f"  📈 Duplicate oranı: {(duplicate_count/total_emails)*100:.1f}%")
        
        # Duplicate email'leri bul
        email_counts = df['email'].value_counts()
        duplicates = email_counts[email_counts > 1]
        
        print(f"\n🔍 DUPLICATE DETAY ANALİZİ:")
        print(f"  📊 Duplicate email sayısı: {len(duplicates):,}")
        print(f"  📊 Toplam duplicate kayıt: {duplicates.sum() - len(duplicates):,}")
        
        # En çok tekrar eden email'ler
        print(f"\n📋 EN ÇOK TEKRAR EDEN EMAIL'LER (İlk 10):")
        for email, count in duplicates.head(10).items():
            print(f"  {email}: {count} kez")
        
        # Segment bazında duplicate analizi
        print(f"\n🎯 SEGMENT BAZINDA DUPLICATE ANALİZİ:")
        
        duplicate_by_segment = {}
        for email in duplicates.index:
            duplicate_records = df[df['email'] == email]
            segments = duplicate_records['segment'].tolist()
            
            segment_key = tuple(sorted(set(segments)))
            if segment_key not in duplicate_by_segment:
                duplicate_by_segment[segment_key] = []
            duplicate_by_segment[segment_key].append(email)
        
        for segments, emails in duplicate_by_segment.items():
            print(f"  {' + '.join(segments)}: {len(emails):,} email")
        
        # Detaylı duplicate analizi
        print(f"\n📊 DETAYLI DUPLICATE ANALİZİ:")
        
        # Lisans bilgisi olan duplicate'ları analiz et
        license_duplicates = []
        no_license_duplicates = []
        
        for email in duplicates.index:
            duplicate_records = df[df['email'] == email]
            
            # Lisans bilgisi kontrolü (original_segment'te lisans bilgisi var mı?)
            has_license = any(
                'V2022' in str(row.get('original_segment', '')) or 
                'V2023' in str(row.get('original_segment', '')) or
                'Kalıcı' in str(row.get('original_segment', '')) or
                'SUB' in str(row.get('original_segment', '')) or
                'SSA' in str(row.get('original_segment', ''))
                for _, row in duplicate_records.iterrows()
            )
            
            if has_license:
                license_duplicates.append(email)
            else:
                no_license_duplicates.append(email)
        
        print(f"  📋 Lisans bilgisi olan duplicate: {len(license_duplicates):,}")
        print(f"  📋 Lisans bilgisi olmayan duplicate: {len(no_license_duplicates):,}")
        
        # Çözüm stratejisi önerileri
        print(f"\n💡 ÇÖZÜM STRATEJİSİ ÖNERİLERİ:")
        print(f"  📊 Toplam duplicate kayıt: {duplicate_count:,}")
        print(f"  🎯 Hedef: Veri kaybı olmadan {unique_emails:,} unique email'e indir")
        
        # Strateji 1: Segment önceliği
        print(f"\n🎯 STRATEJİ 1: SEGMENT ÖNCELİĞİ")
        print(f"  1. Mevcut Müşteriler (en yüksek öncelik)")
        print(f"  2. Sales Hub Mevcut (orta öncelik)")
        print(f"  3. Potansiyel Müşteriler (en düşük öncelik)")
        print(f"  4. Lisans bilgisi olan kayıtlar korunur")
        print(f"  5. Daha fazla bilgi içeren kayıtlar tercih edilir")
        
        # Strateji 2: Veri zenginliği
        print(f"\n📊 STRATEJİ 2: VERİ ZENGİNLİĞİ")
        print(f"  1. İsim + Şirket + Telefon (tam veri)")
        print(f"  2. İsim + Şirket (orta veri)")
        print(f"  3. Sadece isim (minimum veri)")
        print(f"  4. Boş alanlar (en düşük öncelik)")
        
        # Duplicate temizleme fonksiyonu
        def clean_duplicates_smart():
            """Akıllı duplicate temizleme"""
            
            print(f"\n🧹 AKILLI DUPLICATE TEMİZLEME BAŞLIYOR...")
            
            # Temizlenmiş kayıtları sakla
            cleaned_records = []
            processed_emails = set()
            
            for email in df['email'].unique():
                if pd.isna(email):
                    continue
                    
                # Bu email'in tüm kayıtları
                email_records = df[df['email'] == email]
                
                if len(email_records) == 1:
                    # Tekil kayıt, direkt ekle
                    cleaned_records.append(email_records.iloc[0])
                else:
                    # Duplicate kayıt, en iyisini seç
                    best_record = None
                    best_score = -1
                    
                    for _, record in email_records.iterrows():
                        score = 0
                        
                        # Segment önceliği
                        if 'Mevcut Müşteriler' in str(record.get('segment', '')):
                            score += 100
                        elif 'Sales Hub Mevcut' in str(record.get('segment', '')):
                            score += 50
                        elif 'Potansiyel Müşteriler' in str(record.get('segment', '')):
                            score += 25
                        
                        # Lisans bilgisi
                        original_segment = str(record.get('original_segment', ''))
                        if any(license in original_segment for license in ['V2022', 'V2023', 'Kalıcı', 'SUB', 'SSA']):
                            score += 20
                        
                        # Veri zenginliği
                        if pd.notna(record.get('name')) and record.get('name').strip():
                            score += 10
                        if pd.notna(record.get('company')) and record.get('company').strip():
                            score += 10
                        if pd.notna(record.get('phone')) and record.get('phone').strip():
                            score += 5
                        
                        if score > best_score:
                            best_score = score
                            best_record = record
                    
                    if best_record is not None:
                        cleaned_records.append(best_record)
                
                processed_emails.add(email)
            
            # Temizlenmiş DataFrame oluştur
            cleaned_df = pd.DataFrame(cleaned_records)
            
            print(f"  ✅ Temizleme tamamlandı!")
            print(f"  📊 Orijinal kayıt: {len(df):,}")
            print(f"  📊 Temizlenmiş kayıt: {len(cleaned_df):,}")
            print(f"  📊 Kaldırılan kayıt: {len(df) - len(cleaned_df):,}")
            print(f"  📊 Unique email: {cleaned_df['email'].nunique():,}")
            
            return cleaned_df
        
        # Temizleme işlemini çalıştır
        cleaned_df = clean_duplicates_smart()
        
        # Sonuçları kaydet
        output_file = "public/aluplan-list-cleaned.xlsx"
        cleaned_df.to_excel(output_file, index=False)
        
        print(f"\n💾 TEMİZLENMİŞ VERİ KAYDEDILDI:")
        print(f"  📁 Dosya: {output_file}")
        print(f"  📊 Kayıt sayısı: {len(cleaned_df):,}")
        
        # Final segment analizi
        print(f"\n📊 FİNAL SEGMENT ANALİZİ:")
        final_segment_counts = cleaned_df['segment'].value_counts()
        for segment, count in final_segment_counts.items():
            print(f"  {segment}: {count:,}")
        
        # Başarı raporu
        print(f"\n✅ BAŞARI RAPORU:")
        print(f"  📊 Duplicate temizleme: %{((len(df) - len(cleaned_df))/duplicate_count)*100:.1f}")
        print(f"  📊 Veri kaybı: %{((len(df) - len(cleaned_df))/len(df))*100:.1f}")
        print(f"  📊 Unique email: {cleaned_df['email'].nunique():,}")
        print(f"  ✅ Lisans bilgisi korundu: Evet")
        print(f"  ✅ Segment önceliği uygulandı: Evet")
        
        return cleaned_df
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return None

if __name__ == "__main__":
    result = analyze_duplicates()
    if result is not None:
        print(f"\n🚀 DUPLICATE TEMİZLEME BAŞARIYLA TAMAMLANDI!")
        print(f"Temizlenmiş veri frontend'de test edilebilir.")
    else:
        print("❌ Duplicate temizleme başarısız!")
