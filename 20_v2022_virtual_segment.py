import pandas as pd
import numpy as np

print("🔍 V2022 VIRTUAL SEGMENT HAZIRLIĞI")
print("=" * 60)

# V2022 dosyasını yükle
df_v2022 = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx')
print(f"📊 V2022 DOSYASI:")
print(f"   📝 Toplam kayıt: {len(df_v2022):,}")

# Email sütununu bul ve temizle
email_column = 'Main E-Mail'
df_v2022_clean = df_v2022.copy()
df_v2022_clean = df_v2022_clean.dropna(subset=[email_column])
df_v2022_clean = df_v2022_clean[df_v2022_clean[email_column].str.contains('@', na=False)]

# Email listesi
v2022_emails = set(df_v2022_clean[email_column].str.lower().str.strip())
print(f"📧 V2022 geçerli email sayısı: {len(v2022_emails):,}")

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"\n📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")

# V2022 email'lerine sahip mevcut kayıtları bul
mevcut_emails_lower = df_mevcut['email'].str.lower().str.strip()
v2022_matches = df_mevcut[mevcut_emails_lower.isin(v2022_emails)]

print(f"\n🎯 V2022 EŞLEŞME ANALİZİ:")
print(f"   📧 V2022 dosyasındaki email'ler: {len(v2022_emails):,}")
print(f"   ✅ Mevcut sistemde bulunan: {len(v2022_matches):,}")
print(f"   ❌ Sistemde bulunmayan: {len(v2022_emails) - len(v2022_matches):,}")

# Mevcut segmentlere göre dağılım
print(f"\n📋 V2022 MÜŞTERİLERİNİN MEVCUT SEGMENT DAĞILIMI:")
segment_dagilim = v2022_matches['segment'].value_counts()
for segment, count in segment_dagilim.items():
    print(f"   📊 {segment}: {count:,} kayıt")

# Virtual V2022 tag'i eklemek için çözüm
print(f"\n💡 VİRTUAL V2022 SEGMENT ÇÖZÜMÜ:")
print(f"   🎯 V2022 dosyasından {len(v2022_matches):,} müşteri virtual olarak etiketlenebilir")
print(f"   📋 Bu müşteriler mevcut segmentlerini koruyacak")
print(f"   🔍 V2022 filtresi bu müşterileri gösterecek")

# V2022 email listesini JSON formatında kaydet
v2022_email_list = sorted(list(v2022_emails))
print(f"\n📄 V2022 EMAIL LİSTESİ HAZIR:")
print(f"   📝 Toplam email: {len(v2022_email_list):,}")
print(f"   📋 İlk 10 örnek:")
for i, email in enumerate(v2022_email_list[:10], 1):
    print(f"     {i}. {email}")

# TypeScript sabitine dönüştür
print(f"\n💾 TYPESCRIPT SABİTİ:")
print("// V2022 email listesi")
print("const V2022_EMAILS = new Set([")
for email in v2022_email_list[:10]:  # İlk 10 örnek
    print(f'  "{email}",')
print("  // ... total", len(v2022_email_list), "emails")
print("]);")

# Özet
print(f"\n📊 ÖZET:")
print(f"   ✅ V2022 dosyasından {len(v2022_emails):,} geçerli email")
print(f"   ✅ Mevcut sistemde {len(v2022_matches):,} eşleşme")
print(f"   ✅ Virtual segment olarak kullanılabilir")
print(f"   ✅ Segment dağılımı korunacak")

print(f"\n✅ V2022 VIRTUAL SEGMENT HAZIR")
print("=" * 60)
