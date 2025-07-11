import pandas as pd
import numpy as np
from datetime import datetime

print("✅ MEVCUT MÜŞTERİLER SEGMENTİNİ EKLEME")
print("=" * 50)

# Mevcut temiz veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Mevcut kayıt: {len(df_mevcut):,}")
print(f"   📋 Sütun sayısı: {len(df_mevcut.columns)}")

# Hazırlanan mevcut müşteriler verilerini yükle
df_yeni = pd.read_excel('temp_mevcut_musteriler.xlsx')
print(f"\n📦 YENİ MEVCUT MÜŞTERİLER:")
print(f"   📝 Eklenecek kayıt: {len(df_yeni):,}")

# Yeni ID'ler oluştur
baslangic_id = df_mevcut['id'].max() + 1 if len(df_mevcut) > 0 else 1
df_yeni['id'] = range(baslangic_id, baslangic_id + len(df_yeni))

# Segment bilgilerini ekle
df_yeni['segment'] = 'Mevcut Müşteriler'
df_yeni['source_file'] = 'Allplan Müşteriler_Final_2025-03-19-R28.xlsx'
df_yeni['created_date'] = datetime.now().strftime('%Y-%m-%d')

# Diğer sütunları NaN ile doldur
for col in df_mevcut.columns:
    if col not in df_yeni.columns:
        df_yeni[col] = np.nan

# Sütun sıralarını ayarla
df_yeni = df_yeni[df_mevcut.columns]

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

print(f"\n📋 İLK 5 MEVCUT MÜŞTERİ KAYDI:")
mevcut_musteri_kayitlari = df_birlesmis[df_birlesmis['segment'] == 'Mevcut Müşteriler']
print(mevcut_musteri_kayitlari[['id', 'name', 'email', 'company', 'segment']].head().to_string(index=False))

print(f"\n" + "=" * 50)
print("✅ MEVCUT MÜŞTERİLER SEGMENTİ EKLENDİ")
print("=" * 50)
