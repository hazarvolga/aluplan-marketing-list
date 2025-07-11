import pandas as pd
import numpy as np
from datetime import datetime

print("🔍 MEVCUT MÜŞTERİLER VERİSİ DETAYLI ANALİZ")
print("=" * 60)

# Kaynak dosyayı farklı satırlardan okuyalım
kaynak_dosya = "veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx"

# Önce ilk birkaç satırı okuyalım
print("📋 DOSYA BAŞLIKLARI VE İLK SATIRLAR:")
for i in range(5):
    try:
        df_test = pd.read_excel(kaynak_dosya, header=i)
        print(f"\n🔍 Header={i} ile okunan sütunlar:")
        print(f"   📝 Sütun sayısı: {len(df_test.columns)}")
        print(f"   🏷️  Sütun isimleri: {list(df_test.columns)}")
        print(f"   📊 İlk satır verisi:")
        if len(df_test) > 0:
            print(f"   {df_test.iloc[0].to_dict()}")
    except Exception as e:
        print(f"❌ Header={i} hatası: {e}")

# En uygun header satırını bulalım
print(f"\n" + "=" * 60)
print("🎯 EN UYGUN HEADER SATIRI BULMA")
print("=" * 60)

# Header=1 ile tekrar okuyalım (genellikle Excel dosyalarında ikinci satır başlık olur)
try:
    df_kaynak = pd.read_excel(kaynak_dosya, header=1)
    print(f"📊 Header=1 ile okunan veri:")
    print(f"   📝 Toplam kayıt: {len(df_kaynak):,}")
    print(f"   📋 Sütun sayısı: {len(df_kaynak.columns)}")
    print(f"   🏷️  Sütun isimleri: {list(df_kaynak.columns)}")
    
    # İlk 3 kayıt
    print(f"\n📋 İLK 3 KAYIT:")
    print(df_kaynak.head(3).to_string(index=False))
    
    # Email ve şirket sütunlarını tekrar ara
    print(f"\n🔍 VERİ SÜTUNLARI ARAMA:")
    
    # Tüm sütunları kontrol et
    for col in df_kaynak.columns:
        sample_values = df_kaynak[col].dropna().head(3).tolist()
        print(f"   📝 {col}: {sample_values}")
    
    # Email pattern arama
    print(f"\n🔍 EMAIL PATTERN ARAMA:")
    email_found = False
    for col in df_kaynak.columns:
        if col and pd.notna(col):
            # Bu sütunda @ içeren değerler var mı?
            has_email = df_kaynak[col].astype(str).str.contains('@', na=False).any()
            if has_email:
                email_count = df_kaynak[col].astype(str).str.contains('@', na=False).sum()
                print(f"   📧 {col}: {email_count:,} email adresi bulundu")
                email_found = True
    
    if not email_found:
        print("   ❌ Hiçbir sütunda email pattern bulunamadı")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    
print(f"\n" + "=" * 60)
print("📝 MANUAL VERİ KONTROLÜ")
print("=" * 60)

# Eğer email bulunamazsa, dosyayı farklı yollarla okuyalım
try:
    # Tüm veriyi string olarak okuyalım
    df_raw = pd.read_excel(kaynak_dosya, header=None)
    print(f"📊 RAW VERİ (Header=None):")
    print(f"   📝 Toplam satır: {len(df_raw):,}")
    print(f"   📋 Sütun sayısı: {len(df_raw.columns)}")
    
    print(f"\n📋 İLK 10 SATIRDA EMAIL ARAMA:")
    for i in range(min(10, len(df_raw))):
        row = df_raw.iloc[i]
        for j, value in enumerate(row):
            if pd.notna(value) and '@' in str(value):
                print(f"   🎯 Satır {i+1}, Sütun {j+1}: {value}")
    
except Exception as e:
    print(f"❌ Raw okuma hatası: {e}")
