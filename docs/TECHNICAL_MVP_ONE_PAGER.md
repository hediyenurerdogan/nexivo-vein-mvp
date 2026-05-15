# NEXIVO Teknik MVP Özeti

## Amaç

NEXIVO'nun ilk teknik MVP'si, NIR tabanlı parmak damar görüntüsünden cihaz üzerinde işlenebilir biyometrik şablon çıkarılabileceğini ve temel kimlik doğrulama yapılabileceğini göstermeyi hedefler.

## Ne Kanıtlanacak?

- Damar görüntüsü yazılım tarafından okunabilir.
- Parmak bölgesi kırpılabilir.
- Kontrast artırma ve damar cevabı çıkarma adımları çalışır.
- Ham görüntüden karşılaştırılabilir biyometrik şablon üretilebilir.
- Aynı kişi/farklı kişi ayrımı skorlanabilir.
- İlk demo `eşleşti / eşleşmedi` sonucu verebilir.

## Teknik Akış

1. Görüntü alınır.
2. ROI kırpılır.
3. Kontrast artırılır.
4. Damar cevabı ve damar maskesi çıkarılır.
5. Şablon üretilir.
6. Şablonlar karşılaştırılır.
7. Skor ve karar üretilir.

## Donanım Öncesi Durum

- Sentetik veri pipeline testi geçti.
- MMCBNU_6000 açık finger-vein subset testi geçti.
- Eşik analizi için `scripts/analyze_scores.py` eklendi.
- Donanım alışveriş listesi ve test protokolü hazırlandı.
- KVKK/test etik ve gönüllü onam taslağı hazırlandı.

## Donanım Geldiğinde İlk Hedef

NEXIVO'nun kendi NIR prototipiyle 5 kişiden alınan ilk görüntülerde aynı kişi/farklı kişi skor ayrımını göstermek.

