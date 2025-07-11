#!/usr/bin/env python3
"""
Veri Tutarlılığı Analiz Scripti - Aluplan Marketing List
Bu script tüm proje genelinde veri tutarlılığını analiz eder
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import re

def analyze_excel_file(file_path):
    """Excel dosyasını analiz et"""
    try:
        # Excel dosyasını oku
        df = pd.read_excel(file_path)
        
        print(f"\n📊 {file_path} Analizi:")
        print("=" * 50)
        
        # Temel bilgiler
        print(f"Toplam kayıt sayısı: {len(df)}")
        print(f"Sütun sayısı: {len(df.columns)}")
        print(f"Sütunlar: {list(df.columns)}")
        
        # Boş değer analizi
        print("\n📈 Boş Değer Analizi:")
        null_counts = df.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                print(f"  {col}: {count} ({percentage:.1f}%)")
        
        # Email analizi
        if 'email' in df.columns:
            print("\n📧 Email Analizi:")
            email_series = df['email'].dropna()
            print(f"  Toplam email: {len(email_series)}")
            print(f"  Unique email: {email_series.nunique()}")
            print(f"  Duplicate email: {len(email_series) - email_series.nunique()}")
            
            # Email format kontrolü
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            valid_emails = email_series.str.match(email_pattern)
            print(f"  Geçerli email formatı: {valid_emails.sum()}")
            print(f"  Geçersiz email formatı: {(~valid_emails).sum()}")
        
        # Segment analizi
        if 'segment' in df.columns:
            print("\n🎯 Segment Analizi:")
            segment_series = df['segment'].dropna()
            print(f"  Segment bilgisi olan kayıt: {len(segment_series)}")
            
            # Segment değerlerini analiz et
            all_segments = []
            for segments in segment_series:
                if pd.isna(segments):
                    continue
                segment_list = [s.strip() for s in str(segments).split(',')]
                all_segments.extend(segment_list)
            
            segment_counts = pd.Series(all_segments).value_counts()
            print("  Segment dağılımı:")
            for segment, count in segment_counts.items():
                print(f"    {segment}: {count}")
        
        # Company analizi
        if 'company' in df.columns:
            print("\n🏢 Company Analizi:")
            company_series = df['company'].dropna()
            print(f"  Company bilgisi olan kayıt: {len(company_series)}")
            print(f"  Unique company: {company_series.nunique()}")
        
        return {
            'file_path': str(file_path),
            'total_records': len(df),
            'columns': list(df.columns),
            'null_counts': null_counts.to_dict(),
            'unique_emails': email_series.nunique() if 'email' in df.columns else 0,
            'duplicate_emails': (len(email_series) - email_series.nunique()) if 'email' in df.columns else 0
        }
        
    except Exception as e:
        print(f"❌ Hata: {file_path} - {str(e)}")
        return None

def main():
    """Ana fonksiyon"""
    print("🔍 ALUPLAN MARKETING LIST - VERİ TUTARLILIĞI ANALİZİ")
    print("=" * 60)
    print(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Proje dizinini bul
    project_dir = Path(__file__).parent
    
    # Analiz edilecek Excel dosyalarını bul
    excel_files = []
    
    # Ana dizindeki Excel dosyaları
    for file in project_dir.glob("*.xlsx"):
        excel_files.append(file)
    
    # Public dizinindeki Excel dosyaları
    public_dir = project_dir / "public"
    if public_dir.exists():
        for file in public_dir.glob("*.xlsx"):
            excel_files.append(file)
    
    # Data dizinindeki Excel dosyaları (varsa)
    data_dir = project_dir / "data"
    if data_dir.exists():
        for file in data_dir.glob("*.xlsx"):
            excel_files.append(file)
    
    print(f"\n📁 Bulunan Excel dosyaları: {len(excel_files)}")
    for file in excel_files:
        print(f"  - {file}")
    
    # Her dosyayı analiz et
    results = []
    for file in excel_files:
        result = analyze_excel_file(file)
        if result:
            results.append(result)
    
    # Sonuçları kaydet
    output_file = project_dir / "veri_tutarlilik_analizi.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Analiz sonuçları kaydedildi: {output_file}")
    
    # Özet rapor
    print("\n📊 ÖZET RAPOR:")
    print("=" * 30)
    total_records = sum(r['total_records'] for r in results)
    total_unique_emails = sum(r['unique_emails'] for r in results)
    total_duplicate_emails = sum(r['duplicate_emails'] for r in results)
    
    print(f"Toplam dosya sayısı: {len(results)}")
    print(f"Toplam kayıt sayısı: {total_records}")
    print(f"Toplam unique email: {total_unique_emails}")
    print(f"Toplam duplicate email: {total_duplicate_emails}")
    
    print("\n✅ Veri tutarlılığı analizi tamamlandı!")

if __name__ == "__main__":
    main()
