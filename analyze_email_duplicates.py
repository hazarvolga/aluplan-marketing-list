#!/usr/bin/env python3
"""
Email Tekrarlarını Tespit Et ve Segment Çakışmalarını Analiz Et
Bu script email tekrarlarını bulur ve hangi segmentlerden geldiklerini analiz eder
"""

import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

def analyze_email_duplicates():
    """
    Email tekrarlarını tespit et ve segment çakışmalarını analiz et
    
    AMAÇ:
    1. Aynı email'in birden fazla segment'te olup olmadığını tespit et
    2. Çakışan email'lerin hangi segmentlerden geldiğini belirle
    3. Mautic'teki mevcut müşterileri tespit et
    4. Temizleme stratejisi oluştur
    """
    
    print("🔍 EMAIL TEKRARLARI VE SEGMENT ÇAKIŞMA ANALİZİ")
    print("=" * 60)
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ana dosyayı yükle
    print("\n📊 ANA VERİ YÜKLEME...")
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    print(f"   Toplam kayıt: {len(df):,}")
    print(f"   Toplam email: {df['Main E-Mail'].notna().sum():,}")
    
    # Email'leri normalize et
    print("\n🔄 EMAIL'LERİ NORMALİZE ETME...")
    df['normalized_email'] = df['Main E-Mail'].astype(str).str.strip().str.lower()
    df['normalized_email'] = df['normalized_email'].replace('nan', np.nan)
    
    # Geçerli email'leri al
    valid_emails = df[df['normalized_email'].notna()]
    print(f"   Geçerli email: {len(valid_emails):,}")
    
    # AŞAMA 1: Tekrar eden email'leri tespit et
    print("\n🔍 AŞAMA 1: TEKRAR EDEN EMAIL'LERİ TESPİT ETME")
    
    email_counts = valid_emails['normalized_email'].value_counts()
    duplicated_emails = email_counts[email_counts > 1]
    
    print(f"   Tekrar eden email sayısı: {len(duplicated_emails):,}")
    print(f"   Tekrar eden toplam kayıt: {duplicated_emails.sum():,}")
    print(f"   En çok tekrar eden email: {email_counts.iloc[0]:,} kez")
    
    # AŞAMA 2: Segment çakışmalarını analiz et
    print("\n🔍 AŞAMA 2: SEGMENT ÇAKIŞMA ANALİZİ")
    
    segment_conflicts = {}
    
    for email in duplicated_emails.index:
        email_records = valid_emails[valid_emails['normalized_email'] == email]
        segments = email_records['Segment'].unique()
        
        if len(segments) > 1:
            segment_conflicts[email] = {
                'segments': list(segments),
                'count': len(email_records),
                'names': list(email_records['Name'].unique())
            }
    
    print(f"   Segment çakışması olan email: {len(segment_conflicts):,}")
    
    # En problematik durumları göster
    print("\n🚨 EN PROBLEMATİK DURUMLAR:")
    sorted_conflicts = sorted(segment_conflicts.items(), 
                            key=lambda x: len(x[1]['segments']), 
                            reverse=True)
    
    for email, data in sorted_conflicts[:10]:  # İlk 10 tanesi
        print(f"   📧 {email}")
        print(f"     Segment'ler: {data['segments']}")
        print(f"     Kayıt sayısı: {data['count']}")
        print(f"     İsimler: {data['names'][:3]}...")  # İlk 3 isim
        print()
    
    # AŞAMA 3: Mautic'teki mevcut müşterileri tespit et
    print("\n🔍 AŞAMA 3: MAUTIC'TEKİ MEVCUT MÜŞTERİLERİ TESPİT ETME")
    
    # Mautic segment'indeki kayıtları al
    mautic_records = df[df['Segment'] == 'Mautic']
    print(f"   Mautic segment'indeki kayıt: {len(mautic_records):,}")
    
    # Mautic'teki ama başka segment'lerde de olan email'leri bul
    mautic_emails = set(mautic_records['normalized_email'].dropna())
    
    # Mautic dışındaki segment'lere bak
    non_mautic_segments = ['Mevcut Müşteriler', 'Sales Hub', 'DNC']
    
    mautic_conflicts = {}
    for segment in non_mautic_segments:
        segment_records = df[df['Segment'] == segment]
        segment_emails = set(segment_records['normalized_email'].dropna())
        
        # Mautic ile çakışan email'ler
        conflicts = mautic_emails.intersection(segment_emails)
        
        if conflicts:
            mautic_conflicts[segment] = {
                'conflict_emails': list(conflicts),
                'count': len(conflicts)
            }
    
    print("   Mautic ile çakışan segment'ler:")
    for segment, data in mautic_conflicts.items():
        print(f"     {segment}: {data['count']:,} email çakışması")
    
    # AŞAMA 4: Temizleme stratejisi önerisi
    print("\n🎯 AŞAMA 4: TEMİZLEME STRATEJİSİ ÖNERİSİ")
    
    print("   ÖNERİLEN STRATEJİ:")
    print("   1. Mautic + Mevcut Müşteriler → 'Mevcut Müşteri' olarak etiketle")
    print("   2. Mautic + Sales Hub → 'Sales Hub' olarak etiketle")
    print("   3. Mautic + Mevcut Müşteriler + Sales Hub → 'Mevcut Müşteri' (öncelik)")
    print("   4. Sadece Mautic → 'Potansiyel Müşteri' olarak koru")
    print("   5. Mautic + DNC → 'DNC' olarak etiketle (en yüksek öncelik)")
    print()
    
    # Detaylı istatistikler
    print("📊 DETAYLI İSTATİSTİKLER:")
    
    # Segment dağılımı
    print("\n   Segment dağılımı:")
    for segment, count in df['Segment'].value_counts().items():
        print(f"     {segment}: {count:,}")
    
    # Email durumu
    print(f"\n   Email durumu:")
    print(f"     Toplam kayıt: {len(df):,}")
    print(f"     Email var: {df['Main E-Mail'].notna().sum():,}")
    print(f"     Email yok: {df['Main E-Mail'].isna().sum():,}")
    print(f"     Tekrar eden email: {len(duplicated_emails):,}")
    print(f"     Segment çakışması: {len(segment_conflicts):,}")
    
    # Backup ve raporlama
    print("\n💾 RAPOR KAYDETME...")
    
    # Çakışma raporunu kaydet
    conflict_report = []
    for email, data in segment_conflicts.items():
        # NaN değerlerini temizle
        clean_names = [str(name) for name in data['names'] if pd.notna(name)]
        conflict_report.append({
            'email': email,
            'segments': ', '.join(data['segments']),
            'count': data['count'],
            'names': ', '.join(clean_names)
        })
    
    if conflict_report:
        conflict_df = pd.DataFrame(conflict_report)
        conflict_df.to_excel(f'reports/email_conflicts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx', index=False)
        print(f"   Çakışma raporu kaydedildi: reports/email_conflicts_*.xlsx")
    
    print(f"\n✅ ANALİZ TAMAMLANDI!")
    print(f"Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return segment_conflicts, mautic_conflicts

if __name__ == "__main__":
    analyze_email_duplicates()
