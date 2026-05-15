# NEXIVO Teknik MVP Ekibi

Bu doküman, donanım gelmeden önce teknik MVP ekibinin kim hangi alandan sorumlu olacak sorusunu netleştirir. İsimler daha sonra gerçek ekip üyeleriyle değiştirilebilir.

## Ekip Lideri / Product & Validation Lead

**Sorumlu:** Hediyenur Erdoğan + Codex AI Lead

**Odak:** Neyi kanıtlıyoruz, kime anlatacağız, test etik/KVKK notları, demo hikayesi, ekip koordinasyonu.

**Başarı tanımı:** Teknik ekip bir demo üretirken NEXIVO'nun amacı, kanıtlanacak hipotezler, test sınırları ve anlatım dili dağılmadan ilerler.

**Donanım gelmeden yapılacaklar:**

- [x] MVP'nin kanıtlayacağı ana teknik hipotezi yaz.
- [x] Ekip rollerini ve görev dağılımını belirle.
- [x] KVKK/test etik notunu hazırla.
- [x] Demo hikayesini hazırla.
- [ ] İlk 5 test katılımcısı için gönüllü test onam metni taslağını hazırla.
- [ ] Mentor görüşmesi için 1 sayfalık teknik özet çıkar.
- [ ] Haftalık takip ritmini belirle.

## AI CTO & Deep-Tech Mentor

**Kısa title:** AI CTO

**Atanan AI CTO:** Hypatia / AI CTO & Deep-Tech Mentor

**Odak:** Donanım mimarisi, biyometrik ürün stratejisi, Proline rekabet analizi, privacy-first edge mimari, teknik mentorluk.

**Başarı tanımı:** NEXIVO'nun Proline gibi büyük bir sistem entegratörünün küçük kopyası olmasını engeller; ekibi dar, ölçülebilir ve ayrışan bir teknik MVP yönüne iter.

**Sürekli yapılacaklar:**

- [ ] Donanım MVP kararlarını gözden geçir.
- [ ] Proline ve benzeri rakiplerden ayrışma stratejisini güncel tut.
- [ ] Biyometrik şablon ve edge doğrulama mimarisini denetle.
- [ ] Pilot/pitch teknik anlatısını güçlendir.
- [ ] AI mühendislerin çıktılarını haftalık review et.

## Computer Vision Engineer

**Kısa title:** CV Engineer

**Atanan AI mühendis:** Elian Kovacs / NEXIVO-CV-01 / AI Computer Vision Engineer

**Odak:** OpenCV, ROI kırpma, kontrast artırma, damar çizgisi çıkarımı.

**Başarı tanımı:** Donanım gelmeden açık/sentetik görüntülerde tekrarlanabilir bir görüntü işleme pipeline'ı çalışır.

**Donanım gelmeden yapılacaklar:**

- [x] OpenCV pipeline'ını çalıştır.
- [x] Sentetik görüntüde ROI kırpmayı doğrula.
- [x] Kontrast artırma adımını çalıştır.
- [x] Damar cevabı ve damar maskesi çıktısı üret.
- [ ] Açık finger-vein veri seti indirilecekse klasör formatını hazırla.
- [ ] Gerçek görüntü geldiğinde başarısız ROI örneklerini listele.
- [ ] Işık/açı değişiminde kalite skoru öner.

## Hardware Prototyping Engineer

**Kısa title:** Hardware Engineer

**Atanan AI mühendis:** Mira Sato / NEXIVO-HW-01 / AI Hardware Prototyping Engineer

**Odak:** Kamera, IR LED, ışık kontrolü, kutu/gövde, parmak konumlandırma.

**Başarı tanımı:** Donanım gelince aynı gün ilk damar görüntüsü alınabilecek kadar net bağlantı ve kurulum planı hazırdır.

**Donanım gelmeden yapılacaklar:**

- [x] İlk satın alma listesini çıkar.
- [ ] 850 nm IR LED seçeneklerini karşılaştır.
- [ ] Raspberry Pi Camera Module 3 NoIR uyumluluğunu kontrol et.
- [ ] Parmak yerleştirme aparatı için basit çizim hazırla.
- [ ] Ortam ışığını kesecek kutu/gövde planını hazırla.
- [ ] IR ışık güvenliği için düşük güçten başlama prosedürü yaz.
- [ ] İlk testte kamera-parmak-LED mesafe aralıklarını belirle.

## Matching & Test Engineer

**Kısa title:** Biometrics Test Engineer

**Atanan AI mühendis:** Luca Weiss / NEXIVO-BIO-01 / AI Biometrics Test Engineer

**Odak:** Şablon üretimi, skor, eşik, doğrulama, test raporu.

**Başarı tanımı:** Aynı kişi/farklı kişi ayrımını sayısal skorlarla raporlayan ilk test sistemi hazırdır.

**Donanım gelmeden yapılacaklar:**

- [x] Enroll komutunu çalıştır.
- [x] Verify komutunu çalıştır.
- [x] Sentetik veri setinde küçük değerlendirme raporu üret.
- [ ] Eşik değerini farklı test setlerinde karşılaştır.
- [ ] Aynı kişi/farklı kişi skor dağılımı raporu hazırla.
- [ ] FAR/FRR/EER için sonraki metrik planını yaz.
- [ ] Gerçek testte her katılımcıdan kaç görüntü alınacağını netleştir.

## Takip Yöntemi

GitHub Issues, bu dokümandaki görevlerin canlı takip alanıdır. Her rol için ayrı issue açılır. Bir görev tamamlandığında ilgili issue içindeki checkbox işaretlenir.

Repo: https://github.com/hediyenurerdogan/nexivo-vein-mvp
