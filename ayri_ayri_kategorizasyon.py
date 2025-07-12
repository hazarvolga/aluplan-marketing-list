#!/usr/bin/env python3
"""
BASIT ve NET - Başından beri istenen:
Sales Hub: Ayrı kategori
Mevcut Müşteri: Ayrı kategori  
Çakışma olabilir ama ayrı gösterilsin
"""

import pandas as pd

def normalize_email(email):
    if pd.isna(email) or email == '' or str(email).lower() == 'nan':
        return None
    return str(email).strip().lower()

def main():
    print("🎯 BASİT KATEGORİZASYON - AYRI AYRI")
    print("=" * 45)
    print("Sales Hub: Ayrı kategori")
    print("Mevcut Müşteri: Ayrı kategori") 
    print("Çakışma kabul edilir")
    print()
    
    # Veri yükle
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    df['normalized_email'] = df['Main E-Mail'].apply(normalize_email)
    
    print(f"📊 TOPLAM KAYIT: {len(df):,}")
    print(f"📧 EMAIL OLAN KAYIT: {df['normalized_email'].notna().sum():,}")
    print(f"🔍 UNİQUE EMAIL: {df['normalized_email'].nunique():,}")
    print()
    
    # Email'i olan kayıtları al
    df_with_email = df[df['normalized_email'].notna()].copy()
    email_groups = df_with_email.groupby('normalized_email')
    
    # AYRI AYRI SAYMA
    dnc_emails = set()
    sales_hub_emails = set()
    mevcut_emails = set()
    mautic_only_emails = set()
    
    for email, group in email_groups:
        segments = set(group['Segment'].tolist())
        
        # Her segmenti ayrı say
        if 'DNC' in segments:
            dnc_emails.add(email)
        
        if 'Sales Hub' in segments:
            sales_hub_emails.add(email)
        
        if 'Mevcut Müşteriler' in segments:
            mevcut_emails.add(email)
        
        # Sadece Mautic olanlar (diğerlerinde olmayan)
        if ('Mautic' in segments and 
            'DNC' not in segments and 
            'Sales Hub' not in segments and 
            'Mevcut Müşteriler' not in segments):
            mautic_only_emails.add(email)
    
    print("🎯 AYRI AYRI SONUÇLAR:")
    print("=" * 30)
    print(f"🚫 DNC: {len(dnc_emails):,}")
    print(f"💼 Sales Hub: {len(sales_hub_emails):,}")
    print(f"👥 Mevcut Müşteriler: {len(mevcut_emails):,}") 
    print(f"🎯 Potansiyel Müşteriler: {len(mautic_only_emails):,}")
    print()
    
    # Çakışma analizi
    print("🔍 ÇAKIŞMA DURUMU:")
    print("-" * 25)
    
    # Sales Hub + Mevcut çakışma
    sales_mevcut_overlap = sales_hub_emails.intersection(mevcut_emails)
    only_sales = sales_hub_emails - mevcut_emails  
    only_mevcut = mevcut_emails - sales_hub_emails
    
    print(f"🤝 Sales Hub + Mevcut Müşteri çakışan: {len(sales_mevcut_overlap):,}")
    print(f"💼 Sadece Sales Hub: {len(only_sales):,}")
    print(f"👥 Sadece Mevcut Müşteri: {len(only_mevcut):,}")
    print()
    
    # Toplam unique (çakışmalar hariç)
    all_emails = dnc_emails | sales_hub_emails | mevcut_emails | mautic_only_emails
    print(f"📊 TOPLAM UNİQUE CUSTOMER: {len(all_emails):,}")
    print()
    
    # DNC çakışmaları
    dnc_sales = dnc_emails.intersection(sales_hub_emails)
    dnc_mevcut = dnc_emails.intersection(mevcut_emails)
    
    if len(dnc_sales) > 0 or len(dnc_mevcut) > 0:
        print("⚠️  DNC ÇAKIŞMALARI:")
        if len(dnc_sales) > 0:
            print(f"   DNC + Sales Hub: {len(dnc_sales):,}")
        if len(dnc_mevcut) > 0:
            print(f"   DNC + Mevcut: {len(dnc_mevcut):,}")
        print()
    
    # Detaylı breakdown
    print("📋 DETAYLI BREAKDOWN:")
    print("-" * 25)
    print(f"💼 Sales Hub Detay:")
    print(f"   - Çakışan (Mevcut+Sales): {len(sales_mevcut_overlap):,}")
    print(f"   - Sadece Sales Hub: {len(only_sales):,}")
    print(f"   = Toplam: {len(sales_hub_emails):,}")
    print()
    print(f"👥 Mevcut Müşteri Detay:")
    print(f"   - Çakışan (Mevcut+Sales): {len(sales_mevcut_overlap):,}")
    print(f"   - Sadece Mevcut: {len(only_mevcut):,}")
    print(f"   = Toplam: {len(mevcut_emails):,}")
    print()
    
    # Segment bazlı dosya oluştur
    results = []
    
    for email, group in email_groups:
        segments = set(group['Segment'].tolist())
        first_record = group.iloc[0].copy()
        
        # Segment işaretleri
        first_record['is_dnc'] = email in dnc_emails
        first_record['is_sales_hub'] = email in sales_hub_emails
        first_record['is_mevcut'] = email in mevcut_emails
        first_record['is_potansiyel'] = email in mautic_only_emails
        
        # Ana kategori (görüntüleme için)
        if first_record['is_dnc']:
            first_record['display_category'] = 'DNC'
        elif first_record['is_sales_hub'] and first_record['is_mevcut']:
            first_record['display_category'] = 'Sales Hub + Mevcut'
        elif first_record['is_sales_hub']:
            first_record['display_category'] = 'Sales Hub'
        elif first_record['is_mevcut']:
            first_record['display_category'] = 'Mevcut Müşteri'
        elif first_record['is_potansiyel']:
            first_record['display_category'] = 'Potansiyel'
        else:
            first_record['display_category'] = 'Diğer'
            
        results.append(first_record)
    
    final_df = pd.DataFrame(results)
    
    # Dosyayı kaydet
    output_file = 'ayri_ayri_kategorizasyon.xlsx'
    final_df.to_excel(output_file, index=False)
    print(f"💾 Ayrı ayrı kategorizasyon kaydedildi: {output_file}")
    
    print("\n🎯 ÖZET:")
    print("=" * 15)
    print("✅ Sales Hub: Ayrı kategori olarak sayıldı")
    print("✅ Mevcut Müşteri: Ayrı kategori olarak sayıldı")
    print("✅ Çakışmalar gösterildi")
    print("✅ Her segment kendi gerçek sayısında")
    
    return final_df

if __name__ == "__main__":
    main()
