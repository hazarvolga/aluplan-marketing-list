import * as XLSX from 'xlsx';

export interface MarketingData {
  name: string;
  email: string;
  company: string;
  phone: string;
  segment: string;
  processingStatus: 'Sales Hub İşlenmiş' | 'Sales Hub İşlenmemiş' | 'Potansiyel' | 'Diğer';
  isMevcutMusteriler: boolean;
  isPotansiyelMusteriler: boolean;
  isSalesHubMevcut: boolean;
  isV2022: boolean;
  isV2023: boolean;
  spamScore: number;
  spamReason: string;
}

export interface FilterOptions {
  segments: {
    mevcutMusteriler: boolean;
    potansiyelMusteriler: boolean;
    salesHubMevcut: boolean;
    v2022: boolean;
    v2023: boolean;
  };
  searchTerm: string;
}

export function processExcelData(buffer: ArrayBuffer): MarketingData[] {
  const workbook = XLSX.read(buffer, { type: 'array' });
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];
  const rawData = XLSX.utils.sheet_to_json(worksheet);

  return rawData.map((row: any) => {
    const segment = String(row.segment || '').toLowerCase();
    const email = String(row.email || '');
    const spamCheck = checkSpamEmail(email);
    
    // İşlenme durumunu belirle
    let processingStatus: 'Sales Hub İşlenmiş' | 'Sales Hub İşlenmemiş' | 'Potansiyel' | 'Diğer';
    if (segment.includes('sales hub mevcut')) {
      processingStatus = 'Sales Hub İşlenmiş';
    } else if (segment.includes('mevcut müşteriler')) {
      processingStatus = 'Sales Hub İşlenmemiş';
    } else if (segment.includes('potansiyel müşteriler')) {
      processingStatus = 'Potansiyel';
    } else {
      processingStatus = 'Diğer';
    }
    
    return {
      name: String(row.name || ''),
      email: email,
      company: String(row.company || ''),
      phone: String(row.phone || ''),
      segment: String(row.segment || ''),
      processingStatus: processingStatus,
      isMevcutMusteriler: segment.includes('mevcut müşteriler'),
      isPotansiyelMusteriler: segment.includes('potansiyel müşteriler'),
      isSalesHubMevcut: segment.includes('sales hub mevcut'),
      isV2022: segment.includes('v2022'),
      isV2023: segment.includes('v2023'),
      spamScore: spamCheck.score,
      spamReason: spamCheck.reason,
    };
  });
}

export function filterData(data: MarketingData[], filters: FilterOptions): MarketingData[] {
  return data.filter(item => {
    // Search filter
    if (filters.searchTerm) {
      const searchLower = filters.searchTerm.toLowerCase();
      const matchesSearch = 
        item.name.toLowerCase().includes(searchLower) ||
        item.email.toLowerCase().includes(searchLower) ||
        item.company.toLowerCase().includes(searchLower);
      
      if (!matchesSearch) return false;
    }

    // Segment filters
    const { segments } = filters;
    const hasActiveFilters = Object.values(segments).some(Boolean);
    
    if (!hasActiveFilters) return true;

    return (
      (segments.mevcutMusteriler && (item.isMevcutMusteriler || item.isSalesHubMevcut)) ||
      (segments.potansiyelMusteriler && item.isPotansiyelMusteriler) ||
      (segments.salesHubMevcut && item.isSalesHubMevcut) ||
      (segments.v2022 && item.isV2022) ||
      (segments.v2023 && item.isV2023)
    );
  });
}

export function getSegmentCounts(data: MarketingData[]) {
  return {
    total: data.length,
    mevcutMusteriler: data.filter(item => item.isMevcutMusteriler || item.isSalesHubMevcut).length,
    potansiyelMusteriler: data.filter(item => item.isPotansiyelMusteriler).length,
    salesHubMevcut: data.filter(item => item.isSalesHubMevcut).length,
    v2022: data.filter(item => item.isV2022).length,
    v2023: data.filter(item => item.isV2023).length,
  };
}

export function exportToCSV(data: MarketingData[]): string {
  const headers = ['Name', 'Email', 'Company', 'Phone', 'Segment', 'Processing Status'];
  const rows = data.map(item => [
    item.name,
    item.email,
    item.company,
    item.phone,
    item.segment,
    item.processingStatus
  ]);
  
  const csvContent = [headers, ...rows]
    .map(row => row.map(cell => `"${cell}"`).join(','))
    .join('\n');
  
  return csvContent;
}

export interface DataQualityStats {
  totalRecords: number;
  duplicateEmails: number;
  invalidEmails: number;
  emptyNames: number;
  emptyCompanies: number;
  validRecords: number;
  spamEmails: number;
}

export function getDataQualityStats(data: MarketingData[]): DataQualityStats {
  const emails = data.map(item => item.email).filter(email => email);
  const uniqueEmails = [...new Set(emails)];
  const duplicateEmails = emails.length - uniqueEmails.length;
  
  // Email format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const invalidEmails = emails.filter(email => !emailRegex.test(email)).length;
  
  // Spam email check
  const spamStats = getSpamStats(data);
  
  // Empty fields
  const emptyNames = data.filter(item => !item.name.trim()).length;
  const emptyCompanies = data.filter(item => !item.company.trim()).length;
  
  // Valid records (has email, name, and valid email format)
  const validRecords = data.filter(item => 
    item.email.trim() && 
    item.name.trim() && 
    emailRegex.test(item.email)
  ).length;
  
  return {
    totalRecords: data.length,
    duplicateEmails,
    invalidEmails,
    emptyNames,
    emptyCompanies,
    validRecords,
    spamEmails: spamStats.spamCount,
  };
}

// Common spam/disposable email domains
const SPAM_DOMAINS = [
  // Disposable email services
  '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
  'yopmail.com', 'temp-mail.org', 'dispostable.com', 'throwaway.email',
  'getnada.com', 'maildrop.cc', 'sharklasers.com', 'grr.la',
  // Known spam domains
  'example.com', 'test.com', 'sample.com', 'demo.com',
  // Common typos
  'gmial.com', 'gmai.com', 'yahooo.com', 'hotmial.com',
  'outlok.com', 'gmailcom', 'yahoo.co', 'hotmail.co'
];

export interface SpamCheckResult {
  isSpam: boolean;
  reason: string;
  email: string;
  score: number; // 0-100 spam puanı
}

export function checkSpamEmail(email: string): SpamCheckResult {
  const emailLower = email.toLowerCase();
  const domain = emailLower.split('@')[1];
  let score = 0;
  let reasons: string[] = [];
  
  if (!domain) {
    return { isSpam: true, reason: 'Geçersiz email formatı', email, score: 100 };
  }
  
  // High-risk spam domains (90-100 puan)
  const highRiskDomains = [
    '10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com',
    'yopmail.com', 'temp-mail.org', 'dispostable.com', 'throwaway.email'
  ];
  
  if (highRiskDomains.includes(domain)) {
    score = 95;
    reasons.push('Geçici email servisi');
  }
  
  // Medium-risk domains (60-80 puan)
  const mediumRiskDomains = [
    'getnada.com', 'maildrop.cc', 'sharklasers.com', 'grr.la'
  ];
  
  if (mediumRiskDomains.includes(domain)) {
    score = 70;
    reasons.push('Şüpheli email servisi');
  }
  
  // Common typo domains (40-60 puan)
  const typoDomains = [
    'gmial.com', 'gmai.com', 'yahooo.com', 'hotmial.com',
    'outlok.com', 'gmailcom', 'yahoo.co', 'hotmail.co'
  ];
  
  if (typoDomains.includes(domain)) {
    score = 50;
    reasons.push('Typo domain');
  }
  
  // Suspicious patterns (10-30 puan)
  if (domain.includes('temp') || domain.includes('disposable') || domain.includes('fake')) {
    score = Math.max(score, 30);
    reasons.push('Şüpheli domain');
  }
  
  // Too many numbers in local part (10-20 puan)
  const localPart = emailLower.split('@')[0];
  const numberCount = (localPart.match(/\d/g) || []).length;
  if (numberCount > localPart.length * 0.7) {
    score = Math.max(score, 20);
    reasons.push('Şüpheli karakter');
  }
  
  // Very short local part (5-15 puan)
  if (localPart.length < 3) {
    score = Math.max(score, 15);
    reasons.push('Kısa email');
  }
  
  // Random character patterns (5-25 puan)
  const hasRandomPattern = /^[a-z0-9]{10,}$/.test(localPart) && localPart.length > 8;
  if (hasRandomPattern) {
    score = Math.max(score, 25);
    reasons.push('Rastgele karakter');
  }
  
  const reason = reasons.length > 0 ? reasons.join(', ') : 'Geçerli email';
  const isSpam = score >= 40; // 40 puan üzeri spam kabul et
  
  return { isSpam, reason, email, score };
}

export function getSpamStats(data: MarketingData[]) {
  const emails = data.map(item => item.email).filter(email => email);
  const spamResults = emails.map(email => checkSpamEmail(email));
  const spamEmails = spamResults.filter(result => result.isSpam);
  
  return {
    totalEmails: emails.length,
    spamCount: spamEmails.length,
    cleanCount: emails.length - spamEmails.length,
    spamPercentage: emails.length > 0 ? Math.round((spamEmails.length / emails.length) * 100) : 0,
    spamEmails: spamEmails,
  };
}
