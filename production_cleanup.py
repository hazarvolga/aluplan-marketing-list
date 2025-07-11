#!/usr/bin/env python3
"""
Production Veri Temizleme Scripti
Duplicate email'leri temizler ve veri kalitesini artırır
"""

import pandas as pd
from pathlib import Path
import numpy as np

def clean_production_data():
    """Production veri dosyasını temizle"""
    
    # Production dosyasını oku
    file_path = Path("public/aluplan-list.xlsx")
    df = pd.read_excel(file_path)
    
    print(f"📊 Temizlik öncesi: {len(df)} kayıt")
    
    # Duplicate email'leri temizle
    duplicate_count = df.duplicated(subset=['email']).sum()
    print(f"🔍 Duplicate email: {duplicate_count}")
    
    if duplicate_count > 0:
        # Duplicate'leri kaldır, ilkini sakla
        df_clean = df.drop_duplicates(subset=['email'], keep='first')
        print(f"✅ Duplicate'ler temizlendi: {len(df)} -> {len(df_clean)}")
        
        # Temizlenmiş veriyi kaydet
        backup_path = Path("public/aluplan-list-before-cleanup.xlsx")
        df.to_excel(backup_path, index=False)
        print(f"💾 Backup kaydedildi: {backup_path}")
        
        # Temizlenmiş veriyi production'a kaydet
        df_clean.to_excel(file_path, index=False)
        print(f"✅ Temizlenmiş veri kaydedildi: {file_path}")
        
        # Sonuçları kontrol et
        df_final = pd.read_excel(file_path)
        final_duplicates = df_final.duplicated(subset=['email']).sum()
        print(f"🎯 Final kontrol - Duplicate email: {final_duplicates}")
        
        # Segment analizi
        print("\n🎯 Temizlik sonrası segment dağılımı:")
        segment_counts = df_final['segment'].value_counts()
        for segment, count in segment_counts.items():
            print(f"  {segment}: {count}")
            
        return df_final
    else:
        print("✅ Duplicate email bulunamadı")
        return df

if __name__ == "__main__":
    clean_production_data()
