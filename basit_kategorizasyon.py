#!/usr/bin/env python3
"""
Basit ve Net Kategorizasyon:
1. Mevcut Müşteriler (Mevcut Müşteri + Sales Hub olan herkes)
2. Sales Hub (Sadece Sales Hub olanlar - yeni potansiyeller)
3. Potansiyel Müşteriler (Mautic)
4. DNC
"""

import pandas as pd
import numpy as np

def normalize_email(email):
    """Email'i normalize et"""
    if pd.isna(email) or email == '' or str(email).lower() == 'nan':
        return None
    return str(email).strip().lower()

def main():
    print("🎯 BASİT ve NET KATEGORİZASYON")
    print("=" * 50)
    
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
    
    results = []
    
    print("⚡ BASİT KATEGORİZASYON...")
    print()
    
    # Her email için kategori belirle
    for email, group in email_groups:
        segments = set(group['Segment'].tolist())
        
        # İlk kaydı al
        first_record = group.iloc[0].copy()
        
        # Basit kategorizasyon kuralları
        if 'DNC' in segments:
            final_category = 'DNC'
        elif 'Mevcut Müşteriler' in segments:
            # Mevcut Müşteri varsa (Sales Hub olsun olmasın) -> Mevcut Müşteri
            final_category = 'Mevcut Müşteriler'
        elif 'Sales Hub' in segments:
            # Sadece Sales Hub varsa -> Sales Hub
            final_category = 'Sales Hub'
        else:
            # Sadece Mautic -> Potansiyel
            final_category = 'Potansiyel Müşteriler'
        
        first_record['final_category'] = final_category
        results.append(first_record)
    
    # Sonuçları DataFrame'e dönüştür
    final_df = pd.DataFrame(results)
    
    # Final kategori sayıları
    category_counts = final_df['final_category'].value_counts()
    
    print("🎯 NET SONUÇLAR:")
    print("=" * 30)
    
    # Sıralı göster
    categories = ['DNC', 'Mevcut Müşteriler', 'Sales Hub', 'Potansiyel Müşteriler']
    
    total_customers = 0
    for category in categories:
        count = category_counts.get(category, 0)
        total_customers += count
        
        # Emoji ve açıklama
        if category == 'DNC':
            emoji = "🚫"
            desc = "Do Not Contact"
        elif category == 'Mevcut Müşteriler':
            emoji = "👥"
            desc = "Mevcut Müşteri + Sales Hub olanlar"
        elif category == 'Sales Hub':
            emoji = "💼"
            desc = "Sadece Sales Hub - Yeni Potansiyeller"
        elif category == 'Potansiyel Müşteriler':
            emoji = "🎯"
            desc = "Mautic Potansiyel Müşteriler"
        else:
            emoji = "📊"
            desc = ""
        
        print(f"{emoji} {category}: {count:,} {desc}")
    
    print(f"\n📊 TOPLAM CUSTOMER: {total_customers:,}")
    print()
    
    # Detaylı istatistikler
    print("📈 DETAYLI İSTATİSTİKLER:")
    print("-" * 35)
    
    # Orijinal segment analizi
    mevcut_original = len(df[df['Segment'] == 'Mevcut Müşteriler'])
    sales_hub_original = len(df[df['Segment'] == 'Sales Hub'])
    mautic_original = len(df[df['Segment'] == 'Mautic'])
    dnc_original = len(df[df['Segment'] == 'DNC'])
    
    print(f"📊 Orijinal Mevcut Müşteriler: {mevcut_original:,}")
    print(f"📊 Orijinal Sales Hub: {sales_hub_original:,}")
    print(f"📊 Birleşik Mevcut+Sales Hub: {mevcut_original + sales_hub_original:,}")
    print()
    
    # Çakışma analizi için
    df_for_analysis = df_with_email.copy()
    email_segment_analysis = df_for_analysis.groupby('normalized_email')['Segment'].apply(set)
    
    # Mevcut + Sales Hub çakışması
    both_mevcut_sales = 0
    only_mevcut = 0
    only_sales = 0
    
    for email, segments in email_segment_analysis.items():
        if 'DNC' in segments:
            continue  # DNC skip
            
        has_mevcut = 'Mevcut Müşteriler' in segments
        has_sales = 'Sales Hub' in segments
        
        if has_mevcut and has_sales:
            both_mevcut_sales += 1
        elif has_mevcut:
            only_mevcut += 1
        elif has_sales:
            only_sales += 1
    
    print(f"🤝 Hem Mevcut hem Sales Hub: {both_mevcut_sales:,}")
    print(f"👥 Sadece Mevcut Müşteri: {only_mevcut:,}")
    print(f"💼 Sadece Sales Hub: {only_sales:,}")
    print()
    
    # Final kategori açıklaması
    print("✅ FİNAL KATEGORİ AÇIKLAMASI:")
    print("-" * 35)
    print(f"👥 Mevcut Müşteriler: {category_counts.get('Mevcut Müşteriler', 0):,}")
    print(f"   = {both_mevcut_sales:,} (Hem Mevcut+Sales) + {only_mevcut:,} (Sadece Mevcut)")
    print(f"💼 Sales Hub: {category_counts.get('Sales Hub', 0):,}")
    print(f"   = {only_sales:,} (Sadece Sales Hub - yeni potansiyeller)")
    print()
    
    # Dosyayı kaydet
    output_file = 'basit_kategorizasyon.xlsx'
    final_df.to_excel(output_file, index=False)
    print(f"💾 Basit kategorizasyon kaydedildi: {output_file}")
    
    return final_df

if __name__ == "__main__":
    main()
