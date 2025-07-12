#!/usr/bin/env python3
"""
Segment Çakışmalarını Çöz - Müşteri Yolculuğu Bazlı Temizleme
Bu script segment çakışmalarını müşteri yolculuğuna göre çözer
"""

import pandas as pd
import numpy as np
from datetime import datetime

def clean_segment_conflicts():
    """
    Segment çakışmalarını müşteri yolculuğuna göre çöz
    
    MÜŞTERİ YOLCULUĞU HİYERARŞİSİ:
    1. DNC (En yüksek öncelik) - Hiç iletişim kurulmamalı
    2. Mevcut Müşteriler - Kesinleşmiş müşteriler
    3. Sales Hub - Aktif satış sürecindeki müşteriler
    4. Mautic - Potansiyel müşteriler (en düşük öncelik)
    
    MANTIK: Bir kişi birden fazla segmentte olabilir, ama en güncel durumu önemli
    """
    
    print("🔧 SEGMENT ÇAKIŞMALARINI ÇÖZME - MÜŞTERİ YOLCULUĞU BAZLI")
    print("=" * 70)
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ana dosyayı yükle
    print("\n📊 ANA VERİ YÜKLEME...")
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    print(f"   Toplam kayıt: {len(df):,}")
    
    # Email'leri normalize et
    df['normalized_email'] = df['Main E-Mail'].astype(str).str.strip().str.lower()
    df['normalized_email'] = df['normalized_email'].replace('nan', np.nan)
    
    # Öncelik hiyerarşisi
    priority_order = ['DNC', 'Mevcut Müşteriler', 'Sales Hub', 'Mautic']
    
    print("\n🎯 MÜŞTERİ YOLCULUĞU HİYERARŞİSİ:")
    for i, segment in enumerate(priority_order, 1):
        print(f"   {i}. {segment} - {'En yüksek öncelik' if i == 1 else 'Yüksek öncelik' if i == 2 else 'Orta öncelik' if i == 3 else 'En düşük öncelik'}")
    
    # Çakışma çözümleme stratejisi
    print("\n🔄 ÇAKIŞMA ÇÖZÜMLEME STRATEJİSİ:")
    
    # Her email için en yüksek öncelikli segment'i belirle
    email_final_segments = {}
    segment_transitions = {}
    
    # Email'leri grupla
    valid_emails = df[df['normalized_email'].notna()]
    email_groups = valid_emails.groupby('normalized_email')
    
    for email, group in email_groups:
        segments = group['Segment'].unique()
        
        if len(segments) > 1:
            # Çakışma var - en yüksek öncelikli olanı seç
            for priority_segment in priority_order:
                if priority_segment in segments:
                    email_final_segments[email] = priority_segment
                    segment_transitions[email] = {
                        'from_segments': list(segments),
                        'to_segment': priority_segment,
                        'transition_type': 'conflict_resolved'
                    }
                    break
        else:
            # Çakışma yok - mevcut segment'i koru
            email_final_segments[email] = segments[0]
            segment_transitions[email] = {
                'from_segments': list(segments),
                'to_segment': segments[0],
                'transition_type': 'no_conflict'
            }
    
    # İstatistikler
    print("\n📊 ÇAKIŞMA ÇÖZÜMLEME İSTATİSTİKLERİ:")
    
    conflict_count = sum(1 for t in segment_transitions.values() if t['transition_type'] == 'conflict_resolved')
    no_conflict_count = sum(1 for t in segment_transitions.values() if t['transition_type'] == 'no_conflict')
    
    print(f"   Çakışma çözümlenen email: {conflict_count:,}")
    print(f"   Çakışma olmayan email: {no_conflict_count:,}")
    
    # Segment geçişleri
    print("\n🔄 SEGMENT GEÇİŞLERİ:")
    
    transition_stats = {}
    for email, transition in segment_transitions.items():
        if transition['transition_type'] == 'conflict_resolved':
            from_segments = sorted(transition['from_segments'])
            to_segment = transition['to_segment']
            
            transition_key = f"{' + '.join(from_segments)} → {to_segment}"
            
            if transition_key not in transition_stats:
                transition_stats[transition_key] = 0
            transition_stats[transition_key] += 1
    
    # En çok olan geçişleri göster
    sorted_transitions = sorted(transition_stats.items(), key=lambda x: x[1], reverse=True)
    
    print("   En çok yapılan geçişler:")
    for transition, count in sorted_transitions[:10]:
        print(f"     {transition}: {count:,} kişi")
    
    # Yeni temizlenmiş veri oluştur
    print("\n🧹 TEMİZLENMİŞ VERİ OLUŞTURMA...")
    
    # Her email için sadece en yüksek öncelikli kaydı tut
    cleaned_records = []
    
    for email, group in email_groups:
        final_segment = email_final_segments[email]
        
        # Bu email'in en yüksek öncelikli segment'indeki kayıtlarını al
        priority_records = group[group['Segment'] == final_segment]
        
        # En güncel/tam olan kaydı seç (en az boş alan olanı)
        best_record = priority_records.loc[priority_records.isnull().sum(axis=1).idxmin()]
        
        cleaned_records.append(best_record)
    
    # Email'i olmayan kayıtları da ekle
    no_email_records = df[df['normalized_email'].isna()]
    for _, record in no_email_records.iterrows():
        cleaned_records.append(record)
    
    # Temizlenmiş DataFrame oluştur
    cleaned_df = pd.DataFrame(cleaned_records)
    
    # Sonuçları göster
    print("\n📈 TEMİZLENMİŞ VERİ SONUÇLARI:")
    print(f"   Önceki toplam kayıt: {len(df):,}")
    print(f"   Temizlenmiş toplam kayıt: {len(cleaned_df):,}")
    print(f"   Silinen mükerrer kayıt: {len(df) - len(cleaned_df):,}")
    
    print("\n   Temizlenmiş segment dağılımı:")
    for segment, count in cleaned_df['Segment'].value_counts().items():
        print(f"     {segment}: {count:,}")
    
    # Önceki dağılımla karşılaştır
    print("\n   Önceki segment dağılımı:")
    for segment, count in df['Segment'].value_counts().items():
        print(f"     {segment}: {count:,}")
    
    # Temizlenmiş veriyi kaydet
    print("\n💾 TEMİZLENMİŞ VERİYİ KAYDETME...")
    
    # Backup oluştur
    backup_file = f"veri_kaynaklari/birlestirilmis-liste-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(backup_file, index=False)
    print(f"   Backup oluşturuldu: {backup_file}")
    
    # Temizlenmiş veriyi kaydet
    cleaned_df.to_excel('veri_kaynaklari/birlestirilmis-liste-cleaned.xlsx', index=False)
    print(f"   Temizlenmiş veri kaydedildi: veri_kaynaklari/birlestirilmis-liste-cleaned.xlsx")
    
    # Ana dosyaları da güncelle
    cleaned_df.to_excel('data/aluplan-list.xlsx', index=False)
    cleaned_df.to_excel('public/aluplan-list.xlsx', index=False)
    print(f"   Ana dosyalar güncellendi: data/ ve public/")
    
    # Geçiş raporunu kaydet
    transition_report = []
    for email, transition in segment_transitions.items():
        if transition['transition_type'] == 'conflict_resolved':
            transition_report.append({
                'email': email,
                'from_segments': ' + '.join(transition['from_segments']),
                'to_segment': transition['to_segment'],
                'transition_type': transition['transition_type']
            })
    
    if transition_report:
        transition_df = pd.DataFrame(transition_report)
        transition_df.to_excel(f'reports/segment_transitions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx', index=False)
        print(f"   Geçiş raporu kaydedildi: reports/segment_transitions_*.xlsx")
    
    print(f"\n✅ SEGMENT ÇAKIŞMALARI ÇÖZÜLDÜ!")
    print(f"Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return cleaned_df, segment_transitions

if __name__ == "__main__":
    clean_segment_conflicts()
