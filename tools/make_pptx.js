#!/usr/bin/env node
// Sunum şablonunu üretir: sablon/capagastro-sunum.pptx (16:9). Kimlik kitindeki renkler ve logo dosyaları kullanılır.
// Kullanım: node tools/make_pptx.js   (gereksinim: npm i pptxgenjs, ya da global kurulum ile NODE_PATH)
// Yazı tipleri: başlıklarda Georgia, metinde Arial (her bilgisayarda bulunur). Fraunces ve Public Sans kuruluysa
// PowerPoint'te "Yazı tiplerini değiştir" ile Georgia -> Fraunces, Arial -> Public Sans yapılabilir.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const ROOT = path.join(__dirname, "..");
const IMG = p => path.join(ROOT, "img", p);

const C = { teal: "0F5F66", teal2: "0B4A50", tealSoft: "D7E7E6", claret: "8B1E2D", claretSoft: "F3E1E3", paper: "F7F5EF", paper2: "EEEAE0", ink: "1B2A2F", ink2: "4A5A5F", line: "CFC9BA" };
const H = "Georgia", B = "Arial";
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 inç
pres.author = "Çapa Gastroenterohepatoloji";
pres.company = "İstanbul Üniversitesi İstanbul Tıp Fakültesi Gastroenterohepatoloji Bilim Dalı";
pres.title = "Çapa Gastroenterohepatoloji sunum şablonu";

// Ortak altbilgi: sol altta logo, sağ altta sayfa numarası
function footer(slide, n, light) {
  slide.addImage({ path: IMG(light ? "logo-white.png" : "logo.png"), x: 0.5, y: 5.15, w: 2.2, h: 0.265 });
  slide.addText(String(n), { x: 9.0, y: 5.12, w: 0.5, h: 0.3, fontFace: B, fontSize: 10, color: light ? C.paper : C.ink2, align: "right", isTextBox: true, margin: 0 });
}
function title(slide, text, opts) {
  slide.addText(text, Object.assign({ x: 0.5, y: 0.4, w: 9, h: 0.7, fontFace: H, fontSize: 28, color: C.ink, isTextBox: true, margin: 0 }, opts || {}));
}
let n = 0;

// 1. Kapak
{
  const s = pres.addSlide(); n++;
  s.background = { path: IMG("sunum-kapak.png") };
  s.addText("Sunum başlığı buraya", { x: 0.63, y: 2.05, w: 6.2, h: 1.3, fontFace: H, fontSize: 36, color: C.paper, isTextBox: true, margin: 0, valign: "top" });
  s.addText("Alt başlık veya toplantı adı", { x: 0.63, y: 3.35, w: 6.2, h: 0.45, fontFace: B, fontSize: 18, color: C.paper, isTextBox: true, margin: 0 });
  s.addText("Konuşmacı adı, unvanı  ·  Tarih", { x: 0.63, y: 3.85, w: 6.2, h: 0.4, fontFace: B, fontSize: 14, color: C.paper, transparency: 15, isTextBox: true, margin: 0 });
  s.addNotes("Şablon kullanımı: gereken slaytı çoğaltıp metni değiştirin; kullanmadığınız örnek slaytları silin. Renkler ve logo dosyaları besimagargun.com/capagastro/kimlik.html adresinde. Yazı tipleri Georgia ve Arial olarak ayarlıdır; Fraunces ve Public Sans kuruluysa Giriş > Değiştir > Yazı Tiplerini Değiştir ile dönüştürün. Kapak zemini img/sunum-kapak.png dosyasıdır.");
}

// 2. Bölüm ayırıcı
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.teal };
  s.addImage({ path: IMG("logo-mark-white.png"), x: 0.5, y: 0.45, w: 0.55, h: 0.55 });
  s.addText("01", { x: 0.5, y: 1.6, w: 3, h: 1.1, fontFace: H, fontSize: 72, color: C.paper, transparency: 35, isTextBox: true, margin: 0 });
  s.addText("Bölüm başlığı", { x: 0.5, y: 2.75, w: 8.5, h: 0.9, fontFace: H, fontSize: 40, color: C.paper, isTextBox: true, margin: 0 });
  s.addText("Bölümün tek cümlelik özeti veya sorusu", { x: 0.5, y: 3.7, w: 8.5, h: 0.5, fontFace: B, fontSize: 18, color: C.paper, isTextBox: true, margin: 0 });
  footer(s, n, true);
}

// 3. Başlık + maddeler + görsel alanı
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.paper };
  title(s, "Başlık ve maddeler, sağda görsel");
  s.addText([
    { text: "Her slaytta tek fikir; başlık o fikri cümle olarak söylesin", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "En fazla beş madde, her madde tek satır veya iki satır", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Sayıları büyük yazın, kaynağı altta küçük yazın", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Hasta görüntülerinde kimlik bilgisi, tarih ve dosya numarası bulunmaz", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Görsel için sağdaki alanı kullanın; alan gerekmiyorsa metni genişletin", options: { bullet: true } },
  ], { x: 0.5, y: 1.3, w: 5.2, h: 3.4, fontFace: B, fontSize: 16, color: C.ink, valign: "top", isTextBox: true, margin: 0 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.0, y: 1.3, w: 3.5, h: 3.1, fill: { color: C.paper2 }, line: { color: C.line, width: 1 }, rectRadius: 0.12 });
  s.addText("Görsel alanı\n(endoskopi görüntüsü, şema, tablo)", { x: 6.0, y: 1.3, w: 3.5, h: 3.1, fontFace: B, fontSize: 12, color: C.ink2, align: "center", valign: "middle", isTextBox: true });
  s.addText("Kaynak: yazar ve ark. Dergi 2026;12:34-56.", { x: 0.5, y: 4.72, w: 7, h: 0.3, fontFace: B, fontSize: 10, color: C.ink2, isTextBox: true, margin: 0 });
  footer(s, n);
}

// 4. İki sütun karşılaştırma
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.paper };
  title(s, "İki seçenek yan yana");
  [["Seçenek A", ["Kim için uygun", "Ne kadar sürer", "Kanıt düzeyi ve kılavuz önerisi", "Ünitede nasıl uygulanır"]], ["Seçenek B", ["Kim için uygun", "Ne kadar sürer", "Kanıt düzeyi ve kılavuz önerisi", "Ünitede nasıl uygulanır"]]].forEach(([h, items], i) => {
    const x = 0.5 + i * 4.65;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.3, w: 4.35, h: 3.3, fill: { color: C.paper2 }, line: { color: C.line, width: 1 }, rectRadius: 0.12 });
    s.addText(h, { x: x + 0.3, y: 1.5, w: 3.8, h: 0.45, fontFace: H, fontSize: 20, color: C.teal2, isTextBox: true, margin: 0 });
    s.addText(items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j < items.length - 1, paraSpaceAfter: 6 } })), { x: x + 0.3, y: 2.05, w: 3.8, h: 2.4, fontFace: B, fontSize: 15, color: C.ink, valign: "top", isTextBox: true, margin: 0 });
  });
  footer(s, n);
}

// 5. Büyük sayılar
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.paper };
  title(s, "Üç sayı ile sonuç");
  [["241", "PubMed'de dizinli yayın"], ["37", "yan dal mezunu gastroenterolog"], ["1963", "gastroenteroloji seksiyonunun kuruluşu"]].forEach(([v, l], i) => {
    const x = 0.5 + i * 3.1;
    s.addText(v, { x, y: 1.6, w: 2.9, h: 1.2, fontFace: H, fontSize: 60, color: C.teal, isTextBox: true, margin: 0 });
    s.addText(l, { x, y: 2.85, w: 2.7, h: 0.8, fontFace: B, fontSize: 15, color: C.ink2, isTextBox: true, margin: 0, valign: "top" });
  });
  s.addText("Sayılar örnektir; kendi verinizle değiştirin. Kaynak: bilim dalı kayıtları, Eylül 2026.", { x: 0.5, y: 4.72, w: 8, h: 0.3, fontFace: B, fontSize: 10, color: C.ink2, isTextBox: true, margin: 0 });
  footer(s, n);
}

// 6. Olgu sunumu
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.paper };
  title(s, "Olgu: 54 yaşında erkek, 3 aydır disfaji");
  const rows = [["Başvuru", "Katı gıdalara karşı ilerleyici disfaji, 4 kg kilo kaybı"], ["Öykü", "Sigara 30 paket-yıl; reflü yakınması 10 yıl; ilaç: pantoprazol"], ["Bulgular", "Muayene olağan; Hb 11,2 g/dL; endoskopide distal özofagusta darlık"], ["Soru", "Sonraki adım ne olmalı?"]];
  s.addTable(rows.map(r => [{ text: r[0], options: { bold: true, color: C.teal2, fill: { color: C.paper2 } } }, { text: r[1], options: { color: C.ink } }]), { x: 0.5, y: 1.3, w: 5.6, colW: [1.3, 4.3], fontFace: B, fontSize: 14, border: { type: "solid", color: C.line, pt: 0.75 }, margin: 0.08, rowH: 0.62 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.4, y: 1.3, w: 3.1, h: 2.5, fill: { color: C.paper2 }, line: { color: C.line, width: 1 }, rectRadius: 0.12 });
  s.addText("Endoskopi görüntüsü\n(kimlik bilgisi, tarih ve dosya numarası kırpılmış)", { x: 6.4, y: 1.3, w: 3.1, h: 2.5, fontFace: B, fontSize: 11, color: C.ink2, align: "center", valign: "middle", isTextBox: true });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.4, y: 3.95, w: 3.1, h: 0.75, fill: { color: C.claretSoft }, line: { color: C.claretSoft, width: 0 }, rectRadius: 0.1 });
  s.addText("Olgu verileri kimliksizleştirilmiştir; yaş ve tarihler kabalaştırılmıştır.", { x: 6.5, y: 3.95, w: 2.9, h: 0.75, fontFace: B, fontSize: 10, color: C.claret, valign: "middle", isTextBox: true, margin: 0 });
  footer(s, n);
}

// 7. Grafik
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.paper };
  title(s, "Yıllara göre yayın sayısı");
  s.addChart(pres.charts.BAR, [{ name: "Yayın", labels: ["2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026"], values: [11, 8, 11, 18, 8, 11, 32, 22] }], {
    x: 0.5, y: 1.25, w: 9, h: 3.5, barDir: "col", chartColors: [C.teal], showLegend: false, showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: B, dataLabelFontSize: 11, dataLabelColor: C.ink,
    catAxisLabelFontFace: B, catAxisLabelFontSize: 12, catAxisLabelColor: C.ink2, valAxisLabelFontFace: B, valAxisLabelFontSize: 11, valAxisLabelColor: C.ink2, valGridLine: { color: C.line, size: 0.5 }, catGridLine: { style: "none" }, showTitle: false, plotArea: { fill: { color: C.paper } }, chartArea: { fill: { color: C.paper } }
  });
  s.addText("Kaynak: PubMed, bilim dalı yayın listesi (besimagargun.com/capagastro/yayinlar.html), Eylül 2026.", { x: 0.5, y: 4.78, w: 8.5, h: 0.3, fontFace: B, fontSize: 10, color: C.ink2, isTextBox: true, margin: 0 });
  footer(s, n);
}

// 8. Kapanış
{
  const s = pres.addSlide(); n++;
  s.background = { color: C.teal };
  s.addImage({ path: IMG("logo-white.png"), x: 0.5, y: 0.5, w: 3.6, h: 0.434 });
  s.addText("Teşekkürler", { x: 0.5, y: 1.7, w: 8.5, h: 1, fontFace: H, fontSize: 44, color: C.paper, isTextBox: true, margin: 0 });
  s.addText([
    { text: "Ad Soyad, unvan", options: { breakLine: true, bold: true } },
    { text: "ad.soyad@istanbul.edu.tr", options: { breakLine: true } },
    { text: "İstanbul Tıp Fakültesi Gastroenterohepatoloji Bilim Dalı  ·  0212 414 20 00, dahili 30960", options: { breakLine: true } },
    { text: "besimagargun.com/capagastro", options: {} },
  ], { x: 0.5, y: 2.85, w: 8.5, h: 1.5, fontFace: B, fontSize: 16, color: C.paper, valign: "top", isTextBox: true, margin: 0, paraSpaceAfter: 4 });
}

const out = path.join(ROOT, "sablon", "capagastro-sunum.pptx");
fs.mkdirSync(path.dirname(out), { recursive: true });
pres.writeFile({ fileName: out }).then(() => console.log("yazıldı:", out, n + " slayt"));
