# Açık Veri Seti Sonuçları

## Veri Seti

Kaynak: MMCBNU_6000  
Kaynak linki: https://huggingface.co/datasets/www1213/MMCBNU_6000

Dataset kartına göre MMCBNU_6000, 100 gönüllüden alınmış 6.000 finger-vein görüntüsü içerir. Bu repo içinde ham veri commit edilmez. İndirilen zip ve çıkarılan subset `.gitignore` altındadır.

## Kullanılan Subset

Donanım öncesi sanity check için küçük bir subset hazırlandı:

- 8 kişi
- Her kişiden 1 parmak: `L_Fore`
- Kişi başına 8 görüntü
- Toplam 64 görüntü

Hazırlama komutu:

```powershell
python scripts\prepare_mmcBnu_subset.py data\raw\open_downloads\MMCBNU_6000.zip --output data\raw\open_dataset --people 8 --samples 8
```

## Skor Analizi

Komut:

```powershell
python scripts\analyze_scores.py data\raw\open_dataset --scores-csv reports\open_dataset_score_distribution.csv --report-md reports\open_dataset_score_distribution.md --threshold-step 0.01
```

Sonuç:

- Görüntü: 64
- Aynı kişi çiftleri: 224
- Farklı kişi çiftleri: 1792
- Aynı kişi skor medyanı: 0.92865
- Aynı kişi skor ortalaması: 0.91699
- Farklı kişi skor medyanı: 0.78282
- Farklı kişi skor ortalaması: 0.77488
- En iyi threshold: 0.85
- 0.85 threshold ile FAR: 0.0452 (81/1792)
- 0.85 threshold ile FRR: 0.1027 (23/224)
- Default 0.62 threshold ile FAR: 0.9994 (1791/1792)

## Folder-Level Doğrulama

Komut:

```powershell
python scripts\evaluate_folder_dataset.py data\raw\open_dataset --db data\templates_open_dataset --report reports\open_dataset_evaluation_t085.csv --threshold 0.85
```

Sonuç:

- Probe sayısı: 8
- Doğru kabul edilen kimlik: 8/8
- Tüm probe görüntüler doğru kişiye eşleşti.

## Yorum

Açık veri sonucu, yazılım pipeline'ının sentetik olmayan finger-vein görüntüleri üzerinde de çalıştığını gösterir. Bu sonuç ürün doğrulaması değildir; NEXIVO'nun kendi NIR donanımıyla alınacak görüntülerde eşik ve kalite metrikleri yeniden kalibre edilmelidir.

