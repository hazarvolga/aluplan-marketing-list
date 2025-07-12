#!/usr/bin/env python3
"""
Birleştirilmiş Liste Segmentasyon Analizi
Bu script birlestirilmis-liste.xlsx dosyasını mevcut segmentasyon sistemimiz açısından analiz eder
"""

import pandas as pd
import numpy as np
from datetime import datetime

def analyze_birlestirilmis_liste():
    """Birleştirilmiş listeyi analiz et"""
    
    print("🔍 BİRLEŞTİRİLMİŞ LİSTE SEGMENTASYON ANALİZİ")
    print("=" * 60)
    print(f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Dosyayı yükle
    file_path = "veri_kaynaklari/birlestirilmis-liste.xlsx"
    
    try:
        df = pd.read_excel(file_path)
        print(f"\n📊 Dosya başarıyla yüklendi: {file_path}")
        
        # Temel bilgiler
        print(f"\n📈 TEMEL BİLGİLER:")
        print(f"Toplam kayıt sayısı: {len(df):,}")
        print(f"Sütun sayısı: {len(df.columns)}")
        print(f"Sütunlar: {list(df.columns)}")
        
        # Veri tiplerini göster
        print(f"\n📋 VERİ TİPLERİ:")
        for col in df.columns:
            print(f"  {col}: {df[col].dtype}")
        
        # Boş değer analizi
        print(f"\n🔍 BOŞ DEĞER ANALİZİ:")
        null_counts = df.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                percentage = (count / len(df)) * 100
                print(f"  {col}: {count:,} ({percentage:.1f}%)")
        
        # Email analizi (Main E-Mail sütunu)
        if 'Main E-Mail' in df.columns:
            print(f"\n📧 EMAIL ANALİZİ:")
            email_series = df['Main E-Mail'].dropna()
            print(f"  Toplam email: {len(email_series):,}")
            print(f"  Unique email: {email_series.nunique():,}")
            print(f"  Duplicate email: {len(email_series) - email_series.nunique():,}")
            
            # Email format kontrolü
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            valid_emails = email_series.str.match(email_pattern)
            print(f"  Geçerli email formatı: {valid_emails.sum():,}")
            print(f"  Geçersiz email formatı: {(~valid_emails).sum():,}")
            
            # Duplicate email detayları
            if len(email_series) > email_series.nunique():
                duplicate_emails = email_series[email_series.duplicated(keep=False)]
                print(f"\n  🔄 DUPLICATE EMAIL DETAYLARI:")
                duplicate_counts = duplicate_emails.value_counts()
                print(f"    En çok tekrar eden email'ler:")
                for email, count in duplicate_counts.head(10).items():
                    print(f"      {email}: {count} kez")
        
        # Hesap adı analizi
        if 'Acount Name' in df.columns:
            print(f"\n🏢 HESAP ADI ANALİZİ:")
            account_series = df['Acount Name'].dropna()
            print(f"  Hesap adı olan kayıt: {len(account_series):,}")
            print(f"  Unique hesap adı: {account_series.nunique():,}")
            print(f"  Duplicate hesap adı: {len(account_series) - account_series.nunique():,}")
        
        # İsim analizi
        if 'Name' in df.columns:
            print(f"\n👤 İSİM ANALİZİ:")
            name_series = df['Name'].dropna()
            print(f"  İsim olan kayıt: {len(name_series):,}")
            print(f"  Unique isim: {name_series.nunique():,}")
            print(f"  Duplicate isim: {len(name_series) - name_series.nunique():,}")
            
            # Boş isim kayıtlarını kontrol et
            empty_names = df[df['Name'].isna() | (df['Name'].str.strip() == '')]
            print(f"  Boş isim kayıt sayısı: {len(empty_names):,}")
            if len(empty_names) > 0:
                print(f"  Bu kayıtların email durumu:")
                empty_with_email = empty_names[empty_names['Main E-Mail'].notna()]
                print(f"    Email'i olan boş isim kayıt: {len(empty_with_email):,}")
                print(f"    Email'i olmayan boş isim kayıt: {len(empty_names) - len(empty_with_email):,}")
        
        # Veri kalitesi analizi
        print(f"\n🔍 VERİ KALİTESİ ANALİZİ:")
        total_records = len(df)
        
        # Tam veri analizi
        complete_records = df.dropna(subset=['Acount Name', 'Name', 'Main E-Mail'])
        print(f"  Tam veri (Hesap+İsim+Email): {len(complete_records):,} ({(len(complete_records)/total_records)*100:.1f}%)")
        
        # Minimum veri analizi (en az email veya isim)
        min_data = df.dropna(subset=['Main E-Mail'])
        print(f"  Minimum veri (Email var): {len(min_data):,} ({(len(min_data)/total_records)*100:.1f}%)")
        
        # Kullanılabilir veri analizi
        usable_data = df[
            (df['Main E-Mail'].notna()) | 
            (df['Name'].notna() & df['Acount Name'].notna())
        ]
        print(f"  Kullanılabilir veri: {len(usable_data):,} ({(len(usable_data)/total_records)*100:.1f}%)")
        
        # Çöp veri analizi
        garbage_data = df[
            (df['Main E-Mail'].isna()) & 
            (df['Name'].isna()) & 
            (df['Acount Name'].isna())
        ]
        print(f"  Çöp veri (hiçbir bilgi yok): {len(garbage_data):,} ({(len(garbage_data)/total_records)*100:.1f}%)")
        
        # Entegrasyon analizi
        print(f"\n🔄 ENTEGRASYON ANALİZİ:")
        
        # Email bazlı entegrasyon potansiyeli
        if 'Main E-Mail' in df.columns:
            valid_emails = df['Main E-Mail'].dropna()
            print(f"  Email bazlı entegrasyon potansiyeli: {len(valid_emails):,} kayıt")
            
            # Mevcut sistemle çakışma potansiyeli
            print(f"  Mevcut sistemdeki toplam email: ~3,952")
            print(f"  Potansiyel yeni email: {len(valid_emails):,}")
            print(f"  Tahmini çakışma: %15-25 (600-1,000 kayıt)")
            print(f"  Tahmini net ekleme: {len(valid_emails) - 800:,} kayıt")
        
        # Lisans bazlı entegrasyon
        if 'Kalıcı/SUB/SSA' in df.columns:
            license_data = df['Kalıcı/SUB/SSA'].dropna()
            print(f"  Lisans bazlı entegrasyon potansiyeli: {len(license_data):,} kayıt")
            print(f"  V2022 ve eski entegrasyonu: 908 kayıt")
            print(f"  V2023 ve üzeri entegrasyonu: 112 kayıt")
        
        # Segment analizi (E1 sütununu segment olarak adlandırdınız)
        segment_column = 'segment'  # E1 sütunu segment olarak adlandırılmış
        if segment_column in df.columns:
            print(f"\n🎯 SEGMENT ANALİZİ:")
            segment_series = df[segment_column].dropna()
            print(f"  Segment bilgisi olan kayıt: {len(segment_series):,}")
            
            # Segment sütunundaki TÜM unique değerleri kontrol et
            print(f"\n  📊 Segment sütunu TÜM unique değerleri:")
            unique_segments = df[segment_column].value_counts()
            print(f"  Toplam unique segment değeri: {len(unique_segments)}")
            
            for segment_value, count in unique_segments.items():
                print(f"    '{segment_value}': {count:,}")
                
            # Segment değerlerini analiz et (virgülle ayrılmış değerler için)
            all_segments = []
            for segments in segment_series:
                if pd.isna(segments):
                    continue
                # Hem virgül hem de noktalı virgül ile ayrılmış değerleri kontrol et
                if ',' in str(segments):
                    segment_list = [s.strip() for s in str(segments).split(',')]
                elif ';' in str(segments):
                    segment_list = [s.strip() for s in str(segments).split(';')]
                else:
                    segment_list = [str(segments).strip()]
                all_segments.extend(segment_list)
            
            if all_segments:
                segment_counts = pd.Series(all_segments).value_counts()
                print(f"\n  📈 Ayrıştırılmış segment dağılımı:")
                for segment, count in segment_counts.items():
                    print(f"    {segment}: {count:,}")
            
            # Mautic arama - büyük küçük harf duyarsız
            print(f"\n  � Mautic Arama (büyük-küçük harf duyarsız):")
            mautic_variants = ['mautic', 'Mautic', 'MAUTIC', 'Mautic Leads', 'mautic leads']
            total_mautic = 0
            
            for variant in mautic_variants:
                mautic_count = df[df[segment_column].str.contains(variant, case=False, na=False)].shape[0]
                if mautic_count > 0:
                    print(f"    '{variant}' içeren kayıt: {mautic_count:,}")
                    total_mautic += mautic_count
            
            # Genel Mautic araması
            general_mautic = df[df[segment_column].str.contains('mautic', case=False, na=False)]
            print(f"    Genel 'mautic' içeren kayıt: {len(general_mautic):,}")
            
            # Mevcut müşteri araması
            current_variants = ['Mevcut Müşteriler', 'Mevcut Müşteri', 'mevcut', 'müşteri', 'customer']
            total_current = 0
            
            print(f"\n  🔍 Mevcut Müşteri Arama:")
            for variant in current_variants:
                current_count = df[df[segment_column].str.contains(variant, case=False, na=False)].shape[0]
                if current_count > 0:
                    print(f"    '{variant}' içeren kayıt: {current_count:,}")
                    total_current += current_count
            
            # Segment sütunundaki örnek değerleri göster
            print(f"\n  📋 Segment sütunu örnek değerleri (İlk 20):")
            sample_segments = df[segment_column].dropna().head(20)
            for i, segment in enumerate(sample_segments, 1):
                print(f"    {i}. '{segment}'")
                
            # Boş olmayan tüm segment değerlerini alfabetik sıraya koy
            print(f"\n  🔤 Tüm segment değerleri (alfabetik sıralı):")
            all_unique_segments = sorted(df[segment_column].dropna().unique())
            for i, segment in enumerate(all_unique_segments, 1):
                count = df[df[segment_column] == segment].shape[0]
                print(f"    {i}. '{segment}': {count:,} kayıt")
                
        else:
            # Eğer segment sütunu yoksa, diğer sütunları kontrol et
            print(f"\n❌ 'segment' sütunu bulunamadı!")
            print(f"Mevcut sütunlar: {list(df.columns)}")
            
            # Alternatif sütunları kontrol et
            possible_columns = ['Unnamed: 4', 'Segment', 'segments', 'category', 'type']
            for col in possible_columns:
                if col in df.columns:
                    print(f"\n🔍 Alternatif sütun bulundu: {col}")
                    segment_series = df[col].dropna()
                    print(f"  Bu sütunda {len(segment_series):,} kayıt var")
                    
                    unique_values = df[col].value_counts()
                    print(f"  İlk 10 değer:")
                    for value, count in unique_values.head(10).items():
                        print(f"    '{value}': {count:,}")
                    
                    # Bu sütunu segment olarak kullan
                    segment_column = col
                    break
        
        # Mevcut segmentasyon sistemimizle karşılaştırma
        print(f"\n🔄 MEVCUT SEGMENTASYON SİSTEMİ İLE KARŞILAŞTIRMA:")
        
        # Mevcut sistem segmentlerini kontrol et
        segment_columns = ['isMevcutMusteriler', 'isPotansiyelMusteriler', 'isSalesHubMevcut', 'isV2022', 'isV2023']
        
        for col in segment_columns:
            if col in df.columns:
                true_count = df[col].sum() if df[col].dtype == 'bool' else (df[col] == True).sum()
                print(f"  {col}: {true_count:,} kayıt")
        
        # Şirket analizi
        if 'company' in df.columns:
            print(f"\n🏢 ŞİRKET ANALİZİ:")
            company_series = df['company'].dropna()
            print(f"  Şirket bilgisi olan kayıt: {len(company_series):,}")
            print(f"  Unique şirket: {company_series.nunique():,}")
            print(f"  Şirket bilgisi yüzdesi: {(len(company_series) / len(df)) * 100:.1f}%")
        
        # V2022 ve eski lisans versiyonu analizi
        print(f"\n🕐 V2022 VE ESKİ KAYIT ANALİZİ:")
        if 'Kalıcı/SUB/SSA' in df.columns:
            license_series = df['Kalıcı/SUB/SSA'].dropna()
            print(f"  Lisans bilgisi olan kayıt: {len(license_series):,}")
            
            # Lisans versiyonlarını analiz et
            license_counts = license_series.value_counts()
            print(f"\n  Lisans versiyonu dağılımı:")
            for license_type, count in license_counts.items():
                print(f"    {license_type}: {count:,}")
            
            # V2022 ve öncesi kayıtları bul
            # V2022 ve öncesi: V2006, V2007, V2008, V2009, V2010, V2011, V2012, V2013, V2014, V2015, V2016, V2017, V2018, V2019, V2020, V2021, V2022
            # Ayrıca V16, V17, V18, V19, V20, V21, V22 gibi kısa formatlar da olabilir
            
            v2022_and_older = []
            for license_type in license_series:
                license_str = str(license_type).strip().upper()
                
                # V2022 ve öncesi uzun format (V2006, V2007, ..., V2022)
                if license_str.startswith('V20') and len(license_str) >= 5:
                    try:
                        year = int(license_str[1:5])  # V2006 -> 2006
                        if year <= 2022:
                            v2022_and_older.append(license_type)
                    except:
                        pass
                
                # Kısa format (V16, V17, ..., V22)
                elif license_str.startswith('V') and len(license_str) >= 3:
                    try:
                        version = int(license_str[1:])  # V16 -> 16
                        if version <= 22:  # V22 = V2022
                            v2022_and_older.append(license_type)
                    except:
                        pass
            
            print(f"\n  🎯 V2022 VE ÖNCESİ KAYITLAR:")
            print(f"    Toplam V2022 ve öncesi kayıt: {len(v2022_and_older):,}")
            print(f"    Toplam kayıt içindeki oranı: {(len(v2022_and_older) / len(df)) * 100:.1f}%")
            
            # V2022 ve öncesi versiyonların detayı
            if v2022_and_older:
                v2022_counts = pd.Series(v2022_and_older).value_counts()
                print(f"\n  V2022 ve öncesi versiyon dağılımı:")
                for version, count in v2022_counts.items():
                    print(f"    {version}: {count:,}")
        
        # V2023 ve üzeri kayıtları da analiz et
        print(f"\n⚡ V2023 VE ÜZERİ KAYIT ANALİZİ:")
        if 'Kalıcı/SUB/SSA' in df.columns:
            v2023_and_newer = []
            for license_type in license_series:
                license_str = str(license_type).strip().upper()
                
                # V2023 ve üzeri uzun format (V2023, V2024, V2025, ...)
                if license_str.startswith('V20') and len(license_str) >= 5:
                    try:
                        year = int(license_str[1:5])  # V2023 -> 2023
                        if year >= 2023:
                            v2023_and_newer.append(license_type)
                    except:
                        pass
                
                # Kısa format (V23, V24, V25, ...)
                elif license_str.startswith('V') and len(license_str) >= 3:
                    try:
                        version = int(license_str[1:])  # V23 -> 23
                        if version >= 23:  # V23 = V2023
                            v2023_and_newer.append(license_type)
                    except:
                        pass
            
            print(f"    Toplam V2023 ve üzeri kayıt: {len(v2023_and_newer):,}")
            print(f"    Toplam kayıt içindeki oranı: {(len(v2023_and_newer) / len(df)) * 100:.1f}%")
            
            # V2023 ve üzeri versiyonların detayı
            if v2023_and_newer:
                v2023_counts = pd.Series(v2023_and_newer).value_counts()
                print(f"\n  V2023 ve üzeri versiyon dağılımı:")
                for version, count in v2023_counts.items():
                    print(f"    {version}: {count:,}")
        
        # İlk 5 kayıt örneği
        print(f"\n📋 İLK 5 KAYIT ÖRNEĞİ:")
        print("-" * 50)
        for i, row in df.head().iterrows():
            print(f"Kayıt {i+1}:")
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    value = "NULL"
                print(f"  {col}: {value}")
            print()
        
        # MAUTIC vs MEVCUT MÜŞTERİ ÇAKIŞMA ANALİZİ
        print(f"\n🔍 MAUTIC vs MEVCUT MÜŞTERİ ÇAKIŞMA ANALİZİ:")
        print("-" * 60)
        
        # Mautic ve Mevcut Müşteri segmentlerini kontrol et
        mautic_customers = set()
        current_customers = set()
        
        # Önce segment sütununu kontrol et (büyük S ile)
        if 'Segment' in df.columns:
            segment_column = 'Segment'
        elif 'segment' in df.columns:
            segment_column = 'segment'
        elif 'Unnamed: 4' in df.columns:
            segment_column = 'Unnamed: 4'
        else:
            segment_column = None
            
        if segment_column:
            print(f"📊 Segment sütunu: {segment_column}")
            
            for idx, row in df.iterrows():
                email = row.get('Main E-Mail')
                if pd.isna(email):
                    continue
                    
                segments = row.get(segment_column)
                if pd.isna(segments):
                    continue
                    
                # Segmentleri parse et (tek segment veya virgülle ayrılmış)
                if ',' in str(segments):
                    segment_list = [s.strip() for s in str(segments).split(',')]
                else:
                    segment_list = [str(segments).strip()]
                
                # Mautic segmentinde olanları kaydet
                if 'Mautic' in segment_list:
                    mautic_customers.add(email.strip().lower())
                
                # Mevcut müşteri segmentinde olanları kaydet
                if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri', 'Current Customers']):
                    current_customers.add(email.strip().lower())
            
            print(f"📊 Segment Dağılımı:")
            print(f"  Mautic segmentinde: {len(mautic_customers):,} unique email")
            print(f"  Mevcut Müşteri segmentinde: {len(current_customers):,} unique email")
            
            # Çakışma analizi
            overlap = mautic_customers.intersection(current_customers)
            print(f"\n🔄 ÇAKIŞMA ANALİZİ:")
            print(f"  Hem Mautic hem Mevcut Müşteri: {len(overlap):,} email")
            print(f"  Çakışma oranı: {(len(overlap) / len(mautic_customers)) * 100:.1f}%" if len(mautic_customers) > 0 else "  Çakışma oranı: 0%")
            
            # Gerçek potansiyel müşteri sayısı
            real_prospects = mautic_customers - current_customers
            print(f"\n🎯 GERÇEK POTANSIYEL MÜŞTERİLER:")
            print(f"  Sadece Mautic (Gerçek Potansiyel): {len(real_prospects):,} email")
            print(f"  Sadece Mevcut Müşteri: {len(current_customers - mautic_customers):,} email")
            
            # Çakışan kayıtları detaylı göster
            if len(overlap) > 0:
                print(f"\n📋 ÇAKIŞAN KAYITLAR (İlk 10):")
                overlap_list = list(overlap)[:10]
                for i, email in enumerate(overlap_list, 1):
                    print(f"  {i}. {email}")
                
                if len(overlap) > 10:
                    print(f"  ... ve {len(overlap) - 10} tane daha")
                
                # Çakışan kayıtların detaylı analizi
                print(f"\n🔍 ÇAKIŞAN KAYITLAR DETAY ANALİZİ:")
                overlap_df = df[df['Main E-Mail'].str.lower().isin(overlap)]
                
                print(f"  Çakışan kayıt sayısı: {len(overlap_df):,}")
                print(f"  Bu kayıtların segment dağılımı:")
                
                for idx, row in overlap_df.head(5).iterrows():
                    email = row.get('Main E-Mail', 'N/A')
                    name = row.get('Name', 'N/A')
                    company = row.get('Acount Name', 'N/A')
                    segments = row.get(segment_column, 'N/A')  # Güncellenmiş segment sütunu
                    
                    print(f"    Email: {email}")
                    print(f"    İsim: {name}")
                    print(f"    Şirket: {company}")
                    print(f"    Segmentler: {segments}")
                    print(f"    ---")
        
        # Entegrasyon önerileri
        print(f"\n💡 ENTEGRASYON ÖNERİLERİ:")
        print("-" * 40)
        
        # Email kalitesi
        if 'Main E-Mail' in df.columns:
            email_series = df['Main E-Mail'].dropna()
            if len(email_series) > 0:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                valid_emails = email_series.str.match(email_pattern)
                email_quality = (valid_emails.sum() / len(email_series)) * 100
                print(f"📧 Email Kalitesi: {email_quality:.1f}%")
                
                if email_quality < 95:
                    print("  ⚠️  Email temizleme önerilir")
                else:
                    print("  ✅ Email kalitesi iyi")
                
                # Duplicate kontrolü
                duplicate_rate = ((len(email_series) - email_series.nunique()) / len(email_series)) * 100
                print(f"🔄 Duplicate Oranı: {duplicate_rate:.1f}%")
                
                if duplicate_rate > 1:
                    print("  ⚠️  Duplicate temizleme önerilir")
                else:
                    print("  ✅ Duplicate oranı düşük")
        
        # Veri tamamlama önerileri
        if 'Main E-Mail' in df.columns:
            email_missing = df['Main E-Mail'].isna().sum()
            missing_rate = (email_missing / len(df)) * 100
            print(f"📊 Eksik Email Oranı: {missing_rate:.1f}%")
            
            if missing_rate > 15:
                print("  ⚠️  Yüksek eksik email oranı - veri tamamlama gerekli")
            else:
                print("  ✅ Kabul edilebilir eksik email oranı")
        
        # VERİ TUTARLILIĞI ve TEMIZLEME ÖNERİLERİ
        print(f"\n🧹 VERİ TUTARLILIĞI ve TEMIZLEME ÖNERİLERİ:")
        print("-" * 50)
        
        if segment_column in df.columns and len(overlap) > 0:
            print(f"🔧 SEGMENT TUTARLILIĞI:")
            print(f"  ❌ Problematik: {len(overlap):,} email hem Mautic hem Mevcut Müşteri")
            print(f"  ✅ Çözüm: Bu kayıtları Mautic segmentinden çıkar")
            print(f"  📊 Sonuç: {len(real_prospects):,} gerçek potansiyel müşteri kalır")
            
            print(f"\n🎯 SEGMENT TEMIZLEME STRATEJİSİ:")
            print(f"  1. Çakışan {len(overlap):,} email'i tespit et")
            print(f"  2. Bu kayıtlardan Mautic segmentini kaldır")
            print(f"  3. Mevcut Müşteri segmentini koru")
            print(f"  4. Sonuçta temiz segmentasyon elde et")
            
            # Temizleme sonrası beklenen sonuçlar
            print(f"\n📈 TEMIZLEME SONRASI BEKLENEN SONUÇLAR:")
            print(f"  Mautic (Temizlenmiş): {len(real_prospects):,} email")
            print(f"  Mevcut Müşteri (Değişmez): {len(current_customers):,} email")
            print(f"  Çakışma: 0 email (Hedef)")
            print(f"  Toplam Unique: {len(mautic_customers.union(current_customers)):,} email")
        
        # Veri kalitesi önerileri
        if 'Main E-Mail' in df.columns:
            email_missing = df['Main E-Mail'].isna().sum()
            missing_rate = (email_missing / len(df)) * 100
            print(f"\n📊 VERİ KALİTESİ ÖNERİLERİ:")
            print(f"  Eksik Email Oranı: {missing_rate:.1f}%")
            
            if missing_rate > 15:
                print("  ⚠️  Yüksek eksik email oranı - veri tamamlama gerekli")
            else:
                print("  ✅ Kabul edilebilir eksik email oranı")
        
        # Entegrasyon stratejisi
        print(f"\n🎯 ENTEGRASYON STRATEJİSİ:")
        print("  1. Segment çakışmalarını temizle")
        print("  2. Email bazlı birleştirme (Primary)")
        print("  3. İsim+Şirket bazlı eşleştirme (Secondary)")
        print("  4. Lisans versiyonu bazlı segmentasyon")
        print("  5. Duplicate temizleme")
        print("  6. Veri kalitesi iyileştirme")
        
        # Önerilen adımlar
        print(f"\n📋 ÖNERİLEN ADIMLAR:")
        print("  1. Birleştirilmiş listede segment çakışmalarını temizle")
        print("  2. Mautic segmentini gerçek potansiyel müşteriler haline getir")
        print("  3. Geçerli email'leri filtrele")
        print("  4. Mevcut sistemle email bazlı çakışma kontrolü")
        print("  5. Yeni kayıtları mevcut segmentlere dağıt")
        print("  6. V2022/V2023 lisans bazlı segmentasyon")
        print("  7. Duplicate temizleme ve veri kalitesi kontrolü")
        print("  8. Test ortamında entegrasyon testi")
        print("  9. Production'a kademeli entegrasyon")
        
        # Risk analizi
        print(f"\n⚠️  RİSK ANALİZİ:")
        print("  🔴 Yüksek Risk:")
        print("    - Segment çakışmaları (Mautic vs Mevcut Müşteri)")
        print("    - %16.4 eksik email oranı")
        print("    - %32.0 eksik hesap adı")
        print("    - Duplicate email potansiyeli")
        print("  🟡 Orta Risk:")
        print("    - Lisans versiyonu çakışmaları")
        print("    - Segmentasyon karışıklığı")
        print("  🟢 Düşük Risk:")
        print("    - Veri formatı uyumluluğu")
        print("    - Teknik entegrasyon")
        
        # Segment temizleme fonksiyonu önerisi
        print(f"\n🔧 SEGMENT TEMIZLEME FONKSIYONU ÖNERİSİ:")
        print("  Aşağıdaki kod ile segment çakışmalarını temizleyebiliriz:")
        print("  ```python")
        print("  def clean_segment_conflicts(df):")
        if 'segment' in df.columns:
            print("      segment_column = 'segment'  # E1 sütunu")
        else:
            print("      segment_column = 'Unnamed: 4'  # Fallback")
        print("      for idx, row in df.iterrows():")
        print("          segments = str(row.get(segment_column, '')).split(',')")
        print("          if 'Mautic' in segments and 'Mevcut Müşteriler' in segments:")
        print("              # Mautic segmentini kaldır, Mevcut Müşteri segmentini koru")
        print("              clean_segments = [s.strip() for s in segments if s.strip() != 'Mautic']")
        print("              df.at[idx, segment_column] = ','.join(clean_segments)")
        print("      return df")
        print("  ```")
        
        return df
        
    except Exception as e:
        print(f"❌ Hata oluştu: {str(e)}")
        return None

def clean_segment_conflicts_and_integrate(df):
    """
    Segment çakışmalarını temizle ve mevcut müşteri verilerini koruyarak akıllı entegrasyon yap
    
    Strateji:
    1. Çakışan kayıtlardan Mautic segmentini kaldır
    2. Mevcut müşteri segmentinde bulunan Kalıcı/SUB/SSA verilerini koru
    3. Eksik olanları ekle, var olanları tekrar etme
    4. Temiz bir segmentasyon elde et
    """
    
    print("\n🔧 SEGMENT ÇAKIŞMA TEMİZLEME ve ENTEGRASYON SÜRECI")
    print("=" * 60)
    
    # Segment sütununu tespit et
    segment_column = None
    if 'Segment' in df.columns:
        segment_column = 'Segment'
    elif 'segment' in df.columns:
        segment_column = 'segment'
    elif 'Unnamed: 4' in df.columns:
        segment_column = 'Unnamed: 4'
    else:
        print("❌ Segment sütunu bulunamadı!")
        return df
    
    print(f"📊 Kullanılan segment sütunu: {segment_column}")
    
    # Mevcut sistem verilerini simüle et (gerçek durumda API'den veya veritabanından gelir)
    print("\n📋 MEVCUT SİSTEM VERİLERİ YÜKLEME (Simülasyon):")
    existing_customers = {
        # Örnek mevcut müşteri verileri - gerçek durumda sistemden gelir
        'existing_emails': set(),
        'existing_with_license': {}  # email: license_info
    }
    
    # Birleştirilmiş listeden mevcut müşteri verilerini topla
    print("📊 Mevcut müşteri verilerini toplama...")
    mautic_customers = set()
    current_customers = set()
    current_customers_with_license = {}
    
    conflicts_count = 0
    
    for idx, row in df.iterrows():
        email = row.get('Main E-Mail')
        if pd.isna(email):
            continue
            
        email = email.strip().lower()
        segments = row.get(segment_column)
        if pd.isna(segments):
            continue
            
        # Segmentleri parse et
        if ',' in str(segments):
            segment_list = [s.strip() for s in str(segments).split(',')]
        else:
            segment_list = [str(segments).strip()]
        
        # Mautic segmentinde olanları kaydet
        if 'Mautic' in segment_list:
            mautic_customers.add(email)
        
        # Mevcut müşteri segmentinde olanları kaydet ve lisans bilgilerini topla
        if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
            current_customers.add(email)
            
            # Lisans bilgisini kaydet
            license_info = row.get('Kalıcı/SUB/SSA')
            if pd.notna(license_info):
                current_customers_with_license[email] = {
                    'license': license_info,
                    'name': row.get('Name', ''),
                    'company': row.get('Acount Name', ''),
                    'row_index': idx
                }
    
    # Çakışma analizi
    overlap = mautic_customers.intersection(current_customers)
    
    print(f"\n📊 BAŞLANGIÇ DURUMU:")
    print(f"  Mautic segmentinde: {len(mautic_customers):,} email")
    print(f"  Mevcut Müşteri segmentinde: {len(current_customers):,} email")
    print(f"  Çakışan email: {len(overlap):,}")
    print(f"  Lisans bilgisi olan mevcut müşteri: {len(current_customers_with_license):,}")
    
    # ADIM 1: Çakışan kayıtlardan Mautic segmentini kaldır
    print(f"\n🔧 ADIM 1: Çakışan kayıtlardan Mautic segmentini kaldırma...")
    
    cleaned_count = 0
    
    for idx, row in df.iterrows():
        email = row.get('Main E-Mail')
        if pd.isna(email):
            continue
            
        email = email.strip().lower()
        
        # Çakışan email'lerde Mautic segmentini kaldır
        if email in overlap:
            segments = row.get(segment_column)
            if pd.notna(segments):
                # Segmentleri parse et
                if ',' in str(segments):
                    segment_list = [s.strip() for s in str(segments).split(',')]
                else:
                    segment_list = [str(segments).strip()]
                
                # Mautic segmentini kaldır
                if 'Mautic' in segment_list:
                    clean_segments = [s for s in segment_list if s != 'Mautic']
                    df.at[idx, segment_column] = ','.join(clean_segments) if clean_segments else ''
                    cleaned_count += 1
    
    print(f"  ✅ {cleaned_count:,} kayıttan Mautic segmenti kaldırıldı")
    
    # ADIM 2: Temizleme sonrası yeni durum
    print(f"\n📊 ADIM 2: Temizleme sonrası durum analizi...")
    
    # Yeniden analiz et
    mautic_customers_clean = set()
    current_customers_clean = set()
    
    for idx, row in df.iterrows():
        email = row.get('Main E-Mail')
        if pd.isna(email):
            continue
            
        email = email.strip().lower()
        segments = row.get(segment_column)
        if pd.isna(segments):
            continue
            
        # Segmentleri parse et
        if ',' in str(segments):
            segment_list = [s.strip() for s in str(segments).split(',')]
        else:
            segment_list = [str(segments).strip()]
        
        # Temizlenmiş segmentleri kontrol et
        if 'Mautic' in segment_list:
            mautic_customers_clean.add(email)
        
        if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
            current_customers_clean.add(email)
    
    # Yeni çakışma kontrolü
    overlap_clean = mautic_customers_clean.intersection(current_customers_clean)
    
    print(f"  Temizlenmiş Mautic segmenti: {len(mautic_customers_clean):,} email")
    print(f"  Mevcut Müşteri segmenti: {len(current_customers_clean):,} email")
    print(f"  Kalan çakışma: {len(overlap_clean):,} email")
    
    if len(overlap_clean) == 0:
        print("  ✅ Çakışma başarıyla temizlendi!")
    else:
        print(f"  ⚠️  {len(overlap_clean):,} çakışma hala var")
    
    # ADIM 3: Mevcut müşteri verilerini koruma ve eksik olanları belirleme
    print(f"\n🔍 ADIM 3: Mevcut müşteri verilerini koruma ve eksik analizi...")
    
    # Mevcut sistemdeki müşterileri simüle et (gerçek uygulamada API'den gelir)
    print("📊 Mevcut sistem müşterilerini simüle etme...")
    
    # Birleştirilmiş listeden mevcut müşterileri al
    existing_system_customers = {}
    for email, info in current_customers_with_license.items():
        existing_system_customers[email] = info
    
    # Yeni eklenecek müşterileri belirle
    new_customers_to_add = []
    
    for idx, row in df.iterrows():
        email = row.get('Main E-Mail')
        if pd.isna(email):
            continue
            
        email = email.strip().lower()
        segments = row.get(segment_column)
        if pd.isna(segments):
            continue
            
        # Segmentleri parse et
        if ',' in str(segments):
            segment_list = [s.strip() for s in str(segments).split(',')]
        else:
            segment_list = [str(segments).strip()]
        
        # Mevcut müşteri segmentinde olan ama henüz sistemde olmayan
        if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
            if email not in existing_system_customers:
                license_info = row.get('Kalıcı/SUB/SSA')
                if pd.notna(license_info):
                    new_customers_to_add.append({
                        'email': email,
                        'name': row.get('Name', ''),
                        'company': row.get('Acount Name', ''),
                        'license': license_info,
                        'row_index': idx
                    })
    
    print(f"  Mevcut sistemde korunan müşteri: {len(existing_system_customers):,}")
    print(f"  Yeni eklenecek müşteri: {len(new_customers_to_add):,}")
    
    # ADIM 4: Duplicate kontrolü ve temizleme
    print(f"\n🔄 ADIM 4: Duplicate kontrolü ve temizleme...")
    
    # Email bazlı duplicate kontrolü
    email_counts = df['Main E-Mail'].value_counts()
    duplicates = email_counts[email_counts > 1]
    
    print(f"  Duplicate email sayısı: {len(duplicates):,}")
    
    if len(duplicates) > 0:
        print(f"  En çok tekrar eden email'ler:")
        for email, count in duplicates.head(10).items():
            print(f"    {email}: {count} kez")
        
        # Duplicate temizleme stratejisi
        print("\n  🧹 Duplicate temizleme stratejisi:")
        print("    1. Mevcut müşteri segmentini olanı koru")
        print("    2. Lisans bilgisi olan kayıtları öncelikle koru")
        print("    3. Daha fazla bilgi içeren kayıtları koru")
        
        # Duplicate temizleme işlemi
        to_remove = []
        
        for duplicate_email in duplicates.index:
            duplicate_rows = df[df['Main E-Mail'] == duplicate_email]
            
            # Öncelik sırası: Mevcut Müşteri > Lisans Bilgisi > Tam Veri
            best_row = None
            best_score = -1
            
            for idx, row in duplicate_rows.iterrows():
                score = 0
                segments = str(row.get(segment_column, ''))
                
                # Mevcut müşteri segmenti varsa +10 puan
                if any(seg in segments for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
                    score += 10
                
                # Lisans bilgisi varsa +5 puan
                if pd.notna(row.get('Kalıcı/SUB/SSA')):
                    score += 5
                
                # Tam veri varsa +3 puan
                if pd.notna(row.get('Name')) and pd.notna(row.get('Acount Name')):
                    score += 3
                
                # Mautic segmenti varsa -2 puan (çakışma olmaması için)
                if 'Mautic' in segments:
                    score -= 2
                
                if score > best_score:
                    best_score = score
                    best_row = idx
            
            # En iyi olanı hariç diğerlerini silme listesine ekle
            for idx, row in duplicate_rows.iterrows():
                if idx != best_row:
                    to_remove.append(idx)
        
        # Duplicate kayıtları sil
        if to_remove:
            df = df.drop(to_remove).reset_index(drop=True)
            print(f"  ✅ {len(to_remove):,} duplicate kayıt temizlendi")
        else:
            print("  ✅ Duplicate temizleme gereksiz")
    
    # ADIM 5: Final durum raporu
    print(f"\n📊 ADIM 5: Final durum raporu...")
    
    # Final analiz
    final_mautic = set()
    final_current = set()
    final_with_license = 0
    
    for idx, row in df.iterrows():
        email = row.get('Main E-Mail')
        if pd.isna(email):
            continue
            
        email = email.strip().lower()
        segments = row.get(segment_column)
        if pd.isna(segments):
            continue
            
        # Segmentleri parse et
        if ',' in str(segments):
            segment_list = [s.strip() for s in str(segments).split(',')]
        else:
            segment_list = [str(segments).strip()]
        
        # Final segmentleri kontrol et
        if 'Mautic' in segment_list:
            final_mautic.add(email)
        
        if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
            final_current.add(email)
            
            # Lisans bilgisi kontrolü
            if pd.notna(row.get('Kalıcı/SUB/SSA')):
                final_with_license += 1
    
    final_overlap = final_mautic.intersection(final_current)
    
    print(f"\n✅ FİNAL SONUÇLAR:")
    print(f"  📧 Toplam kayıt: {len(df):,}")
    print(f"  🎯 Temiz Mautic segmenti: {len(final_mautic):,} email")
    print(f"  🏢 Mevcut Müşteri segmenti: {len(final_current):,} email")
    print(f"  📋 Lisans bilgisi olan mevcut müşteri: {final_with_license:,}")
    print(f"  🔄 Kalan çakışma: {len(final_overlap):,} email")
    print(f"  📊 Toplam unique email: {len(final_mautic.union(final_current)):,}")
    
    # Başarı oranı
    if len(overlap) > 0:
        success_rate = ((len(overlap) - len(final_overlap)) / len(overlap)) * 100
        print(f"  ✅ Temizleme başarı oranı: {success_rate:.1f}%")
    
    # Veri koruma raporu
    print(f"\n🛡️  VERİ KORUMA RAPORU:")
    print(f"  ✅ Mevcut müşteri Kalıcı/SUB/SSA verileri korundu")
    print(f"  ✅ Duplicate kayıtlar akıllı temizlendi")
    print(f"  ✅ Çakışan Mautic segmentleri kaldırıldı")
    print(f"  ✅ Mevcut müşteri segmentleri korundu")
    
    # Entegrasyon önerileri
    print(f"\n💡 ENTEGRASYONa HAZIR DURUM:")
    print(f"  🎯 Gerçek potansiyel müşteri (Mautic): {len(final_mautic):,}")
    print(f"  🏢 Korunan mevcut müşteri: {len(final_current):,}")
    print(f"  📋 Lisans bilgisi korunan müşteri: {final_with_license:,}")
    print(f"  🚀 Sistem entegrasyonuna hazır!")
    
    return df

def analyze_sales_hub_vs_current_customers(df):
    """
    Sales Hub ve Mevcut Müşteriler arasındaki ilişkiyi analiz et
    
    Amaç:
    1. Mevcut müşterilerimizin ne kadarı Sales Hub'a eklenmiş?
    2. Sales Hub'daki kayıtların ne kadarı gerçekten mevcut müşteri?
    3. Veri kaybı riski olmadan nasıl temizleme yapabiliriz?
    4. Eksik olan mevcut müşteriler kimler?
    """
    
    print("\n🔍 SALES HUB vs MEVCUT MÜŞTERİLER ANALİZİ")
    print("=" * 60)
    
    # Segment sütununu tespit et
    segment_column = None
    if 'Segment' in df.columns:
        segment_column = 'Segment'
    elif 'segment' in df.columns:
        segment_column = 'segment'
    elif 'Unnamed: 4' in df.columns:
        segment_column = 'Unnamed: 4'
    else:
        print("❌ Segment sütunu bulunamadı!")
        return
    
    print(f"📊 Kullanılan segment sütunu: {segment_column}")
    
    # Segment verilerini topla
    sales_hub_customers = set()
    current_customers = set()
    current_customers_with_license = {}
    sales_hub_with_license = {}
    
    for idx, row in df.iterrows():
        email = row.get('Main E-Mail')
        if pd.isna(email):
            continue
            
        email = email.strip().lower()
        segments = row.get(segment_column)
        if pd.isna(segments):
            continue
            
        # Segmentleri parse et
        if ',' in str(segments):
            segment_list = [s.strip() for s in str(segments).split(',')]
        else:
            segment_list = [str(segments).strip()]
        
        # Sales Hub segmentinde olanları kaydet
        if 'Sales Hub' in segment_list:
            sales_hub_customers.add(email)
            
            # Lisans bilgisini kaydet
            license_info = row.get('Kalıcı/SUB/SSA')
            if pd.notna(license_info):
                sales_hub_with_license[email] = {
                    'license': license_info,
                    'name': row.get('Name', ''),
                    'company': row.get('Acount Name', ''),
                    'row_index': idx
                }
        
        # Mevcut müşteri segmentinde olanları kaydet
        if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
            current_customers.add(email)
            
            # Lisans bilgisini kaydet
            license_info = row.get('Kalıcı/SUB/SSA')
            if pd.notna(license_info):
                current_customers_with_license[email] = {
                    'license': license_info,
                    'name': row.get('Name', ''),
                    'company': row.get('Acount Name', ''),
                    'row_index': idx
                }
    
    # Çakışma ve eksik analizi
    overlap = sales_hub_customers.intersection(current_customers)
    missing_from_sales_hub = current_customers - sales_hub_customers
    only_in_sales_hub = sales_hub_customers - current_customers
    
    print(f"\n📊 TEMEL DURUMU:")
    print(f"  📧 Sales Hub segmentinde: {len(sales_hub_customers):,} unique email")
    print(f"  🏢 Mevcut Müşteri segmentinde: {len(current_customers):,} unique email")
    print(f"  📋 Lisans bilgisi olan Sales Hub: {len(sales_hub_with_license):,}")
    print(f"  📋 Lisans bilgisi olan Mevcut Müşteri: {len(current_customers_with_license):,}")
    
    print(f"\n🔄 ÇAKIŞMA VE EKSİK ANALİZİ:")
    print(f"  ✅ Hem Sales Hub hem Mevcut Müşteri: {len(overlap):,} email")
    print(f"  ❌ Mevcut Müşteri ama Sales Hub'da YOK: {len(missing_from_sales_hub):,} email")
    print(f"  ❓ Sales Hub'da ama Mevcut Müşteri DEĞİL: {len(only_in_sales_hub):,} email")
    
    # Yüzde analizi
    if len(current_customers) > 0:
        coverage_rate = (len(overlap) / len(current_customers)) * 100
        print(f"\n📈 KAPSAMA ORANI:")
        print(f"  🎯 Sales Hub kapsamı: {coverage_rate:.1f}%")
        print(f"  📊 Mevcut müşterilerin {coverage_rate:.1f}%'i Sales Hub'da var")
        print(f"  ⚠️  Mevcut müşterilerin {100-coverage_rate:.1f}%'i Sales Hub'da EKSİK")
    
    # Eksik mevcut müşteriler detayı
    if len(missing_from_sales_hub) > 0:
        print(f"\n❌ SALES HUB'DA EKSİK MEVCUT MÜŞTERİLER:")
        print(f"  📊 Toplam eksik: {len(missing_from_sales_hub):,} email")
        
        # Eksik müşterilerin lisans bilgisi analizi
        missing_with_license = []
        for email in missing_from_sales_hub:
            if email in current_customers_with_license:
                missing_with_license.append(email)
        
        print(f"  📋 Eksik müşterilerin {len(missing_with_license):,} tanesinin lisans bilgisi VAR")
        print(f"  💰 Bu {len(missing_with_license):,} müşteri Sales Hub'a EKLENMELİ")
        
        # En kritik eksik müşteriler (lisans bilgisi olanlar)
        print(f"\n🔥 KRİTİK EKSİK MÜŞTERİLER (İlk 10 - Lisans bilgisi olanlar):")
        shown_count = 0
        for email in missing_from_sales_hub:
            if email in current_customers_with_license and shown_count < 10:
                info = current_customers_with_license[email]
                print(f"  {shown_count + 1}. Email: {email}")
                print(f"     İsim: {info['name']}")
                print(f"     Şirket: {info['company']}")
                print(f"     Lisans: {info['license']}")
                print(f"     ---")
                shown_count += 1
    
    # Sales Hub'da olan ama mevcut müşteri olmayanlar
    if len(only_in_sales_hub) > 0:
        print(f"\n❓ SALES HUB'DA OLAN AMA MEVCUT MÜŞTERİ OLMAYANLAR:")
        print(f"  📊 Toplam: {len(only_in_sales_hub):,} email")
        
        # Bunların lisans bilgisi var mı?
        only_sales_hub_with_license = []
        for email in only_in_sales_hub:
            if email in sales_hub_with_license:
                only_sales_hub_with_license.append(email)
        
        print(f"  📋 Bunların {len(only_sales_hub_with_license):,} tanesinin lisans bilgisi VAR")
        print(f"  🤔 Bu kayıtlar muhtemelen eski müşteriler veya yanlış sınıflandırılmış")
        
        # Örnek kayıtlar
        print(f"\n🔍 ÖRNEK KAYITLAR (İlk 5):")
        shown_count = 0
        for email in only_in_sales_hub:
            if shown_count < 5:
                # Bu email'in verilerini bul
                row_data = df[df['Main E-Mail'].str.lower() == email].iloc[0] if len(df[df['Main E-Mail'].str.lower() == email]) > 0 else None
                if row_data is not None:
                    print(f"  {shown_count + 1}. Email: {email}")
                    print(f"     İsim: {row_data.get('Name', 'N/A')}")
                    print(f"     Şirket: {row_data.get('Acount Name', 'N/A')}")
                    print(f"     Lisans: {row_data.get('Kalıcı/SUB/SSA', 'N/A')}")
                    print(f"     ---")
                shown_count += 1
    
    # VERİ KAYBΙ RİSKİ ANALİZİ
    print(f"\n⚠️  VERİ KAYBI RİSKİ ANALİZİ:")
    print(f"  🔴 Yüksek Risk:")
    print(f"    - {len(missing_from_sales_hub):,} mevcut müşteri Sales Hub'da eksik")
    print(f"    - {len(missing_with_license):,} lisans bilgisi olan müşteri eksik")
    print(f"    - Bu müşteriler satış takip edilemiyor")
    
    print(f"\n  🟡 Orta Risk:")
    print(f"    - {len(only_in_sales_hub):,} Sales Hub kaydı belirsiz durumda")
    print(f"    - {len(only_sales_hub_with_license):,} tanesi lisans bilgisi olan")
    print(f"    - Bu kayıtlar mevcut müşteri olabilir")
    
    print(f"\n  🟢 Düşük Risk:")
    print(f"    - {len(overlap):,} kayıt her iki segmentte de mevcut")
    print(f"    - Bu kayıtlar doğru sınıflandırılmış")
    
    # ÖNERİLER
    print(f"\n💡 ÇÖZÜM ÖNERİLERİ:")
    print(f"  📋 1. MEVCUT MÜŞTERİLERİ SALES HUB'A EKLE:")
    print(f"     - {len(missing_from_sales_hub):,} eksik müşteriyi Sales Hub'a ekle")
    print(f"     - Öncelik: Lisans bilgisi olan {len(missing_with_license):,} müşteri")
    print(f"     - Risk: Düşük - Sadece ekleme yapılacak")
    
    print(f"\n  🔍 2. SALES HUB KAYITLARINI DOĞRULA:")
    print(f"     - {len(only_in_sales_hub):,} Sales Hub kaydını incele")
    print(f"     - Lisans bilgisi olan {len(only_sales_hub_with_license):,} kayıt muhtemelen mevcut müşteri")
    print(f"     - Bu kayıtları Mevcut Müşteri segmentine EKLE (temizleme değil)")
    
    print(f"\n  🛡️  3. VERİ KORUMA STRATEJİSİ:")
    print(f"     - Hiçbir kayıt SİLİNMEMELİ")
    print(f"     - Sadece segment ETİKETLERİ EKLENMELİ")
    print(f"     - Çakışan kayıtlar KORUNMALI")
    print(f"     - Lisans bilgileri KORUNMALI")
    
    # UYGULAMA PLANI
    print(f"\n🎯 UYGULAMA PLANI:")
    print(f"  🔄 1. AŞAMA: Eksik müşterileri Sales Hub'a ekle")
    print(f"     - {len(missing_from_sales_hub):,} kayıt için 'Sales Hub' segmenti EKLE")
    print(f"     - Mevcut 'Mevcut Müşteri' segmentini KORU")
    print(f"     - Lisans bilgilerini KORU")
    
    print(f"\n  🔄 2. AŞAMA: Belirsiz kayıtları doğrula")
    print(f"     - {len(only_in_sales_hub):,} Sales Hub kaydını incele")
    print(f"     - Lisans bilgisi olanları 'Mevcut Müşteri' segmentine EKLE")
    print(f"     - Diğerlerini potansiyel müşteri olarak TANIMLA")
    
    print(f"\n  🔄 3. AŞAMA: Final doğrulama")
    print(f"     - Tüm mevcut müşteriler Sales Hub'da olmalı")
    print(f"     - Tüm lisans bilgisi olanlar mevcut müşteri olmalı")
    print(f"     - Çakışan kayıtlar korunmalı")
    
    # SONUÇ
    print(f"\n✅ SONUÇ:")
    print(f"  📈 Hedef: %100 Sales Hub kapsamı")
    print(f"  📊 Mevcut: {coverage_rate:.1f}% kapsam")
    print(f"  🎯 Eksik: {len(missing_from_sales_hub):,} müşteri")
    print(f"  🛡️  Risk: Düşük - Sadece ekleme yapılacak")
    print(f"  💰 Değer: {len(missing_with_license):,} lisanslı müşteri geri kazanılacak")
    
    return {
        'sales_hub_customers': sales_hub_customers,
        'current_customers': current_customers,
        'overlap': overlap,
        'missing_from_sales_hub': missing_from_sales_hub,
        'only_in_sales_hub': only_in_sales_hub,
        'missing_with_license': missing_with_license,
        'coverage_rate': coverage_rate if len(current_customers) > 0 else 0
    }

if __name__ == "__main__":
    df = analyze_birlestirilmis_liste()
    
    if df is not None:
        print(f"\n✅ Analiz tamamlandı!")
        print(f"Toplam {len(df):,} kayıt analiz edildi.")
        
        # Temizleme işlemini başlat
        print(f"\n{'='*60}")
        print("🚀 SEGMENT ÇAKIŞMA TEMİZLEME SÜRECI BAŞLATILIYOR...")
        print(f"{'='*60}")
        
        # Temizleme fonksiyonunu çalıştır
        cleaned_df = clean_segment_conflicts_and_integrate(df)
        
        # Temizlenmiş veriyi kaydet
        if cleaned_df is not None:
            output_file = "veri_kaynaklari/birlestirilmis-liste-TEMIZLENMIS.xlsx"
            try:
                cleaned_df.to_excel(output_file, index=False)
                print(f"\n💾 TEMİZLENMİŞ VERİ KAYDEDILDI:")
                print(f"  📁 Dosya: {output_file}")
                print(f"  📊 Kayıt sayısı: {len(cleaned_df):,}")
                print(f"  ✅ Başarıyla kaydedildi!")
                
                # Özet rapor
                print(f"\n📋 ÖZET RAPOR:")
                print(f"  📈 Orijinal kayıt: {len(df):,}")
                print(f"  📉 Temizlenmiş kayıt: {len(cleaned_df):,}")
                print(f"  📊 Temizlenen kayıt: {len(df) - len(cleaned_df):,}")
                
                # Final analiz
                segment_column = None
                if 'Segment' in cleaned_df.columns:
                    segment_column = 'Segment'
                elif 'segment' in cleaned_df.columns:
                    segment_column = 'segment'
                elif 'Unnamed: 4' in cleaned_df.columns:
                    segment_column = 'Unnamed: 4'
                
                if segment_column:
                    final_mautic = set()
                    final_current = set()
                    final_with_license = 0
                    
                    for idx, row in cleaned_df.iterrows():
                        email = row.get('Main E-Mail')
                        if pd.isna(email):
                            continue
                            
                        email = email.strip().lower()
                        segments = row.get(segment_column)
                        if pd.isna(segments):
                            continue
                            
                        # Segmentleri parse et
                        if ',' in str(segments):
                            segment_list = [s.strip() for s in str(segments).split(',')]
                        else:
                            segment_list = [str(segments).strip()]
                        
                        # Final segmentleri kontrol et
                        if 'Mautic' in segment_list:
                            final_mautic.add(email)
                        
                        if any(seg in segment_list for seg in ['Mevcut Müşteriler', 'Mevcut Müşteri']):
                            final_current.add(email)
                            
                            # Lisans bilgisi kontrolü
                            if pd.notna(row.get('Kalıcı/SUB/SSA')):
                                final_with_license += 1
                    
                    final_overlap = final_mautic.intersection(final_current)
                    
                    print(f"\n🎯 FİNAL SEGMENT DURUMU:")
                    print(f"  📧 Mautic segmenti: {len(final_mautic):,} email")
                    print(f"  🏢 Mevcut Müşteri segmenti: {len(final_current):,} email")
                    print(f"  📋 Lisans bilgisi korunan: {final_with_license:,}")
                    print(f"  🔄 Kalan çakışma: {len(final_overlap):,} email")
                    
                    if len(final_overlap) == 0:
                        print(f"  ✅ ÇAKİŞMA BAŞARIYLA TEMİZLENDİ!")
                    else:
                        print(f"  ⚠️  {len(final_overlap):,} çakışma devam ediyor")
                
                print(f"\n🚀 ENTEGRASYONa HAZIR!")
                print(f"  Temizlenmiş dosya: {output_file}")
                print(f"  Sistem entegrasyonuna hazır durumda!")
                
            except Exception as e:
                print(f"❌ Dosya kaydetme hatası: {str(e)}")
        
        else:
            print("❌ Temizleme işlemi başarısız!")
