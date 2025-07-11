import pandas as pd
import numpy as np

print("🆕 YENİ VERİ SETİ OLUŞTURULUYOR")
print("=" * 50)

# Boş bir DataFrame oluştur - temel yapıyı tanımla
columns = [
    'id',           # Benzersiz ID
    'name',         # İsim
    'email',        # Email
    'company',      # Şirket
    'phone',        # Telefon
    'city',         # Şehir
    'segment',      # Segment (virgülle ayrılmış)
    'source',       # Kaynak dosya
    'is_mautic',    # Mautic'te var mı?
    'is_sales_hub', # Sales Hub'da var mı?
    'is_v2022',     # V2022'de var mı?
    'is_v2023',     # V2023'te var mı?
    'is_dnc',       # DNC listesinde mi?
    'customer_type', # Müşteri tipi (Potansiyel/Mevcut/DNC)
    'spam_score',   # Spam skoru
    'spam_reason',  # Spam sebebi
    'created_date', # Oluşturma tarihi
    'updated_date'  # Güncelleme tarihi
]

# Boş DataFrame oluştur
df_new = pd.DataFrame(columns=columns)

print(f"📊 YENİ VERİ SETİ YAPISI:")
print(f"   📋 Sütun sayısı: {len(df_new.columns)}")
print(f"   🏷️  Sütunlar:")
for i, col in enumerate(df_new.columns, 1):
    print(f"     {i:2d}. {col}")

# Örnek veri tiplerinii tanımla
dtype_mapping = {
    'id': 'int64',
    'name': 'string',
    'email': 'string', 
    'company': 'string',
    'phone': 'string',
    'city': 'string',
    'segment': 'string',
    'source': 'string',
    'is_mautic': 'boolean',
    'is_sales_hub': 'boolean', 
    'is_v2022': 'boolean',
    'is_v2023': 'boolean',
    'is_dnc': 'boolean',
    'customer_type': 'string',
    'spam_score': 'int64',
    'spam_reason': 'string',
    'created_date': 'datetime64[ns]',
    'updated_date': 'datetime64[ns]'
}

# Örnek bir kayıt ekle (test amaçlı)
sample_data = {
    'id': [1],
    'name': ['Test Kullanıcı'],
    'email': ['test@example.com'],
    'company': ['Test Şirketi'],
    'phone': ['0555 123 45 67'],
    'city': ['İstanbul'],
    'segment': ['Test'],
    'source': ['Manual'],
    'is_mautic': [False],
    'is_sales_hub': [False],
    'is_v2022': [False],
    'is_v2023': [False],
    'is_dnc': [False],
    'customer_type': ['Test'],
    'spam_score': [0],
    'spam_reason': [''],
    'created_date': [pd.Timestamp.now()],
    'updated_date': [pd.Timestamp.now()]
}

df_sample = pd.DataFrame(sample_data)

# Dosyayı kaydet
excel_file = "data/aluplan-list.xlsx"
df_sample.to_excel(excel_file, index=False)

print(f"\n💾 DOSYA KAYDEDİLDİ:")
print(f"   📁 Dosya: {excel_file}")
print(f"   📊 Kayıt sayısı: {len(df_sample)}")
print(f"   📋 Sütun sayısı: {len(df_sample.columns)}")

# Dosyayı kontrol et
df_check = pd.read_excel(excel_file)
print(f"\n✅ DOSYA KONTROLÜ:")
print(f"   📁 Dosya okundu: {len(df_check)} kayıt")
print(f"   📋 Sütunlar: {list(df_check.columns)}")

print(f"\n📋 ÖRNEK VERİ:")
print(df_check.to_string(index=False))

print(f"\n🎯 SONRAKİ ADIMLAR:")
print("   1. ✅ Boş veri seti oluşturuldu")
print("   2. 🔄 Mautic verisini ekle")
print("   3. 🔄 Sales Hub verisini ekle") 
print("   4. 🔄 V2022 verisini ekle")
print("   5. 🔄 V2023 verisini ekle")
print("   6. 🔄 DNC verisini ekle")
print("   7. 🔄 Deduplication yap")
print("   8. 🔄 Spam kontrolü yap")
print("   9. 🔄 Müşteri tipi belirle")
print("   10. 🔄 Final kontrol")

print("=" * 50)
