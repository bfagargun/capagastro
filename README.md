# capagastro

Bu dal (main) şu anda yalnız geçici bir "hazırlık aşamasında" sayfası yayınlar. capagastro.org alan adı, www ve HTTPS bağlı kalır; eski adresler de bu sayfaya düşer. `sw.js`, siteyi daha önce açmış tarayıcılardaki çevrimdışı kopyayı siler.

Sitenin tamamı `tam-site` dalındadır. Site kapalıyken içerik çalışması orada yapılır; o dala gönderilen değişiklikler yayına çıkmaz.

Yeniden yayına almak için:

1. main'de kapatma commit'ini geri alın (mesajı "Site geçici olarak kapatıldı" ile başlar): `git revert <commit>`
2. `tam-site` dalını main'e birleştirin: `git merge tam-site`
3. `python3 tools/check.py` ile denetleyip main'i gönderin.
