# Açık Veri Seti Planı

Donanım gelmeden önce yazılım pipeline'ı açık veya sentetik veriyle geliştirilebilir. Bu repo sentetik veri üretici içerir. Gerçek finger-vein veri seti kullanıldığında görüntüler aşağıdaki klasör yapısına dönüştürülmelidir.

```text
data/raw/open_dataset/
  person_001/
    sample_01.png
    sample_02.png
  person_002/
    sample_01.png
    sample_02.png
```

## Değerlendirme Komutu

```powershell
python scripts\evaluate_folder_dataset.py data\raw\open_dataset --db data\templates --report reports\open_dataset_evaluation.csv
```

## CV Engineer İçin Görev

- Veri setindeki kişi/oturum/parmak klasörlerini incele.
- Görüntüleri bu repo formatına dönüştür.
- İlk 5 kişiyle hızlı test yap.
- Sonra 20 kişiyle skor dağılımı çıkar.
- Başarısız örnekleri `reports/failure_cases/` altında sakla.

