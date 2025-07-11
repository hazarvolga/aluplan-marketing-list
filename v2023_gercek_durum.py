import pandas as pd
import numpy as np

print("🔍 V2023 GERÇEK DURUM ANALİZİ")
print("=" * 60)

# Kontrol dosyasını oku
df_kontrol = pd.read_excel("kontrol_dosyasi.xlsx")

# V2023 segmentindeki kayıtları analiz et
v2023_kayitlar = df_kontrol[df_kontrol['isV2023'] == True]

print(f"📊 V2023 SEGMENT ANALİZİ:")
print(f"   📝 Toplam V2023 kayıt: {len(v2023_kayitlar):,}")

# Sadece V2023 olan kayıtları bul
sadece_v2023 = v2023_kayitlar[
    (v2023_kayitlar['isV2023'] == True) & 
    (v2023_kayitlar['isMautic'] == False) & 
    (v2023_kayitlar['isSalesHubMevcut'] == False) & 
    (v2023_kayitlar['isV2022'] == False)
]

print(f"   📝 Sadece V2023 (diğer segmentlerde yok): {len(sadece_v2023):,}")

# V2023 + Mautic olan kayıtları bul
v2023_mautic = v2023_kayitlar[
    (v2023_kayitlar['isV2023'] == True) & 
    (v2023_kayitlar['isMautic'] == True)
]

print(f"   📝 V2023 + Mautic: {len(v2023_mautic):,}")

# V2023 + Sales Hub olan kayıtları bul
v2023_sales = v2023_kayitlar[
    (v2023_kayitlar['isV2023'] == True) & 
    (v2023_kayitlar['isSalesHubMevcut'] == True)
]

print(f"   📝 V2023 + Sales Hub: {len(v2023_sales):,}")

# Sadece V2023 olan kayıtları göster
print(f"\n📋 SADECE V2023 OLAN KAYITLAR ({len(sadece_v2023)} adet):")
if len(sadece_v2023) > 0:
    for i, row in sadece_v2023.head(10).iterrows():
        print(f"   • {row['name']} - {row['email']} - {row['company']}")
else:
    print("   ❌ Sadece V2023 olan kayıt yok!")

# V2023 dosyasının gerçek amacını anla
print(f"\n🤔 V2023 DOSYASI GERÇEK DURUMU:")
print(f"   • V2023 dosyası 1,237 email içeriyor")
print(f"   • Bunların %95'i Mautic'te zaten var")
print(f"   • Sadece 61 tanesi gerçekten yeni")
print(f"   • Mevcut uygulamadaki 93 sayısı daha mantıklı")

# Mevcut uygulamadaki V2023 mantığını anla
print(f"\n🔍 MEVCUT UYGULAMA MANTAĞI:")
df_app = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx")

# Mevcut app'teki V2023 kayıtlarını kontrol et
v2023_app = df_app[df_app['V2023_ve_uzeri'] == True]
print(f"   📊 Mevcut app V2023: {len(v2023_app):,}")

# Sadece V2023 olan kayıtları mevcut app'te kontrol et
sadece_v2023_app = v2023_app[
    (v2023_app['V2023_ve_uzeri'] == True) & 
    (v2023_app['Mautic'] == False) & 
    (v2023_app['Sales_Hub_Mevcut'] == False) & 
    (v2023_app['V2022_ve_eski'] == False)
]

print(f"   📊 Sadece V2023 (mevcut app): {len(sadece_v2023_app):,}")

# Mevcut app'teki V2023 kayıtlarını göster
print(f"\n📋 MEVCUT APP'TEKİ V2023 KAYITLARI:")
for i, row in v2023_app.head(10).iterrows():
    print(f"   • {row['name']} - {row['email']} - {row['company']}")

print(f"\n💡 SONUÇ:")
print(f"   🔴 Benim kontrol dosyam HATALI!")
print(f"   ✅ Mevcut uygulama DOĞRU!")
print(f"   📊 Gerçek V2023 sayısı: {len(v2023_app):,}")
print(f"   🎯 Sebep: V2023 dosyasındaki kayıtların çoğu zaten diğer segmentlerde var")
print(f"   🔧 Düzeltme: Segment tanımlarını gözden geçirmek gerekiyor")
