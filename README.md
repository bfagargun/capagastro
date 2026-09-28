# Çapa Gastroenterohepatoloji web sitesi

İstanbul Tıp Fakültesi Gastroenterohepatoloji Bilim Dalı'nın sitesi. Derleme veya paket gerektirmez; dosyalar olduğu gibi GitHub Pages'te yayınlanır.

Canlı adres: https://besimagargun.com/capagastro/ (İngilizce için `?lang=en` ekleyin)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `index.html` | Ana sayfa (Türkçe ve İngilizce) |
| `yayinlar.html` | Tüm yayınlar; kişiye, türe ve metne göre filtre; OpenAlex atıfları; görüntülenen listeyi BibTeX, RIS veya CSV olarak indirme |
| `hazirlik.html` | Kolonoskopi hazırlık planlayıcı: randevu saati ve solüsyona göre saat saat plan; takvim (.ics), WhatsApp, yazdırma (çıktıda ürüne özel QR); hafta sonu ve resmi tatil uyarısı (`HOLIDAYS_DATED` listesine yeni yılın bayram tarihlerini ekleyin) |
| `islemler.html` | Her işlem için hasta bilgilendirme (hazırlık, işlem günü, sonrası, ne zaman aramalı, SSS); bölüm bazında yazdırma ve paylaşım |
| `egitim.html` | Eğitim ve başvuru: yan dal programı, haftalık akademik program, rotasyon, öğrenci projeleri, gözlemci başvurusu |
| `sevk.html` | Sevk eden hekimler için: kimleri yönlendirmeli, aciliyet şeritleri (acil / öncelikli / rutin), gönderilecekler, tek sayfa yazdırılan sevk formu (kimlik bilgisi e-postaya girmez), iletişim |
| `protokoller.html` | Asistanlar için klinik protokol özetleri (`PROTOCOLS` dizisi: id, title, lead, version, approved, body HTML, src); protokol bazında yazdırma; Türkçe |
| `veri-yonetisimi.html` | Araştırma grubunun veri yönetişimi ve sorumlu yapay zeka ilke belgesi (veri sınıfları, kimliksizleştirme akışı, LLM kuralları, güvenlik, paylaşım, roller) |
| `veri-ve-araclar.html` | Veri seti ve araç kataloğu: her veri seti ve yazılım/model için bir kart (kaynak, dönem, etiketler, erişim sınıfı, kullanım amacı, doğrulama, sınırlar); erişim akışı |
| `veri-sozlesme.html` | Veri kullanım sözleşmesi şablonu (Türkçe): doldurulabilir alanlar, yazdırma/PDF, örnek değerler; hukuk müşavirliği incelemesi bekleyen taslak |
| `kimlik.html`, `img/logo*` | Kurumsal kimlik ve basın kiti: logo dosyaları (SVG ve PNG, `tools/make_logo.py` ve `tools/make_logo_png.js` ile üretilir), renkler, yazı tipleri, ad yazımları, tanıtım metinleri, sunum ve poster şablonları, e-posta imzası; `img/capagastro-kimlik.zip` tüm set |
| `img/og-*.png` | Sayfa başına sosyal medya kartı (WhatsApp, X, LinkedIn önizlemesi); `node tools/make_og.js` ile üretilir |
| `hatirlatici.html` | Takip hatırlatıcıları: HCC taraması, ilaç raporu yenileme, biyolojik tedavi dozları, kontrol kolonoskopisi için .ics takvim dosyası |
| `izlem.html` | Uzun süreli izlem rehberleri: İBH, siroz, karaciğer nakli adayları, Wilson; bizde nasıl işler, ne zaman aramalı |
| `sss.html` | Hastalar için sık sorulan sorular (randevu, işlem günü, sonuç ve raporlar, hazırlık ve ilaçlar, ulaşım, diğer); arama kutusu, FAQPage yapılandırılmış verisi |
| `qr.html`, `img/qr/` | Hasta sayfalarının QR kartları (ünite içi, yazdırılabilir); kodlar `tools/make_qr.py` ile üretilir |
| `pubs.js` | PubMed'den derlenen yayın verisi (`PUBS_ALL`) |
| `404.html` | Bulunamayan sayfalar için |
| `cevrimdisi.html`, `sw.js`, `manifest.webmanifest` | Çevrimdışı yedek sayfa, hizmet çalışanı ve uygulama bildirimi (aşağıda) |
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

Listeler (ekip, mezunlar, projeler, yayınlar) sayfaya ayrıca statik HTML olarak `<!--pre:...-->` işaretleri arasında gömülüdür; böylece JavaScript çalıştırmayan okuyucular ve arama motorları da içeriği görür. Tarayıcıda sayfa her açıldığında listeler verilerden yeniden çizildiği için veriyi değiştirmeniz yeterlidir; işaretler arasındaki statik kopyayı `node tools/prerender.js` yeniler (Playwright gerekir: `npm i -g playwright && npx playwright install chromium`).

Sabit metinlerde (başlıklar, paragraflar, sorumlu araştırmacı özgeçmişi) Türkçe metin öğenin içinde, İngilizcesi `data-en` özniteliğindedir. Yeni bir cümle eklerken ikisini de yazın. Sitede uzun ve kısa tire karakterleri ile şapkalı a kullanılmaz; aralıklarda kısa çizgi (-) kullanılır.

## Yayınlar

`yayinlar.html` açılınca atıf sayılarını OpenAlex API'sinden tarayıcıda çeker (DOI ile, DOI'si olmayanlar PMID ile; 40'lık paketler halinde, `mailto` ile kibar havuz), 7 gün `localStorage`'da saklar ve üst şeride toplam atıf ile bilim dalı h-indeksini, listeye "atıfa göre" sıralamayı ve her kayda atıf etiketini ekler. API'ye erişilemezse sayfa atıfsız çalışır. Yıllara göre yayın grafiği `pubs.js` verisinden çizilir.

`pubs.js` PubMed'den ekip üyelerinin adı ve İstanbul adresiyle derlendi, adaş yazarlar ayıklandı. Her kayıtta `jif` yaklaşık dergi etki faktörüdür ve yalnızca sıralama içindir. Yeni yayın eklemek için aynı biçimde bir satır ekleyin; liste etki faktörüne göre kendiliğinden sıralanır.

Yeni yayınları bulmak için `python3 tools/update_pubs.py` çalıştırın: ekip üyelerinin adı ve İstanbul adresiyle PubMed'i tarar (varsayılan olarak listedeki son yıldan bir yıl öncesinden itibaren; `--since 2020` ile değiştirilir), `pubs.js`'de olmayan kayıtları adres özetiyle `pubs-candidates.json` dosyasına yazar. Dosyada adaş yazarları ayıklayıp uygun kayıtlarda `"keep": true` bırakın, eksik `jif` değerlerini doldurun, sonra `python3 tools/update_pubs.py --apply` ile `pubs.js`'ye ekleyin. Üye listesi betiğin başındaki `MEMBERS` sözlüğündedir; yeni üye gelince oraya PubMed yazar biçimiyle ekleyin. Ana sayfadaki yayın sayısı ve ekip kartlarındaki "Yayınlar (n)" değerleri tarayıcıda `pubs.js`'den hesaplanır; `<!--pre:...-->` işaretleri arasındaki statik kopyaları yenilemek için `node tools/prerender.js` çalıştırın (Playwright gerekir).

## Kolonoskopi hazırlık planlayıcı

`hazirlik.html` sunucusuz çalışır: hasta randevu tarihini, saatini, solüsyonu ve kendisiyle ilgili durumları seçer; plan tarayıcıda hesaplanır, hiçbir veri kaydedilmez veya gönderilmez. Seçimler adres çubuğuna yazılır (`?t=2026-10-08T09:30&s=pegdin&f=sed,ac`), böylece "Bağlantıyı kopyala" ile aynı plan başka bir cihazda açılabilir. Ünite randevu kağıdına ürüne özel bir bağlantı ya da QR kod basabilir; örneğin `hazirlik.html?s=xm` sayfayı X-M Diet seçili açar (`s=pegdin`, `s=xm`, `s=pico`).

Protokoller dosyanın sonundaki `<script>` bölümünün başında, `PROTOCOLS` dizisindedir; ünitede kullanılan üç hazırlık tanımlı ve üçünde de solüsyonun tamamı bir gün önce akşam içilir (sabah ağızdan doz yok): `pegdin` (1 poşet ikiye bölünüp iki ayrı 1,5 L şişede, 17.00 ve 20.00; her şişeden sonra en az yarım litre, toplam en az 1 L ek su), `xm` (2 şişe X-M Diet oral süspansiyon 17.00 ve 20.00; işlem sabahı randevudan 3 ve 2 saat önce 2 adet B.T. Enema lavman) ve `pico` (Picoprep veya CitraFleet, 2 poşet, 17.00 ve 21.00). Her protokolde `dose1Hour` / `dose2Hour` doz saatleri, `d1` / `d2` dozların dakika cinsinden süresi (takvim etkinliği için), `t1` / `t2` adım başlıkları, `how1` / `how2` hasta metinleridir; `tips: true` ise bulantı ve içme ipuçları eklenir. Lavmanlı protokolde `enemaBefore` her lavmanın randevudan kaç dakika önce uygulanacağı (dizi), `enemaTitles` ve `enemas` lavman metinleridir. `rkWarn: true` olan üründe böbrek veya kalp yetmezliği işaretlenirse uyarı çıkar; `warn` ürüne özel bilgi notudur. Zamanlama kuralları `RULES` nesnesindedir: `stop` (ağızdan alımın randevudan kaç dakika önce kesileceği, 120), `morning` (sabah berrak sıvı hatırlatması, 180), `arrive` (üniteye varış, 30), `ironDays`, `dietDays`, `dietDaysConstipation`. Hasta metinleri `T.tr.steps` ve `T.en.steps` altındadır; listeler (`lists`) ve sık sorulan sorular (`faq`) aynı sözlüktedir.

Sayfa alt bilgisindeki "Hazırlayan / Kaynak / Son gözden geçirme" satırı (`stamp`) her içerik değişikliğinde güncellenmelidir; yayına almadan önce bilim dalı onayı alınıp "taslak" ibaresi kaldırılmalıdır.

## İşlem bilgilendirme sayfası

`islemler.html` içeriği dosyanın sonundaki `PROCEDURES` dizisindedir. Her işlemde `id` (bağlantı çapası, ör. `islemler.html#ercp`), her dil için `name`, `short` (bir cümlelik tanım), `facts` (`dur` süre, `sed` sedasyon, `fast` açlık, `comp` refakatçi, `res` sonuç), `prep` / `day` / `after` / `red` madde listeleri ve `faq` soru-cevap çiftleri vardır. Boş bırakılan `red` veya `faq` gösterilmez. Metinlerde geçen "hazırlık planlayıcı" ifadesi kendiliğinden `hazirlik.html` bağlantısına dönüşür. Yeni bir işlem eklemek için diziye aynı yapıda bir kayıt eklemek yeterlidir; üstteki işlem listesi kendiliğinden güncellenir.

## QR kartları

`qr.html` hazırlık kağıdına ve panolara basılacak QR kodlarını iki sütunlu A4 düzeninde listeler. Kodlar `img/qr/` altındadır ve `tools/make_qr.py` ile üretilir (`pip install qrcode pillow`; `python3 tools/make_qr.py --base https://capagastro.org/` gibi). Bağlantı listesi betiğin içindeki `LINKS` dizisindedir; yeni bir sayfa eklenince oraya bir satır ekleyip betiği yeniden çalıştırın. Alan adı değişince kodlar yenilenmelidir; eski kağıtlardaki kodlar önceki adrese gider.

## Dil

Alt sayfaların altbilgisinin üstündeki "site haritası" şeridi `tools/inject_sitenav.py` ile eklenir; yeni bir sayfa eklenince betikteki listeye yazıp betiği yeniden çalıştırın (işaretçiler arasındaki parça yenilenir).

Sayfa, tarayıcı dili Türkçe ise Türkçe, değilse İngilizce açılır. `?lang=en` veya `?lang=tr` bu seçimi zorlar; ziyaretçinin düğmeyle yaptığı seçim tarayıcıda hatırlanır.

## Denetim

Değişiklikten sonra `python3 tools/check.py` çalıştırın: yasak karakterler (uzun/kısa tire, şapkalı a), etiket dengesi, satır içi script sözdizimi (node varsa), JSON-LD, yerel bağlantılar, canonical; ayrıca `sw.js`, `manifest.webmanifest`, `sitemap.xml`. Görsel denetim için Playwright ile ekran görüntüsü alıp açık/koyu tema ve mobil genişlikte bakın; erişilebilirlik için axe-core.

## Arama motorları

Site taslak olduğu için `index.html`, `yayinlar.html`, `hazirlik.html`, `islemler.html`, `hatirlatici.html`, `egitim.html`, `sevk.html`, `protokoller.html`, `izlem.html`, `sss.html`, `veri-yonetisimi.html`, `veri-ve-araclar.html`, `veri-sozlesme.html` ve `kimlik.html` başında `noindex, nofollow` etiketleri var; Google ve diğer arama motorları sayfaları dizine eklemez, bağlantıyı bilen herkes ise açabilir. Yayına hazır olunca bu dosyalardaki "TASLAK" yorumunun altındaki iki `robots`/`googlebot` satırını silin. `robots.txt` ile engellemeyin: tarayıcı sayfayı okuyamazsa `noindex` etiketini de göremez.

Yayına hazırlık için diğer parçalar hazır:

- `sitemap.xml`: herkese açık dokuz sayfa; `python3 tools/make_sitemap.py` ile üretilir (lastmod git tarihinden). Yayın sonrası Google Search Console ve Bing Webmaster Tools'a bu dosyayı bildirin. `protokoller.html` ve `qr.html` ünite içi olduğundan haritada yoktur.
- `robots.txt`: yalnızca site alan adının kökünden sunulurken (özel alan adı) okunur; GitHub Pages alt klasöründeyken etkisi yoktur.
- Her sayfada `hreflang` bağlantıları (`tr`, `en`, `x-default`) ve schema.org yapılandırılmış verisi vardır: ana sayfada kuruluş, kişi ve site; `islemler.html` sayfasında işlemler ve sık sorulan sorular (`FAQPage`, sayfa dilinde JavaScript ile üretilir); `veri-ve-araclar.html` sayfasında veri kataloğu ve veri setleri (`DataCatalog`, `Dataset`; Google Dataset Search için); diğer sayfalarda `MedicalWebPage` veya `WebPage`. Yayın sonrası https://validator.schema.org ve Search Console "Zengin sonuçlar" testinden geçirin.

## Çevrimdışı kullanım ve telefona ekleme

`manifest.webmanifest` ve `sw.js` sayesinde site telefona uygulama gibi eklenebilir (hazırlık planlayıcıda "Telefona ekle" düğmesi, tarayıcı izin verirse görünür) ve hasta sayfaları (`index`, `hazirlik`, `islemler`, `hatirlatici`, `izlem`, `sss`) ilk ziyaretten sonra bağlantı olmadan da açılır; diğer sayfalar bir kez açıldıysa çevrimdışı da çalışır, açılmadıysa `cevrimdisi.html` görünür. Sayfalar her zaman önce ağdan alınır, bu yüzden içerik güncellemeleri hemen görünür. Simgeler `img/icon-*.png` (dolu işaretten üretildi). Eski önbellekleri temizlemek gerekirse `sw.js` içindeki `VERSION` değiştirilir. Yalnızca HTTPS'te (ve localhost'ta) çalışır; alan adı değişince yol göreli olduğu için ek işlem gerekmez.

## Yayınlama

Depo: github.com/bfagargun/capagastro, dal `main`, klasör `/ (root)`. Dosyalar depoya gönderildikten birkaç dakika sonra canlıya yansır.

## Özel alan adı (ör. capagastro.org)

1. Depo köküne içinde yalnızca alan adı yazan `CNAME` dosyası koyun.
2. Alan adı sağlayıcısında: kök için `A` kayıtları 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `www` için `CNAME` kaydı `bfagargun.github.io`.
3. Settings > Pages > Custom domain alanına alan adını yazıp "Enforce HTTPS" kutusunu işaretleyin.
4. `index.html`, `yayinlar.html`, `hazirlik.html`, `islemler.html`, `hatirlatici.html`, `egitim.html`, `sevk.html`, `protokoller.html`, `izlem.html`, `sss.html`, `veri-yonetisimi.html`, `veri-ve-araclar.html`, `veri-sozlesme.html` ve `kimlik.html` içindeki `canonical`, `hreflang`, `og:url`, `og:image` ve JSON-LD (`besimagargun.com/capagastro/`) adreslerini, `404.html` içindeki `/capagastro/` bağlantılarını yeni adrese göre güncelleyin. Sosyal medya kartları (`img/og-*.png`) altta adresi yazılı taşır: `tools/make_og.js` içindeki adres metnini değiştirip `node tools/make_og.js` ile yeniden üretin.
5. `python3 tools/make_sitemap.py --base https://capagastro.org/` ve `python3 tools/make_qr.py --base https://capagastro.org/` çalıştırın; `robots.txt` içindeki `Sitemap:` satırını güncelleyin.
