# NEXIVO Hardware Shopping List

Araştırma tarihi: 2026-05-15  
Rol: AI Hardware Prototyping Engineer  
Kapsam: GitHub issue #3 için Türkiye'den alınabilecek veya kolay tedarik edilebilecek MVP donanım kalemleri.

Fiyatlar hızlı değişir; satın alma öncesi stok, KDV, kargo ve kur etkisi tekrar kontrol edilmelidir. Bu liste ilk prototip için araştırma başlangıcıdır, kesin sipariş listesi değildir.

## Önerilen MVP Sepeti

| Öncelik | Kategori | Önerilen ürün / kaynak | Güncel gözlem | Yaklaşık fiyat aralığı | Not |
|---|---|---|---|---:|---|
| P0 | Raspberry Pi 5 veya 4 | [Raspberry Pi 5 8GB - Direnc.net](https://www.direnc.net/raspberry-pi-5-8gb), [Raspberry Pi 4 4GB - SAMM Market](https://market.samm.com/raspberry-pi-4-4gb), [Raspberry Pi 4 4GB - Robotistan](https://www.robotistan.com/raspberry-pi-4-4gb) | Direnc.net Pi 5 8GB sayfası 10.622,61 TL KDV dahil gösteriyor fakat stok yok. SAMM Pi 4 4GB sayfası stok 27 ve 6.287,47 TL KDV dahil gösteriyor. | 6.300-10.700 TL | MVP için Pi 4 4GB yeterli olabilir; Pi 5 tercih edilirse aktif soğutma ve 27W güç adaptörü eklenmeli. |
| P0 | Raspberry Pi Camera Module 3 NoIR | [Camera Module 3 NoIR Wide - Robotistan](https://www.robotistan.com/raspberry-pi-kamera-modul-3-sensor-noir-wide-af), [Camera Module 3 NoIR - SAMM Market](https://market.samm.com/raspberry-pi-kamera-3-noir), [resmi Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/) | Resmi sayfa Camera Module 3 ailesinin 12MP IMX708, autofocus, NoIR varyantlarında IR-cut filtresiz olduğunu belirtir. Robotistan sayfası NoIR Wide AF için 120 derece FoV ve IR-cut filtresiz kullanım bilgisini verir. | 1.500-3.000 TL | Pi 5 kullanılırsa 22-pin to 15-pin kamera FPC kablosu gerekebilir; [Direnc.net FPC kablo](https://www.direnc.net/raspberry-pi-5-kamera-fpc-kablosu-300mm) 156,37 TL KDV dahil. |
| P0 | 850nm IR LED / modül | [Farnell Türkiye 9-chip 850nm IR LED modül](https://tr.farnell.com/intelligent-led-solutions/ilr-in09-85nl-sc201-wir200/ir-led-module-9-chip-850nm-square/dp/3764870), [Mouser Türkiye 850nm IR LED filtreli liste](https://www.mouser.com.tr/c/?product+type=IR+Emitters+%28IR+LEDs%29&wavelength=850+nm) | Farnell'de 9-chip 850nm modül 26,21 EUR + KDV, stokta görünüyor. Mouser'da tekil 850nm IR LED seçenekleri 0,568 EUR seviyesinden başlıyor. | 25-1.500 TL | İlk deneme için tekil LED dizisi ucuzdur; daha kontrollü aydınlatma için PCB üstü 850nm modül daha iyi. Göz güvenliği için düşük akımla başlanmalı. |
| P0 | LED sürücü / dimmer | [1.8V-12V 2A dimmer - Robotistan](https://www.robotistan.com/18v-12v-2a-dimmer-hiz-kontrol-cihazi), [15A 400W PWM MOSFET modül - Robolink Market](https://www.robolinkmarket.com/15a-400w-pwm-kontrollu-mosfet-anahtarlama-modulu), [LR7843 MOSFET Driver Board - Robotistan](https://www.robotistan.com/lr7843-mosfet-kontrol-modulu) | Robotistan dimmer 106,42 TL KDV dahil; Robolink PWM MOSFET modül 23,40 TL KDV dahil; Robotistan LR7843 52,68 TL KDV dahil. | 25-150 TL | Raspberry Pi GPIO doğrudan LED sürmemeli. PWM kontrollü MOSFET + ayrı LED beslemesi önerilir. |
| P0 | Güç adaptörü | [Raspberry Pi 4 5V 2.8A adaptör - Direnc.net](https://www.direnc.net/raspberry-pi-4-beyaz-guc-adaptoru-5v-2), [resmi Raspberry Pi 27W USB-C PSU](https://www.raspberrypi.com/products/27w-power-supply/?variant=27w-power-supply-eu-white) | Direnc.net Pi 4 adaptörü 242,65 TL KDV dahil. Resmi Raspberry Pi 27W USB-C PSU, Pi 5 ve yüksek güçlü USB çevre birimleri için öneriliyor. | 250-800 TL | Pi 5 için 5.1V/5A 27W resmi veya eşdeğer kaliteli adaptör alınmalı; Pi 4 için 5V/3A USB-C yeterli. |
| P0 | 64GB microSD | [SanDisk Ultra 64GB - Direnc.net](https://www.direnc.net/sandisk-ultra-64gb-100mb/s-microsdxc-uhs-i-hafiza-karti), [Samsung EVO Plus 64GB - Direnc.net](https://www.direnc.net/samsung-evo-plus-64gb-95-mb/sepet) | SanDisk Ultra 64GB 1.213,24 TL KDV dahil; Samsung EVO Plus 64GB sayfası 683,64 TL + KDV gösteriyor. | 700-1.250 TL | Raspberry Pi OS ve görüntü kayıtları için 64GB başlangıçta yeterli. A1/A2 sınıfı kart tercih edilebilir. |
| P0 | Breadboard / jumper / direnç / MOSFET | [Plaket ve Breadboard - Direnc.net](https://www.direnc.net/plaket-ve-breadboard), [140 parça jumper set - Direnc.net](https://www.direnc.net/140-parca-jumper-set-en), [Raspberry Pi Breadboard ve T-Cobbler - Direnc.net](https://www.direnc.net/raspberry-pi-breadboard-ve-t-cobbler), [IRFB4110 MOSFET - Robotistan](https://www.robotistan.com/irfb4110-180a-100v-mosfet-to220) | Direnc.net 830 nokta breadboard 45,83 TL, 140 parça jumper 75,49 TL, T-Cobbler + breadboard 87,32 TL KDV dahil. Robotistan IRFB4110 MOSFET 46,09 TL KDV dahil. | 200-700 TL | Direnç seti ayrıca eklenmeli; LED akımı için hesaplanmış seri direnç veya sabit akım sürücü kullanılmalı. |
| P0 | Multimetre | [Dijital multimetre listesi - Direnc.net](https://www.direnc.net/uni-t-ut39c), [Ölçüm ve test aletleri - Direnc.net](https://www.direnc.net/olcum-ve-test-aletleri) | Direnc.net listesinde ANENG DT830D 159,62-177,94 TL, ANENG DM850 266,03 TL, Uni-T UT33D+ 609,83 TL seviyesinde görünüyor. | 180-650 TL | En az DC voltaj, direnç, süreklilik ve akım ölçümü olan bir model yeterli; daha güvenilir prob seti ayrıca alınabilir. |
| P1 | Siyah kutu / 3D baskı gövde | [HH009 siyah plastik kutu - Direnc.net](https://www.direnc.net/hh009-plastik-kutu-35x70x23mm-siyah), [HH035 siyah plastik kutu - Direnc.net](https://www.direnc.net/hh035-plastic-box-black-143-x-76-x-32mm), [MP-165 siyah metal kutu - Direnc.net](https://www.direnc.net/mp-165-metal-kutu-siyah-229-x-127-x-90mm) | HH009 75,49 TL; HH035 170,58 TL; MP-165 559,97 TL KDV dahil. | 75-600 TL | İlk prototipte mat siyah plastik kutu + iç yüzeye siyah keçe/foam yeterli. 3D baskı gövde Sprint 2 sonrası ölçüler netleşince tasarlanmalı. |
| P1 | Parmak aparatı | Hazır parça yok; 3D baskı veya lazer kesim akrilik önerilir. Alternatif: siyah kutu içine köpük/V kanal parmak yatağı. | Yerel 3D baskı servisleri veya makerspace ile üretilebilir. | 100-500 TL | Amaç parmağı her çekimde aynı yükseklik ve açıyla tutmak. Temas yüzeyi kolay dezenfekte edilebilir olmalı. |
| P1 | Kamera tutucu | [Raspberry Pi kamera tutucu - Elektrovadi](https://www.elektrovadi.com/urun/raspberry-pi-kamera-kutusu-kamera-tutucu), [Pimoroni Raspberry Pi Camera Mount - Farnell Türkiye](https://tr.farnell.com/pimoroni/rpicameramount/raspberry-pi-camera-mount/dp/3446737) | Elektrovadi kamera tutucu 54,64 TL; Farnell Pimoroni mount 4,68 EUR + KDV, sipariş edilebilir. | 55-350 TL | Kamera açısı sabitlenmeli; NoIR kamera kablosu ve Pi 5 kamera adaptör kablosu mekanik gerilim altında kalmamalı. |
| P2 | IR-pass / visible-blocking filtre | [ZWO IR-pass 850nm - ArcticSpaces](https://www.arcticspaces.com/product/ir-pass-filter-850nm/), [ZWO 850nm IR-pass - Astronomy Store](https://astronomy.store/products/zw850ir125), [ZWO 850nm IR-pass - Budapest Telescope Centre](https://tavcso.hu/en/product/IRpass850), [Commonlands 850nm dual-bandpass](https://commonlands.com/products/dual-bandpass-filter-850nm-cdb850) | Avrupa kaynaklarında ZWO 850nm IR-pass filtre 23,11-30 EUR bandında. Commonlands küçük optik parçalar 19 USD başlangıç fiyatı gösteriyor. | 900-2.500 TL | Türkiye'de kolay bulunması zor olabilir. İlk sprintte filtre olmadan görüntü alınır; görünür ışık sızıntısı kontrastı bozarsa 850nm longpass/IR-pass filtre denenir. |

## İlk Satın Alma Önerisi

P0 sepeti hızlı MVP için yeterli görünür:

1. Raspberry Pi 4 4GB veya Pi 5 8GB
2. Raspberry Pi Camera Module 3 NoIR veya NoIR Wide
3. 850nm IR LED/modül
4. PWM MOSFET modül veya 2A dimmer
5. Uygun güç adaptörü
6. 64GB microSD
7. Breadboard, jumper, direnç seti, MOSFET
8. Basit multimetre
9. Siyah plastik kutu

Bu sepet için kaba maliyet:

- Raspberry Pi 4 tabanlı düşük bütçe: yaklaşık 9.500-14.000 TL
- Raspberry Pi 5 tabanlı daha güçlü sepet: yaklaşık 14.000-20.000 TL

Aralıklar kamera, IR LED modül gücü, filtre ve mekanik gövde kararına göre değişir.

## Teknik Notlar

- Raspberry Pi Camera Module 3 NoIR, resmi dokümana göre IR-cut filtresi olmayan varyanttır; 850nm aydınlatma ile damar görüntüleme denemesi için doğru başlangıçtır.
- 850nm LED, kamera sensöründe genellikle daha görünürdür; 940nm daha az görünür kızarıklık yapabilir ama sensör hassasiyeti ve gereken güç değişebilir.
- IR LED doğrudan Raspberry Pi GPIO'dan sürülmemeli; MOSFET/dimmer ve ayrı besleme kullanılmalıdır.
- Parlak IR ışık göze doğrudan tutulmamalı. İlk testler düşük duty cycle / düşük akım ile yapılmalı, LED parmak arkasına veya yanına sabitlenmeli, ışık kaçakları siyah kutu ile kesilmelidir.
- Pi 5 kullanılırsa Camera Module 3 için uygun kamera FPC adaptör kablosu ve aktif soğutucu bütçeye eklenmelidir.

## Issue #3 Kapanmadan Önce Kontrol Listesi

- [ ] Satın alma öncesi stok ve fiyatlar tekrar doğrulandı.
- [ ] Pi 4 mü Pi 5 mi kullanılacağı kararlaştırıldı.
- [ ] NoIR kamera standart mı wide mı seçildi.
- [ ] IR LED akımı ve sürücü topolojisi belirlendi.
- [ ] İlk kutu/parmak aparatı için ölçüler çıkarıldı.
- [ ] IR güvenlik notu test protokolüne eklendi.
