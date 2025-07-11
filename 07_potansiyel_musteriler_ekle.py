import pandas as pd
import numpy as np
from datetime import datetime

print("✅ POTANSİYEL MÜŞTERİLER EKLENİYOR")
print("=" * 50)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Mevcut kayıt: {len(df_mevcut):,}")

# Mautic verilerini yükle
df_mautic = pd.read_excel('veri_kaynaklari/mautic-tum-liste.xlsx')
print(f"\n📦 MAUTIC VERİLERİ:")
print(f"   📝 Toplam kayıt: {len(df_mautic):,}")

# Allplan müşteri emaillerini al
df_allplan = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28.xlsx', header=1)
allplan_emails = set(df_allplan['Main E-Mail'].dropna().str.lower().str.strip())
print(f"   📧 Allplan email sayısı: {len(allplan_emails):,}")

# Mautic'ten sadece Allplan'da olmayan kayıtları al
df_mautic_temiz = df_mautic[['firstname', 'email', 'company', 'phone', 'city']].copy()
df_mautic_temiz = df_mautic_temiz.dropna(subset=['email'])
df_mautic_temiz = df_mautic_temiz[df_mautic_temiz['email'].str.contains('@', na=False)]
df_mautic_temiz['email_lower'] = df_mautic_temiz['email'].str.lower().str.strip()

# Allplan'da olmayan kayıtları filtrele
df_potansiyel = df_mautic_temiz[~df_mautic_temiz['email_lower'].isin(allplan_emails)].copy()
print(f"   📝 Potansiyel müşteri sayısı: {len(df_potansiyel):,}")

# Veri temizleme
print(f"\n🧹 VERİ TEMİZLEME:")
onceki_sayı = len(df_potansiyel)

# Duplicate email temizleme
df_potansiyel = df_potansiyel.drop_duplicates(subset=['email'])
print(f"   1️⃣ Duplicate email temizlendi: {onceki_sayı:,} → {len(df_potansiyel):,}")

# Boş firstname temizleme
df_potansiyel = df_potansiyel.dropna(subset=['firstname'])
print(f"   2️⃣ Boş firstname temizlendi: {len(df_potansiyel):,} kayıt kaldı")

# Veri formatını düzenle
df_potansiyel['firstname'] = df_potansiyel['firstname'].astype(str)
if 'lastname' in df_potansiyel.columns:
    df_potansiyel['lastname'] = df_potansiyel['lastname'].astype(str)
    df_potansiyel['name'] = df_potansiyel['firstname'].str.strip() + ' ' + df_potansiyel['lastname'].str.strip()
else:
    df_potansiyel['name'] = df_potansiyel['firstname'].astype(str)
df_potansiyel['name'] = df_potansiyel['name'].str.strip()

# Yeni ID'ler oluştur
baslangic_id = df_mevcut['id'].max() + 1
df_potansiyel['id'] = range(baslangic_id, baslangic_id + len(df_potansiyel))

# Gerekli sütunları hazırla
df_yeni = pd.DataFrame({
    'id': df_potansiyel['id'],
    'name': df_potansiyel['name'],
    'email': df_potansiyel['email'],
    'company': df_potansiyel['company'].fillna(''),
    'phone': df_potansiyel['phone'].fillna(''),
    'city': df_potansiyel['city'].fillna(''),
    'segment': 'Potansiyel Müşteriler',
    'source': 'mautic-tum-liste.xlsx',
    'created_date': datetime.now().strftime('%Y-%m-%d'),
})

# Diğer sütunları NaN ile doldur
for col in df_mevcut.columns:
    if col not in df_yeni.columns:
        df_yeni[col] = np.nan

# Sütun sıralarını ayarla
df_yeni = df_yeni[df_mevcut.columns]

print(f"\n📊 HAZIRLANMIŞ POTANSİYEL MÜŞTERİLER:")
print(f"   📝 Eklenecek kayıt: {len(df_yeni):,}")
print(f"   📝 İsim dolu: {df_yeni['name'].notna().sum():,}")
print(f"   📧 Email dolu: {df_yeni['email'].notna().sum():,}")
print(f"   🏢 Şirket dolu: {df_yeni['company'].notna().sum():,}")

# Örnekler
print(f"\n📋 EKLENECEK VERİ ÖRNEKLERİ:")
print(df_yeni[['id', 'name', 'email', 'company', 'segment']].head(10).to_string(index=False))

# Verileri birleştir
df_birlesmis = pd.concat([df_mevcut, df_yeni], ignore_index=True)

print(f"\n📊 BİRLEŞMİŞ VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_birlesmis):,}")
print(f"   📝 Eski kayıt: {len(df_mevcut):,}")
print(f"   📝 Yeni kayıt: {len(df_yeni):,}")

# Segment analizi
segment_dagilimi = df_birlesmis['segment'].value_counts()
print(f"\n🎯 SEGMENT DAĞILIMI:")
for segment, count in segment_dagilimi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Dosyayı kaydet
df_birlesmis.to_excel('data/aluplan-list.xlsx', index=False)
print(f"\n💾 DOSYA KAYDEDILDI:")
print(f"   📁 data/aluplan-list.xlsx")
print(f"   📝 Toplam kayıt: {len(df_birlesmis):,}")

print(f"\n" + "=" * 50)
print("✅ POTANSİYEL MÜŞTERİLER EKLENDİ")
print("=" * 50)
print(f"✅ Mevcut Müşteriler: {segment_dagilimi.get('Mevcut Müşteriler', 0):,}")
print(f"✅ Potansiyel Müşteriler: {segment_dagilimi.get('Potansiyel Müşteriler', 0):,}")
print(f"✅ Uygulama: http://localhost:3001")
