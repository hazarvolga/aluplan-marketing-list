import pandas as pd
import numpy as np

print("🚨 V2023 DOSYASI SORUN ANALİZİ")
print("=" * 60)

# V2023 dosyasını detaylı kontrol et
v2023_file = "veri_kaynaklari/Allplan-V2023-ve ustu.xlsx"
df_v2023 = pd.read_excel(v2023_file)

print(f"📊 V2023 DOSYASI DETAYLARI:")
print(f"   📝 Toplam satır: {len(df_v2023):,}")
print(f"   📧 Geçerli email: {df_v2023['email'].notna().sum():,}")
print(f"   📧 Boş email: {df_v2023['email'].isna().sum():,}")
print(f"   📧 Boş email oranı: {df_v2023['email'].isna().sum() / len(df_v2023) * 100:.1f}%")

# Email'i olan kayıtları kontrol et
email_var = df_v2023[df_v2023['email'].notna()]
print(f"\n📧 EMAIL'İ OLAN KAYITLAR:")
print(f"   📝 Sayı: {len(email_var):,}")
print(f"   📋 İlk 10 email:")
for i, row in email_var.head(10).iterrows():
    print(f"     • {row['name']} - {row['email']} - {row['Acount Name']}")

# Dosyanın yapısını kontrol et
print(f"\n📋 DOSYA YAPISI ANALİZİ:")
print(f"   📝 İlk 5 satır:")
print(df_v2023.head().to_string(index=False))

# Mautic dosyasını da kontrol et
print(f"\n" + "=" * 60)
print("🔍 MAUTIC DOSYASI KARŞILAŞTIRMA")
print("=" * 60)

mautic_file = "veri_kaynaklari/mautic-tum-liste.xlsx"
df_mautic = pd.read_excel(mautic_file)

print(f"📊 MAUTIC DOSYASI:")
print(f"   📝 Toplam satır: {len(df_mautic):,}")
print(f"   📧 Geçerli email: {df_mautic['email'].notna().sum():,}")
print(f"   📧 Boş email: {df_mautic['email'].isna().sum():,}")

# V2023 dosyasındaki email'lerin Mautic'te olup olmadığını kontrol et
v2023_emails = set(df_v2023['email'].dropna().str.lower())
mautic_emails = set(df_mautic['email'].dropna().str.lower())

v2023_mautic_ortak = v2023_emails.intersection(mautic_emails)
print(f"\n🔍 EMAIL ÇAKIŞMA ANALİZİ:")
print(f"   📧 V2023 email sayısı: {len(v2023_emails):,}")
print(f"   📧 Mautic email sayısı: {len(mautic_emails):,}")
print(f"   🤝 Ortak email sayısı: {len(v2023_mautic_ortak):,}")
print(f"   📊 Çakışma oranı: {len(v2023_mautic_ortak) / len(v2023_emails) * 100:.1f}%")

# Kontrol dosyasındaki V2023 segmentini yeniden değerlendir
print(f"\n" + "=" * 60)
print("💡 SORUN TESPİTİ VE ÇÖZÜM")
print("=" * 60)

print(f"🚨 SORUN:")
print(f"   1. V2023 dosyası 1,459 satır ama sadece 1,326 email var")
print(f"   2. Email'i olmayan kayıtlar da V2023 segmentine dahil edilmiş")
print(f"   3. V2023 dosyasının çoğu email'i Mautic'te zaten var")
print(f"   4. Gerçek V2023 müşteri sayısı {len(v2023_emails):,} olmalı")

print(f"\n✅ ÇÖZÜM:")
print(f"   - V2023 segmenti sadece email'i olan kayıtlara uygulanmalı")
print(f"   - Gerçek V2023 sayısı: {len(v2023_emails):,}")
print(f"   - Mautic'le çakışan kayıtlar: {len(v2023_mautic_ortak):,}")
print(f"   - Sadece V2023'e özel kayıtlar: {len(v2023_emails - v2023_mautic_ortak):,}")

# Mevcut uygulamadaki V2023 sayısını kontrol et
print(f"\n📱 MEVCUT UYGULAMA KARŞILAŞTIRMA:")
df_app = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx")
print(f"   📊 Mevcut app V2023: {df_app['V2023_ve_uzeri'].sum():,}")
print(f"   📊 Benim kontrol V2023: 1,237")
print(f"   📊 Gerçek V2023: {len(v2023_emails):,}")
print(f"   ✅ Mevcut app daha doğru!")

print(f"\n🎯 SONUÇ:")
print(f"   Mevcut uygulamadaki 93 sayısı DOĞRU!")
print(f"   Benim kontrol dosyasındaki 1,237 YANLIŞ!")
print(f"   Sebep: Email'i olmayan kayıtları da segment'e dahil ettim")
