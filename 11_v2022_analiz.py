import pandas as pd
import numpy as np

print("🔍 V2022 VE ESKİ DOSYA ANALİZİ")
print("=" * 60)

# V2022 dosyasını yükle
try:
    df_v2022 = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx')
    print(f"📊 V2022 VE ESKİ DOSYASI:")
    print(f"   📝 Toplam kayıt: {len(df_v2022):,}")
    print(f"   📝 Sütun sayısı: {len(df_v2022.columns)}")
    
    print(f"\n📋 SÜTUN LİSTESİ:")
    for i, col in enumerate(df_v2022.columns):
        print(f"   {i+1:2d}. {col}")
    
    print(f"\n🔍 VERİ ÖRNEKLERİ:")
    print(df_v2022.head().to_string())
    
    # Email sütunu kontrol et
    email_cols = [col for col in df_v2022.columns if 'email' in col.lower() or 'e-mail' in col.lower() or 'mail' in col.lower()]
    print(f"\n📧 EMAIL SÜTUNLARI:")
    for col in email_cols:
        email_count = df_v2022[col].notna().sum()
        print(f"   📧 {col}: {email_count:,} dolu email")
    
    # Diğer önemli sütunlar
    name_cols = [col for col in df_v2022.columns if 'name' in col.lower() or 'ad' in col.lower() or 'isim' in col.lower()]
    company_cols = [col for col in df_v2022.columns if 'company' in col.lower() or 'firma' in col.lower() or 'şirket' in col.lower()]
    phone_cols = [col for col in df_v2022.columns if 'phone' in col.lower() or 'tel' in col.lower() or 'gsm' in col.lower()]
    
    print(f"\n👤 İSİM SÜTUNLARI:")
    for col in name_cols:
        count = df_v2022[col].notna().sum()
        print(f"   👤 {col}: {count:,} dolu kayıt")
    
    print(f"\n🏢 FİRMA SÜTUNLARI:")
    for col in company_cols:
        count = df_v2022[col].notna().sum()
        print(f"   🏢 {col}: {count:,} dolu kayıt")
    
    print(f"\n📞 TELEFON SÜTUNLARI:")
    for col in phone_cols:
        count = df_v2022[col].notna().sum()
        print(f"   📞 {col}: {count:,} dolu kayıt")
    
    # Mevcut veri setini yükle
    df_mevcut = pd.read_excel('data/aluplan-list.xlsx')
    mevcut_emails = set(df_mevcut['email'].str.lower().str.strip())
    print(f"\n📊 MEVCUT VERİ SETİ:")
    print(f"   📝 Toplam kayıt: {len(df_mevcut):,}")
    print(f"   📧 Mevcut email sayısı: {len(mevcut_emails):,}")
    
    # Email bazlı çakışma analizi
    if email_cols:
        main_email_col = email_cols[0]  # İlk email sütununu kullan
        df_v2022_temiz = df_v2022.dropna(subset=[main_email_col])
        df_v2022_temiz = df_v2022_temiz[df_v2022_temiz[main_email_col].str.contains('@', na=False)]
        df_v2022_temiz['email_lower'] = df_v2022_temiz[main_email_col].str.lower().str.strip()
        
        # Yeni ve çakışan kayıtları belirle
        v2022_emails = set(df_v2022_temiz['email_lower'])
        yeni_emails = v2022_emails - mevcut_emails
        cakisan_emails = v2022_emails & mevcut_emails
        
        print(f"\n🔄 ÇAKIŞMA ANALİZİ:")
        print(f"   📧 V2022 geçerli email: {len(v2022_emails):,}")
        print(f"   ✅ Yeni email: {len(yeni_emails):,}")
        print(f"   🔄 Çakışan email: {len(cakisan_emails):,}")
        
        # Çakışan kayıtların segment analizini yap
        if cakisan_emails:
            print(f"\n🎯 ÇAKIŞAN KAYITLARIN SEGMENT ANALİZİ:")
            for email in list(cakisan_emails)[:10]:  # İlk 10 örnek
                mevcut_segment = df_mevcut[df_mevcut['email'].str.lower().str.strip() == email]['segment'].iloc[0]
                print(f"   📧 {email[:30]}... → Mevcut segment: {mevcut_segment}")
        
        print(f"\n📊 V2022 VE ESKİ SEGMENT ENTEGRASYONU İÇİN HAZIRLIK:")
        print(f"   📝 Eklenebilecek yeni kayıt: {len(yeni_emails):,}")
        print(f"   🔄 Çakışma çözümü gerekli: {len(cakisan_emails):,}")
        
        # Segment öncelik hiyerarşisi
        print(f"\n🎯 SEGMENT ÖNCELİK HİYERARŞİSİ:")
        print(f"   1. Mevcut Müşteriler (en yüksek)")
        print(f"   2. Sales Hub Mevcut")
        print(f"   3. V2023 ve üzeri")
        print(f"   4. V2022 ve eski")
        print(f"   5. Potansiyel Müşteriler (en düşük)")
        
        # Önerilen strateji
        print(f"\n💡 ÖNERİLEN ENTEGRASYON STRATEJİSİ:")
        print(f"   ✅ Yeni kayıtlar: V2022 ve eski segment olarak ekle")
        print(f"   🔄 Çakışan kayıtlar: Segment önceliğine göre işle")
        print(f"   📋 Potansiyel Müşteriler → V2022 ve eski (yükseltme)")
        print(f"   📋 Diğer segmentler → Mevcut segment koru")
        
    else:
        print(f"\n⚠️ EMAIL SÜTUNU BULUNAMADI!")
        print(f"   Dosyadaki sütunları kontrol edin")

except Exception as e:
    print(f"❌ HATA: {e}")
    print(f"   Dosya yolu ve formatını kontrol edin")

print(f"\n" + "=" * 60)
print("🔍 V2022 VE ESKİ DOSYA ANALİZİ TAMAMLANDI")
print("=" * 60)
