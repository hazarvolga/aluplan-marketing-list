import pandas as pd
import numpy as np
from datetime import datetime

print("✅ MEVCUT MÜŞTERİLER VERİSİ HAZIRLIĞI")
print("=" * 50)

# Kaynak dosyayı doğru header ile oku
kaynak_dosya = "veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx"
df_kaynak = pd.read_excel(kaynak_dosya, header=1)

print(f"📊 KAYNAK VERİ:")
print(f"   📁 Dosya: {kaynak_dosya}")
print(f"   📝 Toplam kayıt: {len(df_kaynak):,}")
print(f"   📋 Sütun sayısı: {len(df_kaynak.columns)}")

# Gerekli sütunları belirle
name_col = "Name"  # Yetkili kişi adı
email_col = "Main E-Mail"  # Email adresi
company_col = "Acount Name"  # Şirket adı

print(f"\n🎯 KULLANILACAK SÜTUNLAR:")
print(f"   📝 İsim: {name_col}")
print(f"   📧 Email: {email_col}")
print(f"   🏢 Şirket: {company_col}")

# Veri temizleme
df_temiz = df_kaynak[[company_col, name_col, email_col]].copy()
df_temiz.columns = ['company', 'name', 'email']

# Başlangıç istatistikleri
print(f"\n📊 BAŞLANGIÇ İSTATİSTİKLERİ:")
print(f"   📝 Toplam kayıt: {len(df_temiz):,}")
print(f"   📝 İsim dolu: {df_temiz['name'].notna().sum():,}")
print(f"   📧 Email dolu: {df_temiz['email'].notna().sum():,}")
print(f"   🏢 Şirket dolu: {df_temiz['company'].notna().sum():,}")

# Veri temizleme adımları
print(f"\n🧹 VERİ TEMİZLEME ADIMLARI:")

# 1. Boş name ve email olan kayıtları çıkar
onceki_sayı = len(df_temiz)
df_temiz = df_temiz.dropna(subset=['name', 'email'])
print(f"   1️⃣ Boş name/email temizlendi: {onceki_sayı:,} → {len(df_temiz):,}")

# 2. Email formatı kontrolü
onceki_sayı = len(df_temiz)
df_temiz = df_temiz[df_temiz['email'].str.contains('@', na=False)]
print(f"   2️⃣ Geçersiz email temizlendi: {onceki_sayı:,} → {len(df_temiz):,}")

# 3. Boş string temizleme
df_temiz = df_temiz.replace('', np.nan)
df_temiz = df_temiz.dropna(subset=['name', 'email'])
print(f"   3️⃣ Boş string temizlendi: {len(df_temiz):,} kayıt kaldı")

# 4. Whitespace temizleme
df_temiz['name'] = df_temiz['name'].str.strip()
df_temiz['email'] = df_temiz['email'].str.strip()
df_temiz['company'] = df_temiz['company'].str.strip()
print(f"   4️⃣ Whitespace temizlendi")

# 5. Duplicate email kontrolü
onceki_sayı = len(df_temiz)
df_temiz = df_temiz.drop_duplicates(subset=['email'])
print(f"   5️⃣ Duplicate email temizlendi: {onceki_sayı:,} → {len(df_temiz):,}")

# Final istatistikler
print(f"\n📊 FINAL TEMİZLENMİŞ VERİ:")
print(f"   📝 Toplam kayıt: {len(df_temiz):,}")
print(f"   📝 İsim dolu: {df_temiz['name'].notna().sum():,}")
print(f"   📧 Email dolu: {df_temiz['email'].notna().sum():,}")
print(f"   🏢 Şirket dolu: {df_temiz['company'].notna().sum():,}")

# Örnek veriler
print(f"\n📋 EKLENECEK VERİ ÖRNEKLERİ:")
print(df_temiz.head(10).to_string(index=False))

# Email domain analizi
print(f"\n📧 EMAIL DOMAIN ANALİZİ:")
df_temiz['domain'] = df_temiz['email'].str.extract(r'@([^.]+\.[^.]+)$')
top_domains = df_temiz['domain'].value_counts().head(10)
print(f"   En çok kullanılan domainler:")
for domain, count in top_domains.items():
    print(f"   📧 {domain}: {count:,} adet")

# Spam domain kontrolü
spam_domains = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'yandex.com']
spam_count = df_temiz[df_temiz['domain'].isin(spam_domains)]['domain'].value_counts().sum()
print(f"\n🔴 SPAM DOMAIN UYARISI:")
print(f"   📧 Kişisel email adresi: {spam_count:,} adet")
print(f"   📧 Kurumsal email adresi: {len(df_temiz) - spam_count:,} adet")

print(f"\n" + "=" * 50)
print("❓ ONAY BEKLENİYOR")
print("=" * 50)
print(f"✅ Bu {len(df_temiz):,} kayıt 'Mevcut Müşteriler' segmenti olarak eklensin mi?")
print(f"✅ Format: name, email, company")
print(f"✅ Temizlenmiş ve doğrulanmış veri")
print(f"✅ Segment: 'Mevcut Müşteriler'")
print(f"✅ Duplicate email adresleri temizlenmiş")

# Veriyi geçici olarak kaydet
df_temiz.to_excel('temp_mevcut_musteriler.xlsx', index=False)
print(f"\n💾 Geçici dosya: temp_mevcut_musteriler.xlsx")
print(f"📝 Onayınızı bekliyor...")
