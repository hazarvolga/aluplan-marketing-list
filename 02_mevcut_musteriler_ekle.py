import pandas as pd
import numpy as np
from datetime import datetime

print("🔍 MEVCUT MÜŞTERİLER VERİSİ ANALİZİ")
print("=" * 50)

# Kaynak dosyayı analiz et
kaynak_dosya = "veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx"
df_kaynak = pd.read_excel(kaynak_dosya)

print(f"📊 KAYNAK VERİ ANALİZİ:")
print(f"   📁 Dosya: {kaynak_dosya}")
print(f"   📝 Toplam kayıt: {len(df_kaynak):,}")
print(f"   📋 Sütun sayısı: {len(df_kaynak.columns)}")
print(f"   🏷️  Sütun isimleri: {list(df_kaynak.columns)}")

# İlk 5 kayıt
print(f"\n📋 İLK 5 KAYIT:")
print(df_kaynak.head().to_string(index=False))

# Hangi sütunları kullanabileceğimizi kontrol et
print(f"\n🎯 KULLANILACAK VERİ SÜTUNLARI:")
possible_name_cols = [col for col in df_kaynak.columns if any(x in col.lower() for x in ['name', 'ad', 'isim', 'adı'])]
possible_email_cols = [col for col in df_kaynak.columns if any(x in col.lower() for x in ['email', 'mail', 'eposta'])]
possible_company_cols = [col for col in df_kaynak.columns if any(x in col.lower() for x in ['company', 'firma', 'şirket', 'kurum'])]

print(f"   📝 İsim sütunları: {possible_name_cols}")
print(f"   📧 Email sütunları: {possible_email_cols}")
print(f"   🏢 Şirket sütunları: {possible_company_cols}")

# Veri kalitesi kontrolü
print(f"\n🔍 VERİ KALİTESİ KONTROLÜ:")
for col in df_kaynak.columns:
    null_count = df_kaynak[col].isnull().sum()
    if null_count > 0:
        print(f"   ❌ {col}: {null_count:,} boş kayıt")
    else:
        print(f"   ✅ {col}: Tam dolu")

# Email formatı kontrolü
if possible_email_cols:
    email_col = possible_email_cols[0]
    if email_col in df_kaynak.columns:
        valid_emails = df_kaynak[email_col].dropna().str.contains('@', na=False).sum()
        total_emails = len(df_kaynak[email_col].dropna())
        print(f"   📧 Email formatı: {valid_emails:,}/{total_emails:,} geçerli")

print(f"\n" + "=" * 50)
print("📝 EKLENECEK VERİ ÖNİZLEMESİ")
print("=" * 50)

# Seçilen sütunları belirleme
name_col = possible_name_cols[0] if possible_name_cols else None
email_col = possible_email_cols[0] if possible_email_cols else None
company_col = possible_company_cols[0] if possible_company_cols else None

print(f"🎯 SEÇİLEN SÜTUNLAR:")
print(f"   📝 İsim: {name_col}")
print(f"   📧 Email: {email_col}")
print(f"   🏢 Şirket: {company_col}")

if name_col and email_col and company_col:
    # Temizlenmiş veri önizlemesi
    df_preview = df_kaynak[[name_col, email_col, company_col]].copy()
    df_preview.columns = ['name', 'email', 'company']
    
    # Boş kayıtları çıkar
    df_preview = df_preview.dropna(subset=['name', 'email'])
    
    # Email formatı kontrolü
    df_preview = df_preview[df_preview['email'].str.contains('@', na=False)]
    
    print(f"\n📊 TEMİZLENMİŞ VERİ İSTATİSTİKLERİ:")
    print(f"   📝 Temizlenmiş kayıt sayısı: {len(df_preview):,}")
    print(f"   📧 Geçerli email sayısı: {len(df_preview):,}")
    print(f"   🏢 Şirket bilgisi olan: {df_preview['company'].notna().sum():,}")
    
    print(f"\n📋 EKLENECEK VERİ ÖRNEKLERİ:")
    print(df_preview.head(10).to_string(index=False))
    
    print(f"\n" + "=" * 50)
    print("❓ ONAY BEKLENİYOR")
    print("=" * 50)
    print(f"✅ Bu {len(df_preview):,} kayıt 'Mevcut Müşteriler' segmenti olarak eklensin mi?")
    print(f"✅ Sadece name, email, company bilgileri alınacak")
    print(f"✅ Boş ve geçersiz email adresleri filtrelenmiş")
    print(f"✅ Segment: 'Mevcut Müşteriler'")
else:
    print(f"\n❌ HATA: Gerekli sütunlar bulunamadı!")
    print(f"   Gerekli: name, email, company sütunları")
