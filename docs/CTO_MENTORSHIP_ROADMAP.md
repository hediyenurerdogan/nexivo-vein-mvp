# CTO Mentorluk Yol Haritası

## Amaç

AI CTO, NEXIVO'nun teknik ekibini sadece görev bazlı değil, karar kalitesi ve ürün yönü açısından da yönlendirecek.

## İlk 4 Teknik Mentorluk Alanı

### 1. Donanım Mimari İncelemesi

CTO, Raspberry Pi + NoIR kamera + 850 nm IR LED prototipini aşağıdaki açılardan denetler:

- Görüntü kalitesi
- Tekrarlanabilir parmak hizalama
- IR güvenliği
- Ortam ışığı izolasyonu
- Üretilebilir gövde fikri

### 2. Biyometrik Şablon ve Eşik Mimarisi

CTO, `analyze_scores.py` çıktılarının ürün iddiasına dönüşmesini engeller; bunları yalnızca teknik sanity check olarak konumlandırır.

İlk hedef:

- Açık veri: geçti
- Donanım verisi: sıradaki ana kanıt
- Eşik: donanım görüntülerine göre yeniden kalibre edilecek

### 3. Privacy-First Edge Mimari

CTO'nun teknik beklentisi:

- Ham görüntü geçici tutulur.
- Kalıcı katmanda şablon veya kriptografik temsil konuşulur.
- Dış sisteme mümkünse yalnızca doğrulama sonucu gider.
- API/SDK tasarımı baştan düşünülür.

### 4. Rekabet ve Ürün Konumlandırma

CTO, NEXIVO'yu Proline gibi uçtan uca büyük sistem entegratörü olmaktan korur. İlk niş:

- Laboratuvar erişimi
- Veri merkezi erişimi
- Savunma alt yüklenicisi erişim noktaları
- Kurum içi yüksek güvenlikli oda/cihaz erişimi

## CTO Haftalık Review Formatı

Her review şu başlıklarla yapılır:

- Bu hafta tamamlanan teknik kanıt
- Yeni açılan teknik risk
- Proline'a göre ayrışmayı güçlendiren karar
- Gizlilik/edge mimarisine etkisi
- Bir sonraki hafta yapılacak tek kritik iş

