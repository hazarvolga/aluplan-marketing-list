import pandas as pd

print("🎯 GÜNCEL DOSYA KONTROL")
print("=" * 50)

# Güncellenmiş dosyayı kontrol et
df_updated = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT_UPDATED.xlsx")

print(f"📊 GÜNCEL DOSYA İSTATİSTİKLERİ:")
print(f"   📝 Toplam kayıt: {len(df_updated):,}")
print(f"   📋 Sütun sayısı: {len(df_updated.columns)}")
print(f"   🏷️  Sütunlar: {list(df_updated.columns)}")

print(f"\n🎯 MÜŞTERİ DURUMU ANALİZİ:")
print(f"   🟢 Potansiyel Müşteri: {df_updated['Potansiyel_Musteri'].sum():,}")
print(f"   🔴 Mevcut Müşteri: {df_updated['Mevcut_Musteri'].sum():,}")

# Müşteri durumu dağılımı
musteri_dagilimi = df_updated['Musteri_Durumu'].value_counts()
print(f"\n📊 MÜŞTERİ DURUMU DAĞILIMI:")
for durum, sayi in musteri_dagilimi.items():
    print(f"   📊 {durum}: {sayi:,}")

# Yüksel Proje A.Ş. son kontrol
yuksel_updated = df_updated[df_updated['company'].str.contains('Yüksel', na=False, case=False)]
yuksel_potansiyel = yuksel_updated[yuksel_updated['Potansiyel_Musteri'] == True]
yuksel_mevcut = yuksel_updated[yuksel_updated['Mevcut_Musteri'] == True]

print(f"\n🏢 YÜKSEL PROJE A.Ş. FİNAL KONTROL:")
print(f"   📊 Toplam Yüksel: {len(yuksel_updated)}")
print(f"   🟢 Potansiyel müşteri: {len(yuksel_potansiyel)}")
print(f"   🔴 Mevcut müşteri: {len(yuksel_mevcut)}")

# En çok potansiyel müşteri olan şirketler
potansiyel_musteriler = df_updated[df_updated['Potansiyel_Musteri'] == True]
sirket_sayilari = potansiyel_musteriler['company'].value_counts()

print(f"\n🏆 EN ÇOK POTANSİYEL MÜŞTERİ OLAN ŞİRKETLER:")
for i, (sirket, sayi) in enumerate(sirket_sayilari.head(10).items()):
    if pd.notna(sirket) and sirket.strip() != '':
        print(f"   {i+1}. {sirket}: {sayi} kişi")

print(f"\n✅ SONUÇ:")
print(f"   📁 Güncel dosya hazır: ALLPLAN_MARKETING_LIST_SUPER_BASIT_UPDATED.xlsx")
print(f"   🎯 {df_updated['Potansiyel_Musteri'].sum():,} potansiyel müşteri tespit edildi")
print(f"   🔴 {df_updated['Mevcut_Musteri'].sum():,} mevcut müşteri ayrıldı")
print(f"   🚀 Uygulama güncellendi ve kullanıma hazır")

print("=" * 50)
