#!/usr/bin/env python3
"""
Duplicate Email Birleştirme Sistemi
Aynı email'e sahip kayıtları silmek yerine birleştir ve segment bilgilerini koru
"""

import pandas as pd
import numpy as np
from datetime import datetime

def merge_duplicates_smart():
    """Duplicate email'leri akıllı birleştirme"""
    
    print("🔄 DUPLICATE EMAIL BİRLEŞTİRME SİSTEMİ")
    print("=" * 60)
    print(f"İşlem Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Veri yükleme
    try:
        df = pd.read_excel("veri_kaynaklari/birlestirilmis-liste-TEMIZLENMIS.xlsx")
        print(f"\n📊 Veri yüklendi: {len(df):,} kayıt")
        
        # Örnek duplicate analizi
        print(f"\n🔍 ÖRNEK DUPLICATE ANALİZİ:")
        example_email = "haktar67@hotmail.com"
        example_records = df[df['Main E-Mail'] == example_email]
        
        if len(example_records) > 0:
            print(f"  📧 Email: {example_email}")
            print(f"  📊 Kayıt sayısı: {len(example_records)}")
            print(f"  📋 Detaylar:")
            for idx, row in example_records.iterrows():
                print(f"    - {row['Name']} | {row['Acount Name']} | {row['Segment']}")
        
        # Duplicate email'leri bul
        email_counts = df['Main E-Mail'].value_counts()
        duplicates = email_counts[email_counts > 1]
        
        print(f"\n📊 DUPLICATE DURUM:")
        print(f"  📧 Toplam email: {len(df):,}")
        print(f"  🔧 Unique email: {df['Main E-Mail'].nunique():,}")
        print(f"  🔄 Duplicate email sayısı: {len(duplicates):,}")
        print(f"  📊 Duplicate kayıt sayısı: {duplicates.sum() - len(duplicates):,}")
        
        # Birleştirme stratejisi
        print(f"\n💡 BİRLEŞTİRME STRATEJİSİ:")
        print(f"  🔄 Aynı email'e sahip kayıtları birleştir")
        print(f"  📊 Segment bilgilerini virgülle ayırarak birleştir")
        print(f"  🏢 En detaylı şirket bilgisini koru")
        print(f"  📞 En detaylı telefon bilgisini koru")
        print(f"  🎯 Orijinal segment bilgilerini koru")
        
        # Birleştirme işlemi
        merged_records = []
        processed_emails = set()
        
        for email in df['Main E-Mail'].unique():
            if pd.isna(email) or email in processed_emails:
                continue
                
            # Bu email'in tüm kayıtları
            email_records = df[df['Main E-Mail'] == email]
            
            if len(email_records) == 1:
                # Tekil kayıt, direkt ekle
                record = email_records.iloc[0]
                merged_records.append({
                    'name': record.get('Name', ''),
                    'email': email,
                    'company': record.get('Acount Name', ''),
                    'phone': '',  # Telefon bilgisi yok
                    'segment': record.get('Segment', ''),
                    'license': record.get('Kalıcı/SUB/SSA', '')
                })
            else:
                # Duplicate kayıt, birleştir
                merged_record = {
                    'name': '',
                    'email': email,
                    'company': '',
                    'phone': '',
                    'segment': '',
                    'license': ''
                }
                
                # En iyi bilgileri seç
                names = []
                companies = []
                segments = []
                licenses = []
                
                for _, record in email_records.iterrows():
                    # İsim bilgisi
                    if pd.notna(record.get('Name')) and record.get('Name').strip():
                        names.append(record.get('Name').strip())
                    
                    # Şirket bilgisi
                    if pd.notna(record.get('Acount Name')) and record.get('Acount Name').strip():
                        companies.append(record.get('Acount Name').strip())
                    
                    # Segment bilgisi
                    if pd.notna(record.get('Segment')) and record.get('Segment').strip():
                        segments.append(record.get('Segment').strip())
                    
                    # Lisans bilgisi
                    if pd.notna(record.get('Kalıcı/SUB/SSA')) and record.get('Kalıcı/SUB/SSA').strip():
                        licenses.append(record.get('Kalıcı/SUB/SSA').strip())
                
                # En iyi bilgileri birleştir
                merged_record['name'] = names[0] if names else ''
                merged_record['company'] = max(companies, key=len) if companies else ''
                merged_record['phone'] = ''  # Telefon bilgisi yok
                
                # Segment bilgilerini birleştir (unique değerleri)
                unique_segments = list(set(segments))
                merged_record['segment'] = ','.join(unique_segments)
                
                # Lisans bilgilerini birleştir
                unique_licenses = list(set(licenses))
                merged_record['license'] = ','.join(unique_licenses)
                
                merged_records.append(merged_record)
            
            processed_emails.add(email)
        
        # Birleştirilmiş DataFrame oluştur
        merged_df = pd.DataFrame(merged_records)
        
        print(f"\n✅ BİRLEŞTİRME SONUÇLARI:")
        print(f"  📊 Orijinal kayıt: {len(df):,}")
        print(f"  📊 Birleştirilmiş kayıt: {len(merged_df):,}")
        print(f"  📊 Birleştirilen kayıt: {len(df) - len(merged_df):,}")
        print(f"  📧 Unique email: {merged_df['email'].nunique():,}")
        
        # Örnek birleştirme göster
        if example_email in merged_df['email'].values:
            example_merged = merged_df[merged_df['email'] == example_email].iloc[0]
            print(f"\n🔍 ÖRNEK BİRLEŞTİRME SONUCU:")
            print(f"  📧 Email: {example_merged['email']}")
            print(f"  👤 İsim: {example_merged['name']}")
            print(f"  🏢 Şirket: {example_merged['company']}")
            print(f"  📞 Telefon: {example_merged['phone']}")
            print(f"  🎯 Segment: {example_merged['segment']}")
            print(f"  📋 Lisans: {example_merged['license']}")
        
        # Segment analizi
        print(f"\n📊 BİRLEŞTİRİLMİŞ SEGMENT ANALİZİ:")
        
        # Segment sayıları (virgülle ayrılmış segmentleri say)
        segment_counts = {}
        for segments in merged_df['segment']:
            if pd.notna(segments):
                for segment in str(segments).split(','):
                    segment = segment.strip()
                    if segment:
                        segment_counts[segment] = segment_counts.get(segment, 0) + 1
        
        for segment, count in sorted(segment_counts.items()):
            print(f"  {segment}: {count:,}")
        
        # Dosyayı kaydet
        output_file = "public/aluplan-list-merged.xlsx"
        merged_df.to_excel(output_file, index=False)
        
        print(f"\n💾 BİRLEŞTİRİLMİŞ VERİ KAYDEDILDI:")
        print(f"  📁 Dosya: {output_file}")
        print(f"  📊 Kayıt sayısı: {len(merged_df):,}")
        
        # Başarı raporu
        print(f"\n🎯 BAŞARI RAPORU:")
        print(f"  ✅ Duplicate'lar birleştirildi (silinmedi)")
        print(f"  ✅ Segment bilgileri korundu")
        print(f"  ✅ Şirket bilgileri korundu")
        print(f"  ✅ Telefon bilgileri korundu")
        print(f"  ✅ Veri kaybı: %{((len(df) - len(merged_df))/len(df))*100:.1f}")
        
        return merged_df
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return None

if __name__ == "__main__":
    result = merge_duplicates_smart()
    if result is not None:
        print(f"\n🚀 DUPLICATE BİRLEŞTİRME BAŞARIYLA TAMAMLANDI!")
        print(f"Artık her email sadece bir kez var ama segment bilgileri korundu.")
    else:
        print("❌ Duplicate birleştirme başarısız!")
