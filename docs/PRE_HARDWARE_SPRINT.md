# Donanım Öncesi Sprint Planı

## Sprint Amacı

Donanım gelmeden önce NEXIVO'nun teknik MVP'sinin yazılım, test ve anlatım zemini hazır hale getirilecek. Donanım geldiğinde ekip doğrudan görüntü almaya ve ölçmeye başlayacak.

## Kanıtlanacak Ana Hipotez

NEXIVO, NIR tabanlı parmak damar görüntüsünden cihaz üzerinde işlenebilir biyometrik şablon çıkarabilir ve aynı kişi/farklı kişi ayrımını temel doğrulama skorlarıyla gösterebilir.

## MVP'de Kanıtlanacaklar

- Parmak damar görüntüsü yazılımsal olarak okunabilir.
- Parmak/ROI bölgesi otomatik veya yarı otomatik kırpılabilir.
- Kontrast artırma sonrası damar çizgileri daha görünür hale getirilebilir.
- Ham görüntüden sabit boyutlu biyometrik şablon üretilebilir.
- Kayıtlı şablon ile yeni görüntü karşılaştırılabilir.
- İlk demo `eşleşti / eşleşmedi` sonucu üretebilir.

## MVP'de Kanıtlanmayacaklar

- Ticari cihaz güvenilirliği
- Banka/kurum entegrasyonu
- Seri üretim
- Sertifikasyon
- Kesin liveness/PAD dayanıklılığı
- Büyük ölçekli doğruluk oranı

## Donanım Gelmeden Yapılacak İşler

### 1. Yazılım Pipeline

- [x] Sentetik veri üretici hazır.
- [x] ROI, kontrast, damar cevabı, maske, şablon adımları hazır.
- [x] Kayıt/doğrulama komutları hazır.
- [x] Küçük değerlendirme raporu hazır.
- [ ] Açık veri seti formatına uyarlama yapılacak.
- [ ] Kalite skoru eklenecek.

### 2. Test Tasarımı

- [x] İlk test metrikleri belirlendi.
- [ ] 5 kişilik ilk test protokolü yazılacak.
- [ ] 20 kişilik genişletilmiş test protokolü yazılacak.
- [ ] Her testte tutulacak alanlar tablo haline getirilecek.

### 3. Donanım Hazırlığı

- [x] Satın alma listesi hazır.
- [ ] Ürün linkleri ve tahmini fiyatlar eklenecek.
- [ ] Kutu/gövde ilk çizimi yapılacak.
- [ ] Kamera, LED ve parmak konumu için ilk ölçü aralıkları yazılacak.

### 4. KVKK ve Etik Hazırlık

- [x] Ham görüntü ve şablon ayrımı yazıldı.
- [ ] Gönüllü test onam metni hazırlanacak.
- [ ] Test katılımcıları kişisel isimle değil kodla takip edilecek.
- [ ] Ham görüntülerin nerede/ne kadar saklanacağı netleştirilecek.

### 5. Demo Hikayesi

- [x] İlk demo anlatısı hazır.
- [ ] 1 dakikalık demo video akışı hazırlanacak.
- [ ] Mentor/BİGG görüşmesi için kısa teknik özet hazırlanacak.

## Donanım Geldiğinde İlk Gün Planı

1. Raspberry Pi işletim sistemi hazırlanır.
2. NoIR kamera görüntüsü doğrulanır.
3. 850 nm IR LED düşük güçle test edilir.
4. Parmak konumlandırma aparatı denenir.
5. İlk damar görüntüsü alınır.
6. Görüntü bu repodaki pipeline'a sokulur.
7. İlk 5 kişi için kayıt/doğrulama denemesi yapılır.

