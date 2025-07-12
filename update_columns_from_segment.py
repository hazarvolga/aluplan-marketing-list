#!/usr/bin/env python3
"""
Segment Sütunundan Boş Sütunları Doldurma
Segment sütunundaki bilgileri yeni oluşturulan üç sütuna aktarır
"""

import pandas as pd
import numpy as np
from datetime import datetime

def update_columns_from_segment():
    """
    Segment sütunundaki bilgileri yeni sütunlara aktar
    
    Mantık:
    - Segment = "Mevcut Müşteri" olanlar -> "Mevcut Müşteriler" sütununa "Mevcut Müşteri" yaz
    - Segment = "Sales Hub Mevcut" olanlar -> "Sales Hub" sütununa "Sales Hub Mevcut" yaz
    - Segment = "Potansiyel Müşteriler" olanlar -> "Mautic" sütununa "Potansiyel Müşteri" yaz
    """
    
    print("📝 SEGMENT SÜTUNUNDAN BOŞ SÜTUNLARI DOLDURMA")
    print("=" * 60)
    print(f"Başlangıç: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Birleştirilmiş dosyayı yükle
    print("\n📊 BİRLEŞTİRİLMİŞ LİSTEYİ YÜKLEME...")
    df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    print(f"   Toplam kayıt: {len(df):,}")
    print(f"   Sütunlar: {list(df.columns)}")
    
    # Segment dağılımını göster
    print("\n📈 MEVCUT SEGMENT DAĞILIMI:")
    segment_dist = df['Segment'].value_counts()
    for segment, count in segment_dist.items():
        print(f"   {segment}: {count:,}")
    
    # Boş sütunları kontrol et
    print("\n🔍 BOŞ SÜTUN KONTROLÜ:")
    print(f"   Mevcut Müşteriler boş sayısı: {df['Mevcut Müşteriler'].isnull().sum():,}")
    print(f"   Sales Hub boş sayısı: {df['Sales Hub'].isnull().sum():,}")
    print(f"   Mautic boş sayısı: {df['Mautic'].isnull().sum():,}")
    
    # Segmentleri yeni sütunlara aktar (Segment sütununu değiştirmeden)
    print("\n🔄 SEGMENT BİLGİLERİNİ YENİ SÜTUNLARA KOPYALAMA...")
    print("   NOT: Mevcut Segment sütunu değiştirilmeyecek!")
    
    updated_count = 0
    
    for idx, row in df.iterrows():
        segment = row['Segment']
        
        if pd.isna(segment) or segment.strip() == '':
            continue
            
        # Mevcut Müşteri olanları "Mevcut Müşteriler" sütununa kopyala
        if 'Mevcut Müşteri' in str(segment):
            df.at[idx, 'Mevcut Müşteriler'] = 'Mevcut Müşteri'
            updated_count += 1
            
        # Sales Hub olanları "Sales Hub" sütununa kopyala
        elif 'Sales Hub' in str(segment):
            df.at[idx, 'Sales Hub'] = 'Sales Hub'
            updated_count += 1
            
        # Mautic olanları "Mautic" sütununa kopyala
        elif 'Mautic' in str(segment):
            df.at[idx, 'Mautic'] = 'Mautic'
            updated_count += 1
    
    print(f"   Güncellenen kayıt: {updated_count:,}")
    
    # Güncellenmiş durumu göster
    print("\n📊 GÜNCELLENMİŞ SÜTUN DURUMU:")
    
    mevcut_count = df['Mevcut Müşteriler'].notna().sum()
    sales_hub_count = df['Sales Hub'].notna().sum()
    mautic_count = df['Mautic'].notna().sum()
    
    print(f"   Mevcut Müşteriler doldurulmuş: {mevcut_count:,}")
    print(f"   Sales Hub doldurulmuş: {sales_hub_count:,}")
    print(f"   Mautic doldurulmuş: {mautic_count:,}")
    
    # Değer örnekleri göster
    print("\n🔍 DEĞER ÖRNEKLERİ:")
    
    if mevcut_count > 0:
        mevcut_sample = df[df['Mevcut Müşteriler'].notna()]['Mevcut Müşteriler'].iloc[0]
        print(f"   Mevcut Müşteriler örneği: '{mevcut_sample}'")
    
    if sales_hub_count > 0:
        sales_sample = df[df['Sales Hub'].notna()]['Sales Hub'].iloc[0]
        print(f"   Sales Hub örneği: '{sales_sample}'")
        
    if mautic_count > 0:
        mautic_sample = df[df['Mautic'].notna()]['Mautic'].iloc[0]
        print(f"   Mautic örneği: '{mautic_sample}'")
    
    # Dosyayı kaydet
    print("\n💾 GÜNCELLENMIŞ DOSYAYI KAYDETME...")
    
    # Backup oluştur
    backup_file = f"veri_kaynaklari/birlestirilmis-liste-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    original_df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
    original_df.to_excel(backup_file, index=False)
    print(f"   Backup oluşturuldu: {backup_file}")
    
    # Ana dosyayı güncelle
    df.to_excel('veri_kaynaklari/birlestirilmis-liste.xlsx', index=False)
    print(f"   Ana dosya güncellendi: veri_kaynaklari/birlestirilmis-liste.xlsx")
    
    # data ve public klasörlerini de güncelle
    df.to_excel('data/aluplan-list.xlsx', index=False)
    print(f"   Data dosya güncellendi: data/aluplan-list.xlsx")
    
    df.to_excel('public/aluplan-list.xlsx', index=False)
    print(f"   Public dosya güncellendi: public/aluplan-list.xlsx")
    
    # Final rapor
    print("\n📋 FİNAL RAPOR:")
    print(f"   Toplam kayıt: {len(df):,}")
    print(f"   Mevcut Segment sütunu: DEĞİŞTİRİLMEDİ ✅")
    print(f"   Segment bilgilerinden kopyalanan: {updated_count:,}")
    print(f"   Mevcut Müşteriler sütunu: {mevcut_count:,} kayıt")
    print(f"   Sales Hub sütunu: {sales_hub_count:,} kayıt")
    print(f"   Mautic sütunu: {mautic_count:,} kayıt")
    
    print(f"\n✅ SEGMENT BİLGİLERİ YENİ SÜTUNLARA KOPYALANDI!")
    print("   Mevcut Segment sütunu korundu!")
    print(f"Bitiş: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return df

if __name__ == "__main__":
    update_columns_from_segment()
