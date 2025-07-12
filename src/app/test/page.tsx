export default function TestPage() {
  return (
    <div style={{ padding: '20px' }}>
      <h1>Test Sayfası</h1>
      <p>Bu sayfa çalışıyorsa Next.js temel işlevleri tamam.</p>
      <p>Tarih: {new Date().toLocaleString('tr-TR')}</p>
    </div>
  );
}
