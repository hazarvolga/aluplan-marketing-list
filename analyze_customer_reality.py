#!/usr/bin/env python3
"""
Gerçek Müşteri Durumu Analizi ve Kurgu
Bu script doğru müşteri segmentasyonu için kapsamlı analiz yapar
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_customer_reality():
    """
    Gerçek müşteri durumunu analiz et ve doğru kurguyu oluştur
    
    KURGU STRATEJİSİ:
    
    1. KATMAN 1: Segment Bazlı (Mevcut durum)
    2. KATMAN 2: Email Eşleştirmesi (Gerçek durum)
    3. KATMAN 3: Çakışma Çözümü (Nihai durum)
    4. KATMAN 4: Öncelik Sırası (Kesin durum)
    """
    
    print("🎯 GERÇEK MÜŞTERİ DURUMU ANALİZİ")
    print("=" * 60)
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ana dosyayı yükle
    print("\n📊 ANA VERİ YÜKLEME...")
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    print(f"   Toplam kayıt: {len(df):,}")
    
    # KATMAN 1: Segment Bazlı Analiz
    print("\n🔍 KATMAN 1: SEGMENT BAZLI ANALİZ")
    print("   Bu katman mevcut segment sütununu analiz eder")
    
    segment_analysis = {}
    for segment in df['Segment'].unique():
        if pd.notna(segment):
            count = df[df['Segment'] == segment].shape[0]
            email_count = df[(df['Segment'] == segment) & (df['Main E-Mail'].notna())].shape[0]
            segment_analysis[segment] = {
                'toplam': count,
                'email_var': email_count,
                'email_yok': count - email_count
            }
    
    for segment, stats in segment_analysis.items():
        print(f"   {segment}:")
        print(f"     Toplam: {stats['toplam']:,}")
        print(f"     Email var: {stats['email_var']:,}")
        print(f"     Email yok: {stats['email_yok']:,}")
        print()
    
    # KATMAN 2: Email Eşleştirme Potansiyeli
    print("\n🔍 KATMAN 2: EMAIL EŞLEŞTİRME POTANSİYELİ")
    print("   Bu katman dış kaynaklarla eşleştirme potansiyelini analiz eder")
    
    # Veri kaynakları analizi
    sources = {
        'Allplan': 'veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx',
        'Dynamics': 'veri_kaynaklari/All Contacts-Dynamics-365.xlsx',
        'Mautic': 'veri_kaynaklari/mautic-tum-liste.xlsx'
    }
    
    source_stats = {}
    for source_name, file_path in sources.items():
        try:
            source_df = pd.read_excel(file_path)
            email_cols = [col for col in source_df.columns if 'mail' in col.lower()]
            
            if email_cols:
                email_col = email_cols[0]
                total_records = len(source_df)
                valid_emails = source_df[email_col].notna().sum()
                source_stats[source_name] = {
                    'toplam_kayit': total_records,
                    'email_var': valid_emails,
                    'email_oran': (valid_emails / total_records) * 100
                }
            else:
                source_stats[source_name] = {'email_sütunu': 'Bulunamadı'}
                
        except Exception as e:
            source_stats[source_name] = {'hata': str(e)}
    
    for source, stats in source_stats.items():
        print(f"   {source}:")
        if 'toplam_kayit' in stats:
            print(f"     Toplam kayıt: {stats['toplam_kayit']:,}")
            print(f"     Email var: {stats['email_var']:,}")
            print(f"     Email oranı: {stats['email_oran']:.1f}%")
        else:
            print(f"     Durum: {stats}")
        print()
    
    # KATMAN 3: Çakışma Çözüm Stratejisi
    print("\n🔍 KATMAN 3: ÇAKIŞMA ÇÖZÜM STRATEJİSİ")
    print("   Bu katman çakışmaları nasıl çözeceğimizi belirler")
    
    print("   ÖNERİLEN ÇÖZÜM HİYERARŞİSİ:")
    print("   1. Allplan müşterisi varsa → 'Mevcut Müşteri' (En yüksek öncelik)")
    print("   2. Dynamics'te varsa → 'Sales Hub Mevcut' (Orta öncelik)")
    print("   3. Mautic'te varsa → 'Potansiyel Müşteri' (En düşük öncelik)")
    print("   4. Hiçbirinde yoksa → Mevcut segment'i koru")
    print()
    
    # KATMAN 4: Uygulama Önerisi
    print("\n🔍 KATMAN 4: UYGULAMA ÖNERİSİ")
    print("   Bu katman hangi adımları izleyeceğimizi belirler")
    
    print("   ADIM 1: Email normalize et (küçük harf, boşluk temizle)")
    print("   ADIM 2: Dış kaynaklarla eşleştir")
    print("   ADIM 3: Çakışmaları çöz (hiyerarşi ile)")
    print("   ADIM 4: Yeni kategori sütunları oluştur")
    print("   ADIM 5: Segment sütununu güncelle (opsiyonel)")
    print()
    
    # Nihai Öneri
    print("\n🎯 NİHAİ ÖNERİ:")
    print("   1. Segment sütunu → KORU (geçmiş referans)")
    print("   2. Yeni sütunlar → GERÇEK DURUM (email eşleştirmesi)")
    print("   3. Çakışma çözümü → HİYERARŞİ (Allplan > Dynamics > Mautic)")
    print("   4. Raporlama → HER İKİ DURUMU DA GÖSTER")
    
    print(f"\n✅ ANALİZ TAMAMLANDI!")
    print(f"Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return segment_analysis, source_stats

if __name__ == "__main__":
    analyze_customer_reality()
