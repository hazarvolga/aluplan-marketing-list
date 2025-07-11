import pandas as pd
import json

print("📝 V2022 EMAIL LİSTESİ OLUŞTURULUYOR")
print("=" * 60)

# V2022 dosyasını yükle
df_v2022 = pd.read_excel('veri_kaynaklari/Allplan Müşteriler_Final_2025-03-19-R28 - V2022 ve eski.xlsx')

# Email sütununu temizle
email_column = 'Main E-Mail'
df_v2022_clean = df_v2022.copy()
df_v2022_clean = df_v2022_clean.dropna(subset=[email_column])
df_v2022_clean = df_v2022_clean[df_v2022_clean[email_column].str.contains('@', na=False)]

# Email listesi
v2022_emails = sorted(list(set(df_v2022_clean[email_column].str.lower().str.strip())))

print(f"📧 V2022 email sayısı: {len(v2022_emails):,}")

# TypeScript dosyası olarak kaydet
ts_content = f"""// V2022 ve eski müşteri email listesi
// Bu liste Virtual V2022 segmenti için kullanılır
// Müşteriler mevcut segmentlerini korur, sadece filtreleme için kullanılır
// Toplam: {len(v2022_emails)} email

export const V2022_EMAILS = new Set([
"""

# Email'leri ekle
for email in v2022_emails:
    ts_content += f'  "{email}",\n'

ts_content += "]);\n\n"
ts_content += f"// V2022 email listesi {len(v2022_emails)} adet email içerir\n"
ts_content += "// Bu müşteriler V2022 ve eski segment filtresinde görünür\n"

# Dosyaya yaz
with open('src/lib/v2022-emails.ts', 'w', encoding='utf-8') as f:
    f.write(ts_content)

print(f"✅ V2022 email listesi kaydedildi: src/lib/v2022-emails.ts")
print(f"📝 Toplam {len(v2022_emails)} email")

# İlk 10 email'i göster
print(f"\n📋 İLK 10 EMAIL:")
for i, email in enumerate(v2022_emails[:10], 1):
    print(f"  {i}. {email}")

print(f"\n✅ V2022 VIRTUAL SEGMENT HAZIR")
print("=" * 60)
