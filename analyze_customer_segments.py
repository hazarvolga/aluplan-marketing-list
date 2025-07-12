#!/usr/bin/env python3
"""
Müşteri Segmentlerini Çakışma Analizi ile Tespit Etme
Bu script gerçek müşteri sayılarını ve potansiyel müşterileri tespit eder
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_customer_segments():
    """
    Müşteri segmentlerini çakışma analizi ile tespit et
    
    Mantık:
    1. Mevcut Müşteriler = Allplan'da olanlar (Priority #1)
    2. Sales Hub Mevcut = Dynamics'te olup Allplan'da olmayanlar (Priority #2) 
    3. Potansiyel Müşteriler = Mautic'te olup diğer ikisinde olmayanlar (Priority #3)
    """
    
    print("🔍 MÜŞTERİ SEGMENTLERİ ÇAKIŞMA ANALİZİ")
    print("=" * 60)
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ana dosyayı yükle
    print("\n📊 ANA VERİ DOSYASINI YÜKLEME...")
    df = pd.read_excel('data/aluplan-list.xlsx')
    print(f"   Toplam kayıt: {len(df):,}")
    
    # Kontrol sütunları var mı?
    control_columns = ['isMevcutMusteriler', 'isSalesHubMevcut', 'isMauticPotansiyel']
    missing_columns = [col for col in control_columns if col not in df.columns]
    
    if missing_columns:
        print(f"❌ Eksik kontrol sütunları: {missing_columns}")
        print("   Önce create_control_system.py'yi çalıştırın!")
        return None
    
    print("✅ Kontrol sütunları mevcut")
    
    # 1. Temel istatistikler
    print("\n📈 TEMEL İSTATİSTİKLER:")
    
    allplan_count = df['isMevcutMusteriler'].sum()
    dynamics_count = df['isSalesHubMevcut'].sum() 
    mautic_count = df['isMauticPotansiyel'].sum()
    
    print(f"   Allplan müşterisi işaretlenen: {allplan_count:,}")
    print(f"   Dynamics müşterisi işaretlenen: {dynamics_count:,}")
    print(f"   Mautic potansiyeli işaretlenen: {mautic_count:,}")
    
    # 2. Çakışma analizi
    print("\n🔄 ÇAKIŞMA ANALİZİ:")
    
    # Sadece Allplan'da olanlar
    only_allplan = df[
        (df['isMevcutMusteriler'] == True) & 
        (df['isSalesHubMevcut'] == False) & 
        (df['isMauticPotansiyel'] == False)
    ]
    print(f"   Sadece Allplan'da: {len(only_allplan):,}")
    
    # Sadece Dynamics'te olanlar
    only_dynamics = df[
        (df['isMevcutMusteriler'] == False) & 
        (df['isSalesHubMevcut'] == True) & 
        (df['isMauticPotansiyel'] == False)
    ]
    print(f"   Sadece Dynamics'te: {len(only_dynamics):,}")
    
    # Sadece Mautic'te olanlar
    only_mautic = df[
        (df['isMevcutMusteriler'] == False) & 
        (df['isSalesHubMevcut'] == False) & 
        (df['isMauticPotansiyel'] == True)
    ]
    print(f"   Sadece Mautic'te: {len(only_mautic):,}")
    
    # İkili çakışmalar
    allplan_dynamics = df[
        (df['isMevcutMusteriler'] == True) & 
        (df['isSalesHubMevcut'] == True) & 
        (df['isMauticPotansiyel'] == False)
    ]
    print(f"   Allplan + Dynamics (Mautic yok): {len(allplan_dynamics):,}")
    
    allplan_mautic = df[
        (df['isMevcutMusteriler'] == True) & 
        (df['isSalesHubMevcut'] == False) & 
        (df['isMauticPotansiyel'] == True)
    ]
    print(f"   Allplan + Mautic (Dynamics yok): {len(allplan_mautic):,}")
    
    dynamics_mautic = df[
        (df['isMevcutMusteriler'] == False) & 
        (df['isSalesHubMevcut'] == True) & 
        (df['isMauticPotansiyel'] == True)
    ]
    print(f"   Dynamics + Mautic (Allplan yok): {len(dynamics_mautic):,}")
    
    # Üçlü çakışma
    all_three = df[
        (df['isMevcutMusteriler'] == True) & 
        (df['isSalesHubMevcut'] == True) & 
        (df['isMauticPotansiyel'] == True)
    ]
    print(f"   Her üç sistemde de var: {len(all_three):,}")
    
    # Hiçbirinde olmayanlar
    none_marked = df[
        (df['isMevcutMusteriler'] == False) & 
        (df['isSalesHubMevcut'] == False) & 
        (df['isMauticPotansiyel'] == False)
    ]
    print(f"   Hiç bir sistemde işaretlenmemiş: {len(none_marked):,}")
    
    # 3. Öncelik stratejisi ile gerçek segmentler
    print("\n🎯 ÖNCELİK STRATEJİSİ İLE GERÇEK SEGMENTLER:")
    print("   Mantık: Allplan > Dynamics > Mautic öncelik sırası")
    
    # Gerçek Mevcut Müşteriler (Allplan'da olanlar)
    real_mevcut = df[df['isMevcutMusteriler'] == True]
    print(f"   🏢 Gerçek Mevcut Müşteriler: {len(real_mevcut):,}")
    
    # Gerçek Sales Hub Mevcut (Dynamics'te olup Allplan'da olmayanlar)
    real_sales_hub = df[
        (df['isSalesHubMevcut'] == True) & 
        (df['isMevcutMusteriler'] == False)
    ]
    print(f"   📈 Gerçek Sales Hub Mevcut: {len(real_sales_hub):,}")
    
    # Gerçek Potansiyel Müşteriler (Mautic'te olup diğer ikisinde olmayanlar)
    real_potansiyel = df[
        (df['isMauticPotansiyel'] == True) & 
        (df['isMevcutMusteriler'] == False) & 
        (df['isSalesHubMevcut'] == False)
    ]
    print(f"   💡 Gerçek Potansiyel Müşteriler: {len(real_potansiyel):,}")
    
    # 4. Segment güncellemesi yap
    print("\n🔄 SEGMENT GÜNCELLEMESİ YAPILIYOR...")
    
    df_updated = df.copy()
    updated_count = 0
    
    for idx, row in df_updated.iterrows():
        new_segment = None
        
        # Öncelik sırası: Allplan > Dynamics > Mautic
        if row['isMevcutMusteriler']:
            new_segment = 'Mevcut Müşteriler'
        elif row['isSalesHubMevcut']:
            new_segment = 'Sales Hub Mevcut'
        elif row['isMauticPotansiyel']:
            new_segment = 'Potansiyel Müşteriler'
        else:
            # Hiç bir sistemde yoksa mevcut segmenti koru
            continue
            
        # Segment değişti mi?
        current_segment = row.get('segment', '')
        if current_segment != new_segment:
            df_updated.at[idx, 'segment'] = new_segment
            updated_count += 1
    
    print(f"   Güncellenen kayıt: {updated_count:,}")
    
    # 5. Güncellenmiş segment dağılımı
    print("\n📊 GÜNCELLENMİŞ SEGMENT DAĞILIMI:")
    
    segment_dist = df_updated['segment'].value_counts()
    total_categorized = 0
    
    for segment, count in segment_dist.items():
        print(f"   {segment}: {count:,}")
        if segment in ['Mevcut Müşteriler', 'Sales Hub Mevcut', 'Potansiyel Müşteriler']:
            total_categorized += count
    
    print(f"   Toplam kategorize edilmiş: {total_categorized:,}")
    print(f"   Kategorize edilmemiş: {len(df_updated) - total_categorized:,}")
    
    # 6. Örneklem analizi
    print("\n🔍 ÖRNEKLEM ANALİZİ:")
    
    if len(real_mevcut) > 0:
        print(f"\n   Mevcut Müşteriler Örnekleri (ilk 5):")
        for idx, row in real_mevcut.head().iterrows():
            print(f"     - {row.get('name', 'N/A')} | {row.get('email', 'N/A')} | {row.get('company', 'N/A')}")
    
    if len(real_sales_hub) > 0:
        print(f"\n   Sales Hub Mevcut Örnekleri (ilk 5):")
        for idx, row in real_sales_hub.head().iterrows():
            print(f"     - {row.get('name', 'N/A')} | {row.get('email', 'N/A')} | {row.get('company', 'N/A')}")
    
    if len(real_potansiyel) > 0:
        print(f"\n   Potansiyel Müşteriler Örnekleri (ilk 5):")
        for idx, row in real_potansiyel.head().iterrows():
            print(f"     - {row.get('name', 'N/A')} | {row.get('email', 'N/A')} | {row.get('company', 'N/A')}")
    
    # 7. Dosyayı kaydet
    print("\n💾 GÜNCELLENMIŞ DOSYAYI KAYDETME...")
    
    # Backup
    backup_file = f"data/aluplan-list-backup-segments-{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(backup_file, index=False)
    print(f"   Backup: {backup_file}")
    
    # Ana dosyayı güncelle
    df_updated.to_excel('data/aluplan-list.xlsx', index=False)
    print(f"   Ana dosya güncellendi: data/aluplan-list.xlsx")
    
    # Public klasörü
    df_updated.to_excel('public/aluplan-list.xlsx', index=False)
    print(f"   Public dosya güncellendi: public/aluplan-list.xlsx")
    
    # 8. Özet rapor
    print("\n📋 ÖZET RAPOR:")
    print(f"   Toplam kayıt: {len(df_updated):,}")
    print(f"   Mevcut Müşteriler: {len(real_mevcut):,}")
    print(f"   Sales Hub Mevcut: {len(real_sales_hub):,}")
    print(f"   Potansiyel Müşteriler: {len(real_potansiyel):,}")
    print(f"   Çakışma durumu çözüldü ✅")
    
    print(f"\n✅ MÜŞTERİ SEGMENT ANALİZİ TAMAMLANDI!")
    print(f"Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return df_updated

if __name__ == "__main__":
    analyze_customer_segments()
