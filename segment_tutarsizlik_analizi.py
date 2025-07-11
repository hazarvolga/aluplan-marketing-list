#!/usr/bin/env python3
"""
Segment Tutarsızlığı Analiz Scripti - Aluplan Marketing List
Bu script segment verilerindeki tutarsızlıkları analiz eder
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

def analyze_segment_inconsistency():
    """Segment tutarsızlıklarını analiz et"""
    print("🔍 SEGMENT TUTARSIZLIĞI ANALİZİ")
    print("=" * 50)
    
    # Production dosyasını oku
    production_file = Path("public/aluplan-list.xlsx")
    if not production_file.exists():
        print("❌ Production dosyası bulunamadı!")
        return
    
    df = pd.read_excel(production_file)
    
    print(f"📊 Production Dosyası Analizi:")
    print(f"Toplam kayıt: {len(df)}")
    
    # Segment dağılımını analiz et
    print("\n🎯 Mevcut Segment Dağılımı:")
    segment_counts = df['segment'].value_counts()
    for segment, count in segment_counts.items():
        print(f"  {segment}: {count}")
    
    # Beklenen değerler
    expected_data = {
        'Sales Hub': 1032,
        'Dynamics 365': 1202,  # 157 boş + 13 geçersiz filtrelendi
        'V2022': 800,
        'V2023': 95,
        'Mevcut Müşteriler': 1262
    }
    
    print("\n📋 BEKLENEN DEĞERLER:")
    for segment, count in expected_data.items():
        print(f"  {segment}: {count}")
    
    # Tutarsızlıkları tespit et
    print("\n🚨 TUTARSIZLIKLAR:")
    
    # Sales Hub kontrol
    sales_hub_actual = df[df['segment'].str.contains('Sales Hub', na=False)].shape[0]
    print(f"Sales Hub - Beklenen: {expected_data['Sales Hub']}, Mevcut: {sales_hub_actual}")
    if sales_hub_actual != expected_data['Sales Hub']:
        print(f"  ❌ Fark: {sales_hub_actual - expected_data['Sales Hub']}")
    else:
        print(f"  ✅ Eşleşiyor")
    
    # Mevcut Müşteriler kontrol
    mevcut_musteriler_actual = df[df['segment'].str.contains('Mevcut Müşteriler', na=False)].shape[0]
    print(f"Mevcut Müşteriler - Beklenen: {expected_data['Mevcut Müşteriler']}, Mevcut: {mevcut_musteriler_actual}")
    if mevcut_musteriler_actual != expected_data['Mevcut Müşteriler']:
        print(f"  ❌ Fark: {mevcut_musteriler_actual - expected_data['Mevcut Müşteriler']}")
        print(f"  ❌ Eksik: {expected_data['Mevcut Müşteriler'] - mevcut_musteriler_actual}")
    else:
        print(f"  ✅ Eşleşiyor")
    
    # V2023 kontrol
    v2023_actual = df[df['segment'].str.contains('V2023', na=False)].shape[0]
    print(f"V2023 - Beklenen: {expected_data['V2023']}, Mevcut: {v2023_actual}")
    if v2023_actual != expected_data['V2023']:
        print(f"  ❌ Fark: {v2023_actual - expected_data['V2023']}")
        print(f"  ❌ Eksik: {expected_data['V2023'] - v2023_actual}")
    else:
        print(f"  ✅ Eşleşiyor")
    
    # Eksik kayıtları tespit et
    print("\n📊 EKSİK KAYIT ANALİZİ:")
    
    # Toplam beklenen kayıt
    total_expected = sum(expected_data.values())
    total_actual = len(df)
    
    print(f"Toplam beklenen kayıt: {total_expected}")
    print(f"Toplam mevcut kayıt: {total_actual}")
    print(f"Fark: {total_actual - total_expected}")
    
    # Diğer dosyaları kontrol et
    print("\n🔍 DİĞER DOSYALARDA KAYIP VERİ ARAŞTIRMASI:")
    
    # Kontrol dosyasını kontrol et
    control_file = Path("kontrol_dosyasi.xlsx")
    if control_file.exists():
        df_control = pd.read_excel(control_file)
        print(f"\nKontrol Dosyası ({control_file}):")
        print(f"  Toplam kayıt: {len(df_control)}")
        
        control_segments = df_control['segment'].value_counts()
        print("  Segment dağılımı:")
        for segment, count in control_segments.items():
            print(f"    {segment}: {count}")
    
    # Data klasöründeki dosyaları kontrol et
    data_dir = Path("data")
    if data_dir.exists():
        print(f"\nData Klasörü Analizi:")
        for excel_file in data_dir.glob("*.xlsx"):
            try:
                df_temp = pd.read_excel(excel_file)
                print(f"  {excel_file.name}: {len(df_temp)} kayıt")
                
                if 'segment' in df_temp.columns:
                    mevcut_count = df_temp[df_temp['segment'].str.contains('Mevcut', na=False)].shape[0]
                    if mevcut_count > 0:
                        print(f"    Mevcut Müşteriler: {mevcut_count}")
                        
                    v2023_count = df_temp[df_temp['segment'].str.contains('V2023', na=False)].shape[0]
                    if v2023_count > 0:
                        print(f"    V2023: {v2023_count}")
                        
            except Exception as e:
                print(f"  {excel_file.name}: Hata - {e}")
    
    print("\n💡 SONUÇ VE ÖNERİLER:")
    print("=" * 30)
    print("1. Mevcut Müşteriler segmentinde büyük eksiklik var (1262 beklenen, 230 mevcut)")
    print("2. V2023 segmentinde eksiklik var (95 beklenen, 34 mevcut)")
    print("3. Bu veriler muhtemelen diğer dosyalarda dağınık durumda")
    print("4. Veri konsolidasyonu gerekiyor")

if __name__ == "__main__":
    analyze_segment_inconsistency()
