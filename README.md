# Çapa Gastroenterohepatoloji web sitesi

İstanbul Tıp Fakültesi Gastroenterohepatoloji Bilim Dalı'nın sitesi. Derleme veya paket gerektirmez; dosyalar olduğu gibi GitHub Pages'te yayınlanır.

Canlı adres: https://besimagargun.com/capagastro/ (İngilizce için `?lang=en` ekleyin)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `index.html` | Ana sayfa (Türkçe ve İngilizce) |
| `yayinlar.html` | Tüm yayınlar; kişiye, türe ve metne göre filtre |
| `hazirlik.html` | Kolonoskopi hazırlık planlayıcı: randevu saati ve solüsyona göre saat saat plan; takvim (.ics), WhatsApp, yazdırma |
| `islemler.html` | Her işlem için hasta bilgilendirme (hazırlık, işlem günü, sonrası, ne zaman aramalı, SSS); bölüm bazında yazdırma ve paylaşım |
| `egitim.html` | Eğitim ve başvuru: yan dal programı, haftalık akademik program, rotasyon, öğrenci projeleri, gözlemci başvurusu |
| `protokoller.html` | Asistanlar için klinik protokol özetleri (`PROTOCOLS` dizisi: id, title, lead, version, approved, body HTML, src); protokol bazında yazdırma; Türkçe |
| `veri-yonetisimi.html` | Araştırma grubunun veri yönetişimi ve sorumlu yapay zeka ilke belgesi (veri sınıfları, kimliksizleştirme akışı, LLM kuralları, güvenlik, paylaşım, roller) |
| `hatirlatici.html` | Takip hatırlatıcıları: HCC taraması, ilaç raporu yenileme, biyolojik tedavi dozları, kontrol kolonoskopisi için .ics takvim dosyası |
| `qr.html`, `img/qr/` | Hasta sayfalarının QR kartları (ünite içi, yazdırılabilir); kodlar `tools/make_qr.py` ile üretilir |
| `pubs.js` | PubMed'den derlenen yayın verisi (`PUBS_ALL`) |
| `404.html` | Bulunamayan sayfalar için |
| `og.png` | Bağlantı paylaşıldığında görünen görsel (1200x630) |
| `apple-touch-icon.png` | Telefon ana ekranı simgesi |
| `.nojekyll` | GitHub Pages'in dosyaları işlememesi için |

## İçerik güncelleme

Ana sayfadaki değişken içerik `index.html` dosyasının sonundaki `<script>` bölümünde, "İÇERİK VERİLERİ" başlığı altındadır. Her öğenin Türkçesi `tr`, İngilizcesi `en` alanındadır.

- `PROJECTS`: araştırma projeleri. `status`: `on` (sürüyor), `pub` (yayımlandı), `plan` (planlama). `link`: yayın adresi.
- `TEAM`: öğretim üyeleri ve yan dal asistanları. `photo`: fotoğraf adresi, `user`: profil.istanbul.edu.tr kullanıcı adı, `orcid`: ORCID numarası, `pi: true`: sorumlu araştırmacı etiketi.
- `ALUMNI`: mezunlar, onur panosundaki sırayla (en eskiden en yeniye); yeni mezun listenin sonuna eklenir. `years`: yan dal eğitim yılları (ör. `"2023-2026"`), `now` / `nowEn`: bugünkü kurum, `link`: isteğe bağlı bağlantı. Boş alanlar gösterilmez.
- `COLLAB`: iş birliği yapılan kurumlar.
- `PI_PUBS`: sorumlu araştırmacı bölümündeki seçilmiş yayınların DOI listesi (`pubs.js` içinden çekilir).
- `NEWS`: haberler ve duyurular. `d`: tarih (`"2026-10-17"`, `"2026-07"` veya `"2026"`), `tag`: [Türkçe, İngilizce] etiket, `tr` / `en`: [başlık, metin], `link`: isteğe bağlı bağlantı (DOI bağlantısı "Yayın", diğerleri "Ayrıntı" düğmesi olur). En yeni 6 haber görünür, kalanı "Daha eski haberler" düğmesiyle açılır.
- `FACTS`: üst şerit sayıları. Değeri boş (`""`) bırakılan madde gizlenir; ekip, proje ve yayın sayıları kendiliğinden hesaplanır.

Listeler (ekip, mezunlar, projeler, yayınlar) sayfaya ayrıca statik HTML olarak `<!--pre:...-->` işaretleri arasında gömülüdür; böylece JavaScript çalıştırmayan okuyucular ve arama motorları da içeriği görür. Tarayıcıda sayfa her açıldığında listeler verilerden yeniden çizildiği için veriyi değiştirmeniz yeterlidir; işaretler arasındaki statik kopya ise bir sonraki güncellemede yenilenir.

Sabit metinlerde (başlıklar, paragraflar, sorumlu araştırmacı özgeçmişi) Türkçe metin öğenin içinde, İngilizcesi `data-en` özniteliğindedir. Yeni bir cümle eklerken ikisini de yazın. Sitede uzun ve kısa tire karakterleri ile şapkalı a kullanılmaz; aralıklarda kısa çizgi (-) kullanılır.

## Yayınlar

`yayinlar.html` açılınca atıf sayılarını OpenAlex API'sinden tarayıcıda çeker (DOI ile, DOI'si olmayanlar PMID ile; 40'lık paketler halinde, `mailto` ile kibar havuz), 7 gün `localStorage`'da saklar ve üst şeride toplam atıf ile bilim dalı h-indeksini, listeye "atıfa göre" sıralamayı ve her kayda atıf etiketini ekler. API'ye erişilemezse sayfa atıfsız çalışır. Yıllara göre yayın grafiği `pubs.js` verisinden çizilir.

`pubs.js` PubMed'den ekip üyelerinin adı ve İstanbul adresiyle derlendi, adaş yazarlar ayıklandı. Her kayıtta `jif` yaklaşık dergi etki faktörüdür ve yalnızca sıralama içindir. Yeni yayın eklemek için aynı biçimde bir satır ekleyin; liste etki faktörüne göre kendiliğinden sıralanır.

## Kolonoskopi hazırlık planlayıcı

`hazirlik.html` sunucusuz çalışır: hasta randevu tarihini, saatini, solüsyonu ve kendisiyle ilgili durumları seçer; plan tarayıcıda hesaplanır, hiçbir veri kaydedilmez veya gönderilmez. Seçimler adres çubuğuna yazılır (`?t=2026-10-08T09:30&s=pegdin&f=sed,ac`), böylece "Bağlantıyı kopyala" ile aynı plan başka bir cihazda açılabilir. Ünite randevu kağıdına ürüne özel bir bağlantı ya da QR kod basabilir; örneğin `hazirlik.html?s=xm` sayfayı X-M Diet seçili açar (`s=pegdin`, `s=xm`, `s=pico`).

Protokoller dosyanın sonundaki `<script>` bölümünün başında, `PROTOCOLS` dizisindedir; ünitede kullanılan üç hazırlık tanımlı ve üçünde de solüsyonun tamamı bir gün önce akşam içilir (sabah ağızdan doz yok): `pegdin` (1 poşet ikiye bölünüp iki ayrı 1,5 L şişede, 17.00 ve 20.00; her şişeden sonra en az yarım litre, toplam en az 1 L ek su), `xm` (2 şişe X-M Diet oral süspansiyon 17.00 ve 20.00; işlem sabahı randevudan 3 ve 2 saat önce 2 adet B.T. Enema lavman) ve `pico` (Picoprep veya CitraFleet, 2 poşet, 17.00 ve 21.00). Her protokolde `dose1Hour` / `dose2Hour` doz saatleri, `d1` / `d2` dozların dakika cinsinden süresi (takvim etkinliği için), `t1` / `t2` adım başlıkları, `how1` / `how2` hasta metinleridir; `tips: true` ise bulantı ve içme ipuçları eklenir. Lavmanlı protokolde `enemaBefore` her lavmanın randevudan kaç dakika önce uygulanacağı (dizi), `enemaTitles` ve `enemas` lavman metinleridir. `rkWarn: true` olan üründe böbrek veya kalp yetmezliği işaretlenirse uyarı çıkar; `warn` ürüne özel bilgi notudur. Zamanlama kuralları `RULES` nesnesindedir: `stop` (ağızdan alımın randevudan kaç dakika önce kesileceği, 120), `morning` (sabah berrak sıvı hatırlatması, 180), `arrive` (üniteye varış, 30), `ironDays`, `dietDays`, `dietDaysConstipation`. Hasta metinleri `T.tr.steps` ve `T.en.steps` altındadır; listeler (`lists`) ve sık sorulan sorular (`faq`) aynı sözlüktedir.

Sayfa alt bilgisindeki "Hazırlayan / Kaynak / Son gözden geçirme" satırı (`stamp`) her içerik değişikliğinde güncellenmelidir; yayına almadan önce bilim dalı onayı alınıp "taslak" ibaresi kaldırılmalıdır.

## İşlem bilgilendirme sayfası

`islemler.html` içeriği dosyanın sonundaki `PROCEDURES` dizisindedir. Her işlemde `id` (bağlantı çapası, ör. `islemler.html#ercp`), her dil için `name`, `short` (bir cümlelik tanım), `facts` (`dur` süre, `sed` sedasyon, `fast` açlık, `comp` refakatçi, `res` sonuç), `prep` / `day` / `after` / `red` madde listeleri ve `faq` soru-cevap çiftleri vardır. Boş bırakılan `red` veya `faq` gösterilmez. Metinlerde geçen "hazırlık planlayıcı" ifadesi kendiliğinden `hazirlik.html` bağlantısına dönüşür. Yeni bir işlem eklemek için diziye aynı yapıda bir kayıt eklemek yeterlidir; üstteki işlem listesi kendiliğinden güncellenir.

## QR kartları

`qr.html` hazırlık kağıdına ve panolara basılacak QR kodlarını iki sütunlu A4 düzeninde listeler. Kodlar `img/qr/` altındadır ve `tools/make_qr.py` ile üretilir (`pip install qrcode pillow`; `python3 tools/make_qr.py --base https://capagastro.org/` gibi). Bağlantı listesi betiğin içindeki `LINKS` dizisindedir; yeni bir sayfa eklenince oraya bir satır ekleyip betiği yeniden çalıştırın. Alan adı değişince kodlar yenilenmelidir; eski kağıtlardaki kodlar önceki adrese gider.

## Dil

Sayfa, tarayıcı dili Türkçe ise Türkçe, değilse İngilizce açılır. `?lang=en` veya `?lang=tr` bu seçimi zorlar; ziyaretçinin düğmeyle yaptığı seçim tarayıcıda hatırlanır.

## Arama motorları

Site taslak olduğu için `index.html`, `yayinlar.html`, `hazirlik.html`, `islemler.html`, `hatirlatici.html`, `egitim.html`, `protokoller.html` ve `veri-yonetisimi.html` başında `noindex, nofollow` etiketleri var; Google ve diğer arama motorları sayfaları dizine eklemez, bağlantıyı bilen herkes ise açabilir. Yayına hazır olunca bu dosyalardaki "TASLAK" yorumunun altındaki iki `robots`/`googlebot` satırını silin. `robots.txt` ile engellemeyin: tarayıcı sayfayı okuyamazsa `noindex` etiketini de göremez.

## Yayınlama

Depo: github.com/bfagargun/capagastro, dal `main`, klasör `/ (root)`. Dosyalar depoya gönderildikten birkaç dakika sonra canlıya yansır.

## Özel alan adı (ör. capagastro.org)

1. Depo köküne içinde yalnızca alan adı yazan `CNAME` dosyası koyun.
2. Alan adı sağlayıcısında: kök için `A` kayıtları 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` için `CNAME` kaydı `bfagargun.github.io`.
3. Settings > Pages > Custom domain alanına alan adını yazıp "Enforce HTTPS" kutusunu işaretleyin.
4. `index.html`, `yayinlar.html`, `hazirlik.html`, `islemler.html`, `hatirlatici.html`, `egitim.html` ve `veri-yonetisimi.html` içindeki `canonical`, `og:url` ve `og:image` adreslerini, `404.html` içindeki `/capagastro/` bağlantılarını yeni adrese göre güncelleyin.
