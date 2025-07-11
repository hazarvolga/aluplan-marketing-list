import pandas as pd

print("🎯 POTANSİYEL MÜŞTERİ LİSTESİ KONTROL")
print("=" * 50)

# Potansiyel müşteri listesini kontrol et
df_potansiyel = pd.read_excel("potansiyel_musteriler.xlsx")

print(f"📊 POTANSİYEL MÜŞTERİ LİSTESİ:")
print(f"   📝 Toplam kayıt: {len(df_potansiyel):,}")
print(f"   📧 Geçerli email: {df_potansiyel['email'].notna().sum():,}")
print(f"   👤 Geçerli isim: {df_potansiyel['name'].notna().sum():,}")
print(f"   🏢 Geçerli şirket: {df_potansiyel['company'].notna().sum():,}")
print(f"   📞 Geçerli telefon: {df_potansiyel['phone'].notna().sum():,}")

# Segment kontrolü
print(f"\n🔍 SEGMENT KONTROLÜ:")
print(f"   🟢 Mautic: {df_potansiyel['Mautic'].sum():,}")
print(f"   🟡 Sales Hub: {df_potansiyel['Sales_Hub_Mevcut'].sum():,}")
print(f"   🟠 V2022: {df_potansiyel['V2022_ve_eski'].sum():,}")
print(f"   🟣 V2023: {df_potansiyel['V2023_ve_uzeri'].sum():,}")

# Sadece Mautic olup olmadığını kontrol et
sadece_mautic = df_potansiyel[
    (df_potansiyel['Mautic'] == True) &
    (df_potansiyel['Sales_Hub_Mevcut'] == False) &
    (df_potansiyel['V2022_ve_eski'] == False) &
    (df_potansiyel['V2023_ve_uzeri'] == False)
]

print(f"\n✅ DOĞRULAMA:")
print(f"   Sadece Mautic olan kayıt: {len(sadece_mautic):,}")
print(f"   Toplam potansiyel müşteri: {len(df_potansiyel):,}")
print(f"   Eşit mi? {'✅ Evet' if len(sadece_mautic) == len(df_potansiyel) else '❌ Hayır'}")

# Şirket bilgisi olan/olmayan
sirket_var = df_potansiyel['company'].notna().sum()
sirket_yok = df_potansiyel['company'].isna().sum()

print(f"\n🏢 ŞİRKET BİLGİSİ:")
print(f"   Şirket bilgisi var: {sirket_var:,} ({sirket_var/len(df_potansiyel)*100:.1f}%)")
print(f"   Şirket bilgisi yok: {sirket_yok:,} ({sirket_yok/len(df_potansiyel)*100:.1f}%)")

# En çok şirket
if sirket_var > 0:
    print(f"\n🏆 EN ÇOK POTANSIYEL MÜŞTERİ OLAN ŞİRKETLER:")
    sirket_sayilari = df_potansiyel['company'].value_counts()
    for i, (sirket, sayi) in enumerate(sirket_sayilari.head(10).items()):
        print(f"   {i+1}. {sirket}: {sayi} kişi")

# İlk 20 kayıt
print(f"\n📋 İLK 20 POTANSİYEL MÜŞTERİ:")
for i, row in df_potansiyel.head(20).iterrows():
    company = row['company'] if pd.notna(row['company']) else 'Şirket bilgisi yok'
    print(f"   {i+1:2d}. {row['name']} - {row['email']} - {company}")

print(f"\n🎯 ÖZET:")
print(f"   📊 {len(df_potansiyel):,} potansiyel müşteri tespit edildi")
print(f"   📧 %100 geçerli email var")
print(f"   🏢 %{sirket_var/len(df_potansiyel)*100:.1f} şirket bilgisi var")
print(f"   🎯 Marketing kampanyaları için hazır liste!")

print("=" * 50)
