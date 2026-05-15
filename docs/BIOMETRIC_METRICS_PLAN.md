# Biyometrik Metrik Planı

## Amaç

NEXIVO MVP testlerinde skorların ne anlama geldiğini ölçülebilir hale getirmek.

## Temel Kavramlar

- **Genuine pair:** Aynı kişiye ait iki görüntü çifti.
- **Impostor pair:** Farklı kişilere ait iki görüntü çifti.
- **Threshold:** Skor bu değerin üstündeyse eşleşme kabul edilir.
- **FAR:** Farklı kişiyi yanlış kabul etme oranı.
- **FRR:** Aynı kişiyi yanlış reddetme oranı.
- **EER:** FAR ve FRR'nin birbirine yaklaştığı hata seviyesi.

## Donanım Öncesi Bulgular

- Sentetik analizde en iyi eşik yaklaşık 0.84 çıktı.
- MMCBNU_6000 küçük subset analizinde en iyi eşik yaklaşık 0.85 çıktı.
- Default 0.62 eşiği açık veri pairwise analizinde fazla gevşek kaldı.

## Donanım Geldiğinde Yapılacaklar

1. 5 kişi x kişi başı en az 8 görüntü topla.
2. `analyze_scores.py` ile same/different dağılımını çıkar.
3. Best threshold, FAR ve FRR değerlerini raporla.
4. `evaluate_folder_dataset.py` ile folder-level doğru kabul oranını ölç.
5. Eşik değerini donanım görüntülerine göre yeniden kalibre et.

