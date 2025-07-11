import pandas as pd
import numpy as np

print("🎉 GÜNCEL VERİ SETİ ANALİZİ")
print("=" * 50)

# Güncel veri setini analiz et
df = pd.read_excel('data/aluplan-list.xlsx')

print(f"📊 GÜNCEL VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df):,}")
print(f"   📋 Sütun sayısı: {len(df.columns)}")

# Segment analizi
segment_dagilimi = df['segment'].value_counts()
print(f"\n🎯 SEGMENT DAĞILIMI:")
for segment, count in segment_dagilimi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Kaynak analizi
print(f"\n📁 KAYNAK DAĞILIMI:")
kaynak_dagilimi = df['source'].value_counts()
for kaynak, count in kaynak_dagilimi.items():
    if pd.notna(kaynak):
        print(f"   📄 {kaynak}: {count:,} kayıt")

# Email kalitesi
email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
gecerli_email = df['email'].str.contains(email_pattern, regex=True, na=False).sum()
print(f"\n📧 EMAIL KALİTESİ:")
print(f"   📧 Geçerli email formatı: {gecerli_email:,}")
print(f"   📧 Toplam email: {df['email'].notna().sum():,}")

# Veri tamamlığı
print(f"\n📊 VERİ TAMAMLIĞI:")
print(f"   📝 Name dolu: {df['name'].notna().sum():,}")
print(f"   📧 Email dolu: {df['email'].notna().sum():,}")
print(f"   🏢 Company dolu: {df['company'].notna().sum():,}")

print(f"\n" + "=" * 50)
print("🌟 UYGULAMA DURUMU")
print("=" * 50)
print(f"✅ Mevcut Müşteriler: {segment_dagilimi.get('Mevcut Müşteriler', 0):,}")
print(f"✅ Potansiyel Müşteriler: {segment_dagilimi.get('Potansiyel Müşteriler', 0):,}")
print(f"✅ Toplam Kayıt: {len(df):,}")
print(f"✅ Uygulama: http://localhost:3001")
print(f"✅ Yeni segment yapısı hazır!")

print(f"\n🔄 YENİ FİLTRELER:")
print(f"   📋 Mevcut Müşteriler (Allplan müşterileri)")
print(f"   📋 Potansiyel Müşteriler (Mautic'ten gelen adaylar)")
print(f"   📋 Sales Hub Mevcut")
print(f"   📋 V2022 ve eski") 
print(f"   📋 V2023 ve üzeri")
