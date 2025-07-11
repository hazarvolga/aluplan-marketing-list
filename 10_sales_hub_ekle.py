import pandas as pd
import numpy as np
from datetime import datetime

print("✅ DYNAMICS 365 SALES HUB MEVCUT EKLENİYOR")
print("=" * 60)

# Mevcut veri setini yükle
df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
print(f"📊 MEVCUT VERİ SETİ:")
print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")

# Dynamics 365 verilerini yükle
df_dynamics = pd.read_excel('veri_kaynaklari/All Contacts-Dynamics-365.xlsx')
print(f"\n📦 DYNAMICS 365 VERİLERİ:")
print(f"   📝 Toplam kayıt: {len(df_dynamics):,}")
print(f"   📧 Email sütunu: Email")

# Mevcut email listesini al
mevcut_emails = set(df_mevcut['email'].str.lower().str.strip())
print(f"   📧 Mevcut email sayısı: {len(mevcut_emails):,}")

# Dynamics'ten sadece sistemde olmayan kayıtları al
df_dynamics_temiz = df_dynamics[[' Full Name', 'First Name', 'Last Name', 'Email', 'Business Phone', 'Job Title']].copy()
df_dynamics_temiz = df_dynamics_temiz.dropna(subset=['Email'])
df_dynamics_temiz = df_dynamics_temiz[df_dynamics_temiz['Email'].str.contains('@', na=False)]
df_dynamics_temiz['email_lower'] = df_dynamics_temiz['Email'].str.lower().str.strip()

# Sistemde olmayan kayıtları filtrele
df_yeni_sales = df_dynamics_temiz[~df_dynamics_temiz['email_lower'].isin(mevcut_emails)].copy()
print(f"   📝 Yeni Sales Hub kayıt sayısı: {len(df_yeni_sales):,}")

# Çakışan kayıtları analiz et
df_cakisan = df_dynamics_temiz[df_dynamics_temiz['email_lower'].isin(mevcut_emails)].copy()
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
            # Potansiyel müşteriden Sales Hub'a yükselt
            cakisan_cozum.append({
                'email': email,
                'action': 'upgrade',
                'from': 'Potansiyel Müşteriler',
                'to': 'Sales Hub Mevcut',
                'reason': 'Dynamics 365 daha yüksek öncelikli'
            })
        else:
            # Mevcut müşteri veya daha yüksek öncelikli segment
            cakisan_cozum.append({
                'email': email,
                'action': 'keep_existing',
                'existing_segment': segment,
                'reason': 'Mevcut segment daha yüksek öncelikli'
            })

print(f"   🔄 Çakışma çözüm stratejisi uygulandı:")
upgrade_count = len([c for c in cakisan_cozum if c['action'] == 'upgrade'])
keep_count = len([c for c in cakisan_cozum if c['action'] == 'keep_existing'])
print(f"   📈 Potansiyel → Sales Hub yükseltme: {upgrade_count:,}")
print(f"   📋 Mevcut segment korundu: {keep_count:,}")

# Yeni kayıtları hazırla
if len(df_yeni_sales) > 0:
    # İsim birleştirme
    df_yeni_sales['name'] = df_yeni_sales[' Full Name'].fillna(
        df_yeni_sales['First Name'].astype(str) + ' ' + df_yeni_sales['Last Name'].astype(str)
    ).str.strip()
    
    # Yeni ID'ler oluştur
    baslangic_id = df_mevcut['id'].max() + 1
    df_yeni_sales['id'] = range(baslangic_id, baslangic_id + len(df_yeni_sales))
    
    # Gerekli sütunları hazırla
    df_yeni = pd.DataFrame({
        'id': df_yeni_sales['id'],
        'name': df_yeni_sales['name'],
        'email': df_yeni_sales['Email'],
        'company': df_yeni_sales['Job Title'].fillna(''),  # Job Title'ı company olarak kullan
        'phone': df_yeni_sales['Business Phone'].fillna(''),
        'city': '',
        'segment': 'Sales Hub Mevcut',
        'source': 'All Contacts-Dynamics-365.xlsx',
        'created_date': datetime.now().strftime('%Y-%m-%d'),
    })
    
    # Diğer sütunları NaN ile doldur
    for col in df_mevcut.columns:
        if col not in df_yeni.columns:
            df_yeni[col] = np.nan
    
    # Sütun sıralarını ayarla
    df_yeni = df_yeni[df_mevcut.columns]
    
    print(f"\n📊 YENİ SALES HUB KAYITLARI:")
    print(f"   📝 Eklenecek kayıt: {len(df_yeni):,}")
    print(f"   📝 İsim dolu: {df_yeni['name'].notna().sum():,}")
    print(f"   📧 Email dolu: {df_yeni['email'].notna().sum():,}")
    print(f"   🏢 Company dolu: {df_yeni['company'].notna().sum():,}")
    
    # Örnekler
    print(f"\n📋 EKLENECEK VERİ ÖRNEKLERİ:")
    print(df_yeni[['id', 'name', 'email', 'company', 'segment']].head(10).to_string(index=False))
    
    # Çakışma çözümü - segment yükseltmeleri
    if upgrade_count > 0:
        print(f"\n🔄 SEGMENT YÜKSELTMELERİ:")
        for cozum in cakisan_cozum:
            if cozum['action'] == 'upgrade':
                # Potansiyel müşteriyi Sales Hub'a yükselt
                df_mevcut.loc[df_mevcut['email'].str.lower().str.strip() == cozum['email'], 'segment'] = 'Sales Hub Mevcut'
        print(f"   📈 {upgrade_count:,} kayıt Potansiyel → Sales Hub'a yükseltildi")
    
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
    print(f"   Dynamics 365'teki tüm kayıtlar zaten sistemde mevcut")

print(f"\n" + "=" * 60)
print("✅ SALES HUB MEVCUT SEGMENTİ EKLENDİ")
print("=" * 60)
print(f"✅ Mevcut Müşteriler: {segment_dagilimi.get('Mevcut Müşteriler', 0):,}")
print(f"✅ Sales Hub Mevcut: {segment_dagilimi.get('Sales Hub Mevcut', 0):,}")
print(f"✅ Potansiyel Müşteriler: {segment_dagilimi.get('Potansiyel Müşteriler', 0):,}")
print(f"✅ Toplam: {len(df_birlesmis):,}")
print(f"✅ Uygulama: http://localhost:3001")
