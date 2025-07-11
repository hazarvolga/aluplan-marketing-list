import pandas as pd
import numpy as np
from collections import defaultdict
import re

print("📊 VERİ KALİTESİ VE KAYNAK ANALİZİ")
print("=" * 60)

# Veri setini yükle
df = pd.read_excel('data/aluplan-list.xlsx')
print(f"📝 Toplam kayıt: {len(df):,}")

# Email format kontrolü
def is_valid_email(email):
    if pd.isna(email):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email)))

# Segment bazlı analiz
segments = df['segment'].value_counts()
print(f"\n🎯 SEGMENT DAĞILIMI:")
for segment, count in segments.items():
    print(f"   📋 {segment}: {count:,} kayıt")

# Her segment için detaylı analiz
segment_analiz = {}

for segment in segments.index:
    segment_df = df[df['segment'] == segment]
    
    # Temel istatistikler
    toplam = len(segment_df)
    
    # Email kalitesi
    bos_email = segment_df['email'].isna().sum()
    gecersiz_email = segment_df['email'].apply(lambda x: not is_valid_email(x) if pd.notna(x) else False).sum()
    gecerli_email = toplam - bos_email - gecersiz_email
    
    # İsim kalitesi
    bos_isim = segment_df['name'].isna().sum()
    
    # Şirket kalitesi
    bos_sirket = segment_df['company'].isna().sum()
    
    # Telefon kalitesi
    bos_telefon = segment_df['phone'].isna().sum()
    
    # Kaynak dağılımı
    kaynak_dagilimi = segment_df['source'].value_counts()
    
    # Oluşturulma tarihi
    tarih_dagilimi = segment_df['created_date'].value_counts()
    
    segment_analiz[segment] = {
        'toplam': toplam,
        'email_gecerli': gecerli_email,
        'email_bos': bos_email,
        'email_gecersiz': gecersiz_email,
        'email_kalite_yuzde': (gecerli_email / toplam * 100) if toplam > 0 else 0,
        'isim_dolu': toplam - bos_isim,
        'isim_kalite_yuzde': ((toplam - bos_isim) / toplam * 100) if toplam > 0 else 0,
        'sirket_dolu': toplam - bos_sirket,
        'sirket_kalite_yuzde': ((toplam - bos_sirket) / toplam * 100) if toplam > 0 else 0,
        'telefon_dolu': toplam - bos_telefon,
        'telefon_kalite_yuzde': ((toplam - bos_telefon) / toplam * 100) if toplam > 0 else 0,
        'kaynak_dagilimi': kaynak_dagilimi,
        'tarih_dagilimi': tarih_dagilimi
    }

# Detaylı rapor
print(f"\n📋 DETAYLI SEGMENT ANALİZİ:")
print("=" * 60)

for segment, analiz in segment_analiz.items():
    print(f"\n🎯 {segment} ({analiz['toplam']:,} kayıt)")
    print(f"   📧 Email: {analiz['email_gecerli']:,} geçerli (%{analiz['email_kalite_yuzde']:.1f})")
    if analiz['email_bos'] > 0:
        print(f"   ⚠️  Email boş: {analiz['email_bos']:,}")
    if analiz['email_gecersiz'] > 0:
        print(f"   ❌ Email geçersiz: {analiz['email_gecersiz']:,}")
    
    print(f"   👤 İsim: {analiz['isim_dolu']:,} dolu (%{analiz['isim_kalite_yuzde']:.1f})")
    print(f"   🏢 Şirket: {analiz['sirket_dolu']:,} dolu (%{analiz['sirket_kalite_yuzde']:.1f})")
    print(f"   📞 Telefon: {analiz['telefon_dolu']:,} dolu (%{analiz['telefon_kalite_yuzde']:.1f})")
    
    print(f"   📂 Kaynak dağılımı:")
    for kaynak, sayi in analiz['kaynak_dagilimi'].items():
        print(f"      • {kaynak}: {sayi:,} kayıt")

# Tekrar email analizi
print(f"\n🔄 TEKRAR EMAIL ANALİZİ:")
print("=" * 60)

email_counts = df['email'].value_counts()
tekrar_emails = email_counts[email_counts > 1]

if len(tekrar_emails) > 0:
    print(f"⚠️  Tekrar eden email sayısı: {len(tekrar_emails):,}")
    print(f"📊 Toplam tekrar kayıt: {tekrar_emails.sum() - len(tekrar_emails):,}")
    
    # En çok tekrar eden emailler
    print(f"\n📋 EN ÇOK TEKRAR EDEN EMAİLLER:")
    for email, count in tekrar_emails.head(10).items():
        print(f"   📧 {email}: {count} kez")
        # Bu email'in hangi segmentlerde olduğunu göster
        segments_for_email = df[df['email'] == email]['segment'].value_counts()
        for seg, cnt in segments_for_email.items():
            print(f"      • {seg}: {cnt} kayıt")
else:
    print("✅ Tekrar eden email yok")

# Boş alan analizi
print(f"\n❌ BOŞ ALAN ANALİZİ:")
print("=" * 60)

for column in ['name', 'email', 'company', 'phone']:
    bos_sayisi = df[column].isna().sum()
    bos_yuzde = (bos_sayisi / len(df) * 100)
    print(f"📊 {column}: {bos_sayisi:,} boş (%{bos_yuzde:.1f})")

# Kaynak bazlı analiz
print(f"\n📂 KAYNAK BAZLI ANALİZ:")
print("=" * 60)

kaynak_analiz = df.groupby('source').agg({
    'id': 'count',
    'email': lambda x: x.notna().sum(),
    'name': lambda x: x.notna().sum(),
    'company': lambda x: x.notna().sum(),
    'phone': lambda x: x.notna().sum()
}).round(2)

kaynak_analiz.columns = ['Toplam', 'Email_Dolu', 'İsim_Dolu', 'Şirket_Dolu', 'Telefon_Dolu']
print(kaynak_analiz)

# JSON formatında özet çıktı (UI için)
print(f"\n💾 UI İÇİN JSON FORMATI:")
print("=" * 60)

ui_data = {}
for segment, analiz in segment_analiz.items():
    # Kısa açıklama metni oluştur
    aciklama_parts = []
    
    # En önemli kalite bilgisi
    if analiz['email_kalite_yuzde'] < 90:
        aciklama_parts.append(f"Email kalitesi: %{analiz['email_kalite_yuzde']:.0f}")
    
    # En çok kullanılan kaynak
    ana_kaynak = analiz['kaynak_dagilimi'].index[0] if len(analiz['kaynak_dagilimi']) > 0 else "Bilinmeyen"
    if "xlsx" in ana_kaynak:
        kaynak_kisa = ana_kaynak.replace('.xlsx', '').replace('veri_kaynaklari/', '')
        aciklama_parts.append(f"Ana kaynak: {kaynak_kisa}")
    
    # Veri kalitesi özeti
    dolu_alanlar = []
    if analiz['isim_kalite_yuzde'] > 90:
        dolu_alanlar.append("İsim")
    if analiz['sirket_kalite_yuzde'] > 50:
        dolu_alanlar.append("Şirket")
    if analiz['telefon_kalite_yuzde'] > 30:
        dolu_alanlar.append("Telefon")
    
    if dolu_alanlar:
        aciklama_parts.append(f"Dolu: {', '.join(dolu_alanlar)}")
    
    ui_data[segment] = {
        'count': analiz['toplam'],
        'quality_note': " • ".join(aciklama_parts) if aciklama_parts else "Veri kalitesi iyi"
    }

print("const segmentQualityInfo = {")
for segment, info in ui_data.items():
    print(f"  '{segment}': {{")
    print(f"    count: {info['count']},")
    print(f"    note: '{info['quality_note']}'")
    print(f"  }},")
print("};")

print(f"\n✅ ANALİZ TAMAMLANDI")
print("=" * 60)
