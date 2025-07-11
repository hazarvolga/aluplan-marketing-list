import pandas as pd
import numpy as np

print("🔍 MEVCUT UYGULAMA VERİSİ ANALİZİ")
print("=" * 50)

# Mevcut uygulamanın kullandığı dosyayı analiz et
app_file = "data/ALLPLAN_MARKETING_LIST_SUPER_BASIT.xlsx"
df_app = pd.read_excel(app_file)

print(f"📊 MEVCUT UYGULAMA VERİSİ:")
print(f"   📝 Toplam kayıt: {len(df_app):,}")
print(f"   📋 Sütun sayısı: {len(df_app.columns)}")
print(f"   🏷️  Sütun isimleri: {list(df_app.columns)}")

# İlk 5 kayıt
print(f"\n📋 İLK 5 KAYIT:")
print(df_app.head().to_string(index=False))

# Segment analizi
segment_columns = [col for col in df_app.columns if any(x in col.lower() for x in ['mautic', 'sales', 'v2022', 'v2023'])]
if segment_columns:
    print(f"\n🎯 SEGMENT SÜTUNLARI: {segment_columns}")
    for col in segment_columns:
        if col in df_app.columns:
            print(f"   {col}: {df_app[col].sum():,} True değeri")

# Spam analizi
if 'spamScore' in df_app.columns:
    print(f"\n🔴 SPAM ANALİZİ:")
    spam_distribution = df_app['spamScore'].value_counts().sort_index()
    print(f"   Spam dağılımı: {spam_distribution.to_dict()}")
    print(f"   Spam email (>30): {(df_app['spamScore'] > 30).sum():,}")

print(f"\n" + "=" * 50)
print("🆚 KARŞILAŞTIRMA")
print("=" * 50)

# Kontrol dosyasını da oku
kontrol_file = "kontrol_dosyasi.xlsx"
df_kontrol = pd.read_excel(kontrol_file)

print(f"📊 KARŞILAŞTIRMA:")
print(f"   📱 Mevcut App: {len(df_app):,} kayıt")
print(f"   🔧 Kontrol: {len(df_kontrol):,} kayıt")
print(f"   🔺 Fark: {len(df_kontrol) - len(df_app):,} kayıt")

# Segment karşılaştırması
if 'isMautic' in df_app.columns and 'isMautic' in df_kontrol.columns:
    print(f"\n🎯 SEGMENT KARŞILAŞTIRMA:")
    print(f"   Mautic - App: {df_app['isMautic'].sum():,} vs Kontrol: {df_kontrol['isMautic'].sum():,}")
    print(f"   Sales Hub - App: {df_app['isSalesHubMevcut'].sum():,} vs Kontrol: {df_kontrol['isSalesHubMevcut'].sum():,}")
    print(f"   V2022 - App: {df_app['isV2022'].sum():,} vs Kontrol: {df_kontrol['isV2022'].sum():,}")
    print(f"   V2023 - App: {df_app['isV2023'].sum():,} vs Kontrol: {df_kontrol['isV2023'].sum():,}")

print(f"\n💡 FARKLILIK SEBEPLERİ:")
print("   1. Farklı kaynak dosyalar kullanılıyor")
print("   2. Farklı veri işleme yöntemleri")
print("   3. Farklı segment tanımları")
print("   4. Farklı deduplication stratejileri")
