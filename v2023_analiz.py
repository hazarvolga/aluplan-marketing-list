import pandas as pd
import numpy as np

print("🔍 V2023 SEGMENT DETAY ANALİZİ")
print("=" * 60)

# Veri kaynaklarını tek tek kontrol et
veri_klasoru = "veri_kaynaklari"

print("📊 KAYNAK DOSYALARI TEK TEK KONTROL:")
print("-" * 40)

# 1. V2023 dosyasını kontrol et
v2023_file = f"{veri_klasoru}/Allplan-V2023-ve ustu.xlsx"
df_v2023 = pd.read_excel(v2023_file)
print(f"🟣 V2023 DOSYASI:")
print(f"   📝 Toplam satır: {len(df_v2023):,}")
print(f"   📋 Sütunlar: {list(df_v2023.columns)}")

# Email sayısını kontrol et
valid_emails_v2023 = df_v2023['email'].notna().sum() if 'email' in df_v2023.columns else 0
print(f"   📧 Geçerli email: {valid_emails_v2023:,}")

# 2. Sales Hub dosyasını kontrol et
sales_file = f"{veri_klasoru}/All Contacts-Dynamics-365.xlsx"
df_sales = pd.read_excel(sales_file)
print(f"\n🟡 SALES HUB DOSYASI:")
print(f"   📝 Toplam satır: {len(df_sales):,}")
print(f"   📋 Sütunlar: {list(df_sales.columns)}")

# Email sayısını kontrol et
valid_emails_sales = df_sales['Email'].notna().sum() if 'Email' in df_sales.columns else 0
print(f"   📧 Geçerli email: {valid_emails_sales:,}")

# 3. V2022 dosyasını kontrol et
v2022_file = f"{veri_klasoru}/Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx"
df_v2022 = pd.read_excel(v2022_file)
print(f"\n🟠 V2022 DOSYASI:")
print(f"   📝 Toplam satır: {len(df_v2022):,}")
print(f"   📋 Sütunlar: {list(df_v2022.columns)}")

# Email sayısını kontrol et
valid_emails_v2022 = df_v2022['Main E-Mail'].notna().sum() if 'Main E-Mail' in df_v2022.columns else 0
print(f"   📧 Geçerli email: {valid_emails_v2022:,}")

# 4. Kontrol dosyasındaki V2023 segmentini analiz et
print(f"\n" + "=" * 60)
print("🔍 KONTROL DOSYASI V2023 ANALİZİ")
print("=" * 60)

df_kontrol = pd.read_excel("kontrol_dosyasi.xlsx")

# V2023 segmentindeki kayıtları filtrele
v2023_kontrol = df_kontrol[df_kontrol['isV2023'] == True]
print(f"📊 V2023 SEGMENT KONTROL:")
print(f"   📝 Toplam V2023 kayıt: {len(v2023_kontrol):,}")

# Segment kombinasyonlarını kontrol et
print(f"\n🎯 V2023 SEGMENT KOMBINASYONLARI:")
v2023_segments = v2023_kontrol['segment'].value_counts()
print(v2023_segments.head(10))

# Sadece V2023 olan kayıtları kontrol et
sadece_v2023 = v2023_kontrol[
    (v2023_kontrol['isV2023'] == True) & 
    (v2023_kontrol['isMautic'] == False) & 
    (v2023_kontrol['isSalesHubMevcut'] == False) & 
    (v2023_kontrol['isV2022'] == False)
]
print(f"\n🔍 SADECE V2023 OLAN KAYITLAR:")
print(f"   📝 Sadece V2023: {len(sadece_v2023):,}")

# Hem V2023 hem Sales Hub olan kayıtları kontrol et
v2023_sales = v2023_kontrol[
    (v2023_kontrol['isV2023'] == True) & 
    (v2023_kontrol['isSalesHubMevcut'] == True)
]
print(f"   📝 V2023 + Sales Hub: {len(v2023_sales):,}")

# Hem V2023 hem V2022 olan kayıtları kontrol et
v2023_v2022 = v2023_kontrol[
    (v2023_kontrol['isV2023'] == True) & 
    (v2023_kontrol['isV2022'] == True)
]
print(f"   📝 V2023 + V2022: {len(v2023_v2022):,}")

print(f"\n💡 ANALİZ SONUCU:")
print(f"   Ham V2023 dosyası: {len(df_v2023):,} satır")
print(f"   V2023 geçerli email: {valid_emails_v2023:,}")
print(f"   Kontrol'de V2023 segment: {len(v2023_kontrol):,}")
print(f"   Bu sayı NORMAL değil! Segment tanımında hata var.")

# V2023 dosyasının ilk 10 kaydını göster
print(f"\n📋 V2023 DOSYASI İLK 10 KAYIT:")
print(df_v2023[['name', 'email', 'Acount Name']].head(10).to_string(index=False))
