#!/usr/bin/env python3
"""
Çakışma Kabul Eden Kategorizasyon:
Her segment kendi öneminde - aynı kişi birden fazla kategoride olabilir
"""

import pandas as pd
import numpy as np

def normalize_email(email):
    """Email'i normalize et"""
    if pd.isna(email) or email == '' or str(email).lower() == 'nan':
        return None
    return str(email).strip().lower()

def main():
    print("🎯 ÇAKIŞMA KABUL EDEN KATEGORİZASYON")
    print("=" * 50)
    print("Her segment kendi öneminde - aynı kişi birden fazla kategoride sayılır")
    print()
    
    # Birleştirilmiş listeyi yükle
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    
    # Email normalize
    df['normalized_email'] = df['Main E-Mail'].apply(normalize_email)
    
    print(f"📊 TOPLAM KAYIT: {len(df):,}")
    print(f"📧 EMAIL OLAN KAYIT: {df['normalized_email'].notna().sum():,}")
    print(f"🔍 UNİQUE EMAIL: {df['normalized_email'].nunique():,}")
    print()
    
    # Email'i olan kayıtları al
    df_with_email = df[df['normalized_email'].notna()].copy()
    
    # Email gruplarını oluştur
    email_groups = df_with_email.groupby('normalized_email')
    
    # Her segment için ayrı ayrı say
    segment_emails = {
        'DNC': set(),
        'Sales Hub': set(),
        'Mevcut Müşteriler': set(),
        'Potansiyel Müşteriler': set()  # Mautic
    }
    
    print("⚡ SEGMENT BAZLI ANALİZ...")
    print()
    
    # Her email için hangi segmentlerde olduğunu belirle
    for email, group in email_groups:
        segments = set(group['Segment'].tolist())
        
        # DNC kontrolü
        if 'DNC' in segments:
            segment_emails['DNC'].add(email)
        
        # Sales Hub kontrolü
        if 'Sales Hub' in segments:
            segment_emails['Sales Hub'].add(email)
        
        # Mevcut Müşteriler kontrolü
        if 'Mevcut Müşteriler' in segments:
            segment_emails['Mevcut Müşteriler'].add(email)
        
        # Potansiyel (Mautic) kontrolü
        if 'Mautic' in segments:
            # Sadece Mautic olanları (diğer segmentlerde olmayanları)
            if not ('DNC' in segments or 'Sales Hub' in segments or 'Mevcut Müşteriler' in segments):
                segment_emails['Potansiyel Müşteriler'].add(email)
    
    print("🎯 SEGMENT SAYILARI (Çakışmalı):")
    print("=" * 35)
    
    # Her segment için sayıları göster
    categories_info = [
        ('🚫 DNC', 'DNC', 'Do Not Contact'),
        ('💼 Sales Hub', 'Sales Hub', 'Aktif Satış Süreci'),
        ('👥 Mevcut Müşteriler', 'Mevcut Müşteriler', 'Mevcut Müşteri Tabanı'),
        ('🎯 Potansiyel Müşteriler', 'Potansiyel Müşteriler', 'Sadece Mautic - Yeni Potansiyeller')
    ]
    
    total_unique = set()
    
    for emoji_name, key, description in categories_info:
        count = len(segment_emails[key])
        print(f"{emoji_name}: {count:,} - {description}")
        total_unique.update(segment_emails[key])
    
    print(f"\n📊 TOPLAM UNİQUE CUSTOMER: {len(total_unique):,}")
    print()
    
    # Çakışma analizi
    print("🔍 ÇAKIŞMA ANALİZİ:")
    print("-" * 25)
    
    # Sales Hub + Mevcut Müşteri çakışması
    sales_mevcut_overlap = segment_emails['Sales Hub'].intersection(segment_emails['Mevcut Müşteriler'])
    
    print(f"🤝 Sales Hub + Mevcut Müşteri çakışan: {len(sales_mevcut_overlap):,}")
    print(f"💼 Sadece Sales Hub: {len(segment_emails['Sales Hub'] - segment_emails['Mevcut Müşteriler']):,}")
    print(f"👥 Sadece Mevcut Müşteri: {len(segment_emails['Mevcut Müşteriler'] - segment_emails['Sales Hub']):,}")
    print()
    
    # DNC çakışmaları
    dnc_others = []
    for key in ['Sales Hub', 'Mevcut Müşteriler']:
        overlap = segment_emails['DNC'].intersection(segment_emails[key])
        if len(overlap) > 0:
            dnc_others.append(f"DNC + {key}: {len(overlap):,}")
    
    if dnc_others:
        print("⚠️  DNC ÇAKIŞMALARI:")
        for overlap_info in dnc_others:
            print(f"   {overlap_info}")
        print()
    
    # Detaylı istatistikler
    print("📈 DETAYLI İSTATİSTİKLER:")
    print("-" * 30)
    
    # Orijinal sayılarla karşılaştırma
    original_counts = df['Segment'].value_counts()
    for segment in ['DNC', 'Sales Hub', 'Mevcut Müşteriler', 'Mautic']:
        if segment == 'Mautic':
            display_name = 'Potansiyel Müşteriler'
            final_key = 'Potansiyel Müşteriler'
        else:
            display_name = segment
            final_key = segment
            
        original = original_counts.get(segment, 0)
        final = len(segment_emails[final_key])
        
        print(f"📊 {display_name}:")
        print(f"   Orijinal kayıt: {original:,}")
        print(f"   Unique email: {final:,}")
        print(f"   Temizlenen duplicate: {original - final:,}")
        print()
    
    # Segment dağılım tablosu oluştur
    results = []
    
    for email, group in email_groups:
        segments = set(group['Segment'].tolist())
        first_record = group.iloc[0].copy()
        
        # Her segment için işaretle
        first_record['is_dnc'] = 'DNC' in segments
        first_record['is_sales_hub'] = 'Sales Hub' in segments
        first_record['is_mevcut'] = 'Mevcut Müşteriler' in segments
        first_record['is_potansiyel'] = ('Mautic' in segments and 
                                       'DNC' not in segments and 
                                       'Sales Hub' not in segments and 
                                       'Mevcut Müşteriler' not in segments)
        
        # Ana kategori belirle (gösterim için)
        if first_record['is_dnc']:
            first_record['main_category'] = 'DNC'
        elif first_record['is_sales_hub']:
            first_record['main_category'] = 'Sales Hub'
        elif first_record['is_mevcut']:
            first_record['main_category'] = 'Mevcut Müşteriler'
        elif first_record['is_potansiyel']:
            first_record['main_category'] = 'Potansiyel Müşteriler'
        else:
            first_record['main_category'] = 'Diğer'
        
        results.append(first_record)
    
    # Sonuçları DataFrame'e dönüştür
    final_df = pd.DataFrame(results)
    
    # Dosyayı kaydet
    output_file = 'cakisma_kabul_kategorizasyon.xlsx'
    final_df.to_excel(output_file, index=False)
    print(f"💾 Çakışma kabul kategorizasyon kaydedildi: {output_file}")
    
    print("\n🎯 ÖZET:")
    print("=" * 20)
    print("✅ Her segment kendi öneminde sayıldı")
    print("✅ Çakışmalar kabul edildi")
    print("✅ Gerçek business durumunu yansıtıyor")
    print(f"✅ Toplam unique customer: {len(total_unique):,}")
    
    return final_df, segment_emails

if __name__ == "__main__":
    main()
