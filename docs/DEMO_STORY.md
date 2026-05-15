# NEXIVO Demo Hikayesi

## Tek Cümle

NEXIVO, NIR tabanlı parmak damar görüntüsünden cihaz üzerinde biyometrik şablon çıkararak gizlilik odaklı kimlik doğrulama yapan bir teknik MVP geliştiriyor.

## Kime Anlatıyoruz?

İlk anlatım kitlesi:

- Teknik mentorlar
- BİGG uygulayıcı kuruluşları
- ARDVENTURE / TEKMER / kuluçka ekipleri
- Potansiyel teknik ekip arkadaşları
- Güvenlik ve erişim kontrolü alanındaki ilk pilot kurumlar

## Demo Akışı

1. Kullanıcı parmağını okuyucuya yerleştirir.
2. NIR ışık damar desenini görünür hale getirir.
3. Kamera görüntüyü alır.
4. Yazılım parmak bölgesini kırpar.
5. Kontrast artırılır ve damar cevabı çıkarılır.
6. Ham görüntüden biyometrik şablon üretilir.
7. Yeni şablon kayıtlı şablonla karşılaştırılır.
8. Sistem yalnızca doğrulama sonucu üretir.

## Demo Ekranında Gösterilecekler

- Orijinal görüntü
- ROI
- Kontrast artırılmış görüntü
- Damar cevabı
- Damar maskesi
- Şablon görselleştirmesi
- Eşleşme skoru
- Sonuç: `eşleşti / eşleşmedi`

## Demo Sonunda Söylenecek Mesaj

Bu MVP ticari cihaz değildir. Amacı, damar biyometrisiyle gizlilik odaklı ve cihaz üstünde çalışabilecek bir kimlik doğrulama altyapısının teknik temelini göstermektir. Sonraki aşamada gerçek NIR donanımı, küçük kullanıcı testi, kalite metriği ve liveness risk analizi eklenecektir.

