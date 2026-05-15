# Donanım Kurulum Planı

## İlk Kurulum

Başlangıç düzeni:

- NoIR kamera parmağın üstünden veya yandan sabitlenir.
- 850 nm IR LED düşük güçle başlatılır.
- Ortam ışığını kesmek için siyah mat kutu kullanılır.
- Parmak aynı yükseklik ve açıyla yerleştirilir.

## İlk Mesafe Aralıkları

- Kamera-parmak mesafesi: 6-12 cm aralığında denenir.
- LED-parmak mesafesi: 2-6 cm aralığında denenir.
- Kamera açısı: parmağa dik veya hafif eğimli.
- LED açısı: doğrudan göze kaçmayacak şekilde parmak dokusuna yönlendirilir.

## IR Güvenlik Prosedürü

- IR LED doğrudan göze tutulmaz.
- Düşük akım/duty cycle ile başlanır.
- LED GPIO'dan doğrudan sürülmez.
- PWM MOSFET/dimmer ve ayrı besleme kullanılır.
- Her test öncesi bağlantı multimetreyle kontrol edilir.

## Parmak Aparatı

İlk prototip için V kanallı basit bir parmak yatağı yeterlidir. Temas yüzeyi kolay temizlenebilir olmalı, parmak aynı pozisyonda durmalı ve kameranın görüş alanını kapatmamalıdır.

