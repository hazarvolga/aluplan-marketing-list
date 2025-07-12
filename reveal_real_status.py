#!/usr/bin/env python3
"""
Gerçek Mevcut Durumu Ortaya Çıkar
Bu script çakışmaları çözerek gerçek müşteri sayılarını ortaya çıkarır
"""

import pandas as pd
import numpy as np
from datetime import datetime

def reveal_real_customer_status():
    """
    Gerçek müşteri durumunu ortaya çıkar
    
    GERÇEK DURUM KURGUSU:
    1. DNC → İletişim yasak (en yüksek öncelik)
    2. Mevcut Müşteriler → Kesin müşteri
    3. Sales Hub → Aktif satış sürecinde
    4. Mautic → Sadece diğerlerinde yoksa potansiyel
    
    HEDEF: Gerçek sayıları ortaya çıkar
    """
    
    print("🔍 GERÇEK MEVCUT DURUMU ORTAYA ÇIKARMA")
    print("=" * 60)
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ana dosyayı yükle
    print("\n📊 ANA VERİ YÜKLEME...")
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    print(f"   Toplam kayıt: {len(df):,}")
    
    # Email'leri normalize et
    df['normalized_email'] = df['Main E-Mail'].astype(str).str.strip().str.lower()
    df['normalized_email'] = df['normalized_email'].replace('nan', np.nan)
    
    # ADIM 1: Mevcut durum analizi
    print("\n📈 ADIM 1: MEVCUT DURUM ANALİZİ")
    
    print("   Segment dağılımı:")
    segment_counts = df['Segment'].value_counts()
    for segment, count in segment_counts.items():
        print(f"     {segment}: {count:,}")
    
    # Email bazlı analiz
    valid_emails = df[df['normalized_email'].notna()]
    email_groups = valid_emails.groupby('normalized_email')
    
    print(f"\n   Email durumu:")
    print(f"     Toplam kayıt: {len(df):,}")
    print(f"     Email var: {len(valid_emails):,}")
    print(f"     Unique email: {len(email_groups):,}")
    print(f"     Tekrar eden email: {len(email_groups) - len(valid_emails) + len(df):,}")
    
    # ADIM 2: Çakışmaları tespit et
    print("\n🔍 ADIM 2: ÇAKIŞMALARI TESPİT ETME")
    
    email_conflicts = {}
    
    for email, group in email_groups:
        segments = group['Segment'].unique()
        if len(segments) > 1:
            email_conflicts[email] = {
                'segments': list(segments),
                'count': len(group)
            }
    
    print(f"   Çakışma olan email: {len(email_conflicts):,}")
    
    # En çok çakışan durumları analiz et
    print("\n   En çok çakışan segment kombinasyonları:")
    
    segment_combos = {}
    for email, data in email_conflicts.items():
        combo = tuple(sorted(data['segments']))
        if combo not in segment_combos:
            segment_combos[combo] = 0
        segment_combos[combo] += 1
    
    sorted_combos = sorted(segment_combos.items(), key=lambda x: x[1], reverse=True)
    
    for combo, count in sorted_combos[:10]:
        print(f"     {' + '.join(combo)}: {count:,} email")
    
    # ADIM 3: Gerçek durumu belirle
    print("\n🎯 ADIM 3: GERÇEK DURUMU BELİRLEME")
    
    # Her email için gerçek durumu belirle
    real_status = {}
    
    for email, group in email_groups:
        segments = set(group['Segment'].unique())
        
        # Öncelik sırası ile gerçek durumu belirle
        if 'DNC' in segments:
            real_status[email] = 'DNC'
        elif 'Mevcut Müşteriler' in segments:
            real_status[email] = 'Mevcut Müşteriler'
        elif 'Sales Hub' in segments:
            real_status[email] = 'Sales Hub'
        elif 'Mautic' in segments:
            real_status[email] = 'Potansiyel Müşteriler'
        else:
            # Diğer durumlar
            real_status[email] = list(segments)[0]
    
    # ADIM 4: Gerçek sayıları hesapla
    print("\n📊 ADIM 4: GERÇEK SAYILAR")
    
    real_counts = {}
    for status in real_status.values():
        if status not in real_counts:
            real_counts[status] = 0
        real_counts[status] += 1
    
    # Email olmayan kayıtları da say
    no_email_records = df[df['normalized_email'].isna()]
    for _, record in no_email_records.iterrows():
        segment = record['Segment']
        if segment not in real_counts:
            real_counts[segment] = 0
        real_counts[segment] += 1
    
    print("   GERÇEK MÜŞTERİ SAYILARI:")
    total_real = 0
    for status, count in sorted(real_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"     {status}: {count:,}")
        total_real += count
    
    print(f"\n   Toplam gerçek kişi: {total_real:,}")
    
    # ADIM 5: Mautic temizliği
    print("\n🧹 ADIM 5: MAUTIC TEMİZLİĞİ")
    
    # Mautic'te olup başka yerde de olan email'leri bul
    mautic_emails = set()
    for email, group in email_groups:
        if 'Mautic' in group['Segment'].unique():
            mautic_emails.add(email)
    
    print(f"   Mautic'te olan email: {len(mautic_emails):,}")
    
    # Mautic'ten çıkarılacaklar
    mautic_to_remove = set()
    for email in mautic_emails:
        if real_status[email] != 'Potansiyel Müşteriler':
            mautic_to_remove.add(email)
    
    print(f"   Mautic'ten çıkarılacak: {len(mautic_to_remove):,}")
    print(f"   Mautic'te kalacak: {len(mautic_emails) - len(mautic_to_remove):,}")
    
    # ADIM 6: Temizlenmiş segment dağılımı
    print("\n📈 ADIM 6: TEMİZLENMİŞ SEGMENT DAĞILIMI")
    
    # Temizlenmiş veri için segment dağılımı
    cleaned_segments = {}
    
    # Email'i olan kayıtlar
    for email, status in real_status.items():
        if status == 'Potansiyel Müşteriler':
            cleaned_segments['Potansiyel Müşteriler'] = cleaned_segments.get('Potansiyel Müşteriler', 0) + 1
        else:
            cleaned_segments[status] = cleaned_segments.get(status, 0) + 1
    
    # Email'i olmayan kayıtlar
    for _, record in no_email_records.iterrows():
        segment = record['Segment']
        cleaned_segments[segment] = cleaned_segments.get(segment, 0) + 1
    
    print("   TEMİZLENMİŞ SEGMENT DAĞILIMI:")
    for segment, count in sorted(cleaned_segments.items(), key=lambda x: x[1], reverse=True):
        print(f"     {segment}: {count:,}")
    
    # ADIM 7: Karşılaştırma
    print("\n⚖️ ADIM 7: KARŞILAŞTIRMA")
    
    print("   ÖNCEKİ DURUM vs YENİ DURUM:")
    print(f"     {'Segment':<20} {'Önceki':<10} {'Yeni':<10} {'Fark':<10}")
    print(f"     {'-'*20} {'-'*10} {'-'*10} {'-'*10}")
    
    all_segments = set(list(segment_counts.keys()) + list(cleaned_segments.keys()))
    
    for segment in sorted(all_segments):
        old_count = segment_counts.get(segment, 0)
        new_count = cleaned_segments.get(segment, 0)
        diff = new_count - old_count
        
        print(f"     {segment:<20} {old_count:<10,} {new_count:<10,} {diff:<+10,}")
    
    # ADIM 8: Sonuç
    print("\n🎯 ADIM 8: SONUÇ")
    
    print("   ÖNEMLİ BULGULAR:")
    print(f"     • Toplam kayıt: {len(df):,} → {total_real:,}")
    print(f"     • Mükerrer temizlendi: {len(df) - total_real:,}")
    print(f"     • Gerçek potansiyel müşteri: {cleaned_segments.get('Potansiyel Müşteriler', 0):,}")
    print(f"     • Gerçek mevcut müşteri: {cleaned_segments.get('Mevcut Müşteriler', 0):,}")
    print(f"     • Gerçek sales hub: {cleaned_segments.get('Sales Hub', 0):,}")
    print(f"     • DNC listesi: {cleaned_segments.get('DNC', 0):,}")
    
    print(f"\n✅ GERÇEK DURUM ORTAYA ÇIKARILDI!")
    print(f"Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return real_status, cleaned_segments

if __name__ == "__main__":
    reveal_real_customer_status()
