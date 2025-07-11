import pandas as pd
import numpy as np

print("🔍 YÜKSEL PROJE A.Ş. DETAY KONTROL")
print("=" * 60)

# Mevcut uygulama verisi
df_app = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx")

# Yüksel Proje A.Ş. kayıtlarını kontrol et
yuksel_kayitlari = df_app[df_app['company'].str.contains('Yüksel', na=False, case=False)]

print(f"📊 YÜKSEL PROJE A.Ş. ANALİZİ:")
print(f"   📝 Toplam Yüksel kayıt: {len(yuksel_kayitlari)}")

if len(yuksel_kayitlari) > 0:
    print(f"\n🎯 YÜKSEL KAYITLARI SEGMENT ANALİZİ:")
    print(f"   🟢 Mautic: {yuksel_kayitlari['Mautic'].sum()}")
    print(f"   🟡 Sales Hub: {yuksel_kayitlari['Sales_Hub_Mevcut'].sum()}")
    print(f"   🟠 V2022: {yuksel_kayitlari['V2022_ve_eski'].sum()}")
    print(f"   🟣 V2023: {yuksel_kayitlari['V2023_ve_uzeri'].sum()}")
    
    # Sadece Mautic olan Yüksel kayıtları
    sadece_mautic_yuksel = yuksel_kayitlari[
        (yuksel_kayitlari['Mautic'] == True) &
        (yuksel_kayitlari['Sales_Hub_Mevcut'] == False) &
        (yuksel_kayitlari['V2022_ve_eski'] == False) &
        (yuksel_kayitlari['V2023_ve_uzeri'] == False)
    ]
    
    print(f"   🎯 Sadece Mautic (potansiyel): {len(sadece_mautic_yuksel)}")
    
    # Mevcut müşteri olan Yüksel kayıtları
    mevcut_musteri_yuksel = yuksel_kayitlari[
        (yuksel_kayitlari['Sales_Hub_Mevcut'] == True) |
        (yuksel_kayitlari['V2022_ve_eski'] == True) |
        (yuksel_kayitlari['V2023_ve_uzeri'] == True)
    ]
    
    print(f"   🔴 Mevcut müşteri: {len(mevcut_musteri_yuksel)}")
    
    print(f"\n📋 TÜM YÜKSEL KAYITLARI:")
    for i, row in yuksel_kayitlari.iterrows():
        segments = []
        if row['Mautic']: segments.append('Mautic')
        if row['Sales_Hub_Mevcut']: segments.append('Sales Hub')
        if row['V2022_ve_eski']: segments.append('V2022')
        if row['V2023_ve_uzeri']: segments.append('V2023')
        
        print(f"   • {row['name']} - {row['email']} - [{', '.join(segments)}]")

# Potansiyel müşteri listesindeki Yüksel kayıtlarını kontrol et
df_potansiyel = pd.read_excel("potansiyel_musteriler.xlsx")
yuksel_potansiyel = df_potansiyel[df_potansiyel['company'].str.contains('Yüksel', na=False, case=False)]

print(f"\n🚨 POTANSİYEL MÜŞTERİ LİSTESİNDEKİ YÜKSEL:")
print(f"   📝 Potansiyel listede Yüksel: {len(yuksel_potansiyel)}")

if len(yuksel_potansiyel) > 0:
    print(f"\n📋 POTANSİYEL LİSTEDEKİ YÜKSEL KAYITLARI (İLK 10):")
    for i, row in yuksel_potansiyel.head(10).iterrows():
        print(f"   • {row['name']} - {row['email']} - {row['company']}")

# Çakışma kontrolü
print(f"\n🔍 ÇAKIŞMA KONTROLÜ:")
if len(yuksel_kayitlari) > 0 and len(yuksel_potansiyel) > 0:
    print(f"   Ana listede Yüksel: {len(yuksel_kayitlari)}")
    print(f"   Potansiyel listede Yüksel: {len(yuksel_potansiyel)}")
    print(f"   ⚠️  Yüksel'in 54 kişisi potansiyel müşteri olarak listelendi")
    print(f"   🔍 Bu kişiler gerçekten sadece Mautic'te mi?")
    
    if len(sadece_mautic_yuksel) > 0:
        print(f"\n✅ DOĞRULAMA:")
        print(f"   Sadece Mautic olan Yüksel: {len(sadece_mautic_yuksel)}")
        print(f"   Bu kayıtlar potansiyel müşteri olabilir")
    else:
        print(f"\n🚨 SORUN:")
        print(f"   Yüksel'de sadece Mautic olan kayıt yok!")
        print(f"   Tüm Yüksel kayıtları başka segmentlerde de var")

# Ham Mautic dosyasında Yüksel kontrolü
print(f"\n📂 HAM MAUTİC DOSYASINDAKİ YÜKSEL:")
df_mautic_raw = pd.read_excel("veri_kaynaklari/mautic-tum-liste.xlsx")
yuksel_mautic_raw = df_mautic_raw[df_mautic_raw['company'].str.contains('Yüksel', na=False, case=False)]
print(f"   Ham Mautic'te Yüksel: {len(yuksel_mautic_raw)}")

print(f"\n💡 ANALİZ SONUCU:")
if len(yuksel_potansiyel) == 54 and len(mevcut_musteri_yuksel) > 0:
    print(f"   🚨 SORUN VAR!")
    print(f"   Yüksel Proje A.Ş. zaten mevcut müşteri olabilir")
    print(f"   54 kişilik liste potansiyel müşteri değil")
else:
    print(f"   ✅ Normal görünüyor")

print("=" * 60)
