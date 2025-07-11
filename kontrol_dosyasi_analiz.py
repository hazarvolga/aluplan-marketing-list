import pandas as pd
import numpy as np

# Kontrol dosyasını oku
print("🔍 KONTROL DOSYASI ANALİZİ")
print("=" * 50)

df = pd.read_excel('kontrol_dosyasi.xlsx')

print(f"📊 GENEL İSTATİSTİKLER:")
print(f"   📝 Toplam kayıt: {len(df):,}")
print(f"   📧 Geçerli email: {df['email'].notna().sum():,}")
print(f"   👤 Geçerli isim: {df['name'].notna().sum():,}")
print(f"   🏢 Geçerli şirket: {df['company'].notna().sum():,}")
print(f"   📞 Geçerli telefon: {df['phone'].notna().sum():,}")

print(f"\n🎯 SEGMENT DAĞILIMI:")
print(f"   🟢 Mautic: {df['isMautic'].sum():,}")
print(f"   🟡 Sales Hub Mevcut: {df['isSalesHubMevcut'].sum():,}")
print(f"   🟠 V2022 ve eski: {df['isV2022'].sum():,}")
print(f"   🟣 V2023 ve üzeri: {df['isV2023'].sum():,}")
print(f"   ⚠️  DNC kayıtları: {df['isDNC'].sum():,}")

print(f"\n🔴 SPAM ANALİZİ:")
spam_counts = df.groupby('spamScore').size().sort_index()
print(f"   Spam skorları: {spam_counts.to_dict()}")
print(f"   Toplam spam (>30): {(df['spamScore'] > 30).sum():,}")

print(f"\n📋 SEGMENT ÇAKIŞMALARI:")
# Çoklu segment analizi
multi_segment = df[df['segment'].str.contains(',', na=False)]
print(f"   Çoklu segment: {len(multi_segment):,}")
if len(multi_segment) > 0:
    print(f"   Örnek çakışmalar:")
    for i, row in multi_segment.head(5).iterrows():
        print(f"     • {row['name']} - {row['email']} - [{row['segment']}]")

print(f"\n🔍 ÖZELLİKLER:")
print(f"   En uzun isim: {df['name'].str.len().max()} karakter")
print(f"   En uzun şirket: {df['company'].str.len().max()} karakter")
print(f"   Boş isim: {df['name'].isna().sum():,}")
print(f"   Boş şirket: {df['company'].isna().sum():,}")

print(f"\n🏆 EN YÜKSEK SPAM SKORLARI:")
high_spam = df[df['spamScore'] > 50].sort_values('spamScore', ascending=False)
if len(high_spam) > 0:
    for i, row in high_spam.head(5).iterrows():
        print(f"   • {row['email']} - Skor: {row['spamScore']} - Sebep: {row['spamReason']}")
else:
    print("   ✅ Yüksek spam skoru yok")

print(f"\n💎 KALİTE METRİKLERİ:")
# Email format kontrolü
import re
email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
valid_emails = df['email'].apply(lambda x: bool(re.match(email_pattern, str(x))) if pd.notna(x) else False)
print(f"   ✅ Geçerli email formatı: {valid_emails.sum():,}")
print(f"   ❌ Geçersiz email formatı: {(~valid_emails).sum():,}")

# Duplicate email kontrolü
duplicate_emails = df['email'].duplicated().sum()
print(f"   🔄 Duplicate email: {duplicate_emails:,}")

print(f"\n🎉 KONTROL DOSYASI HAZIR!")
print("=" * 50)
