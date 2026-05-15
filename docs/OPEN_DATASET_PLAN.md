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

## Kısa Karar

Önerilen ilk gerçek açık veri denemesi: **MMCBNU_6000 küçük subset**.

Neden:

- Hugging Face üzerinde erişilebilir; tam veri 677 MB görünse de subset script'i ilk N kişi/finger örneğini parça parça indirir.
- Görüntüler finger-vein pipeline için uygun çözünürlükte: 480 x 640 BMP kaynak, Hugging Face viewer'da JPG olarak sunuluyor.
- Her gönüllü için 6 parmak ve parmak başına 10 tekrar var; bu repo için `person_001_L_Fore/sample_01.png` gibi finger-instance bazlı kimlik klasörleri üretilebilir.

UTFVP ve SDUMLA-HMT araştırma açısından iyi veri setleri ama ilk sprint için erişim sürtünmeleri var:

- **UTFVP**: University of Twente sayfası veri setini araştırma gruplarına lisans anlaşması ve onay sonrası dağıttığını belirtiyor. Küçük ve kaliteli olduğu için ikinci aday; doğrudan otomatik indirme yok.
- **SDUMLA-HMT**: Resmi sayfa araştırma ve ticari olmayan kullanım şartı veriyor, veriyi almak için Prof. Lu Yang'a e-posta gönderilmesini istiyor. Doğrudan otomatik indirme yok.

Kaynaklar:

- MMCBNU_6000 Hugging Face: https://huggingface.co/datasets/luyu0311/MMCBNU_6000
- UTFVP resmi erişim sayfası: https://www.utwente.nl/en/eemcs/dmb/downloads/utfvp/
- UTFVP metadata: https://research.utwente.nl/en/datasets/university-of-twente-finger-vascular-pattern-utfvp/
- SDUMLA-HMT resmi sayfa: https://time.sdu.edu.cn/kycg/gksjk.htm

## MMCBNU_6000 Hızlı Subset

Repo formatına dönüştürülmüş 5 kişi x 6 parmak x 10 tekrar = 300 görüntü üretir. Script Hugging Face dataset-server satırlarını indirir ve `row_idx` sırasından subject/finger/sample klasörü oluşturur. Bu sıra Hugging Face önizlemesindeki blok düzeniyle uyumludur; gerçek validasyon için tam arşiv/metadata ile tekrar kontrol edilmelidir.

```powershell
cd C:\Users\90541\Downloads\nexivo-vein-mvp
.\.venv\Scripts\python.exe scripts\download_mmcbnu_subset.py --people 5 --output data\raw\open_dataset_mmcbnu_5p
```

Sonra değerlendirme:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_folder_dataset.py data\raw\open_dataset_mmcbnu_5p --db data\templates --report reports\mmcbnu_5p_evaluation.csv
```

Skor dağılımı için:

```powershell
.\.venv\Scripts\python.exe scripts\analyze_scores.py data\raw\open_dataset_mmcbnu_5p --report-md reports\mmcbnu_5p_scores.md --scores-csv reports\mmcbnu_5p_scores.csv
```

## Alternatif Veri Setleri

| Veri seti | Durum | MVP için karar |
| --- | --- | --- |
| MMCBNU_6000 | Hugging Face üzerinde erişilebilir, lisans alanı AFL-3.0 görünüyor. | İlk küçük gerçek-data denemesi için seç. |
| UTFVP | Resmi sayfada lisans anlaşması ve araştırma grubu onayı gerekiyor. | Lisans formu gönderilirse ikinci turda kullan. |
| SDUMLA-HMT | Resmi sayfa e-posta ile talep istiyor; ticari olmayan araştırma şartı var. | İzin gelene kadar beklet. |

## CV Engineer İçin Görev

- MMCBNU subset ile ilk 5 kişiyi indir.
- `reports/mmcbnu_5p_evaluation.csv` ve `reports/mmcbnu_5p_scores.md` üret.
- Başarısız ROI örneklerini `reports/failure_cases/` altında listele.
- UTFVP için lisans formu ve SDUMLA-HMT için izin e-postası gerekliliğini sprint takibine not düş.

## Issue #2 İçin Yorum Taslağı

~~~markdown
CV açık veri araştırması tamamlandı.

En hızlı uygulanabilir gerçek veri seçeneği MMCBNU_6000 küçük subset. Hugging Face üzerinde erişilebilir; 5 kişi x 6 parmak x 10 tekrar için repo formatına dönüştüren script eklendi:

```powershell
.\.venv\Scripts\python.exe scripts\download_mmcbnu_subset.py --people 5 --output data\raw\open_dataset_mmcbnu_5p
.\.venv\Scripts\python.exe scripts\evaluate_folder_dataset.py data\raw\open_dataset_mmcbnu_5p --db data\templates --report reports\mmcbnu_5p_evaluation.csv
```

Notlar:
- UTFVP kaliteli ve küçük ama resmi sayfa lisans anlaşması + araştırma grubu onayı istiyor.
- SDUMLA-HMT resmi sayfa e-posta ile talep ve ticari olmayan araştırma kullanım şartı belirtiyor.
- MMCBNU subset, donanım gelmeden ROI/kontrast/damar maskesi pipeline'ını gerçek görüntüyle sanity-check etmek için seçildi.
~~~

## Issue #5 İçin Yorum Taslağı

~~~markdown
Açık finger-vein veri seti kararı:

- İlk sprint gerçek-data sanity check: MMCBNU_6000 küçük subset.
- Komutlar ve gerekçe `docs/OPEN_DATASET_PLAN.md` içine eklendi.
- UTFVP ve SDUMLA-HMT otomatik indirilebilir değil; lisans/onay veya e-posta talebi gerekiyor.

Sonraki adım: MMCBNU 5 kişilik subset ile `reports/mmcbnu_5p_evaluation.csv` ve `reports/mmcbnu_5p_scores.md` üretilecek, sonuçlar Biometrics Test Engineer issue'suna bağlanacak.
~~~

## Kabul Kriterleri

- En az 8 kişi, kişi başına en az 4 görüntü ile açık veri smoke analizi geçmeli.
- Same/different pair sayıları 0'dan büyük olmalı.
- Rapor best threshold, FAR/FRR ve default `0.62` sonucunu içermeli.
- Seçilen threshold ile `evaluate_folder_dataset.py` tekrar çalıştırılıp doğru kabul oranı issue'ya eklenmeli.
- Sentetik sonuçlar ürün doğrulama iddiası olarak kullanılmamalı.
