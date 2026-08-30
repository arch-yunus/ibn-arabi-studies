#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ibn-arabi-studies • İnteraktif CLI Araştırma, Alıntı ve Kavram Motoru v3.0
Şeyhü'l-Ekber Muhyiddin İbnü'l-Arabî Külliyatı & Ontolojik Dizin
"""

import sys
import os
import random
import unicodedata

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def normalize_text(text):
    if not text:
        return ""
    text = text.replace('İ', 'i').replace('I', 'i')
    text = text.lower()
    replacements = {
        'â': 'a', 'î': 'i', 'û': 'u', 'ô': 'o', 'ê': 'e',
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        '‘': '', '’': '', "'": '', '-': ' ', '—': ' ', '\u0307': ''
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.strip()

# 40+ Temel Ekberî Kavramlar Sözlüğü
GLOSSARY = {
    "vahdet-i vucud": {
        "arabic": "وحدة الوجود",
        "desc": "Varlığın ontolojik birliği; mutlak anlamda var olan yalnızca Hakk'tır, kesret O'nun esmâ ve sıfât tecellileridir."
    },
    "ayan-i sabite": {
        "arabic": "الأعيان الثابتة",
        "desc": "Eşyanın henüz dış dünyada zuhur etmeden önce Allah'ın ezeli ilmindeki sabit hakikatleri ve potansiyelleri (mâ şemmet râyihate'l-vücûd)."
    },
    "insan-i kamil": {
        "arabic": "الإنسان الكامل",
        "desc": "Bütün ilahi isim ve mertebeleri kendinde cem eden, kâinatın manevi direği, âlemin ruhu ve Hakk'ın halifesi."
    },
    "nefes-i rahmani": {
        "arabic": "النفس الرحماني",
        "desc": "İlahi varlık nefesi; harflerin ve kâinatın yokluktan varlığa çıkışını sağlayan rahmet cereyanı."
    },
    "alem-i misal": {
        "arabic": "عالم المثال / البرزخ",
        "desc": "Ruh ile madde arasındaki berzah boyutu; mânanın suret kazandığı rüya, keşif ve hayal âlemi."
    },
    "hazarat-i hams": {
        "arabic": "الحضرات الخمس",
        "desc": "Beş İlahi Mertebe: Lâ-Taayyün (Zât), Taayyün-i Evvel (Vahdet), Taayyün-i Sânî (Vâhidiyyet), Ceberût-Melekût, Şehâdet (Mülk)."
    },
    "la tekrara fit-tecelli": {
        "arabic": "لا تكرار في التجلي",
        "desc": "Tecellide asla tekrar yoktur; Hakk hiçbir kula aynı surette iki kez tecelli etmez, her an yeni bir şe'ndedir."
    },
    "halk-i cedid": {
        "arabic": "الخلق الجديد",
        "desc": "Sürekli ve anlık yaratılış; varlığın her an yok olup ardı sıra yeniden yaratılması (tecelli-i dâim)."
    },
    "feyz-i akdes": {
        "arabic": "الفيض الأقدس",
        "desc": "Zât'ın kendi zâtına tecellisiyle a'yân-ı sâbitenin ve ezelî istidatların ilâhî ilimde taayyün etmesi."
    },
    "feyz-i mukaddes": {
        "arabic": "الفيض المقدس",
        "desc": "A'yân-ı sâbitenin istidatlarına göre haricî vücûd kazanarak dış dünyada zuhûra gelmesi."
    },
    "berzah": {
        "arabic": "البرزخ",
        "desc": "İki zıt veya farklı hakikat arasında köprü kuran engel, geçit ve irtibat boyutu (örneğin ruh ile beden arasındaki nefis)."
    },
    "hakikat-i muhammediyye": {
        "arabic": "الحقيقة المحمدية",
        "desc": "Varlığın ilk taayyünü, Nûr-ı Evvel, akl-ı evvel; kâinatın yaratılış çekirdeği ve ilk ilâhî ayna."
    },
    "hatmul-velaye": {
        "arabic": "ختم الولاية",
        "desc": "Velayet mührü; mutlak velayet mührü Hz. Îsâ, özel Muhammedî velayet mührü ise Şeyhü'l-Ekber'dir."
    },
    "ahadiyyet": {
        "arabic": "الأحدية",
        "desc": "Zât'ın her türlü nisbet, isim, sıfat ve çokluktan münezzeh olduğu mutlak tenzih ve gayb mertebesi."
    },
    "vahidiyyet": {
        "arabic": "الواحدية",
        "desc": "Esmâ ve sıfatların zuhur ettiği, çokluğun ilâhî ilimde ayrıştığı vahdet mertebesi."
    },
    "fena fillah": {
        "arabic": "الفناء في الله",
        "desc": "Sâlikin kendi izafi benliğini, iradesini ve sıfatlarını ilâhî zâtta yok etmesi."
    },
    "beka billah": {
        "arabic": "البقاء بالله",
        "desc": "Fenâdan sonra Hakk'ın esmâ tecellileriyle kâim olarak halkın arasına dönüp irşad vazifesi görme makamı."
    },
    "cem ve fark": {
        "arabic": "الجمع والفرق",
        "desc": "Cem: Kesrette vahdeti görmek. Fark: Mertebeleri gözetip kul ile Rab ayrımını şeriat terazisinde korumak."
    },
    "an-i daim": {
        "arabic": "الآن الدائم",
        "desc": "Bölünme kabul etmeyen, geçmiş ve geleceği kuşatan sürekli ilâhî tecelli şimdisi."
    },
    "tehalluk": {
        "arabic": "التخلق بأخلاق الله",
        "desc": "Allah'ın ahlakıyla ahlaklanmak; esmâ-i hüsnânın mânasını nefsinde fiilen tecelli ettirmek."
    },
    "ilmul-huruf": {
        "arabic": "علم الحروف",
        "desc": "28 Arap harfinin ilâhî isimler ve felekler mertebesindeki kozmik mahreçlerinin irfânî ilmi."
    },
    "hakkul-yakin": {
        "arabic": "حق اليقين",
        "desc": "İkiliğin tamamen ortadan kalktığı, tevhîdin bizzat zevk ve zâtî tecrübe ile bilindiği en üstün yakîn mertebesi."
    }
}

# Özgün Arapça & Türkçe Alıntılar Külliyatı (Cevâhir-i Ekberiyye)
QUOTES = [
    {
        "id": 1,
        "category": "ask",
        "source": "Tercümânü'l-Eşvâk, 11. Kasîde",
        "arabic": "أَدِينُ بِدِينِ الْحُبِّ أَنَّى تَوَجَّهَتْ • رَكَائِبُهُ فَالْحُبُّ دِينِي وَإِيمَانِي",
        "turkish": "Aşkın kervanı hangi yöne yönelirse yönelsin, ben aşk dinine tâbiyim; zira aşk benim dinim ve imanımdır!"
    },
    {
        "id": 2,
        "category": "varlik",
        "source": "el-Fütûhâtü'l-Mekkiyye, Bab 198",
        "arabic": "سُبْحَانَ مَنْ أَظْهَرَ الأَشْيَاءَ وَهُوَ عَيْنُهَا",
        "turkish": "Eşyayı zuhûra çıkaran ve bizzat o zuhûr eden eşyanın aynı (hakikati) olan Zât münezzehtir!"
    },
    {
        "id": 3,
        "category": "kalp",
        "source": "Fusûsü'l-Hikem, Fass-ı Şuayb",
        "arabic": "مَا وَسِعَنِي أَرْضِي وَلاَ سَمَائِي وَلَكِنْ وَسِعَنِي قَلْبُ عَبْدِيَ المُؤْمِنِ",
        "turkish": "Beni ne yerim ne de göğüm kuşatabildi; fakat mümin kulumun kalbi Beni kuşattı (kudsî hadis)."
    },
    {
        "id": 4,
        "category": "insan",
        "source": "Fusûsü'l-Hikem, Fass-ı Âdem",
        "arabic": "فَكَانَ الْإِنْسَانُ عَيْنَ فَصِّ هَذَا الخَاتَمِ، وَالنَّقْشَ الَّذِي خَتَمَ المَلِكُ بِهِ عَلَى خَزَائِنِهِ",
        "turkish": "İnsan, bu varlık yüzüğünün kaşındaki gözbebeği ve padişahın hazinelerini mühürlediği mührün üzerindeki nakıştır."
    },
    {
        "id": 5,
        "category": "tecelli",
        "source": "Fusûsü'l-Hikem, Fass-ı Şuayb & el-Fütûhât Bab 369",
        "arabic": "إِنَّ التَّجَلِّيَ لاَ يَتَكَرَّرُ أَبَداً، فَلاَ يَتَجَلَّى الحَقُّ فِي صُورَةٍ وَاحِدَةٍ مَرَّتَيْنِ",
        "turkish": "Tecelli asla tekrar etmez; Hakk Teâlâ hiçbir kula aynı surette iki defa görünmez."
    },
    {
        "id": 6,
        "category": "marifet",
        "source": "Risâletü'l-Vücûd & Hadis Şerhi",
        "arabic": "مَنْ عَرَفَ نَفْسَهُ فَقَدْ عَرَفَ رَبَّهُ، عَرَفْتُ رَبِّي بِرَبِّي",
        "turkish": "Nefsini bilen Rabbini bilir. Ben Rabbimi yine Rabbimle bildim; Rabbim olmasaydı O'nu bilemezdim."
    },
    {
        "id": 7,
        "category": "seriat",
        "source": "el-Fütûhâtü'l-Mekkiyye, Bab 558",
        "arabic": "كُلُّ حَقِيقَةٍ لاَ تُؤَيِّدُهَا الشَّرِيعَةُ فَهِيَ زَنْدَقَةٌ",
        "turkish": "Şeriatın teyit etmediği her hakikat zındıklıktır; hakikatin aydınlatmadığı şeriat ise ruhsuzdur."
    },
    {
        "id": 8,
        "category": "hayal",
        "source": "Fusûsü'l-Hikem, Fass-ı Yûsuf",
        "arabic": "النَّاسُ نِيَامٌ فَإِذَا مَاتُوا انْتَبَهُوا، فَالدُّنْيَا نَوْمٌ وَمَا فِيهَا حُلْمٌ",
        "turkish": "İnsanlar uykudadırlar, öldükleri vakit uyanırlar. Şu halde dünya bir uyku, onda gördüklerin bir rüyadır."
    },
    {
        "id": 9,
        "category": "itikat",
        "source": "Fusûsü'l-Hikem, Fass-ı Nûh",
        "arabic": "إِيَّاكَ أَنْ تَتَقَيَّدَ بِعَقْدٍ مَخْصُوصٍ وَتَكْفُرَ بِمَا سِوَاهُ، فَكُنْ هَيُولَى لِصُوَرِ العُقُودِ كُلِّهَا",
        "turkish": "Sakın tek bir inanç kalıbına hapsolup diğerlerini inkâr etme; bütün inanç suretlerini kabul eden bir heyûlâ ol!"
    },
    {
        "id": 10,
        "category": "zaman",
        "source": "el-Fütûhâtü'l-Mekkiyye, Bab 390",
        "arabic": "الزَّمَانُ نِسْبَةٌ عَدَمِيَّةٌ، وَإِنَّمَا هُوَ الآنُ الدَّائِمُ الَّذِي لاَ يَنْقَسِمُ",
        "turkish": "Zaman izafi bir nisbettir, dışta bağımsız varlığı yoktur; gerçek olan bölünmeyen 'Ân-ı Dâim'dir."
    }
]

FUSUS_FASLS = [
    (1, "Hz. Âdem", "Hikmet-i İlâhiyye", "Âlemin yaratılışı, ayna metaforu ve hilafet"),
    (2, "Hz. Şît", "Hikmet-i Nefsiyye", "Hibe, bağış ve ilahi isimlerin sırları"),
    (3, "Hz. Nûh", "Hikmet-i Sübbûhiyye", "Tenzih ve teşbih dengesi; tevhîdin kuşatıcılığı"),
    (4, "Hz. İdrîs", "Hikmet-i Kuddûsiyye", "Yücelik mertebesi ve mekânsal tenzih"),
    (5, "Hz. İbrâhîm", "Hikmet-i Müheymiyye", "Aşkta fena hali ve ilahi dostluk (Hullet)"),
    (6, "Hz. İshâk", "Hikmet-i Hakkiyye", "Rüyaların tabiri, kurban sırrı ve koçun tevili"),
    (7, "Hz. İsmâil", "Hikmet-i Aliyye", "Rıza makamı ve rubûbiyyet-ubûdiyyet ilişkisi"),
    (8, "Hz. Yâkûb", "Hikmet-i Rûhiyyet", "Dinî teslimiyet ve kalbî istikamet"),
    (9, "Hz. Yûsuf", "Hikmet-i Nûriyye", "Âlem-i Misâl, rüya ontolojisi ve suretler"),
    (10, "Hz. Hûd", "Hikmet-i Ahadiyye", "Sırat-ı müstakîm ve perçemden tutulma"),
    (11, "Hz. Sâlih", "Hikmet-i Fethiyye", "İlahi fethin açılışı ve mucize hakikati"),
    (12, "Hz. Şuayb", "Hikmet-i Kalbiyye", "Kalbin değişkenliği ve tecellide tekrar olmaması"),
    (13, "Hz. Lût", "Hikmet-i Melekiyye", "Kudret, tasarruf ve acziyet dengesi"),
    (14, "Hz. Üzeyr", "Hikmet-i Kadriyye", "Kader sırrı ve a'yân-ı sâbite istidatları"),
    (15, "Hz. Îsâ", "Hikmet-i Nebeviyye", "Nefes-i Rahmânî ile dirilme ve kelime sırrı"),
    (16, "Hz. Süleymân", "Hikmet-i Rahmâniyye", "Rahmaniyet ve Rahimiyet; mülk ve tasarruf"),
    (17, "Hz. Dâvûd", "Hikmet-i Vücûdiyye", "Hilafet nassı, demirin yumuşatılması ve adalet"),
    (18, "Hz. Yûnus", "Hikmet-i Nefesiyye", "Tabiatın karanlığı ve balığın karnındaki tesbih"),
    (19, "Hz. Eyyûb", "Hikmet-i Gaybiyye", "Bela, sabır ve su ile arınmanın şifası"),
    (20, "Hz. Yahyâ", "Hikmet-i Celâliyye", "İlahi isimlerin celali ve bekâ hali"),
    (21, "Hz. Zekeriyyâ", "Hikmet-i Mâlikiyye", "İhtiyarlıkta gelen rahmet ve varlık bağışı"),
    (22, "Hz. İlyâs", "Hikmet-i İnsiyye", "Tabiat ile akıl arasındaki denge"),
    (23, "Hz. Lokmân", "Hikmet-i İhsâniyye", "Şirkten arınma ve hikmetin derinliği"),
    (24, "Hz. Hârûn", "Hikmet-i İmâmiyye", "Surete tapınma uyarısı, imâmet ve hilm"),
    (25, "Hz. Mûsâ", "Hikmet-i Ulviyye", "Firavun ile münazara, asâ mucizesi ve tecellî"),
    (26, "Hz. Hâlid b. Sinân", "Hikmet-i Samediyye", "Berzah âleminin haberleri"),
    (27, "Hz. Muhammed", "Hikmet-i Ferdiyye", "Varlığın gayesi, üç sevdirilen şey ve Hatm-i Nübüvvet")
]

FUTUHAT_BABS = [
    (1, "Marifet-i Rûh", "Kâbe'deki Ruhanî Genç (el-Fetâ) ile buluşma ve sırlar"),
    (6, "Merâtib-i Vücûd", "Varlık dereceleri, Heyûlâ ve Arş-ı Âlâ"),
    (63, "Âlem-i Hayâl", "Misâl âlemi ve kesretin gölge tabiatı"),
    (73, "Velâyet Mertebeleri", "Ricâlü'l-Gayb hiyerarşisi ve Tirmizî'nin 155 sorusu"),
    (178, "Bâbü'l-Muhabbe", "İlahî, ruhanî ve tabiî aşk; âşıkların 7 alameti"),
    (198, "Nefes-i Rahmânî", "28 harfin kozmik mahreçleri ve varoluş nefesi"),
    (390, "Zamanın Hakikati", "Zamanın görece oluşu ve bölünmeyen Ân-ı Dâim"),
    (558, "Vasiyetler ve Nasihatler", "Sâliklere şeriat ve ahlak ölçüleri"),
    (559, "Marifetullah ve Esmâ", "Esmâ-i Hüsnâ'nın şuhûdu ve nihai marifet")
]

def banner():
    print("=" * 72)
    print("   [📖] IBN-ARABI-STUDIES • ARAŞTIRMA, ALINTI VE KAVRAM MOTORU v3.0")
    print("   Muhyiddin İbnü'l-Arabî Külliyatı & Cevâhir-i Ekberiyye")
    print("=" * 72)

def search_term(query):
    n_query = normalize_text(query)
    found = False
    print(f"\n[🔍] '{query}' için Sözlük Arama Sonuçları:")
    print("-" * 60)
    for term, data in GLOSSARY.items():
        n_term = normalize_text(term)
        n_desc = normalize_text(data["desc"])
        if n_query in n_term or n_query in n_desc or any(w in n_desc for w in n_query.split()):
            print(f"📌 {term.upper()} ({data['arabic']}):\n   {data['desc']}\n")
            found = True
    if not found:
        print("❌ Eşleşen terim bulunamadı. docs/terminology-glossary.md dosyasına göz atın.")

def show_quotes(filter_word=None):
    print("\n[📜] ŞEYHÜ'L-EKBER'DEN ÖZGÜN ALINTILAR VE HİKMETLER:")
    print("-" * 72)
    matched = []
    if filter_word:
        n_filter = normalize_text(filter_word)
        for q in QUOTES:
            if (n_filter in normalize_text(q["category"]) or
                n_filter in normalize_text(q["turkish"]) or
                n_filter in normalize_text(q["source"])):
                matched.append(q)
    else:
        matched = QUOTES

    if not matched:
        print(f"❌ '{filter_word}' ile eşleşen alıntı bulunamadı. Kategori: ask, varlik, kalp, insan, tecelli, seriat, hayal, zaman")
        return

    for q in matched:
        print(f"💎 [{q['id']}] Kategori: #{q['category'].upper()} • {q['source']}")
        print(f"   Arapça : {q['arabic']}")
        print(f"   Türkçe : \"{q['turkish']}\"\n")

def random_quote():
    q = random.choice(QUOTES)
    print("\n[✨] GÜNÜN EKBERÎ HİKMETİ:")
    print("-" * 72)
    print(f"💎 Kategori: #{q['category'].upper()} • {q['source']}")
    print(f"   Arapça : {q['arabic']}")
    print(f"   Türkçe : \"{q['turkish']}\"")
    print("-" * 72)

def list_fusus(filter_text=None):
    print("\n[💎] FUSÛSÜ'L-HİKEM 27 PEYGAMBER VE HİKMET LİSTESİ:")
    print("-" * 72)
    print(f"{'#':<4} {'Peygamber':<18} {'Hikmet Türü':<24} {'Temel Mesele'}")
    print("-" * 72)
    n_filter = normalize_text(filter_text) if filter_text else None
    for num, prophet, wisdom, subject in FUSUS_FASLS:
        n_p = normalize_text(prophet)
        n_w = normalize_text(wisdom)
        n_s = normalize_text(subject)
        if n_filter is None or n_filter in n_p or n_filter in n_w or n_filter in n_s:
            print(f"{num:<4} {prophet:<18} {wisdom:<24} {subject}")
    print("-" * 72)

def list_futuhat():
    print("\n[🏛️] EL-FÜTÛHÂTÜ'L-MEKKİYYE SEÇME BABLAR:")
    print("-" * 72)
    print(f"{'Bab':<6} {'Konu Başlığı':<26} {'Muhteva'}")
    print("-" * 72)
    for bab, title, desc in FUTUHAT_BABS:
        print(f"Bab {bab:<3} {title:<26} {desc}")
    print("-" * 72)

def print_ontology():
    print("\n[🌌] EKBERÎ ONTOLOJİ ŞEMASI (HAZARÂT-I HAMS):")
    print('''
    [ 0. LÂ-TAAYYÜN / AHADİYYET ]  -> Mutlak Zât, Gayb-ı Mutlak
                 │
                 ▼
    [ 1. TAAYYÜN-İ EVVEL / VAHDET ] -> Hakîkat-i Muhammediyye, Nûr-ı Evvel
                 │
                 ▼
    [ 2. TAAYYÜN-İ SÂNÎ / VÂHİDİYYET ] -> Esmâ & Sıfatlar, A'yân-ı Sâbite
                 │
           ┌──────┴──────┐
           ▼             ▼
    [ CEBERÛT ]     [ MELEKÛT ]     -> Âlem-i Ervâh & Âlem-i Misâl (Berzah)
           └──────┬──────┘
                  ▼
    [ 3. ŞEHÂDET / MÜLK ]           -> Duyulur Maddî Evren, Felekler, Tabiat
                 │
                 ▼
    [ ⭐️ İNSAN-I KÂMİL ]            -> Bütün Mertebeleri Kendinde Cem Eden Ayna
    ''')

def main():
    banner()
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  python tools/ekber_cli.py search <kavram>      : Terim sözlüğünde arama yap (40+ kavram)")
        print("  python tools/ekber_cli.py quote [kategori]     : Özgün alıntıları getir (ask, varlik, tecelli...)")
        print("  python tools/ekber_cli.py random-quote         : Rastgele bir hikmet vecizesi göster")
        print("  python tools/ekber_cli.py fusus [filtre]       : Fusûs 27 faslını listele")
        print("  python tools/ekber_cli.py futuhat              : Fütûhât meşhur bablarını listele")
        print("  python tools/ekber_cli.py ontology             : Ontoloji haritasını yazdır")
        print("\nÖrnekler:")
        print("  python tools/ekber_cli.py quote ask")
        print("  python tools/ekber_cli.py search velayet")
        print("  python tools/ekber_cli.py fusus harun")
        return

    cmd = sys.argv[1].lower()
    if cmd == "search" and len(sys.argv) >= 3:
        search_term(" ".join(sys.argv[2:]))
    elif cmd in ("quote", "alinti", "hikmet"):
        filter_word = sys.argv[2] if len(sys.argv) >= 3 else None
        show_quotes(filter_word)
    elif cmd in ("random-quote", "random", "hikmet-gunluk"):
        random_quote()
    elif cmd == "fusus":
        filter_text = sys.argv[2] if len(sys.argv) >= 3 else None
        list_fusus(filter_text)
    elif cmd == "futuhat":
        list_futuhat()
    elif cmd == "ontology":
        print_ontology()
    else:
        print("Geçersiz komut. Yardım için parametresiz çalıştırın.")

if __name__ == "__main__":
    main()
