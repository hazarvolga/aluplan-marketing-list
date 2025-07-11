import pandas as pd
import numpy as np

print("🔄 GÜNCEL ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx OLUŞTURULUYOR")
print("=" * 70)

# Mevcut uygulama verisini oku
df_mevcut = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx")

print(f"📊 MEVCUT DURUM:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")
print(f"   🟢 Mautic: {df_mevcut['Mautic'].sum():,}")
print(f"   🟡 Sales Hub: {df_mevcut['Sales_Hub_Mevcut'].sum():,}")
print(f"   🟠 V2022: {df_mevcut['V2022_ve_eski'].sum():,}")
print(f"   🟣 V2023: {df_mevcut['V2023_ve_uzeri'].sum():,}")

# Potansiyel müşteri analizi
sadece_mautic = df_mevcut[
    (df_mevcut['Mautic'] == True) &
    (df_mevcut['Sales_Hub_Mevcut'] == False) &
    (df_mevcut['V2022_ve_eski'] == False) &
    (df_mevcut['V2023_ve_uzeri'] == False)
]

mevcut_musteri = df_mevcut[
    (df_mevcut['Sales_Hub_Mevcut'] == True) |
    (df_mevcut['V2022_ve_eski'] == True) |
    (df_mevcut['V2023_ve_uzeri'] == True)
]

print(f"\n🎯 SEGMENT ANALİZİ:")
print(f"   🟢 Potansiyel müşteri (sadece Mautic): {len(sadece_mautic):,}")
print(f"   🔴 Mevcut müşteri (Sales Hub/V2022/V2023): {len(mevcut_musteri):,}")

# Yeni sütun ekle: Potansiyel_Musteri
df_guncellenmis = df_mevcut.copy()

# Potansiyel müşteri sütunu ekle
df_guncellenmis['Potansiyel_Musteri'] = (
    (df_guncellenmis['Mautic'] == True) &
    (df_guncellenmis['Sales_Hub_Mevcut'] == False) &
    (df_guncellenmis['V2022_ve_eski'] == False) &
    (df_guncellenmis['V2023_ve_uzeri'] == False)
)

# Mevcut müşteri sütunu ekle
df_guncellenmis['Mevcut_Musteri'] = (
    (df_guncellenmis['Sales_Hub_Mevcut'] == True) |
    (df_guncellenmis['V2022_ve_eski'] == True) |
    (df_guncellenmis['V2023_ve_uzeri'] == True)
)

# Müşteri durumu sütunu ekle
df_guncellenmis['Musteri_Durumu'] = df_guncellenmis.apply(lambda row: 
    'Mevcut Müşteri' if row['Mevcut_Musteri'] else 
    'Potansiyel Müşteri' if row['Potansiyel_Musteri'] else 
    'Diğer', axis=1
)

print(f"\n📊 YENİ SÜTUNLAR EKLENDİ:")
print(f"   ✅ Potansiyel_Musteri: {df_guncellenmis['Potansiyel_Musteri'].sum():,}")
print(f"   ✅ Mevcut_Musteri: {df_guncellenmis['Mevcut_Musteri'].sum():,}")
print(f"   ✅ Musteri_Durumu: kategorik sütun")

# Müşteri durumu dağılımı
musteri_dagilimi = df_guncellenmis['Musteri_Durumu'].value_counts()
print(f"\n🎯 MÜŞTERİ DURUMU DAĞILIMI:")
for durum, sayi in musteri_dagilimi.items():
    print(f"   📊 {durum}: {sayi:,}")

# Sütun sıralaması yeniden düzenle
sira = [
    'name', 'email', 'company', 'phone', 'segment',
    'Mautic', 'Sales_Hub_Mevcut', 'V2022_ve_eski', 'V2023_ve_uzeri',
    'Potansiyel_Musteri', 'Mevcut_Musteri', 'Musteri_Durumu'
]

# Eksik sütunları kontrol et
mevcut_sutunlar = df_guncellenmis.columns.tolist()
eksik_sutunlar = [s for s in sira if s not in mevcut_sutunlar]
if eksik_sutunlar:
    print(f"\n⚠️  Eksik sütunlar: {eksik_sutunlar}")
    sira = [s for s in sira if s in mevcut_sutunlar]

df_guncellenmis = df_guncellenmis[sira]

# Güncellenmiş dosyayı kaydet
yeni_dosya = "data/ALLPLAN_MARKETING_LIST_SUPER_BASIT_UPDATED.xlsx"
df_guncellenmis.to_excel(yeni_dosya, index=False)

print(f"\n💾 YENİ DOSYA KAYDEDİLDİ:")
print(f"   📁 {yeni_dosya}")
print(f"   📊 {len(df_guncellenmis):,} kayıt")
print(f"   📋 {len(df_guncellenmis.columns)} sütun")

# Potansiyel müşterilerden örnekler
print(f"\n📋 POTANSİYEL MÜŞTERİ ÖRNEKLERİ:")
potansiyel_ornekler = df_guncellenmis[df_guncellenmis['Potansiyel_Musteri'] == True]
for i, row in potansiyel_ornekler.head(10).iterrows():
    print(f"   • {row['name']} - {row['email']} - {row['company']}")

# Dosya karşılaştırması
print(f"\n🔍 DOSYA KARŞILAŞTIRMA:")
print(f"   📁 Eski: ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx ({len(df_mevcut):,} kayıt)")
print(f"   📁 Yeni: ALLPLAN_MARKETING_LIST_SUPER_BASIT_UPDATED.xlsx ({len(df_guncellenmis):,} kayıt)")
print(f"   ➕ Eklenen sütunlar: Potansiyel_Musteri, Mevcut_Musteri, Musteri_Durumu")

print(f"\n🎯 ÖZET:")
print(f"   ✅ Potansiyel müşteri analizi eklendi")
print(f"   ✅ Mevcut müşteri analizi eklendi")
print(f"   ✅ Müşteri durumu kategorize edildi")
print(f"   ✅ Yeni dosya kullanıma hazır")

print("=" * 70)
