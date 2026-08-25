#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import unicodedata

# Fix Windows console UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    replacements = {
        'â': 'a', 'î': 'i', 'û': 'u', 'ô': 'o', 'ê': 'e',
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c',
        '‘': '', '’': '', "'": '', '-': ' ', '—': ' '
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.strip()

GLOSSARY = {
    "vahdet-i vucud": "Varlığın ontolojik birliği; mutlak anlamda var olan yalnızca Hakk'tır, kesret O'nun esmâ tecellisidir.",
    "ayan-i sabite": "Eşyanın henüz dış dünyada zuhur etmeden önce Allah'ın ezeli ilmindeki sabit hakikatleri ve potansiyelleri.",
    "insan-i kamil": "Bütün ilahi isim ve mertebeleri kendinde cem eden, kâinatın manevi direği ve Hakk'ın halifesi.",
    "nefes-i rahmani": "İlahi varlık nefesi; harflerin ve kâinatın yokluktan varlığa çıkışını sağlayan rahmet cereyanı.",
    "alem-i misal": "Ruh ile madde arasındaki berzah boyutu; mânanın suret kazandığı rüya ve hayal âlemi.",
    "hazarat-i hams": "Beş İlahi Mertebe: Zât (Gayb-ı Mutlak), Vâhidiyyet, Ceberût, Melekût, Şehâdet.",
    "la tekrara fit-tecelli": "Tecellide asla tekrar yoktur; Hakk her an yeni bir şe'nde tecelli eder.",
    "hakkul-yakin": "İkiliğin tamamen ortadan kalktığı, tevhîdin bizzat zevk ve tecrübe ile bilindiği son makam.",
    "feyz-i akdes": "Zât'ın kendi zâtına tecellisiyle a'yân-ı sâbitenin ve ezelî istidatların ilâhî ilimde taayyün etmesi.",
    "feyz-i mukaddes": "A'yân-ı sâbitenin haricî vücûd kazanarak dış dünyada zuhûra gelmesi.",
    "berzah": "İki zıt veya farklı hakikat arasında köprü kuran engel, geçit ve irtibat boyutu."
}

FUSUS_FASLS = [
    (1, "Hz. Âdem", "Hikmet-i İlâhiyye", "Âlemin yaratılışı, ayna metaforu ve hilafet"),
    (2, "Hz. Şît", "Hikmet-i Nefsiyye", "Hibe, bağış ve ilahi isimlerin sırları"),
    (3, "Hz. Nûh", "Hikmet-i Sübbûhiyye", "Tenzih ve teşbih dengesi; tevhîdin kuşatıcılığı"),
    (4, "Hz. İdrîs", "Hikmet-i Kuddûsiyye", "Yücelik mertebesi ve mekânsal tenzih"),
    (5, "Hz. İbrâhîm", "Hikmet-i Müheymiyye", "Aşkta fena hali ve ilahi dostluk (Hullet)"),
    (6, "Hz. İshâk", "Hikmet-i Hakkiyye", "Rüyaların tabiri ve kurban sırrı"),
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
    (17, "Hz. Dâvûd", "Hikmet-i Vücûdiyye", "Hilafet, demirin yumuşatılması ve hüküm"),
    (18, "Hz. Yûnus", "Hikmet-i Nefesiyye", "Tabiatın karanlığı ve balığın karnındaki tesbih"),
    (19, "Hz. Eyyûb", "Hikmet-i Gaybiyye", "Bela, sabır ve su ile arınmanın şifası"),
    (20, "Hz. Yahyâ", "Hikmet-i Celâliyye", "İlahi isimlerin celali ve bekâ hali"),
    (21, "Hz. Zekeriyyâ", "Hikmet-i Mâlikiyye", "İhtiyarlıkta gelen rahmet ve varlık bağışı"),
    (22, "Hz. İlyâs", "Hikmet-i İnsiyye", "Tabiat ile akıl arasındaki denge"),
    (23, "Hz. Lokmân", "Hikmet-i İhsâniyye", "Şirkten arınma ve hikmetin derinliği"),
    (24, "Hz. Hârûn", "Hikmet-i İmâmiyye", "Surete tapınma uyarısı ve rahmetin önceliği"),
    (25, "Hz. Mûsâ", "Hikmet-i Ulviyye", "Firavun ile münazara, asâ mucizesi ve tecellî"),
    (26, "Hz. Hâlid b. Sinân", "Hikmet-i Samediyye", "Berzah âleminin haberleri"),
    (27, "Hz. Muhammed", "Hikmet-i Ferdiyye", "Varlığın gayesi, üç sevdirilen şey ve Hatm-i Nübüvvet")
]

def banner():
    print("=" * 70)
    print("   [📖] IBN-ARABI-STUDIES • ARAŞTIRMA VE KAVRAM MOTORU v2.0")
    print("   Muhyiddin İbnü'l-Arabî Külliyatı & Ontolojik Dizin")
    print("=" * 70)

def search_term(query):
    n_query = normalize_text(query)
    found = False
    print(f"\n[🔍] '{query}' için Sözlük Arama Sonuçları:")
    print("-" * 50)
    for term, desc in GLOSSARY.items():
        n_term = normalize_text(term)
        n_desc = normalize_text(desc)
        if n_query in n_term or n_query in n_desc or any(w in n_desc for w in n_query.split()):
            print(f"📌 {term.upper()}:\n   {desc}\n")
            found = True
    if not found:
        print("❌ Eşleşen terim bulunamadı. docs/terminology-glossary.md dosyasına göz atın.")

def list_fusus(filter_text=None):
    print("\n[💎] FUSÛSÜ'L-HİKEM 27 PEYGAMBER VE HİKMET LİSTESİ:")
    print("-" * 70)
    print(f"{'#':<4} {'Peygamber':<18} {'Hikmet Türü':<24} {'Temel Mesele'}")
    print("-" * 70)
    n_filter = normalize_text(filter_text) if filter_text else None
    for num, prophet, wisdom, subject in FUSUS_FASLS:
        n_p = normalize_text(prophet)
        n_w = normalize_text(wisdom)
        n_s = normalize_text(subject)
        if n_filter is None or n_filter in n_p or n_filter in n_w or n_filter in n_s:
            print(f"{num:<4} {prophet:<18} {wisdom:<24} {subject}")
    print("-" * 70)

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
        print("  python tools/ekber_cli.py search <kavram>   : Terim sözlüğünde arama yap")
        print("  python tools/ekber_cli.py fusus [filtre]    : Fusûs 27 faslını listele")
        print("  python tools/ekber_cli.py ontology          : Ontoloji haritasını yazdır")
        print("\nÖrnek:")
        print("  python tools/ekber_cli.py search nefes")
        print("  python tools/ekber_cli.py fusus musa")
        return

    cmd = sys.argv[1].lower()
    if cmd == "search" and len(sys.argv) >= 3:
        search_term(" ".join(sys.argv[2:]))
    elif cmd == "fusus":
        filter_text = sys.argv[2] if len(sys.argv) >= 3 else None
        list_fusus(filter_text)
    elif cmd == "ontology":
        print_ontology()
    else:
        print("Geçersiz komut. Yardım için parametresiz çalıştırın.")

if __name__ == "__main__":
    main()
