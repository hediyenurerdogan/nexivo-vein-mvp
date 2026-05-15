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

Skor dağılımını ve eşik adayını çıkar:

```powershell
python scripts\analyze_scores.py data\raw\synthetic_scores --scores-csv reports\score_distribution_synthetic_scores.csv --report-md reports\score_distribution_synthetic_scores.md --threshold-step 0.01
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

Açık veya gerçek veri subset'i hazırlandığında skor/eşik analizi:

```powershell
python scripts\analyze_scores.py data\raw\open_dataset --scores-csv reports\open_dataset_score_distribution.csv --report-md reports\open_dataset_score_distribution.md --threshold-step 0.01
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
- [Açık veri seti sonuçları](docs/OPEN_DATASET_RESULTS.md)
- [Donanım ve yol haritası](docs/MVP_DONANIM_VE_YOL_HARITASI.md)
- [Donanım satın alma araştırması](docs/HARDWARE_SHOPPING_LIST.md)
- [Teknik MVP özeti](docs/TECHNICAL_MVP_ONE_PAGER.md)
- [İlk gerçek test protokolü](docs/FIRST_REAL_TEST_PROTOCOL.md)
- [Biyometrik metrik planı](docs/BIOMETRIC_METRICS_PLAN.md)
- [Görüntü kalite skoru planı](docs/IMAGE_QUALITY_SCORE_PLAN.md)
- [Donanım kurulum planı](docs/HARDWARE_SETUP_PLAN.md)
- [Haftalık takip ritmi](docs/WEEKLY_TEAM_RHYTHM.md)
- [AI ekip değerlendirme kaydı](docs/TEAM_RETROSPECTIVE.md)
- [AI ekip profilleri](docs/AI_TEAM_PROFILES.md)
- [AI CTO charter](docs/AI_CTO_CHARTER.md)
- [CTO ekip genişleme review](docs/CTO_TEAM_EXPANSION_REVIEW.md)
- [LinkedIn AI team launch](docs/LINKEDIN_AI_TEAM_LAUNCH.md)
- [Proline rekabet analizi](docs/PROLINE_COMPETITIVE_ANALYSIS.md)
- [CTO mentorluk yol haritası](docs/CTO_MENTORSHIP_ROADMAP.md)
- [GitHub takip rehberi](docs/GITHUB_TRACKING.md)

Donanım öncesi hızlı kontrol:

```powershell
python scripts\smoke_test.py
```
