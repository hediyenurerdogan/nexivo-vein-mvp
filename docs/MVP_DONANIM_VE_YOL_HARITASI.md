# NEXIVO MVP Donanım ve Yol Haritası

## MVP Hedefi

İlk MVP'nin hedefi ticari cihaz üretmek değildir. Hedef, NIR ışıkla parmak damar görüntüsü alıp bu görüntüden biyometrik şablon çıkaran ve basit eşleştirme yapan bir teknik prototip oluşturmaktır.

Önerilen başlangıç noktası parmak damarıdır. Avuç içi damarı uzun vadede değerlendirilebilir; fakat ilk prototipte parmak damarı daha ucuz, daha kontrollü ve daha hızlı test edilebilir.

## Önce Alınacaklar

| Öncelik | Parça | Amaç |
|---|---|---|
| 1 | Raspberry Pi 5 veya Raspberry Pi 4 | Edge cihaz prototipi |
| 1 | Raspberry Pi Camera Module 3 NoIR | IR filtresiz kamera ile damar görüntüsü almak |
| 1 | 850 nm IR LED modülü veya LED dizisi | Damar yapısını görünür hale getirmek |
| 1 | LED sürücü / dimmer | IR ışık şiddetini kontrollü ayarlamak |
| 1 | Raspberry Pi güç adaptörü | Stabil güç |
| 1 | 64 GB microSD kart | İşletim sistemi, veri ve demo dosyaları |
| 1 | Breadboard, jumper kablo, direnç, MOSFET modül | Prototip bağlantıları |
| 1 | Multimetre | Voltaj ve akım kontrolü |
| 1 | Siyah mat kutu veya 3D baskı gövde | Ortam ışığını kesmek |
| 1 | Parmak yerleştirme aparatı | Aynı hizalamayı tekrar etmek |
| 2 | 850 nm IR-pass / visible-blocking filtre | Kontrast iyileştirme |
| 2 | Kamera tutucu / mini tripod | Kamerayı sabit tutmak |

## Sonra Alınacaklar

| Parça | Ne zaman gerekli? |
|---|---|
| 940 nm IR LED | 850 nm ile görüntü kalitesi karşılaştırması yapılacaksa |
| IR-cut filtresi çıkarılabilir USB kamera | Raspberry Pi kamerası yetersiz kalırsa |
| Monochrome endüstriyel kamera | Daha net damar görüntüsü gerekiyorsa |
| Jetson Orin Nano veya mini PC | Daha ağır yapay zeka modeli cihaz üzerinde çalışacaksa |
| Final 3D baskı gövde | Demo yatırımcı/mentor görüşmesine hazırlanırken |
| Özel PCB | MVP sonrası pilot prototip aşamasında |

## Güvenlik Notu

IR ışık göze doğrudan tutulmamalıdır. İlk testlerde düşük ışık şiddetiyle başlanmalı, LED sürücüyle kontrollü artırılmalı ve mümkünse difüzör kullanılmalıdır.

## Teknik Sprint Planı

### Sprint 1: Yazılım Pipeline

- Açık veya sentetik veriyle görüntü işleme pipeline'ı çalıştırılır.
- ROI kırpma, kontrast artırma, damar cevabı çıkarma ve basit eşleştirme test edilir.
- Bu repodaki scriptler bu sprint için hazırlandı.

### Sprint 2: İlk Donanım Görüntüsü

- Raspberry Pi, NoIR kamera ve 850 nm IR LED kurulur.
- Ortam ışığını kesen basit kutu hazırlanır.
- Farklı ışık şiddetlerinde ilk damar görüntüleri alınır.

### Sprint 3: Kayıt ve Doğrulama

- Her kullanıcıdan 5-10 örnek görüntü alınır.
- Ham görüntüden şablon çıkarılır.
- Yeni görüntüyle kayıtlı şablon karşılaştırılır.
- Demo sonucu `eşleşti / eşleşmedi` olarak gösterilir.

### Sprint 4: Küçük Test

- Önce 5 kişi, sonra 20 kişiyle test yapılır.
- Aynı kişi tekrar tanınıyor mu?
- Farklı kişi reddediliyor mu?
- Işık, açı ve parmak konumu değişince skor nasıl etkileniyor?

### Sprint 5: Demo ve Rapor

- Donanım fotoğrafı
- 1 dakikalık demo videosu
- Test sonuçları
- Teknik riskler
- Sonraki prototip maliyeti

Bu çıktılar BİGG, ARDVENTURE, TEKMER ve teknik mentor görüşmelerinde kullanılabilir.

