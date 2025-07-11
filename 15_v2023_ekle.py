import pandas as pd
import numpy as np
from datetime import datetime

print("✅ V2023 VE ÜZERİ SEGMENTİ EKLENİYOR")
print("=" * 60)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")

# V2023 verilerini yükle
df_v2023 = pd.read_excel('veri_kaynaklari/Allplan-V2023-ve ustu.xlsx')
print(f"\n📦 V2023 VE ÜZERİ VERİLERİ:")
print(f"   📝 Toplam kayıt: {len(df_v2023):,}")
print(f"   📧 Email sütunu: email")

# Mevcut email listesini al
mevcut_emails = set(df_mevcut['email'].str.lower().str.strip())
print(f"   📧 Mevcut email sayısı: {len(mevcut_emails):,}")

# V2023'ten temiz verileri al
df_v2023_temiz = df_v2023[['Acount Name', 'name', 'email', 'Cep', 'Customer Segment', 'Şehir']].copy()
df_v2023_temiz = df_v2023_temiz.dropna(subset=['email'])
df_v2023_temiz = df_v2023_temiz[df_v2023_temiz['email'].str.contains('@', na=False)]
df_v2023_temiz['email_lower'] = df_v2023_temiz['email'].str.lower().str.strip()

# Sistemde olmayan kayıtları filtrele
df_yeni_v2023 = df_v2023_temiz[~df_v2023_temiz['email_lower'].isin(mevcut_emails)].copy()
print(f"   📝 Yeni V2023 kayıt sayısı: {len(df_yeni_v2023):,}")

# Çakışan kayıtları analiz et
df_cakisan = df_v2023_temiz[df_v2023_temiz['email_lower'].isin(mevcut_emails)].copy()
print(f"   🔄 Çakışan kayıt sayısı: {len(df_cakisan):,}")

print(f"\n🧹 VERİ TEMİZLEME VE ÇAKIŞMA ÇÖZÜMÜ:")

# Çakışan kayıtları çözüm stratejisine göre işle
cakisan_cozum = []
for _, row in df_cakisan.iterrows():
    email = row['email_lower']
    # Mevcut kayıttaki segmenti kontrol et
    mevcut_kayit = df_mevcut[df_mevcut['email'].str.lower().str.strip() == email]
    if len(mevcut_kayit) > 0:
        segment = mevcut_kayit.iloc[0]['segment']
        if segment == 'Potansiyel Müşteriler':
            # Potansiyel müşteriden V2023'e yükselt
            cakisan_cozum.append({
                'email': email,
                'action': 'upgrade',
                'from': 'Potansiyel Müşteriler',
                'to': 'V2023 ve üzeri',
                'reason': 'V2023 daha yüksek öncelikli'
            })
        else:
            # Mevcut müşteri, Sales Hub veya daha yüksek öncelikli segment
            cakisan_cozum.append({
                'email': email,
                'action': 'keep_existing',
                'existing_segment': segment,
                'reason': 'Mevcut segment daha yüksek öncelikli'
            })

print(f"   🔄 Çakışma çözüm stratejisi uygulandı:")
upgrade_count = len([c for c in cakisan_cozum if c['action'] == 'upgrade'])
keep_count = len([c for c in cakisan_cozum if c['action'] == 'keep_existing'])
print(f"   📈 Potansiyel → V2023 yükseltme: {upgrade_count:,}")
print(f"   📋 Mevcut segment korundu: {keep_count:,}")

# Yeni kayıtları hazırla
if len(df_yeni_v2023) > 0:
    # Yeni ID'ler oluştur
    baslangic_id = df_mevcut['id'].max() + 1
    df_yeni_v2023['id'] = range(baslangic_id, baslangic_id + len(df_yeni_v2023))
    
    # Gerekli sütunları hazırla
    df_yeni = pd.DataFrame({
        'id': df_yeni_v2023['id'],
        'name': df_yeni_v2023['name'].fillna(''),
        'email': df_yeni_v2023['email'],
        'company': df_yeni_v2023['Acount Name'].fillna(''),
        'phone': df_yeni_v2023['Cep'].fillna(''),
        'city': df_yeni_v2023['Şehir'].fillna(''),
        'segment': 'V2023 ve üzeri',
        'source': 'Allplan-V2023-ve ustu.xlsx',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
    })
    
    # Diğer sütunları NaN ile doldur
    for col in df_mevcut.columns:
        if col not in df_yeni.columns:
            df_yeni[col] = np.nan
    
    # Sütun sıralarını ayarla
    df_yeni = df_yeni[df_mevcut.columns]
    
    print(f"\n📊 YENİ V2023 KAYITLARI:")
    print(f"   📝 Eklenecek kayıt: {len(df_yeni):,}")
    print(f"   📝 İsim dolu: {df_yeni['name'].notna().sum():,}")
    print(f"   📧 Email dolu: {df_yeni['email'].notna().sum():,}")
    print(f"   🏢 Company dolu: {df_yeni['company'].notna().sum():,}")
    print(f"   🏙️ City dolu: {df_yeni['city'].notna().sum():,}")
    
    # Örnekler
    print(f"\n📋 EKLENECEK VERİ ÖRNEKLERİ:")
    print(df_yeni[['id', 'name', 'email', 'company', 'city', 'segment']].head(10).to_string(index=False))
    
    # Çakışma çözümü - segment yükseltmeleri
    if upgrade_count > 0:
        print(f"\n🔄 SEGMENT YÜKSELTMELERİ:")
        for cozum in cakisan_cozum:
            if cozum['action'] == 'upgrade':
                # Potansiyel müşteriyi V2023'e yükselt
                df_mevcut.loc[df_mevcut['email'].str.lower().str.strip() == cozum['email'], 'segment'] = 'V2023 ve üzeri'
        print(f"   📈 {upgrade_count:,} kayıt Potansiyel → V2023 ve üzeri'ne yükseltildi")
    
    # Verileri birleştir
    df_birlesmis = pd.concat([df_mevcut, df_yeni], ignore_index=True)
    
    print(f"\n📊 BİRLEŞMİŞ VERİ SETİ:")
    print(f"   📝 Toplam kayıt: {len(df_birlesmis):,}")
    print(f"   📝 Eski kayıt: {len(df_mevcut):,}")
    print(f"   📝 Yeni kayıt: {len(df_yeni):,}")
    
    # Segment analizi
    segment_dagilimi = df_birlesmis['segment'].value_counts()
    print(f"\n🎯 GÜNCEL SEGMENT DAĞILIMI:")
    for segment, count in segment_dagilimi.items():
        print(f"   📋 {segment}: {count:,} kayıt")
    
    # Dosyayı kaydet
    df_birlesmis.to_excel('data/aluplan-list.xlsx', index=False)
    print(f"\n💾 DOSYA KAYDEDILDI:")
    print(f"   📁 data/aluplan-list.xlsx")
    print(f"   📝 Toplam kayıt: {len(df_birlesmis):,}")

else:
    print(f"\n⚠️ YENİ KAYIT BULUNAMADI!")
    print(f"   V2023'teki tüm kayıtlar zaten sistemde mevcut")
    # Sadece segment yükseltmeleri yap
    if upgrade_count > 0:
        print(f"\n🔄 SEGMENT YÜKSELTMELERİ:")
        for cozum in cakisan_cozum:
            if cozum['action'] == 'upgrade':
                df_mevcut.loc[df_mevcut['email'].str.lower().str.strip() == cozum['email'], 'segment'] = 'V2023 ve üzeri'
        print(f"   📈 {upgrade_count:,} kayıt Potansiyel → V2023 ve üzeri'ne yükseltildi")
        
        # Güncel segment dağılımı
        segment_dagilimi = df_mevcut['segment'].value_counts()
        print(f"\n🎯 GÜNCEL SEGMENT DAĞILIMI:")
        for segment, count in segment_dagilimi.items():
            print(f"   📋 {segment}: {count:,} kayıt")
        
        # Dosyayı kaydet
        df_mevcut.to_excel('data/aluplan-list.xlsx', index=False)
        print(f"\n💾 DOSYA KAYDEDILDI:")
        print(f"   📁 data/aluplan-list.xlsx")
        print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")
        df_birlesmis = df_mevcut
    else:
        segment_dagilimi = df_mevcut['segment'].value_counts()
        df_birlesmis = df_mevcut

print(f"\n" + "=" * 60)
print("✅ V2023 VE ÜZERİ SEGMENTİ EKLENDİ")
print("=" * 60)
print(f"✅ Sales Hub Mevcut: {segment_dagilimi.get('Sales Hub Mevcut', 0):,}")
print(f"✅ V2023 ve üzeri: {segment_dagilimi.get('V2023 ve üzeri', 0):,}")
print(f"✅ Mevcut Müşteriler: {segment_dagilimi.get('Mevcut Müşteriler', 0):,}")
print(f"✅ Potansiyel Müşteriler: {segment_dagilimi.get('Potansiyel Müşteriler', 0):,}")
print(f"✅ Toplam: {len(df_birlesmis):,}")
print(f"✅ Uygulama: http://localhost:3001")
