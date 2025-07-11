import pandas as pd
import numpy as np

print("🔍 YENİ VERİ SETİ ANALİZİ")
print("=" * 50)

# Yeni veri setini analiz et
yeni_file = "data/aluplan-list.xlsx"
df_yeni = pd.read_excel(yeni_file)

print(f"📊 YENİ VERİ SETİ:")
print(f"   📁 Dosya: {yeni_file}")
print(f"   📝 Toplam kayıt: {len(df_yeni):,}")
print(f"   📋 Sütun sayısı: {len(df_yeni.columns)}")
print(f"   🏷️  Sütun isimleri: {list(df_yeni.columns)}")

# İlk 5 kayıt
print(f"\n📋 İLK 5 KAYIT:")
print(df_yeni.head().to_string(index=False))

# Segment analizi
segment_dagilimi = df_yeni['segment'].value_counts()
print(f"\n🎯 SEGMENT DAĞILIMI:")
for segment, count in segment_dagilimi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Email kalitesi analizi
email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
gecerli_email = df_yeni['email'].str.contains(email_pattern, regex=True, na=False).sum()
print(f"\n📧 EMAIL KALİTESİ:")
print(f"   📧 Geçerli email formatı: {gecerli_email:,}")
print(f"   📧 Toplam email: {df_yeni['email'].notna().sum():,}")
print(f"   📧 Boş email: {df_yeni['email'].isna().sum():,}")

# Eksik veri analizi
print(f"\n🔍 EKSİK VERİ ANALİZİ:")
for col in ['name', 'email', 'company']:
    if col in df_yeni.columns:
        eksik = df_yeni[col].isna().sum()
        print(f"   ❌ {col}: {eksik:,} eksik kayıt")

print(f"\n" + "=" * 50)
print("🆚 ESKİ VE YENİ VERİ KARŞILAŞTIRMA")
print("=" * 50)

# Eski veri setini oku
try:
    eski_file = "data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx"
    df_eski = pd.read_excel(eski_file)
    
    print(f"📊 KARŞILAŞTIRMA:")
    print(f"   📱 Eski sistem: {len(df_eski):,} kayıt")
    print(f"   🔧 Yeni sistem: {len(df_yeni):,} kayıt")
    print(f"   🔺 Fark: {len(df_yeni) - len(df_eski):,} kayıt")
    
    # Eski sistem segment sayıları
    if 'isMautic' in df_eski.columns:
        print(f"\n🎯 ESKİ SİSTEM SEGMENT SAYILARI:")
        print(f"   📧 Mautic: {df_eski['isMautic'].sum():,}")
        print(f"   📧 Sales Hub: {df_eski['isSalesHubMevcut'].sum():,}")
        print(f"   📧 V2022: {df_eski['isV2022'].sum():,}")
        print(f"   📧 V2023: {df_eski['isV2023'].sum():,}")
    
    # Yeni sistem segment sayıları
    print(f"\n🎯 YENİ SİSTEM SEGMENT SAYILARI:")
    for segment, count in segment_dagilimi.items():
        print(f"   📧 {segment}: {count:,}")
    
except Exception as e:
    print(f"❌ Eski dosya okunamadı: {e}")

print(f"\n" + "=" * 50)
print("✅ YENİ VERİ SETİ HAZIR")
print("=" * 50)
print(f"✅ Toplam kayıt: {len(df_yeni):,}")
print(f"✅ Mevcut Müşteriler: {segment_dagilimi.get('Mevcut Müşteriler', 0):,}")
print(f"✅ Kaynak: Allplan Müşteriler_Final_2025-03-19-R28.xlsx")
print(f"✅ Uygulama lokasyonu: http://localhost:3000")
