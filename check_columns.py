#!/usr/bin/env python3
"""
Temizlenmiş veri sütunlarını kontrol et
"""

import pandas as pd

# Dosyayı yükle
df = pd.read_excel("veri_kaynaklari/birlestirilmis-liste-TEMIZLENMIS.xlsx")

print("📊 Sütun bilgileri:")
print(f"Toplam kayıt: {len(df):,}")
print(f"Toplam sütun: {len(df.columns)}")
print("\nSütunlar:")
for i, col in enumerate(df.columns):
    print(f"  {i+1}. {col}")

print("\nİlk 3 kayıt:")
print(df.head(3))
