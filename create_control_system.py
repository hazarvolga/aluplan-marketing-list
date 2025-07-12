#!/usr/bin/env python3
"""
Email Eşleştirme ile Tam Kontrol Sistemi
Bu script birlestirilmis-liste.xlsx'i kullanarak 3 kaynak ile email eşleştirmesi yapar
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_email_control_system():
    """
    Email eşleştirme ile tam kontrol sistemi oluştur
    
    3 yeni sütun ekle:
    1. isMevcutMusteriler - Allplan müşterilerinden eşleşenler
    2. isSalesHubMevcut - Dynamics 365'ten eşleşenler  
    3. isMauticPotansiyel - Mautic'ten eşleşenler
    """
    
    print("🔧 EMAIL EŞLEŞTİRME İLE TAM KONTROL SİSTEMİ")
    print("=" * 60)
    print(f"Başlangıç Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Ana veri dosyasını yükle (birlestirilmis-liste.xlsx)
    print("\n📊 ANA VERİ DOSYASINI YÜKLEME...")
    df_main = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    print(f"   Ana dosya: {len(df_main):,} kayıt")
    print(f"   Sütunlar: {list(df_main.columns)}")
    
    # Email sütununu tespit et
    main_email_col = None
    for col in df_main.columns:
        if 'mail' in col.lower():
            main_email_col = col
            break
    
    if not main_email_col:
        print("❌ Ana dosyada email sütunu bulunamadı!")
        return None
    
    print(f"   Email sütunu: {main_email_col}")
    
    # Ana dosyada email'leri temizle ve normalize et
    df_main[main_email_col] = df_main[main_email_col].astype(str).str.strip().str.lower()
    main_emails = set(df_main[df_main[main_email_col].notna()][main_email_col].unique())
    print(f"   Unique email sayısı: {len(main_emails):,}")
    
    # 2. Allplan Müşteriler dosyasını yükle
    print("\n🏢 ALLPLAN MÜŞTERİLERİ YÜKLEME...")
    try:
        df_allplan = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx')
        print(f"   Allplan dosya: {len(df_allplan):,} kayıt")
        print(f"   Sütunlar: {list(df_allplan.columns)}")
        
        # Email sütununu bul
        allplan_email_col = None
        for col in df_allplan.columns:
            if 'mail' in col.lower():
                allplan_email_col = col
                break
        
        if allplan_email_col:
            print(f"   Email sütunu: {allplan_email_col}")
            # Email'leri normalize et
            df_allplan[allplan_email_col] = df_allplan[allplan_email_col].astype(str).str.strip().str.lower()
            allplan_emails = set(df_allplan[df_allplan[allplan_email_col].notna()][allplan_email_col].unique())
            print(f"   Unique email sayısı: {len(allplan_emails):,}")
            
            # NaN ve 'nan' değerlerini temizle
            allplan_emails = {email for email in allplan_emails if email != 'nan' and pd.notna(email) and email.strip() != ''}
            print(f"   Temizlenmiş email sayısı: {len(allplan_emails):,}")
        else:
            print("   ❌ Email sütunu bulunamadı!")
            allplan_emails = set()
            
    except Exception as e:
        print(f"   ❌ Allplan dosyası yüklenemedi: {str(e)}")
        allplan_emails = set()
    
    # 3. Dynamics 365 dosyasını yükle
    print("\n📈 DYNAMICS 365 YÜKLEME...")
    try:
        df_dynamics = pd.read_excel('veri_kaynaklari/All Contacts-Dynamics-365.xlsx')
        print(f"   Dynamics dosya: {len(df_dynamics):,} kayıt")
        print(f"   Sütunlar: {list(df_dynamics.columns)}")
        
        # Email sütununu bul
        dynamics_email_col = None
        for col in df_dynamics.columns:
            if 'mail' in col.lower():
                dynamics_email_col = col
                break
        
        if dynamics_email_col:
            print(f"   Email sütunu: {dynamics_email_col}")
            # Email'leri normalize et
            df_dynamics[dynamics_email_col] = df_dynamics[dynamics_email_col].astype(str).str.strip().str.lower()
            dynamics_emails = set(df_dynamics[df_dynamics[dynamics_email_col].notna()][dynamics_email_col].unique())
            print(f"   Unique email sayısı: {len(dynamics_emails):,}")
            
            # NaN ve 'nan' değerlerini temizle
            dynamics_emails = {email for email in dynamics_emails if email != 'nan' and pd.notna(email) and email.strip() != ''}
            print(f"   Temizlenmiş email sayısı: {len(dynamics_emails):,}")
        else:
            print("   ❌ Email sütunu bulunamadı!")
            dynamics_emails = set()
            
    except Exception as e:
        print(f"   ❌ Dynamics dosyası yüklenemedi: {str(e)}")
        dynamics_emails = set()
    
    # 4. Mautic dosyasını yükle
    print("\n📧 MAUTIC YÜKLEME...")
    try:
        df_mautic = pd.read_excel('veri_kaynaklari/mautic-tum-liste.xlsx')
        print(f"   Mautic dosya: {len(df_mautic):,} kayıt")
        print(f"   Sütunlar: {list(df_mautic.columns)}")
        
        # Email sütununu bul
        mautic_email_col = None
        for col in df_mautic.columns:
            if 'mail' in col.lower():
                mautic_email_col = col
                break
        
        if mautic_email_col:
            print(f"   Email sütunu: {mautic_email_col}")
            # Email'leri normalize et
            df_mautic[mautic_email_col] = df_mautic[mautic_email_col].astype(str).str.strip().str.lower()
            mautic_emails = set(df_mautic[df_mautic[mautic_email_col].notna()][mautic_email_col].unique())
            print(f"   Unique email sayısı: {len(mautic_emails):,}")
            
            # NaN ve 'nan' değerlerini temizle
            mautic_emails = {email for email in mautic_emails if email != 'nan' and pd.notna(email) and email.strip() != ''}
            print(f"   Temizlenmiş email sayısı: {len(mautic_emails):,}")
        else:
            print("   ❌ Email sütunu bulunamadı!")
            mautic_emails = set()
            
    except Exception as e:
        print(f"   ❌ Mautic dosyası yüklenemedi: {str(e)}")
        mautic_emails = set()
    
    # 5. Email eşleştirmesi yap
    print("\n🔄 EMAIL EŞLEŞTİRMESİ YAPILIYOR...")
    
    # Yeni sütunları başlat
    df_main['isMevcutMusteriler'] = False
    df_main['isSalesHubMevcut'] = False
    df_main['isMauticPotansiyel'] = False
    
    allplan_matches = 0
    dynamics_matches = 0
    mautic_matches = 0
    
    for idx, row in df_main.iterrows():
        email = row[main_email_col]
        
        if pd.isna(email) or email == 'nan' or email.strip() == '':
            continue
            
        email = str(email).strip().lower()
        
        # Allplan eşleştirmesi
        if email in allplan_emails:
            df_main.at[idx, 'isMevcutMusteriler'] = True
            allplan_matches += 1
        
        # Dynamics eşleştirmesi  
        if email in dynamics_emails:
            df_main.at[idx, 'isSalesHubMevcut'] = True
            dynamics_matches += 1
            
        # Mautic eşleştirmesi
        if email in mautic_emails:
            df_main.at[idx, 'isMauticPotansiyel'] = True
            mautic_matches += 1
    
    print(f"   ✅ Allplan eşleşme: {allplan_matches:,}")
    print(f"   ✅ Dynamics eşleşme: {dynamics_matches:,}")
    print(f"   ✅ Mautic eşleşme: {mautic_matches:,}")
    
    # 6. Çakışma analizı
    print("\n📊 ÇAKIŞMA ANALİZİ:")
    
    allplan_true = df_main['isMevcutMusteriler'].sum()
    dynamics_true = df_main['isSalesHubMevcut'].sum()
    mautic_true = df_main['isMauticPotansiyel'].sum()
    
    print(f"   Allplan müşterisi: {allplan_true:,}")
    print(f"   Sales Hub müşterisi: {dynamics_true:,}")
    print(f"   Mautic potansiyeli: {mautic_true:,}")
    
    # Çakışmalar
    both_allplan_dynamics = df_main[
        (df_main['isMevcutMusteriler'] == True) & 
        (df_main['isSalesHubMevcut'] == True)
    ]
    print(f"   Hem Allplan hem Sales Hub: {len(both_allplan_dynamics):,}")
    
    both_allplan_mautic = df_main[
        (df_main['isMevcutMusteriler'] == True) & 
        (df_main['isMauticPotansiyel'] == True)
    ]
    print(f"   Hem Allplan hem Mautic: {len(both_allplan_mautic):,}")
    
    both_dynamics_mautic = df_main[
        (df_main['isSalesHubMevcut'] == True) & 
        (df_main['isMauticPotansiyel'] == True)
    ]
    print(f"   Hem Sales Hub hem Mautic: {len(both_dynamics_mautic):,}")
    
    all_three = df_main[
        (df_main['isMevcutMusteriler'] == True) & 
        (df_main['isSalesHubMevcut'] == True) & 
        (df_main['isMauticPotansiyel'] == True)
    ]
    print(f"   Her üç sistemde de var: {len(all_three):,}")
    
    # 7. Segment güncelleme stratejisi
    print("\n🎯 SEGMENT GÜNCELLEME STRATEJİSİ:")
    
    # Öncelik sırası: Allplan > Sales Hub > Mautic
    segment_updates = 0
    
    for idx, row in df_main.iterrows():
        new_segment = None
        
        if row['isMevcutMusteriler']:
            new_segment = 'Mevcut Müşteriler'
        elif row['isSalesHubMevcut']:
            new_segment = 'Sales Hub Mevcut'
        elif row['isMauticPotansiyel']:
            new_segment = 'Potansiyel Müşteriler'
        else:
            # Mevcut segmenti koru
            continue
            
        # Segment güncellemesi gerekiyor mu?
        current_segment = row.get('segment', '')
        if current_segment != new_segment:
            df_main.at[idx, 'segment'] = new_segment
            segment_updates += 1
    
    print(f"   Güncellenen segment: {segment_updates:,}")
    
    # 8. Güncellenmiş dosyayı kaydet
    print("\n💾 GÜNCELLENMIŞ DOSYAYI KAYDETME...")
    
    # Backup oluştur
    backup_file = f"data/aluplan-list-backup-control-{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    original_df = pd.read_excel('data/aluplan-list.xlsx')
    original_df.to_excel(backup_file, index=False)
    print(f"   Backup oluşturuldu: {backup_file}")
    
    # Ana dosyayı güncelle
    df_main.to_excel('data/aluplan-list.xlsx', index=False)
    print(f"   Ana dosya güncellendi: data/aluplan-list.xlsx")
    
    # Public klasörünü de güncelle
    df_main.to_excel('public/aluplan-list.xlsx', index=False)
    print(f"   Public dosya güncellendi: public/aluplan-list.xlsx")
    
    # 9. Final rapor
    print("\n📈 FİNAL RAPOR:")
    print(f"   Toplam kayıt: {len(df_main):,}")
    print(f"   Yeni sütunlar eklendi: isMevcutMusteriler, isSalesHubMevcut, isMauticPotansiyel")
    print(f"   Email eşleştirme tamamlandı")
    print(f"   Segment güncellemeleri uygulandı")
    
    # Segment dağılımı
    segment_dist = df_main['segment'].value_counts()
    print(f"\n   📊 Güncel segment dağılımı:")
    for segment, count in segment_dist.items():
        print(f"     {segment}: {count:,}")
    
    print(f"\n✅ EMAIL EŞLEŞTİRME KONTROL SİSTEMİ TAMAMLANDI!")
    print(f"Bitiş Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return df_main

if __name__ == "__main__":
    create_email_control_system()
