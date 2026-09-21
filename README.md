# Çapa Gastroenterohepatoloji web sitesi

Tek dosyalık, bağımlılıksız bir site: `index.html`. Sunucu, derleme veya paket gerekmez.

## Yayınlama (GitHub Pages)

1. GitHub'da yeni bir depo açın, örneğin `capagastro`.
2. `index.html` ve `img/` klasörünü depo köküne yükleyin.
3. Settings > Pages > Build and deployment: Source = "Deploy from a branch", Branch = `main`, klasör = `/ (root)`.
4. Birkaç dakika sonra site `https://<kullanıcı>.github.io/capagastro/` adresinde yayında olur.

## Özel alan adı (örn. capagastro.org)

1. Depo köküne içinde yalnızca `capagastro.org` yazan `CNAME` adlı bir dosya koyun.
2. Alan adı sağlayıcısında DNS kayıtları:
   - `A` kayıtları (kök alan adı): 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - `CNAME` kaydı: `www` -> `<kullanıcı>.github.io`
3. Settings > Pages > Custom domain alanına alan adını yazıp "Enforce HTTPS" kutusunu işaretleyin.

## İçerik güncelleme

Tüm içerik `index.html` dosyasının sonundaki `<script>` bölümünde, "İÇERİK VERİLERİ" başlığı altındadır:

- `FACTS`: üst şerit sayıları (değeri boş bırakılan madde gizlenir)
- `PROJECTS`: araştırma projeleri (`status`: `on`, `pub`, `plan`)
- `TEAM`: ekip; `avesis` numarası varsa fotoğraf AVESİS'ten çekilir, yoksa `img/<user>.jpg` aranır
- `PUBS`: yayınlar (dergi, başlık, yıl, DOI)

Metin bölümlerinde her öğe Türkçe içeriği gövdede, İngilizce karşılığını `data-en` özniteliğinde taşır. Yeni bir cümle eklerken ikisini de yazın.

## Fotoğraflar

`img/` klasörüne `filiz.akyuz.jpg`, `kadirdr.jpg` gibi kullanıcı adıyla kaydedin (kare, en az 300x300 px). AVESİS numarası bilinen kişilerde dosya gerekmez.
