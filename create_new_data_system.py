#!/usr/bin/env python3
"""
Yeni Veri Sistemi için Excel Dosyası Oluşturma
Şu sayılara göre:
- Mevcut Müşteriler: 1,260 (Dynamics 365 + Allplan Final)
- Potansiyel Müşteriler: 2,660 (mautic-tum-liste.xlsx)
- Sales Hub Mevcut: 1,030 (küçük kart)
- V2022 ve eski: 800 (küçük kart)
- V2023 için başka çözüm bulunacak
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_new_data_system():
    """Yeni veri sistemi için Excel dosyası oluştur"""
    
    print("🚀 YENİ VERİ SİSTEMİ OLUŞTURMA")
    print("=" * 60)
    print(f"Oluşturma Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Temizlenmiş veri dosyasını yükle
    temizlenmis_dosya = "veri_kaynaklari/birlestirilmis-liste-TEMIZLENMIS.xlsx"
    
    try:
        df = pd.read_excel(temizlenmis_dosya)
        print(f"\n📊 Temizlenmiş veri yüklendi: {len(df):,} kayıt")
        
        # Segment analizi
        print(f"\n🔍 SEGMENT ANALİZİ:")
        
        # Segment sütununu tespit et
        segment_column = None
        if 'Segment' in df.columns:
            segment_column = 'Segment'
        elif 'segment' in df.columns:
            segment_column = 'segment'
        elif 'Unnamed: 4' in df.columns:
            segment_column = 'Unnamed: 4'
        else:
            print("❌ Segment sütunu bulunamadı!")
            return
        
        print(f"📊 Segment sütunu: {segment_column}")
        
        # Hedef segmentleri ayır
        mevcut_musteriler = []
        potansiyel_musteriler = []
        sales_hub_mevcut = []
        v2022_emails = set()
        
        # V2022 email listesini yükle
        v2022_dosya = "veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx"
        try:
            v2022_df = pd.read_excel(v2022_dosya)
            v2022_emails = set(v2022_df['Main E-Mail'].dropna().str.lower().str.strip())
            print(f"📧 V2022 email listesi yüklendi: {len(v2022_emails):,} email")
        except Exception as e:
            print(f"⚠️ V2022 dosyası yüklenemedi: {e}")
        
        # Mautic listesini yükle
        mautic_dosya = "veri_kaynaklari/mautic-tum-liste.xlsx"
        try:
            mautic_df = pd.read_excel(mautic_dosya)
            print(f"📧 Mautic listesi yüklendi: {len(mautic_df):,} kayıt")
        except Exception as e:
            print(f"⚠️ Mautic dosyası yüklenemedi: {e}")
        
        # Kayıtları sınıflandır
        for idx, row in df.iterrows():
            email = row.get('Main E-Mail', '')
            if pd.isna(email):
                continue
                
            email = email.strip().lower()
            segments = row.get(segment_column, '')
            if pd.isna(segments):
                continue
                
            # Segmentleri parse et
            if ',' in str(segments):
                segment_list = [s.strip() for s in str(segments).split(',')]
            else:
                segment_list = [str(segments).strip()]
            
            # Kayıt verilerini hazırla
            kayit = {
                'name': row.get('Name', ''),
                'email': email,
                'company': row.get('Acount Name', ''),
                'phone': row.get('Phone', ''),
                'segment': '',  # Yeni segment sistemi
                'original_segment': segments  # Orijinal segment bilgisi
            }
            
            # Segment sınıflandırması
            if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
                kayit['segment'] = 'Mevcut Müşteriler'
                mevcut_musteriler.append(kayit)
            elif any(seg in segment_list for seg in ['Sales Hub Mevcut', 'Sales Hub']):
                kayit['segment'] = 'Sales Hub Mevcut'
                sales_hub_mevcut.append(kayit)
            elif any(seg in segment_list for seg in ['Potansiyel Müşteriler', 'Potansiyel', 'Mautic']):
                kayit['segment'] = 'Potansiyel Müşteriler'
                potansiyel_musteriler.append(kayit)
            
        print(f"\n📊 SINIFLANDIRMA SONUÇLARI:")
        print(f"  🏢 Mevcut Müşteriler: {len(mevcut_musteriler):,}")
        print(f"  🎯 Potansiyel Müşteriler: {len(potansiyel_musteriler):,}")
        print(f"  🔧 Sales Hub Mevcut: {len(sales_hub_mevcut):,}")
        
        # Yeni veri sistemi oluştur
        all_records = []
        
        # Mevcut müşteriler (1,260 hedef)
        for kayit in mevcut_musteriler[:1260]:
            all_records.append(kayit)
        
        # Potansiyel müşteriler (2,660 hedef)
        for kayit in potansiyel_musteriler[:2660]:
            all_records.append(kayit)
        
        # Sales Hub mevcut (1,030 hedef)
        for kayit in sales_hub_mevcut[:1030]:
            all_records.append(kayit)
        
        # V2022 email kontrolü ekle
        for kayit in all_records:
            if kayit['email'] in v2022_emails:
                if kayit['segment'] == 'Mevcut Müşteriler':
                    kayit['segment'] = 'Mevcut Müşteriler,V2022'
                elif kayit['segment'] == 'Sales Hub Mevcut':
                    kayit['segment'] = 'Sales Hub Mevcut,V2022'
                elif kayit['segment'] == 'Potansiyel Müşteriler':
                    kayit['segment'] = 'Potansiyel Müşteriler,V2022'
        
        # DataFrame oluştur
        yeni_df = pd.DataFrame(all_records)
        
        # Sonuçları analiz et
        print(f"\n📈 YENİ VERİ SİSTEMİ SONUÇLARI:")
        print(f"  📊 Toplam kayıt: {len(yeni_df):,}")
        
        # Segment sayıları
        segment_counts = yeni_df['segment'].value_counts()
        print(f"\n📊 SEGMENT DAĞILIMI:")
        for segment, count in segment_counts.items():
            print(f"  {segment}: {count:,}")
        
        # V2022 analizi
        v2022_count = yeni_df[yeni_df['segment'].str.contains('V2022', na=False)].shape[0]
        print(f"\n🕐 V2022 ANALİZİ:")
        print(f"  V2022 içeren kayıt: {v2022_count:,}")
        
        # Yeni dosyayı kaydet
        output_file = "public/aluplan-list-new-system.xlsx"
        yeni_df.to_excel(output_file, index=False)
        print(f"\n💾 YENİ VERİ SİSTEMİ KAYDEDILDI:")
        print(f"  📁 Dosya: {output_file}")
        print(f"  📊 Kayıt sayısı: {len(yeni_df):,}")
        
        # Hedef sayılarla karşılaştır
        print(f"\n🎯 HEDEF SAYILARLA KARŞILAŞTIRMA:")
        mevcut_count = yeni_df[yeni_df['segment'].str.contains('Mevcut Müşteriler', na=False)].shape[0]
        potansiyel_count = yeni_df[yeni_df['segment'].str.contains('Potansiyel Müşteriler', na=False)].shape[0]
        sales_hub_count = yeni_df[yeni_df['segment'].str.contains('Sales Hub Mevcut', na=False)].shape[0]
        
        print(f"  🏢 Mevcut Müşteriler: {mevcut_count:,} / 1,260 (Hedef)")
        print(f"  🎯 Potansiyel Müşteriler: {potansiyel_count:,} / 2,660 (Hedef)")
        print(f"  🔧 Sales Hub Mevcut: {sales_hub_count:,} / 1,030 (Hedef)")
        print(f"  🕐 V2022 ve eski: {v2022_count:,} / 800 (Hedef)")
        
        # Başarı oranları
        print(f"\n✅ BAŞARI ORANLARI:")
        print(f"  Mevcut Müşteriler: {(mevcut_count/1260)*100:.1f}%")
        print(f"  Potansiyel Müşteriler: {(potansiyel_count/2660)*100:.1f}%")
        print(f"  Sales Hub Mevcut: {(sales_hub_count/1030)*100:.1f}%")
        print(f"  V2022 ve eski: {(v2022_count/800)*100:.1f}%")
        
        return yeni_df
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return None

if __name__ == "__main__":
    result = create_new_data_system()
    if result is not None:
        print(f"\n🚀 YENİ VERİ SİSTEMİ BAŞARIYLA OLUŞTURULDU!")
        print(f"Frontend'de test edilebilir.")
    else:
        print("❌ Yeni veri sistemi oluşturulamadı!")
