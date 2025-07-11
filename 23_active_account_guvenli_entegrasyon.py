import pandas as pd
import numpy as np
from datetime import datetime

print("🔒 ACTIVE ACCOUNT PRODUCTS - GÜVENLİ ENTEGRASYON ANALİZİ")
print("=" * 70)

# Mevcut veri setini yükle (readonly)
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")

# Active Account Products dosyasını yükle
df_active = pd.read_excel('veri_kaynaklari/Active Account Products 11_07_2025 21-28-06.xlsx')
print(f"\n📦 ACTIVE ACCOUNT PRODUCTS:")
print(f"   📝 Toplam kayıt: {len(df_active):,}")
print(f"   📝 Firma sayısı: {df_active['Account (Hesap)'].nunique():,}")

print(f"\n🔍 GÜVENLİ ENTEGRASYON STRATEJİLERİ:")

# Strateji 1: Sadece mevcut firmaların segment bilgilerini güncelle
print(f"\n1️⃣ MEVCUT FİRMALAR İÇİN SEGMENT GÜNCELLEME:")
active_firmalar = set(df_active['Account (Hesap)'].str.lower().str.strip())
mevcut_firmalar = set(df_mevcut['company'].str.lower().str.strip().dropna())
ortak_firmalar = active_firmalar.intersection(mevcut_firmalar)

print(f"   📊 Ortak firma sayısı: {len(ortak_firmalar):,}")
for firma in sorted(ortak_firmalar):
    # Bu firmanın Active Account'taki version bilgileri
    firma_active = df_active[df_active['Account (Hesap)'].str.lower().str.strip() == firma]
    versions = firma_active['SSA/SUB/PERP'].value_counts()
    print(f"   ✅ {firma.title()}: {dict(versions)}")

# Strateji 2: Yeni firmaları ayrı segment olarak ekle
print(f"\n2️⃣ YENİ FİRMALAR İÇİN AYRΙ SEGMENT:")
yeni_firmalar = active_firmalar - mevcut_firmalar
print(f"   📊 Yeni firma sayısı: {len(yeni_firmalar):,}")
for firma in sorted(yeni_firmalar):
    firma_active = df_active[df_active['Account (Hesap)'].str.lower().str.strip() == firma]
    versions = firma_active['SSA/SUB/PERP'].value_counts()
    print(f"   🆕 {firma.title()}: {dict(versions)}")

# Strateji 3: Test veri seti oluşturma
print(f"\n3️⃣ TEST VERİ SETİ OLUŞTURMA:")

# Test için sadece yeni firmaları ekleyeceğiz
test_kayitlar = []
baslangic_id = df_mevcut['id'].max() + 1

for firma in sorted(yeni_firmalar):
    firma_active = df_active[df_active['Account (Hesap)'].str.lower().str.strip() == firma]
    
    # Her firma için bir kayıt oluştur
    versions = ', '.join(firma_active['SSA/SUB/PERP'].unique())
    
    test_kayit = {
        'id': baslangic_id,
        'name': '',  # Email yok, name boş bırakıyoruz
        'email': f'info@{firma.replace(" ", "").lower()}.com',  # Dummy email
        'company': firma_active['Account (Hesap)'].iloc[0],  # Orijinal firma adı
        'phone': '',
        'city': '',
        'segment': f'V2023+ Aktif Lisans',  # Yeni segment
        'source': 'Active Account Products 11_07_2025 21-28-06.xlsx',
        'is_mautic': False,
        'is_sales_hub': False,
        'is_v2022': False,
        'is_v2023': True,  # Hepsi V2023+
        'is_dnc': False,
        'customer_type': 'Active License',
        'spam_score': 0,
        'spam_reason': '',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
        'updated_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    test_kayitlar.append(test_kayit)
    baslangic_id += 1

print(f"   📝 Oluşturulacak test kayıt sayısı: {len(test_kayitlar)}")

# Test DataFrame oluştur
df_test_yeni = pd.DataFrame(test_kayitlar)

print(f"\n📋 TEST KAYITLARI ÖRNEKLERİ:")
print(df_test_yeni[['id', 'company', 'email', 'segment']].head().to_string(index=False))

print(f"\n🔒 GÜVENLİ ENTEGRASYON ÖNERİLERİ:")
print(f"   1️⃣ Test dosyası oluştur (orijinal dosyaya dokunma)")
print(f"   2️⃣ Sadece yeni firmaları ekle ({len(yeni_firmalar)} firma)")
print(f"   3️⃣ Mevcut firmaların segmentlerini güncelleme (opsiyonel)")
print(f"   4️⃣ Tüm değişiklikleri gözden geçirdikten sonra ana dosyaya uygula")

# Test dosyası oluştur
df_test_birlesmis = pd.concat([df_mevcut, df_test_yeni], ignore_index=True)

print(f"\n📊 TEST VERİ SETİ ÖZET:")
print(f"   📝 Toplam kayıt: {len(df_test_birlesmis):,}")
print(f"   📝 Eski kayıt: {len(df_mevcut):,}")
print(f"   📝 Yeni kayıt: {len(df_test_yeni):,}")

# Test dosyasını kaydet
test_dosya = 'data/aluplan-list-TEST-active-account.xlsx'
df_test_birlesmis.to_excel(test_dosya, index=False)

segment_dagilimi = df_test_birlesmis['segment'].value_counts()
print(f"\n🎯 TEST SEGMENT DAĞILIMI:")
for segment, count in segment_dagilimi.items():
    print(f"   📋 {segment}: {count:,} kayıt")

print(f"\n💾 TEST DOSYASI OLUŞTURULDU:")
print(f"   📁 {test_dosya}")
print(f"   📝 Toplam kayıt: {len(df_test_birlesmis):,}")
print(f"   ⚠️ Bu bir TEST dosyasıdır, orijinal veri değişmedi!")

print(f"\n" + "=" * 70)
print("✅ GÜVENLİ TEST ANALİZİ TAMAMLANDI")
print("=" * 70)
