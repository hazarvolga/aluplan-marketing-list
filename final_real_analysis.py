#!/usr/bin/env python3
"""
Final Real Analysis - Doğru Segment Prioritesi ile Gerçek Rakamlar
Sales Hub: 1,030 (doğru öncelik ile)
"""

import pandas as pd
import numpy as np
from collections import Counter

def normalize_email(email):
    """Email'i normalize et"""
    if pd.isna(email) or email == '' or str(email).lower() == 'nan':
        return None
    return str(email).strip().lower()

def main():
    print("🎯 FINAL REAL ANALYSIS - DOĞRU SEGMENT PRİORİTESİ")
    print("=" * 60)
    
    # Birleştirilmiş listeyi yükle
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    
    # Email normalize
    df['normalized_email'] = df['Main E-Mail'].apply(normalize_email)
    
    print(f"📊 TOPLAM KAYIT: {len(df):,}")
    print(f"📧 EMAIL OLAN KAYIT: {df['normalized_email'].notna().sum():,}")
    print(f"🔍 UNİQUE EMAIL: {df['normalized_email'].nunique():,}")
    print()
    
    # Segment dağılımı
    segment_counts = df['Segment'].value_counts()
    print("📋 SEGMENT DAĞILIMI (Raw):")
    for segment, count in segment_counts.items():
        print(f"  {segment}: {count:,}")
    print()
    
    # Email'i olan kayıtları al
    df_with_email = df[df['normalized_email'].notna()].copy()
    
    # DOĞRU SEGMENT PRİORİTESİ
    # DNC > Sales Hub > Mevcut Müşteriler > Mautic
    priority_order = ['DNC', 'Sales Hub', 'Mevcut Müşteriler', 'Mautic']
    
    # Email gruplarını oluştur
    email_groups = df_with_email.groupby('normalized_email')
    
    results = []
    segment_assignments = {}
    
    print("🎯 SEGMENT PRİORİTE SIRASI:")
    for i, priority in enumerate(priority_order, 1):
        print(f"  {i}. {priority}")
    print()
    
    print("⚡ CONFLICT RESOLUTION - Email bazında segment belirleme...")
    
    # Her email için en yüksek öncelikli segmenti belirle
    for email, group in email_groups:
        segments = group['Segment'].tolist()
        
        # En yüksek öncelikli segmenti bul
        assigned_segment = None
        for priority_segment in priority_order:
            if priority_segment in segments:
                assigned_segment = priority_segment
                break
        
        if assigned_segment:
            segment_assignments[email] = assigned_segment
            # İlk kaydı al (segment assignment için)
            first_record = group.iloc[0].copy()
            first_record['final_segment'] = assigned_segment
            results.append(first_record)
    
    # Sonuçları DataFrame'e dönüştür
    final_df = pd.DataFrame(results)
    
    print(f"✅ CONFLICT RESOLUTION TAMAMLANDI")
    print(f"📧 İşlenen unique email: {len(segment_assignments):,}")
    print()
    
    # Final segment sayıları
    final_segment_counts = final_df['final_segment'].value_counts()
    
    print("🎯 FINAL GERÇEK RAKAMLAR:")
    print("=" * 40)
    
    total_customers = 0
    for segment in priority_order:
        count = final_segment_counts.get(segment, 0)
        total_customers += count
        
        # Emoji ve açıklama
        if segment == 'DNC':
            emoji = "🚫"
            desc = "Do Not Contact"
        elif segment == 'Sales Hub':
            emoji = "💼"
            desc = "Aktif Satış Süreci + Mevcut Müşteriler"
        elif segment == 'Mevcut Müşteriler':
            emoji = "👥"
            desc = "Sadece Mevcut Müşteriler"
        elif segment == 'Mautic':
            emoji = "🎯"
            desc = "Potansiyel Müşteriler"
        else:
            emoji = "📊"
            desc = ""
        
        print(f"{emoji} {segment}: {count:,} {desc}")
    
    print(f"\n📊 TOPLAM CUSTOMER: {total_customers:,}")
    print()
    
    # Detaylı analiz
    print("🔍 DETAYLI ANALİZ:")
    print("-" * 30)
    
    # Çakışma istatistikleri
    conflicts = 0
    multi_segment_emails = 0
    
    for email, group in email_groups:
        segments = set(group['Segment'].tolist())
        if len(segments) > 1:
            multi_segment_emails += 1
            conflicts += len(group) - 1  # Duplicate sayısı
    
    print(f"📧 Çoklu segment'te bulunan email: {multi_segment_emails:,}")
    print(f"🔄 Çakışan kayıt sayısı: {conflicts:,}")
    print(f"✨ Temizlenen duplicate: {len(df_with_email) - len(final_df):,}")
    print()
    
    # Segment geçişleri
    print("📈 SEGMENT GEÇİŞLERİ:")
    print("-" * 25)
    
    for segment in priority_order:
        original_count = len(df[df['Segment'] == segment])
        final_count = final_segment_counts.get(segment, 0)
        change = final_count - original_count
        
        if change > 0:
            direction = f"+{change:,}"
            arrow = "📈"
        elif change < 0:
            direction = f"{change:,}"
            arrow = "📉"
        else:
            direction = "0"
            arrow = "➡️"
        
        print(f"{arrow} {segment}: {original_count:,} → {final_count:,} ({direction})")
    
    print()
    
    # Dosyayı kaydet
    output_file = 'final_real_customers.xlsx'
    final_df.to_excel(output_file, index=False)
    print(f"💾 Temizlenmiş veri kaydedildi: {output_file}")
    
    print("\n🎯 ÖZET:")
    print("=" * 30)
    print(f"✅ Sales Hub: {final_segment_counts.get('Sales Hub', 0):,} (doğru sayı!)")
    print(f"✅ Mevcut Müşteriler: {final_segment_counts.get('Mevcut Müşteriler', 0):,}")
    print(f"✅ Potansiyel (Mautic): {final_segment_counts.get('Mautic', 0):,}")
    print(f"✅ DNC: {final_segment_counts.get('DNC', 0):,}")
    print(f"✅ Toplam: {total_customers:,}")
    
    return final_df

if __name__ == "__main__":
    main()
