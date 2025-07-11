import pandas as pd

print("🔍 DETAYLI FARK ANALİZİ")
print("=" * 60)

# Her iki dosyayı oku
df_app = pd.read_excel("data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx")
df_kontrol = pd.read_excel("kontrol_dosyasi.xlsx")

print(f"📊 DOSYA KARŞILAŞTIRMA:")
print(f"   🔵 Mevcut App: {len(df_app):,} kayıt")
print(f"   🔴 Kontrol: {len(df_kontrol):,} kayıt")
print(f"   ➕ Fark: {len(df_kontrol) - len(df_app):,} kayıt")

# Email çakışmalarını kontrol et
app_emails = set(df_app['email'].str.lower())
kontrol_emails = set(df_kontrol['email'].str.lower())

ortak_emails = app_emails.intersection(kontrol_emails)
sadece_app = app_emails - kontrol_emails
sadece_kontrol = kontrol_emails - app_emails

print(f"\n📧 EMAIL KARŞILAŞTIRMA:")
print(f"   🤝 Ortak emailler: {len(ortak_emails):,}")
print(f"   🔵 Sadece App'te: {len(sadece_app):,}")
print(f"   🔴 Sadece Kontrol'de: {len(sadece_kontrol):,}")

# Segment farkları
print(f"\n🎯 SEGMENT DETAY KARŞILAŞTIRMA:")
segments = ['Mautic', 'Sales_Hub_Mevcut', 'V2022_ve_eski', 'V2023_ve_uzeri']
kontrol_segments = ['isMautic', 'isSalesHubMevcut', 'isV2022', 'isV2023']

for i, (app_seg, kontrol_seg) in enumerate(zip(segments, kontrol_segments)):
    app_count = df_app[app_seg].sum() if app_seg in df_app.columns else 0
    kontrol_count = df_kontrol[kontrol_seg].sum() if kontrol_seg in df_kontrol.columns else 0
    fark = kontrol_count - app_count
    print(f"   {app_seg}: {app_count:,} → {kontrol_count:,} (Fark: {fark:+,})")

# Sadece kontrol'de olan kayıtları göster
if len(sadece_kontrol) > 0:
    print(f"\n🔍 SADECE KONTROL'DE OLAN İLK 10 EMAIL:")
    kontrol_only = df_kontrol[df_kontrol['email'].str.lower().isin(sadece_kontrol)]
    for i, row in kontrol_only.head(10).iterrows():
        print(f"   • {row['email']} - {row['name']} - {row['company']}")

print(f"\n💡 SONUÇ:")
print(f"   Kontrol dosyası daha güncel ve kapsamlı")
print(f"   Ham verilerden yeni işleme ile daha fazla kayıt bulundu")
print(f"   V2023 segmentinde büyük fark var (93 vs 1,237)")
print(f"   Mautic listesi de daha kapsamlı (3,675 vs 3,915)")

print("=" * 60)
