# KVKK ve Test Etik Notu

Bu doküman hukuki danışmanlık değildir. İlk teknik MVP testlerinde riskleri azaltmak ve ekibin dikkat etmesi gereken sınırları netleştirmek için hazırlanmıştır.

## Temel İlke

NEXIVO testlerinde biyometrik veri çok hassas kabul edilmelidir. Testler yalnızca açık rıza veren gönüllülerle yapılmalı, gereksiz veri toplanmamalı ve kişisel kimlik bilgileri mümkün olduğunca ayrıştırılmalıdır.

## Ham Görüntü ve Şablon Ayrımı

**Ham görüntü:** Kameradan alınan damar/parmaktan oluşan görsel veri.

**Biyometrik şablon:** Ham görüntüden çıkarılmış, karşılaştırma için kullanılan matematiksel temsil.

Ürün vizyonunda hedef, ham görüntüyü kalıcı olarak saklamamak ve doğrulamayı mümkün olduğunca cihaz üzerinde yapmaktır. MVP araştırma aşamasında ham görüntüler kısa süreli saklanabilir; fakat bunun amacı, süresi ve erişimi baştan yazılmalıdır.

## Test Katılımcısı Takibi

- Katılımcılar gerçek isimle değil `P001`, `P002` gibi kodlarla takip edilmeli.
- Telefon, T.C. kimlik, adres gibi gereksiz kişisel veriler alınmamalı.
- Test verileri ortak mesajlaşma gruplarında paylaşılmamalı.
- Veri klasörleri sadece teknik ekip erişiminde olmalı.

## İlk Test İçin Minimum Kayıt

Her katılımcı için tutulabilecek alanlar:

- Katılımcı kodu
- Parmak tipi
- Görüntü sayısı
- Işık dalga boyu
- Kamera mesafesi
- Test tarihi
- Görüntü kalite notu

## Onam Metni Taslağı

Testten önce katılımcıya kısa ve anlaşılır şekilde şunlar söylenmeli:

> Bu çalışma NEXIVO adlı erken aşama teknik prototipin damar biyometrisi görüntüleme ve doğrulama kabiliyetini test etmek için yapılmaktadır. Test kapsamında parmak damar görüntünüz alınabilir. Veriler ürün geliştirme ve teknik doğrulama amacıyla kullanılacak, üçüncü kişilerle paylaşılmayacaktır. Teste katılım gönüllüdür; istediğiniz zaman verinizin silinmesini talep edebilirsiniz.

Daha ayrıntılı onam metni için: [VOLUNTEER_TEST_CONSENT.md](VOLUNTEER_TEST_CONSENT.md)

## Silme ve Saklama

- Katılımcı silme isterse ham görüntüler ve şablon dosyaları silinmeli.
- MVP test verileri kalıcı ürün verisi gibi görülmemeli.
- İlk aşamada ham görüntüler yalnızca algoritma geliştirme için saklanmalı.
- Demo veya sunumda gerçek kişinin görüntüsü kullanılacaksa ayrıca izin alınmalı.
