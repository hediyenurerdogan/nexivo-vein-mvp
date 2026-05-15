# Görüntü Kalite Skoru Planı

## Amaç

Gerçek NIR donanımı geldiğinde her görüntünün işlenebilir olup olmadığını hızlıca ölçmek.

## İlk Kalite Sinyalleri

- ROI bulunabildi mi?
- ROI genişliği/yüksekliği beklenen aralıkta mı?
- Görüntü aşırı karanlık mı?
- Görüntü aşırı parlak mı?
- Kontrast yeterli mi?
- Damar cevabı maskesi çok boş veya çok dolu mu?
- Aynı kişinin tekrar görüntüleri benzer skor veriyor mu?

## Başlangıç Metrikleri

- Ortalama parlaklık
- Standart sapma / kontrast
- ROI alan oranı
- Vein mask doluluk oranı
- Laplacian variance ile bulanıklık göstergesi

## Donanım Geldiğinde Kabul Kriteri

İlk 5 kişilik testte görüntülerin en az %80'i kalite kontrolünden geçmelidir. Kalite kontrolünden geçmeyen görüntüler ayrı klasörde saklanmalı ve nedenleri issue'ya yazılmalıdır.

