import pandas as pd
import numpy as np

print("🎯 MAUTIC POTANSİYEL MÜŞTERİ ANALİZİ")
print("=" * 60)

# Mevcut uygulama verisi
df_app = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx")

# Ham Mautic verisi
df_mautic_raw = pd.read_excel("veri_kaynaklari/mautic-tum-liste.xlsx")

print(f"📊 MEVCUT DURUMU:")
print(f"   📱 Uygulama toplam kayıt: {len(df_app):,}")
print(f"   🟢 Mautic segment: {df_app['Mautic'].sum():,}")
print(f"   🟡 Sales Hub Mevcut: {df_app['Sales_Hub_Mevcut'].sum():,}")
print(f"   🟠 V2022 ve eski: {df_app['V2022_ve_eski'].sum():,}")
print(f"   🟣 V2023 ve üzeri: {df_app['V2023_ve_uzeri'].sum():,}")

print(f"\n   📂 Ham Mautic dosyası: {len(df_mautic_raw):,} kayıt")
print(f"   📧 Ham Mautic geçerli email: {df_mautic_raw['email'].notna().sum():,}")

print(f"\n🔍 MAUTIC SEGMENT ANALİZİ:")

# Sadece Mautic segmentindeki kayıtları al
mautic_kayitlar = df_app[df_app['Mautic'] == True]
print(f"   📝 Toplam Mautic kayıt: {len(mautic_kayitlar):,}")

# Sadece Mautic olan (diğer segmentlerde olmayan) kayıtları bul
sadece_mautic = mautic_kayitlar[
    (mautic_kayitlar['Mautic'] == True) & 
    (mautic_kayitlar['Sales_Hub_Mevcut'] == False) & 
    (mautic_kayitlar['V2022_ve_eski'] == False) & 
    (mautic_kayitlar['V2023_ve_uzeri'] == False)
]

print(f"   🎯 Sadece Mautic (potansiyel müşteri): {len(sadece_mautic):,}")

# Mautic + diğer segmentlerdeki kayıtları (mevcut müşteriler)
mautic_sales = mautic_kayitlar[
    (mautic_kayitlar['Mautic'] == True) & 
    (mautic_kayitlar['Sales_Hub_Mevcut'] == True)
]

mautic_v2022 = mautic_kayitlar[
    (mautic_kayitlar['Mautic'] == True) & 
    (mautic_kayitlar['V2022_ve_eski'] == True)
]

mautic_v2023 = mautic_kayitlar[
    (mautic_kayitlar['Mautic'] == True) & 
    (mautic_kayitlar['V2023_ve_uzeri'] == True)
]

print(f"   🔄 Mautic + Sales Hub: {len(mautic_sales):,}")
print(f"   🔄 Mautic + V2022: {len(mautic_v2022):,}")
print(f"   🔄 Mautic + V2023: {len(mautic_v2023):,}")

# Mautic'te olan ama herhangi bir mevcut müşteri segmentinde olmayan kayıtlar
mevcut_musteri_kayitlar = mautic_kayitlar[
    (mautic_kayitlar['Sales_Hub_Mevcut'] == True) |
    (mautic_kayitlar['V2022_ve_eski'] == True) |
    (mautic_kayitlar['V2023_ve_uzeri'] == True)
]

potansiyel_musteri_kayitlar = mautic_kayitlar[
    (mautic_kayitlar['Sales_Hub_Mevcut'] == False) &
    (mautic_kayitlar['V2022_ve_eski'] == False) &
    (mautic_kayitlar['V2023_ve_uzeri'] == False)
]

print(f"\n📊 SONUÇLAR:")
print(f"   🟢 Toplam Mautic: {len(mautic_kayitlar):,}")
print(f"   🔴 Mevcut müşteri (Mautic'te): {len(mevcut_musteri_kayitlar):,}")
print(f"   🟢 Potansiyel müşteri (Mautic'te): {len(potansiyel_musteri_kayitlar):,}")

print(f"\n✅ DOĞRULAMA:")
print(f"   Mevcut + Potansiyel = {len(mevcut_musteri_kayitlar)} + {len(potansiyel_musteri_kayitlar)} = {len(mevcut_musteri_kayitlar) + len(potansiyel_musteri_kayitlar)}")
print(f"   Toplam Mautic = {len(mautic_kayitlar)}")
print(f"   Eşit mi? {'✅ Evet' if len(mevcut_musteri_kayitlar) + len(potansiyel_musteri_kayitlar) == len(mautic_kayitlar) else '❌ Hayır'}")

print(f"\n📋 POTANSİYEL MÜŞTERİLERDEN ÖRNEKLER:")
for i, row in potansiyel_musteri_kayitlar.head(10).iterrows():
    print(f"   • {row['name']} - {row['email']} - {row['company']}")

print(f"\n💡 ÖZET:")
print(f"   🎯 Toplam Mautic listesi: {len(mautic_kayitlar):,}")
print(f"   🔴 Bunların {len(mevcut_musteri_kayitlar):,} tanesi zaten mevcut müşteri")
print(f"   🟢 Gerçek potansiyel müşteri: {len(potansiyel_musteri_kayitlar):,}")
print(f"   📊 Potansiyel müşteri oranı: {len(potansiyel_musteri_kayitlar) / len(mautic_kayitlar) * 100:.1f}%")

# Potansiyel müşteri listesini kaydet
potansiyel_musteri_kayitlar.to_excel("potansiyel_musteriler.xlsx", index=False)
print(f"\n💾 Potansiyel müşteri listesi kaydedildi: potansiyel_musteriler.xlsx")

print("=" * 60)
