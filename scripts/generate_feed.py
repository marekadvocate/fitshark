#!/usr/bin/env python3
"""
Generátor realistického B2B produktového feedu pre SK veľkoobchodného
distribútora automobilových dielov a príslušenstva.

Výstup: CSV s 10 000 SKU (1 riadok = 1 variant), jeden dodávateľ.
Trh SK, EUR, slovenčina, DPH 23 %.

Spustenie:  python3 generate_feed.py
"""

import csv
import random

# Deterministický výstup (reprodukovateľný feed)
random.seed(42)

ROWS = 10_000
SUPPLIER = "MotoDiely SK s.r.o."
CODE_PREFIX = ""  # voliteľná predpona kódu pre odlíšenie dodávateľov (multi-feed)
CURRENCY = "EUR"
VAT = 23
UPDATED = "2026-06-02"
OUTPUT = "automotive_feed_10k.csv"

# ── Reálne značky vozidiel na SK trhu (model, generácia/roky) ──────────────
VEHICLES = [
    ("Škoda Octavia", "II (1Z) 2004–2013"), ("Škoda Octavia", "III (5E) 2013–2020"),
    ("Škoda Fabia", "II (5J) 2007–2014"), ("Škoda Superb", "II (3T) 2008–2015"),
    ("Volkswagen Golf", "VI (5K) 2008–2013"), ("Volkswagen Golf", "VII 2012–2020"),
    ("Volkswagen Passat", "B7 2010–2014"), ("Volkswagen Passat", "B8 2014–2023"),
    ("Audi A4", "B8 2007–2015"), ("Audi A6", "C7 2011–2018"),
    ("BMW 3", "E90 2005–2012"), ("BMW 5", "F10 2010–2017"),
    ("Mercedes-Benz C", "W204 2007–2014"), ("Mercedes-Benz E", "W212 2009–2016"),
    ("Opel Astra", "J 2009–2015"), ("Opel Insignia", "A 2008–2017"),
    ("Ford Focus", "III 2010–2018"), ("Ford Mondeo", "IV 2007–2014"),
    ("Peugeot 308", "II 2013–2021"), ("Renault Mégane", "III 2008–2016"),
    ("Kia Ceed", "II (JD) 2012–2018"), ("Hyundai i30", "II (GD) 2011–2017"),
    ("Toyota Corolla", "E170 2013–2019"), ("Dacia Duster", "I 2010–2018"),
]

DELIVERY_BY_STATUS = {
    "Skladom": "24 h",
    "Na ceste": "2–3 dni",
    "Na objednávku": "7–14 dní",
    "Vypredané": "—",
}


def rand_price(low, high):
    """Náhodná cena v rozsahu, zaokrúhlená na 2 desatinné."""
    return round(random.uniform(low, high), 2)


def ean13():
    """EAN-13 s platnou kontrolnou číslicou (predpona 859 = SK)."""
    base = "859" + "".join(str(random.randint(0, 9)) for _ in range(9))
    s = sum((1 if i % 2 == 0 else 3) * int(d) for i, d in enumerate(base))
    check = (10 - s % 10) % 10
    return base + str(check)


def code(prefix, n):
    tag = f"{CODE_PREFIX}-" if CODE_PREFIX else ""
    return f"{tag}{prefix}-{n:06d}"


def availability():
    status = random.choices(
        ["Skladom", "Na ceste", "Na objednávku", "Vypredané"],
        weights=[60, 12, 25, 3],
    )[0]
    qty = {
        "Skladom": random.randint(5, 480),
        "Na ceste": random.randint(0, 40),
        "Na objednávku": 0,
        "Vypredané": 0,
    }[status]
    return status, qty, DELIVERY_BY_STATUS[status]


def vehicle():
    make, gen = random.choice(VEHICLES)
    return f"{make} {gen}"


# ── Definícia kategórií ────────────────────────────────────────────────────
# Každá kategória: generátor riadku ako dict atribútov produktu.

def brzdy():
    sub, brands, axis, vals, lo, hi, oe = random.choice([
        ("Brzdové kotúče", ["Brembo", "ATE", "TRW", "Bosch", "Febi"],
         "Náprava", ["Predná", "Zadná"], 18, 75, True),
        ("Brzdové platničky", ["Brembo", "ATE", "TRW", "Bosch", "Ferodo"],
         "Náprava", ["Predná sada", "Zadná sada"], 22, 68, True),
        ("Brzdový strmeň", ["TRW", "ATE", "Cifam"],
         "Strana", ["Predný ľavý", "Predný pravý", "Zadný ľavý", "Zadný pravý"], 45, 160, True),
        ("Brzdové čeľuste", ["TRW", "Bosch", "Febi"],
         "Náprava", ["Zadná sada"], 24, 55, True),
    ])
    brand = random.choice(brands)
    val = random.choice(vals)
    return dict(
        kat="Brzdový systém", sub=sub, znacka=brand,
        nazov=f"{sub} {brand} – {vehicle()}",
        popis=f"{sub} značky {brand} pre {val.lower()} nápravu. Originálna kvalita, "
              f"schválené na cestnú prevádzku (ECE R90).",
        axis=axis, val=val, voc=rand_price(lo, hi),
        hmot=round(random.uniform(0.8, 9.5), 2),
        rozmery=f"{random.choice([256,280,288,300,312,330])} mm",
        oe=oe, kompat=True, marza=(1.30, 1.55), zaruka=24,
    )


def filtre():
    sub, brands, lo, hi = random.choice([
        ("Olejový filter", ["Mann-Filter", "Mahle", "Bosch", "Hengst"], 4, 16),
        ("Vzduchový filter", ["Mann-Filter", "Mahle", "Bosch", "Filtron"], 6, 28),
        ("Kabínový filter", ["Mann-Filter", "Bosch", "Mahle"], 5, 24),
        ("Palivový filter", ["Mann-Filter", "Bosch", "Mahle", "Hengst"], 8, 35),
    ])
    brand = random.choice(brands)
    return dict(
        kat="Filtre", sub=sub, znacka=brand,
        nazov=f"{sub} {brand} – {vehicle()}",
        popis=f"{sub} {brand} pre spoľahlivú filtráciu. Presná lícovacia geometria, "
              f"dlhá životnosť podľa servisných intervalov výrobcu.",
        axis="Typ", val=random.choice(["Štandard", "Aktívne uhlie", "Vysoký prietok"]),
        voc=rand_price(lo, hi), hmot=round(random.uniform(0.1, 1.4), 2),
        rozmery="—", oe=True, kompat=True, marza=(1.35, 1.60), zaruka=24,
    )


def oleje():
    sub, brands = ("Motorový olej", ["Castrol", "Mobil", "Shell", "Valvoline", "Liqui Moly"])
    brand = random.choice(brands)
    visk = random.choice(["0W-20", "0W-30", "5W-30", "5W-40", "10W-40", "15W-40"])
    bal = random.choice(["1 L", "4 L", "5 L", "20 L"])
    base = {"1 L": (6, 14), "4 L": (24, 52), "5 L": (28, 64), "20 L": (95, 210)}[bal]
    return dict(
        kat="Prevádzkové kvapaliny", sub=sub, znacka=brand,
        nazov=f"{sub} {brand} {visk} {bal}",
        popis=f"Plne syntetický {sub.lower()} {brand} {visk}. Spĺňa normy ACEA a "
              f"schválenia výrobcov (VW, MB, BMW). Balenie {bal}.",
        axis="Viskozita / Balenie", val=f"{visk} / {bal}",
        voc=rand_price(*base), hmot=round({"1 L":1.0,"4 L":3.8,"5 L":4.7,"20 L":18.5}[bal], 1),
        rozmery=bal, oe=False, kompat=False, marza=(1.20, 1.45), zaruka=0,
    )


def kvapaliny():
    sub, brands, bal, lo, hi = random.choice([
        ("Chladiaca kvapalina", ["Febi", "Liqui Moly", "Castrol"], "1,5 L", 6, 18),
        ("Brzdová kvapalina DOT4", ["ATE", "Bosch", "TRW"], "0,5 L", 5, 14),
        ("AdBlue", ["BASF", "Liqui Moly"], "10 L", 9, 22),
        ("Kvapalina do ostrekovačov", ["Sheron", "Liqui Moly"], "3 L", 3, 9),
    ])
    brand = random.choice(brands)
    return dict(
        kat="Prevádzkové kvapaliny", sub=sub, znacka=brand,
        nazov=f"{sub} {brand} {bal}",
        popis=f"{sub} {brand}, balenie {bal}. Pripravená na priame použitie, "
              f"v súlade s technickými normami.",
        axis="Balenie", val=bal, voc=rand_price(lo, hi),
        hmot=round(random.uniform(0.6, 11.0), 1), rozmery=bal,
        oe=False, kompat=False, marza=(1.25, 1.50), zaruka=0,
    )


def pneumatiky():
    brand = random.choice(["Continental", "Michelin", "Goodyear", "Barum", "Matador", "Sava", "Bridgestone"])
    width = random.choice([175, 185, 195, 205, 215, 225, 235])
    profile = random.choice([45, 50, 55, 60, 65])
    diameter = random.choice([15, 16, 17, 18])
    season = random.choice(["Letná", "Zimná", "Celoročná"])
    li = random.randint(88, 99)
    si = random.choice(["H", "V", "W", "T"])
    size = f"{width}/{profile} R{diameter}"
    return dict(
        kat="Pneumatiky", sub=season + " pneumatika", znacka=brand,
        nazov=f"{brand} {size} {li}{si} – {season.lower()}",
        popis=f"{season} pneumatika {brand} {size}, index nosnosti {li}, "
              f"rýchlostný index {si}. EU štítok: palivo C, priľnavosť B, hluk 71 dB.",
        axis="Rozmer", val=f"{size} {li}{si}",
        voc=rand_price(38, 165), hmot=round(random.uniform(7.0, 12.5), 1),
        rozmery=size, oe=False, kompat=False, marza=(1.18, 1.40), zaruka=24,
    )


def disky():
    brand = random.choice(["Borbet", "Alcar", "Ronal", "Dezent", "OE"])
    typ = random.choice(["Hliníkový disk", "Oceľový disk"])
    diameter = random.choice([15, 16, 17, 18])
    width = random.choice([6.0, 6.5, 7.0, 7.5, 8.0])
    pcd = random.choice(["5x112", "5x114,3", "4x100", "5x108"])
    et = random.choice([35, 40, 45, 48, 50])
    return dict(
        kat="Disky", sub=typ, znacka=brand,
        nazov=f"{typ} {brand} {width}Jx{diameter} {pcd} ET{et}",
        popis=f"{typ} {brand}, rozmer {width}Jx{diameter}, rozteč {pcd}, "
              f"ET{et}. Certifikované, vhodné pre celoročné použitie.",
        axis="Rozmer", val=f"{width}Jx{diameter} {pcd} ET{et}",
        voc=rand_price(28, 140), hmot=round(random.uniform(6.5, 13.0), 1),
        rozmery=f"{width}Jx{diameter}", oe=False, kompat=False, marza=(1.25, 1.55), zaruka=24,
    )


def baterie():
    brand = random.choice(["Varta", "Exide", "Bosch", "Banner"])
    cap = random.choice([44, 54, 60, 70, 74, 80, 95])
    return dict(
        kat="Elektrika", sub="Autobatéria", znacka=brand,
        nazov=f"Autobatéria {brand} {cap} Ah 12V",
        popis=f"Štartovacia autobatéria {brand} {cap} Ah, 12 V. Bezúdržbová, "
              f"vysoký štartovací prúd, vhodná aj pre vozidlá so štart-stop.",
        axis="Kapacita", val=f"{cap} Ah",
        voc=rand_price(48, 165), hmot=round(random.uniform(11.0, 22.0), 1),
        rozmery="242x175x190 mm", oe=False, kompat=True, marza=(1.20, 1.40), zaruka=24,
    )


def diely_ostatne():
    sub, brands, lo, hi, oe = random.choice([
        ("Tlmič pruženia", ["Sachs", "Bilstein", "KYB", "Monroe"], 35, 130, True),
        ("Spojková sada", ["Sachs", "LuK", "Valeo"], 95, 320, True),
        ("Vodná pumpa", ["SKF", "Gates", "Hepu"], 28, 95, True),
        ("Ložisko kolesa", ["SKF", "FAG", "SNR"], 22, 88, True),
        ("Zapaľovacia sviečka", ["NGK", "Denso", "Bosch"], 3, 14, True),
        ("Zapaľovacia cievka", ["Bosch", "NGK", "Beru"], 25, 75, True),
        ("Rozvodová sada", ["Gates", "INA", "Contitech"], 55, 180, True),
        ("Výfukový tlmič", ["Bosal", "Walker", "Ernst"], 40, 145, True),
    ])
    brand = random.choice(brands)
    return dict(
        kat="Náhradné diely", sub=sub, znacka=brand,
        nazov=f"{sub} {brand} – {vehicle()}",
        popis=f"{sub} {brand}. Presné lícovanie podľa OE špecifikácie, "
              f"overená spoľahlivosť a životnosť.",
        axis="Strana", val=random.choice(["Ľavý", "Pravý", "—", "Sada"]),
        voc=rand_price(lo, hi), hmot=round(random.uniform(0.3, 12.0), 2),
        rozmery="—", oe=oe, kompat=True, marza=(1.30, 1.55), zaruka=24,
    )


def doplnky():
    sub, brands, lo, hi = random.choice([
        ("Gumové koberce (sada)", ["Petex", "Rezaw-Plast", "Frogum"], 12, 45),
        ("Textilné koberce (sada)", ["Petex", "AutoMega"], 9, 32),
        ("Autopoťahy (sada)", ["Kegel", "Petex"], 25, 95),
        ("Autokozmetika – šampón", ["Sonax", "Meguiar's", "K2"], 4, 18),
        ("Držiak telefónu", ["Cellularline", "Baseus"], 6, 24),
        ("Štartovacie káble", ["Bottari", "K2"], 9, 38),
        ("Strešný box", ["Thule", "Hapro"], 180, 520),
        ("Snehové reťaze", ["Pewag", "Konig"], 35, 120),
    ])
    brand = random.choice(brands)
    return dict(
        kat="Autodoplnky", sub=sub, znacka=brand,
        nazov=f"{sub} {brand}",
        popis=f"{sub} {brand}. Kvalitné spracovanie, jednoduchá montáž, "
              f"univerzálne alebo modelovo špecifické prevedenie.",
        axis="Prevedenie", val=random.choice(["Univerzál", "Čierna", "Sivá", "Sada"]),
        voc=rand_price(lo, hi), hmot=round(random.uniform(0.1, 9.0), 2),
        rozmery="—", oe=False, kompat=False, marza=(1.35, 1.70), zaruka=12,
    )


def ziarovky_stierace():
    sub, brands, lo, hi = random.choice([
        ("Žiarovka H7", ["Osram", "Philips", "Bosch"], 2, 12),
        ("Žiarovka LED", ["Osram", "Philips"], 14, 48),
        ("Stierač (sada)", ["Bosch", "Valeo", "SWF"], 8, 32),
    ])
    brand = random.choice(brands)
    return dict(
        kat="Osvetlenie a viditeľnosť", sub=sub, znacka=brand,
        nazov=f"{sub} {brand} – {vehicle()}",
        popis=f"{sub} {brand}. Vysoká svietivosť / dokonalé stieranie, "
              f"dlhá životnosť, schválené pre cestnú prevádzku.",
        axis="Balenie", val=random.choice(["1 ks", "2 ks (pár)", "Sada"]),
        voc=rand_price(lo, hi), hmot=round(random.uniform(0.05, 0.8), 2),
        rozmery="—", oe=False, kompat=True, marza=(1.30, 1.60), zaruka=12,
    )


# Rozdelenie 10k SKU naprieč generátormi (váhy ~ podiel sortimentu)
GENERATORS = [
    (brzdy, 14), (filtre, 12), (diely_ostatne, 18), (oleje, 8),
    (kvapaliny, 6), (pneumatiky, 12), (disky, 6), (baterie, 4),
    (doplnky, 12), (ziarovky_stierace, 8),
]
gen_funcs = [g for g, _ in GENERATORS]
gen_weights = [w for _, w in GENERATORS]

HEADER = [
    "dodavatelsky_kod", "ean", "mpn", "oe_cislo", "znacka", "dodavatel",
    "nazov_produktu", "popis", "kategoria", "podkategoria", "typ_variantu",
    "hodnota_variantu", "voc_bez_dph_eur", "moc_s_dph_eur", "mena", "dph_sadzba_pct",
    "sklad_mnozstvo", "dostupnost", "doba_dodania", "min_objednavka", "ks_v_baleni",
    "hmotnost_kg", "rozmery", "zaruka_mesiace", "kompatibilita_vozidla", "datum_aktualizacie",
]


def build_record(i):
    """Kanonický záznam (dict) — schéma-neutrálny, mapovateľný do feedu dodávateľa."""
    g = random.choices(gen_funcs, weights=gen_weights)[0]()
    voc = g["voc"]
    marza = random.uniform(*g["marza"])
    moc = round(voc * marza * (1 + VAT / 100), 2)
    status, qty, delivery = availability()
    prefix = {
        "Brzdový systém": "BRK", "Filtre": "FLT", "Náhradné diely": "PRT",
        "Prevádzkové kvapaliny": "FLU", "Pneumatiky": "TYR", "Disky": "RIM",
        "Elektrika": "BAT", "Autodoplnky": "ACC", "Osvetlenie a viditeľnosť": "LGT",
    }.get(g["kat"], "GEN")
    return {
        "dodavatelsky_kod": code(prefix, i),
        "ean": ean13(),
        "mpn": f"{g['znacka'][:3].upper()}{random.randint(10000, 999999)}",
        "oe_cislo": f"OE{random.randint(1000000, 9999999)}" if g["oe"] else "",
        "znacka": g["znacka"], "dodavatel": SUPPLIER,
        "nazov_produktu": g["nazov"], "popis": g["popis"],
        "kategoria": g["kat"], "podkategoria": g["sub"],
        "typ_variantu": g["axis"], "hodnota_variantu": g["val"],
        "voc_bez_dph_eur": f"{voc:.2f}", "moc_s_dph_eur": f"{moc:.2f}",
        "mena": CURRENCY, "dph_sadzba_pct": VAT,
        "sklad_mnozstvo": qty, "dostupnost": status, "doba_dodania": delivery,
        "min_objednavka": random.choice([1, 1, 1, 2, 4, 5, 10]),
        "ks_v_baleni": random.choice([1, 1, 1, 2, 4]),
        "hmotnost_kg": f"{g['hmot']:.2f}", "rozmery": g["rozmery"],
        "zaruka_mesiace": g["zaruka"],
        "kompatibilita_vozidla": vehicle() if g["kompat"] else "Univerzálne",
        "datum_aktualizacie": UPDATED,
    }


def build_row(i):
    rec = build_record(i)
    return [rec[k] for k in HEADER]


def main():
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for i in range(1, ROWS + 1):
            w.writerow(build_row(i))
    print(f"Hotovo: {OUTPUT} ({ROWS} riadkov, {len(HEADER)} stĺpcov)")


if __name__ == "__main__":
    main()
