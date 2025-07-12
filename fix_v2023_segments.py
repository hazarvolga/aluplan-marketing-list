#!/usr/bin/env python3
"""
V2023 Segment Düzeltme Script'i
Bu script V2023 ve üzeri segmentlerini birleştirilmiş listeden email eşleştirmesi ile düzeltir
"""

import pandas as pd
import numpy as np
from datetime import datetime

def fix_v2023_segments():
    """V2023 segmentlerini birleştirilmiş listeden email eşleştirmesi ile düzelt"""
    
    print("🔍 V2023 SEGMENT DÜZELTME SÜRECI")
    print("=" * 50)
    
    # 1. Kaynak dosyayı yükle (birlestirilmis-liste.xlsx)
    try:
        source_df = pd.read_excel('veri_kaynaklari/birlestirilmis-liste.xlsx')
        print(f"✅ Kaynak dosya yüklendi: {len(source_df):,} kayıt")
    except Exception as e:
        print(f"❌ Kaynak dosya yükleme hatası: {e}")
        return
    
    # 2. Hedef dosyayı yükle (aluplan-list.xlsx)
    try:
        target_df = pd.read_excel('public/aluplan-list.xlsx')
        print(f"✅ Hedef dosya yüklendi: {len(target_df):,} kayıt")
    except Exception as e:
        print(f"❌ Hedef dosya yükleme hatası: {e}")
        return
    
    print(f"\n📋 Kaynak dosya sütunları: {list(source_df.columns)}")
    print(f"📋 Hedef dosya sütunları: {list(target_df.columns)}")
    
    # 3. V2023 ve üzeri kayıtları bul
    v2023_records = target_df[target_df['segment'] == 'V2023 ve üzeri'].copy()
    print(f"\n🎯 V2023 ve üzeri kayıt sayısı: {len(v2023_records):,}")
    
    # 4. Kaynak dosyada segment sütununu tespit et
    segment_column = None
    possible_segment_columns = ['Segment', 'segment', 'Unnamed: 4']
    
    for col in possible_segment_columns:
        if col in source_df.columns:
            segment_column = col
            break
    
    if not segment_column:
        print("❌ Kaynak dosyada segment sütunu bulunamadı!")
        return
    
    print(f"📊 Kaynak dosya segment sütunu: {segment_column}")
    
    # 5. Email eşleştirme ve segment düzeltme
    corrections = []
    not_found = []
    
    for idx, row in v2023_records.iterrows():
        email = row['email']
        
        # Kaynak dosyada bu email'i ara
        source_match = source_df[source_df['Main E-Mail'].str.lower() == email.lower()]
        
        if len(source_match) > 0:
            # Eşleşme bulundu
            source_row = source_match.iloc[0]
            original_segment = source_row[segment_column]
            
            # Segment değerini parse et
            if pd.notna(original_segment):
                # Virgülle ayrılmış segmentleri kontrol et
                if ',' in str(original_segment):
                    segment_list = [s.strip() for s in str(original_segment).split(',')]
                else:
                    segment_list = [str(original_segment).strip()]
                
                # Gerçek segmenti belirle
                real_segment = None
                if 'Mevcut Müşteriler' in segment_list:
                    real_segment = 'Mevcut Müşteriler'
                elif 'Sales Hub' in segment_list:
                    real_segment = 'Sales Hub Mevcut'
                elif 'Mautic' in segment_list:
                    real_segment = 'Potansiyel Müşteriler'
                else:
                    real_segment = segment_list[0]  # İlk segmenti al
                
                corrections.append({
                    'index': idx,
                    'email': email,
                    'name': row['name'],
                    'company': row['company'],
                    'old_segment': 'V2023 ve üzeri',
                    'new_segment': real_segment,
                    'original_segments': str(original_segment),
                    'license': row.get('license', 'N/A')
                })
            else:
                not_found.append({
                    'email': email,
                    'reason': 'Segment bilgisi boş'
                })
        else:
            not_found.append({
                'email': email,
                'reason': 'Email bulunamadı'
            })
    
    # 6. Sonuçları göster
    print(f"\n📊 EŞLEŞTIRME SONUÇLARI:")
    print(f"  ✅ Eşleşen kayıt: {len(corrections):,}")
    print(f"  ❌ Bulunamayan kayıt: {len(not_found):,}")
    
    if corrections:
        print(f"\n🔍 DÜZELTME DETAYLARI:")
        segment_counts = {}
        for correction in corrections:
            segment = correction['new_segment']
            segment_counts[segment] = segment_counts.get(segment, 0) + 1
        
        for segment, count in segment_counts.items():
            print(f"  📋 {segment}: {count} kayıt")
        
        # İlk 10 düzeltmeyi göster
        print(f"\n📋 İLK 10 DÜZELTME ÖRNEĞİ:")
        for i, correction in enumerate(corrections[:10]):
            print(f"  {i+1}. {correction['email']}")
            print(f"     Şirket: {correction['company']}")
            print(f"     Eski: {correction['old_segment']}")
            print(f"     Yeni: {correction['new_segment']}")
            print(f"     Kaynak: {correction['original_segments']}")
            print(f"     ---")
    
    if not_found:
        print(f"\n❌ BULUNAMAYAN KAYITLAR (İlk 5):")
        for item in not_found[:5]:
            print(f"  📧 {item['email']}: {item['reason']}")
        if len(not_found) > 5:
            print(f"  ... ve {len(not_found) - 5} tane daha")
    
    # 7. Düzeltmeleri uygula
    if corrections:
        print(f"\n🔧 DÜZELTME UYGULAMA:")
        
        # Backup oluştur
        backup_path = 'public/aluplan-list-backup-v2023.xlsx'
        target_df.to_excel(backup_path, index=False)
        print(f"✅ Backup kaydedildi: {backup_path}")
        
        # Düzeltmeleri uygula
        for correction in corrections:
            target_df.at[correction['index'], 'segment'] = correction['new_segment']
        
        # Düzeltilmiş dosyayı kaydet
        try:
            # Ana dosyayı güncelle
            main_path = 'public/aluplan-list.xlsx'
            target_df.to_excel(main_path, index=False)
            print(f"✅ Ana dosya güncellendi: {main_path}")
            
            # Data klasörünü de güncelle
            data_path = 'data/aluplan-list.xlsx'
            target_df.to_excel(data_path, index=False)
            print(f"✅ Data klasörü güncellendi: {data_path}")
            
            print(f"\n🎉 DÜZELTME BAŞARIYLA TAMAMLANDI!")
            print(f"  📊 Düzeltilen kayıt: {len(corrections):,}")
            print(f"  📋 Yeni segment dağılımı:")
            
            for segment, count in segment_counts.items():
                print(f"    {segment}: {count}")
            
            # Son kontrol
            final_v2023 = target_df[target_df['segment'] == 'V2023 ve üzeri']
            print(f"\n✅ FINAL KONTROL:")
            print(f"  Kalan 'V2023 ve üzeri' kayıt: {len(final_v2023):,}")
            
            if len(final_v2023) == 0:
                print("  🎯 Tüm V2023 kayıtları başarıyla düzeltildi!")
            else:
                print(f"  ⚠️  {len(final_v2023):,} kayıt hala V2023 olarak kaldı")
                
                # Kalan kayıtları göster
                print(f"\n📋 KALAN V2023 KAYITLARI:")
                for idx, row in final_v2023.head(10).iterrows():
                    print(f"  • {row['email']} - {row['name']} - {row['company']}")
            
            return target_df
            
        except Exception as e:
            print(f"❌ Dosya kaydetme hatası: {e}")
    
    return None

if __name__ == "__main__":
    print("🚀 V2023 SEGMENT DÜZELTME SCRIPT'İ")
    print("=" * 50)
    
    result = fix_v2023_segments()
    
    if result is not None:
        print(f"\n🎉 V2023 SEGMENT DÜZELTME TAMAMLANDI!")
        print(f"✅ Sistem artık güncel segmentlerle çalışacak")
        print(f"✅ Lisans filtreleme sistemi doğru lisansları gösterecek")
        print(f"✅ Değişiklikler hem frontend hem backend'e yansıtıldı")
        
        # Segment dağılımı göster
        print(f"\n📊 GÜNCEL SEGMENT DAĞILIMI:")
        segment_counts = result['segment'].value_counts()
        for segment, count in segment_counts.items():
            print(f"  {segment}: {count:,}")
        
        print(f"\n🔄 DEPLOYMENT İÇİN HAZIR!")
        print(f"  1. Değişiklikler kaydedildi")
        print(f"  2. Build ve deploy edilebilir")
        print(f"  3. Canlı sistemde test edilebilir")
        
    else:
        print(f"\n❌ V2023 segment düzeltme başarısız!")
        print(f"  Lütfen hata mesajlarını kontrol edin")
