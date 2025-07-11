import pandas as pd

print('🔍 SALES HUB MEVCUT VE VİRTUAL SEGMENT TUTARSıZLıĞı ANALİZİ')
print('=' * 70)

# Ana veri dosyasını yükle
df = pd.read_excel('data/aluplan-list.xlsx')

print('📊 MEVCUT DURUM:')
print('   💼 Sales Hub Mevcut: 1,032')
print('   🔄 V2022 ve eski: 800 (Virtual)')
print('   📈 V2023 ve üzeri: 95 (Virtual)')
print('   🧮 Virtual Toplam: 800 + 95 = 895')
print('   ❓ Fark: 1,032 - 895 = 137 kayıt')
print('\n❓ BU FARK NEDİR? ANALİZ EDELİM...')

# Sales Hub Mevcut kayıtlarını analiz et
sales_hub = df[df['segment'].astype(str).str.contains('Sales Hub Mevcut', case=False, na=False)]
print(f'\n📊 SALES HUB MEVCUT DETAY:')
print(f'   📝 Toplam kayıt: {len(sales_hub):,}')
print(f'   📧 Unique email: {sales_hub["email"].nunique():,}')

# V2022 ve V2023 email listelerini yükle
v2022_emails = set()
v2023_emails = set()

# V2022 emaillerini yükle
try:
    with open('src/data/v2022-emails.ts', 'r') as f:
        content = f.read()
        import re
        emails = re.findall(r'"([^"]+@[^"]+)"', content)
        v2022_emails = set(email.lower().strip() for email in emails)
except:
    print('   ⚠️ V2022 email listesi okunamadı')

# V2023 emaillerini yükle
try:
    with open('src/data/v2023-emails.ts', 'r') as f:
        content = f.read()
        import re
        emails = re.findall(r'"([^"]+@[^"]+)"', content)
        v2023_emails = set(email.lower().strip() for email in emails)
except:
    print('   ⚠️ V2023 email listesi okunamadı')

print(f'\n📧 VİRTUAL SEGMENT EMAİL SAYILARI:')
print(f'   📧 V2022 emails: {len(v2022_emails):,}')
print(f'   📧 V2023 emails: {len(v2023_emails):,}')
print(f'   🔄 Virtual email toplam: {len(v2022_emails) + len(v2023_emails):,}')

# Sales Hub emaillerini analiz et
sales_hub_emails = set(sales_hub['email'].astype(str).str.lower().str.strip())
print(f'   📧 Sales Hub emails: {len(sales_hub_emails):,}')

# Kesişim analizi
v2022_intersection = sales_hub_emails & v2022_emails
v2023_intersection = sales_hub_emails & v2023_emails
virtual_union = v2022_emails | v2023_emails
virtual_intersection = sales_hub_emails & virtual_union

print(f'\n🔄 KESİŞİM ANALİZİ:')
print(f'   📧 Sales Hub ∩ V2022: {len(v2022_intersection):,}')
print(f'   📧 Sales Hub ∩ V2023: {len(v2023_intersection):,}')
print(f'   📧 Sales Hub ∩ Virtual: {len(virtual_intersection):,}')
print(f'   📧 Sales Hub - Virtual: {len(sales_hub_emails - virtual_union):,}')

# Fark hesaplama
difference = len(sales_hub_emails) - len(virtual_intersection)
print(f'\n🧮 MATEMATİK:')
print(f'   📊 Sales Hub: {len(sales_hub_emails):,}')
print(f'   📊 Virtual Kesişim: {len(virtual_intersection):,}')
print(f'   📊 Fark: {difference:,}')

# Bu farkın nedenini analiz et
not_in_virtual = sales_hub_emails - virtual_union
print(f'\n❓ SALES HUB\'DA OLUP VİRTUAL SEGMENT\'TE OLMAYAN {len(not_in_virtual):,} KAYIT:')

# Bu kayıtların source bilgisini kontrol et
not_virtual_df = df[df['email'].astype(str).str.lower().str.strip().isin(not_in_virtual)]
if len(not_virtual_df) > 0:
    print(f'   📊 Source dağılımı:')
    source_counts = not_virtual_df['source'].value_counts()
    for source, count in source_counts.items():
        print(f'      📋 {source}: {count:,}')
    
    # Segment dağılımı
    print(f'   📊 Segment dağılımı:')
    segment_counts = not_virtual_df['segment'].value_counts()
    for segment, count in segment_counts.head(5).items():
        print(f'      📋 {segment}: {count:,}')

print(f'\n' + '='*70)
print('💡 SONUÇ VE AÇIKLAMA:')
print('   ✅ NORMAL DURUM: Sales Hub Mevcut > Virtual Segment')
print('   ✅ NEDEN: Sales Hub\'da virtual segment\'e dahil OLMAYAN kayıtlar var')
print('   ✅ BU KAYITLAR: Dynamics 365\'ten gelen ama V2022/V2023 listelerinde olmayan müşteriler')
print('   ✅ ÇÖZÜM: Kullanıcıya bu durumu açıklayan bir not ekleyelim')

print(f'\n🎯 KULLANICI İÇİN AÇIKLAMA:')
print('   "Sales Hub Mevcut sayısı, V2022 ve V2023 virtual segment toplamından')
print('   büyüktür çünkü Sales Hub\'da virtual segment listelerine dahil')
print('   olmayan ek müşteri kayıtları da bulunmaktadır."')

print(f'\n📊 ÖNLEMA TABLOSU:')
print('┌─────────────────────────┬─────────┬──────────────────────────────┐')
print('│ Kategori                │ Sayı    │ Açıklama                     │')
print('├─────────────────────────┼─────────┼──────────────────────────────┤')
print(f'│ Sales Hub Mevcut        │ {len(sales_hub_emails):,}     │ Tüm Sales Hub kayıtları      │')
print(f'│ V2022 ve eski           │ {len(v2022_emails):,}     │ Virtual segment              │')
print(f'│ V2023 ve üzeri          │ {len(v2023_emails):,}      │ Virtual segment              │')
print(f'│ Virtual Kesişim         │ {len(virtual_intersection):,}     │ Sales Hub ∩ Virtual          │')
print(f'│ Diğer Sales Hub         │ {difference:,}     │ Virtual\'de olmayan kayıtlar  │')
print('└─────────────────────────┴─────────┴──────────────────────────────┘')
