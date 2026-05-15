# NEXIVO Vein MVP

Bu repo, NEXIVO'nun ilk teknik MVP'si için NIR tabanlı parmak damar biyometrisi pipeline'ını başlatır.

Amaç ticari ürün çıkarmak değil; şu teknik akışı kanıtlamaktır:

1. Damar görüntüsünü oku.
2. Parmak bölgesini kırp.
3. Kontrastı artır.
4. Damar çizgilerini çıkar.
5. Ham görüntü yerine sabit boyutlu biyometrik şablon üret.
6. Basit eşleştirme ile `eşleşti / eşleşmedi` sonucu ver.

## Kurulum

Windows PowerShell:

```powershell
cd C:\Users\90541\Documents\Playground\nexivo-vein-mvp
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

## Hızlı Demo

Gerçek veri olmadan sentetik parmak damar görüntüleri üret:

```powershell
python scripts\generate_synthetic_dataset.py --output data\raw\synthetic --people 5 --samples 6
```

Bir görüntüyü işle ve ara çıktıları gör:

```powershell
python scripts\process_image.py data\raw\synthetic\person_001\sample_01.png --output data\processed\sample_01
```

Bir kişiyi kaydet:

```powershell
python scripts\enroll.py --person-id person_001 --images data\raw\synthetic\person_001 --db data\templates
```

Yeni görüntüyü doğrula:

```powershell
python scripts\verify.py data\raw\synthetic\person_001\sample_06.png --db data\templates
```

Küçük veri setinde eşleştirme başarısını ölç:

```powershell
python scripts\evaluate_folder_dataset.py data\raw\synthetic --db data\templates
```

## Gerçek Veri Klasör Yapısı

Gerçek görüntüler geldiğinde her kişiyi ayrı klasöre koy:

```text
data/raw/real/
  person_001/
    sample_01.png
    sample_02.png
  person_002/
    sample_01.png
    sample_02.png
```

Sonra:

```powershell
python scripts\evaluate_folder_dataset.py data\raw\real --db data\templates
```

## Teknik Not

Bu pipeline bilinçli olarak basit tutuldu. İlk hedef; mühendis ekibin görüntü kalitesi, ROI kararlılığı ve basit eşleştirme skorlarını görmesidir.

Ticari ürüne yaklaşırken eklenmesi gerekenler:

- Daha güçlü ROI hizalama
- Tekrarlı kayıt kalitesi kontrolü
- Liveness / PAD testleri
- Şablon şifreleme
- Cihaz üzerinde çalışan servis
- API/SDK entegrasyon katmanı
- FAR/FRR/EER metrikleriyle ciddi doğrulama

## Ekip ve Takip

Donanım gelmeden önceki görev dağılımı ve sprint planı:

- [Teknik ekip rolleri ve görevler](docs/TEAM_ROLES_AND_TASKS.md)
- [Donanım öncesi sprint planı](docs/PRE_HARDWARE_SPRINT.md)
- [KVKK ve test etik notu](docs/KVKK_AND_TEST_ETHICS.md)
- [Gönüllü test onam metni](docs/VOLUNTEER_TEST_CONSENT.md)
- [Demo hikayesi](docs/DEMO_STORY.md)
- [Açık veri seti planı](docs/OPEN_DATASET_PLAN.md)
- [Donanım ve yol haritası](docs/MVP_DONANIM_VE_YOL_HARITASI.md)
- [Donanım satın alma araştırması](docs/HARDWARE_SHOPPING_LIST.md)
- [GitHub takip rehberi](docs/GITHUB_TRACKING.md)

Donanım öncesi hızlı kontrol:

```powershell
python scripts\smoke_test.py
```
