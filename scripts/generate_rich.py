#!/usr/bin/env python3
"""
Detailné automobilové feedy pripravené na PRIAME KOPÍROVANIE do Google Sheets.

Formát: TAB-oddeľované (.tsv) → otvor súbor, Ctrl/Cmd+A, Cmd+C, vlož do A1.
Google Sheets automaticky rozdelí do stĺpcov (žiadny import dialóg).

~60 parametrov na produkt. 11 rôznych dodávateľov, 10 000 SKU každý.
Trh SK, EUR, DPH 23 %.

Spustenie:  python3 generate_rich.py
"""

import csv
import generate_feed as gf

rnd = gf.random
VAT = gf.VAT
VEHICLES = gf.VEHICLES
UPDATED = gf.UPDATED


# ── Pomocné dáta ───────────────────────────────────────────────────────────
ORIGIN = ["Nemecko", "Česko", "Poľsko", "Taliansko", "Francúzsko", "Španielsko",
          "Slovensko", "Turecko", "Japonsko", "Čína"]
WAREHOUSE = ["BA-01 Bratislava", "ZA-02 Žilina", "KE-03 Košice",
             "DC-PRG Praha", "DC-WIEN Viedeň"]
PACKAGING = ["Kartón", "Blister", "Fólia", "Plastová nádoba", "Sada v krabici"]

HS_CODES = {
    "Brzdový systém": "8708.30", "Filtre": "8421.23", "Náhradné diely": "8708.99",
    "Prevádzkové kvapaliny": "3819.00", "Pneumatiky": "4011.10", "Disky": "8708.70",
    "Elektrika": "8507.10", "Autodoplnky": "8708.29", "Osvetlenie a viditeľnosť": "8512.20",
}
CAT_CODE = {
    "Brzdový systém": "BRK", "Filtre": "FLT", "Náhradné diely": "PRT",
    "Prevádzkové kvapaliny": "FLU", "Pneumatiky": "TYR", "Disky": "RIM",
    "Elektrika": "BAT", "Autodoplnky": "ACC", "Osvetlenie a viditeľnosť": "LGT",
}


def price(lo, hi):
    return round(rnd.uniform(lo, hi), 2)


def vehicle():
    mk, gen = rnd.choice(VEHICLES)
    return f"{mk} {gen}"


def years_from_vehicle(v):
    """Vytiahne roky 'od–do' z reťazca kompatibility (napr. '2007–2013')."""
    for tok in v.replace("–", "-").split():
        if "-" in tok and tok[:4].isdigit():
            a, _, b = tok.partition("-")
            return a, (b if b.isdigit() else "")
    return "", ""


def avail():
    status = rnd.choices(["Skladom", "Na ceste", "Na objednávku", "Vypredané"],
                         weights=[60, 12, 25, 3])[0]
    qty = {"Skladom": rnd.randint(5, 480), "Na ceste": rnd.randint(0, 40),
           "Na objednávku": 0, "Vypredané": 0}[status]
    days = {"Skladom": 1, "Na ceste": 3, "Na objednávku": rnd.choice([7, 10, 14]),
            "Vypredané": 0}[status]
    txt = {"Skladom": "24 h", "Na ceste": "2–3 dni",
           "Na objednávku": f"{days} dní", "Vypredané": "—"}[status]
    return status, qty, txt, days


# ── Generátory kategórií (vracajú detailný dict atribútov) ──────────────────
def brzdy():
    sub, brands, pos, lo, hi = rnd.choice([
        ("Brzdové kotúče", ["Brembo", "ATE", "TRW", "Bosch", "Zimmermann"], "Predná/Zadná náprava", 18, 75),
        ("Brzdové platničky", ["Brembo", "ATE", "TRW", "Ferodo", "Bosch"], "Predná/Zadná náprava", 22, 68),
        ("Brzdový strmeň", ["TRW", "ATE", "Cifam"], "Os kolesa", 45, 160),
        ("Brzdové čeľuste", ["TRW", "Bosch", "Febi"], "Zadná náprava", 24, 55),
    ])
    b = rnd.choice(brands)
    dia = rnd.choice([256, 280, 288, 300, 312, 330])
    deposit = price(20, 60) if sub == "Brzdový strmeň" else 0
    return dict(
        kat="Brzdový systém", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}, priemer {dia} mm",
        dlhy=f"{sub} značky {b} s priemerom {dia} mm. Schválené podľa ECE R90, "
             f"povrchová úprava proti korózii, vyvážené pre nízku hlučnosť.",
        voc=price(lo, hi), marza=(1.30, 1.55), zaruka=24, oe=True, kompat=True,
        hmot=round(rnd.uniform(0.8, 9.5), 2), dims=(dia, dia, rnd.randint(18, 90)),
        norma="ECE R90", pozicia=pos, strana=rnd.choice(["Ľavá", "Pravá", ""]),
        deposit=deposit,
    )


def filtre():
    sub, brands, lo, hi = rnd.choice([
        ("Olejový filter", ["Mann-Filter", "Mahle", "Bosch", "Hengst"], 4, 16),
        ("Vzduchový filter", ["Mann-Filter", "Mahle", "Bosch", "Filtron"], 6, 28),
        ("Kabínový filter", ["Mann-Filter", "Bosch", "Mahle"], 5, 24),
        ("Palivový filter", ["Mann-Filter", "Bosch", "Mahle", "Hengst"], 8, 35),
    ])
    b = rnd.choice(brands)
    typ = rnd.choice(["Štandard", "Aktívne uhlie", "Vysoký prietok"])
    return dict(
        kat="Filtre", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}, typ {typ}",
        dlhy=f"{sub} {b} ({typ}). Presná lícovacia geometria, vysoká filtračná "
             f"účinnosť a dlhá životnosť podľa servisných intervalov výrobcu.",
        voc=price(lo, hi), marza=(1.35, 1.60), zaruka=24, oe=True, kompat=True,
        hmot=round(rnd.uniform(0.1, 1.4), 2), dims=(rnd.randint(60, 300), rnd.randint(60, 250), rnd.randint(30, 120)),
        norma="ISO 4548", variant_typ="Typ filtra", variant_val=typ,
    )


def oleje():
    b = rnd.choice(["Castrol", "Mobil", "Shell", "Valvoline", "Liqui Moly"])
    visk = rnd.choice(["0W-20", "0W-30", "5W-30", "5W-40", "10W-40", "15W-40"])
    bal = rnd.choice([1, 4, 5, 20])
    base = {1: (6, 14), 4: (24, 52), 5: (28, 64), 20: (95, 210)}[bal]
    voc = price(*base)
    acea = rnd.choice(["A3/B4", "C2", "C3", "A5/B5"])
    api = rnd.choice(["SN", "SP", "SN PLUS"])
    return dict(
        kat="Prevádzkové kvapaliny", sub="Motorový olej", znacka=b, vyrobca=b,
        nazov=f"Motorový olej {b} {visk} {bal} L",
        kratky=f"Syntetický olej {b} {visk}, balenie {bal} L",
        dlhy=f"Plne syntetický motorový olej {b} {visk}. Normy ACEA {acea}, API {api}, "
             f"schválenia VW/MB/BMW. Balenie {bal} L.",
        voc=voc, marza=(1.20, 1.45), zaruka=0, oe=False, kompat=False,
        hmot=round({1: 1.0, 4: 3.8, 5: 4.7, 20: 18.5}[bal], 1),
        dims=(rnd.randint(90, 300), rnd.randint(90, 300), rnd.randint(120, 400)),
        objem=float(bal), jednotka="€/L", norma=f"ACEA {acea} / API {api}",
        variant_typ="Viskozita/Balenie", variant_val=f"{visk} / {bal} L",
        olej_visk=visk, olej_norma=f"ACEA {acea}, API {api}",
    )


def kvapaliny():
    sub, brands, vol, lo, hi, norma = rnd.choice([
        ("Chladiaca kvapalina", ["Febi", "Liqui Moly", "Castrol"], 1.5, 6, 18, "G12++"),
        ("Brzdová kvapalina", ["ATE", "Bosch", "TRW"], 0.5, 5, 14, "DOT 4"),
        ("AdBlue", ["BASF", "Liqui Moly"], 10, 9, 22, "ISO 22241"),
        ("Kvapalina do ostrekovačov", ["Sheron", "Liqui Moly"], 3, 3, 9, "—"),
    ])
    b = rnd.choice(brands)
    return dict(
        kat="Prevádzkové kvapaliny", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b} {vol} L", kratky=f"{sub} {b}, {vol} L, {norma}",
        dlhy=f"{sub} {b}, norma {norma}, balenie {vol} L. Pripravená na priame "
             f"použitie, v súlade s technickými špecifikáciami výrobcov vozidiel.",
        voc=price(lo, hi), marza=(1.25, 1.50), zaruka=0, oe=False, kompat=False,
        hmot=round(vol * rnd.uniform(1.0, 1.1), 2),
        dims=(rnd.randint(90, 250), rnd.randint(90, 250), rnd.randint(150, 400)),
        objem=float(vol), jednotka="€/L", norma=norma,
        variant_typ="Balenie", variant_val=f"{vol} L",
    )


def pneumatiky():
    b = rnd.choice(["Continental", "Michelin", "Goodyear", "Barum", "Matador", "Sava", "Bridgestone"])
    w = rnd.choice([175, 185, 195, 205, 215, 225, 235]); pr = rnd.choice([45, 50, 55, 60, 65])
    di = rnd.choice([15, 16, 17, 18]); li = rnd.randint(88, 99); si = rnd.choice(["H", "V", "W", "T"])
    size = f"{w}/{pr} R{di}"; season = rnd.choice(["Letná", "Zimná", "Celoročná"])
    fuel = rnd.choice(["B", "C", "D", "E"]); grip = rnd.choice(["A", "B", "C"]); noise = rnd.randint(68, 73)
    return dict(
        kat="Pneumatiky", sub=f"{season} pneumatika", znacka=b, vyrobca=b,
        nazov=f"{b} {size} {li}{si} {season.lower()}",
        kratky=f"{season} pneu {b} {size} {li}{si}",
        dlhy=f"{season} pneumatika {b} {size}, nosnosť {li}, rýchlosť {si}. "
             f"EÚ štítok: palivo {fuel}, priľnavosť na mokre {grip}, hluk {noise} dB.",
        voc=price(38, 165), marza=(1.18, 1.40), zaruka=24, oe=False, kompat=False,
        hmot=round(rnd.uniform(7.0, 12.5), 1), dims=(di * 25 + 100, w, w),
        norma="ECE R30", pneu_rozmer=f"{size} {li}{si}", pneu_sezona=season,
        eu_fuel=fuel, eu_grip=grip, eu_noise=noise,
        variant_typ="Rozmer", variant_val=f"{size} {li}{si}",
    )


def disky():
    b = rnd.choice(["Borbet", "Alcar", "Ronal", "Dezent", "OE"])
    typ = rnd.choice(["Hliníkový disk", "Oceľový disk"]); di = rnd.choice([15, 16, 17, 18])
    w = rnd.choice([6.0, 6.5, 7.0, 7.5, 8.0]); pcd = rnd.choice(["5x112", "5x114,3", "4x100", "5x108"])
    et = rnd.choice([35, 40, 45, 48, 50])
    return dict(
        kat="Disky", sub=typ, znacka=b, vyrobca=b,
        nazov=f"{typ} {b} {w}Jx{di} {pcd} ET{et}",
        kratky=f"{typ} {b} {w}Jx{di}, {pcd}, ET{et}",
        dlhy=f"{typ} {b}, {w}Jx{di}, rozteč {pcd}, ET{et}. Certifikované (TÜV), "
             f"vhodné na celoročné použitie, povrchová úprava lakovaním.",
        voc=price(28, 140), marza=(1.25, 1.55), zaruka=24, oe=False, kompat=False,
        hmot=round(rnd.uniform(6.5, 13.0), 1), dims=(di * 25 + 50, di * 25 + 50, int(w * 25)),
        norma="TÜV / ECE", variant_typ="Rozmer", variant_val=f"{w}Jx{di} {pcd} ET{et}",
    )


def baterie():
    b = rnd.choice(["Varta", "Exide", "Bosch", "Banner"]); cap = rnd.choice([44, 54, 60, 70, 74, 80, 95])
    cca = cap * rnd.choice([9, 10, 11])
    return dict(
        kat="Elektrika", sub="Autobatéria", znacka=b, vyrobca=b,
        nazov=f"Autobatéria {b} {cap} Ah 12V {cca}A",
        kratky=f"Autobatéria {b} {cap} Ah, štart. prúd {cca} A",
        dlhy=f"Štartovacia batéria {b} {cap} Ah, 12 V, štartovací prúd {cca} A. "
             f"Bezúdržbová, vhodná pre vozidlá so systémom štart-stop.",
        voc=price(48, 165), marza=(1.20, 1.40), zaruka=24, oe=False, kompat=True,
        hmot=round(rnd.uniform(11.0, 22.0), 1), dims=(242, 175, 190),
        deposit=price(8, 15), norma="EN 50342", variant_typ="Kapacita", variant_val=f"{cap} Ah",
    )


def diely_ostatne():
    sub, brands, lo, hi, repas = rnd.choice([
        ("Tlmič pruženia", ["Sachs", "Bilstein", "KYB", "Monroe"], 35, 130, False),
        ("Spojková sada", ["Sachs", "LuK", "Valeo"], 95, 320, False),
        ("Vodná pumpa", ["SKF", "Gates", "Hepu"], 28, 95, False),
        ("Ložisko kolesa", ["SKF", "FAG", "SNR"], 22, 88, False),
        ("Zapaľovacia sviečka", ["NGK", "Denso", "Bosch"], 3, 14, False),
        ("Zapaľovacia cievka", ["Bosch", "NGK", "Beru"], 25, 75, False),
        ("Rozvodová sada", ["Gates", "INA", "Contitech"], 55, 180, False),
        ("Alternátor", ["Bosch", "Valeo", "Denso"], 90, 280, True),
        ("Štartér", ["Bosch", "Valeo", "Denso"], 80, 240, True),
    ])
    b = rnd.choice(brands)
    return dict(
        kat="Náhradné diely", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}",
        dlhy=f"{sub} {b}. Presné lícovanie podľa OE špecifikácie, overená "
             f"spoľahlivosť a životnosť. {'Repasovaný diel s vratnou zálohou.' if repas else ''}".strip(),
        voc=price(lo, hi), marza=(1.30, 1.55), zaruka=24, oe=True, kompat=True,
        hmot=round(rnd.uniform(0.3, 12.0), 2),
        dims=(rnd.randint(50, 400), rnd.randint(50, 300), rnd.randint(30, 250)),
        stav=("Repasovaný" if repas else "Nový"),
        deposit=(price(25, 90) if repas else 0),
        pozicia=rnd.choice(["Predná náprava", "Zadná náprava", "Motor", ""]),
        strana=rnd.choice(["Ľavá", "Pravá", "", "Sada"]),
    )


def doplnky():
    sub, brands, lo, hi = rnd.choice([
        ("Gumové koberce (sada)", ["Petex", "Rezaw-Plast", "Frogum"], 12, 45),
        ("Textilné koberce (sada)", ["Petex", "AutoMega"], 9, 32),
        ("Autopoťahy (sada)", ["Kegel", "Petex"], 25, 95),
        ("Autošampón", ["Sonax", "Meguiar's", "K2"], 4, 18),
        ("Držiak telefónu", ["Cellularline", "Baseus"], 6, 24),
        ("Štartovacie káble", ["Bottari", "K2"], 9, 38),
        ("Strešný box", ["Thule", "Hapro"], 180, 520),
        ("Snehové reťaze", ["Pewag", "Konig"], 35, 120),
    ])
    b = rnd.choice(brands); farba = rnd.choice(["Čierna", "Sivá", "Béžová", "—"])
    return dict(
        kat="Autodoplnky", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}, {farba.lower()}",
        dlhy=f"{sub} {b}. Kvalitné spracovanie, jednoduchá montáž, univerzálne "
             f"alebo modelovo špecifické prevedenie.",
        voc=price(lo, hi), marza=(1.35, 1.70), zaruka=12, oe=False, kompat=False,
        hmot=round(rnd.uniform(0.1, 9.0), 2),
        dims=(rnd.randint(50, 600), rnd.randint(50, 400), rnd.randint(20, 300)),
        farba=farba, variant_typ="Prevedenie", variant_val=rnd.choice(["Univerzál", farba, "Sada"]),
    )


def ziarovky_stierace():
    sub, brands, lo, hi = rnd.choice([
        ("Žiarovka H7", ["Osram", "Philips", "Bosch"], 2, 12),
        ("Žiarovka LED", ["Osram", "Philips"], 14, 48),
        ("Stierač (sada)", ["Bosch", "Valeo", "SWF"], 8, 32),
    ])
    b = rnd.choice(brands)
    return dict(
        kat="Osvetlenie a viditeľnosť", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}",
        dlhy=f"{sub} {b}. Vysoká svietivosť / dokonalé stieranie, dlhá životnosť, "
             f"schválené pre cestnú prevádzku (ECE).",
        voc=price(lo, hi), marza=(1.30, 1.60), zaruka=12, oe=False, kompat=True,
        hmot=round(rnd.uniform(0.05, 0.8), 2),
        dims=(rnd.randint(40, 700), rnd.randint(20, 60), rnd.randint(20, 60)),
        norma="ECE R37/R112", variant_typ="Balenie", variant_val=rnd.choice(["1 ks", "2 ks (pár)", "Sada"]),
    )


GENERATORS = [
    (brzdy, 14), (filtre, 12), (diely_ostatne, 18), (oleje, 8), (kvapaliny, 6),
    (pneumatiky, 12), (disky, 6), (baterie, 4), (doplnky, 12), (ziarovky_stierace, 8),
]
GEN_FUNCS = [g for g, _ in GENERATORS]
DEFAULT_W = [w for _, w in GENERATORS]


# ── Zostavenie detailného záznamu (~60 parametrov) ─────────────────────────
COLUMNS = [
    "riadok_id", "dodavatelsky_kod", "ean", "mpn", "oe_cisla", "tecdoc_id",
    "znacka", "vyrobca", "dodavatel",
    "kategoria", "podkategoria", "kategoria_kod",
    "nazov_produktu", "kratky_popis", "dlhy_popis",
    "typ_variantu", "hodnota_variantu", "pozicia_montaze", "strana", "farba",
    "mena", "dph_sadzba_pct", "voc_bez_dph", "voc_s_dph", "moc_bez_dph", "moc_s_dph",
    "marza_pct", "rabat_pct", "akciova_cena_s_dph", "cena_za_jednotku", "jednotka_ceny",
    "zaloha_za_diel",
    "sklad_mnozstvo", "sklad_lokalita", "dostupnost", "doba_dodania", "doba_dodania_dni",
    "min_objednavka", "objednavkovy_nasobok", "ks_v_baleni", "balenie_typ", "expedicia_do",
    "hmotnost_netto_kg", "hmotnost_brutto_kg", "dlzka_mm", "sirka_mm", "vyska_mm",
    "objem_l", "rozmery_text",
    "kompatibilita_vozidla", "rok_vyroby_od", "rok_vyroby_do", "norma_certifikat",
    "colny_kod_hs", "krajina_povodu", "stav_tovaru", "zaruka_mesiace",
    "pneu_sezonnost", "eu_stitok_palivo", "eu_stitok_prilnavost", "eu_stitok_hluk_db",
    "olej_viskozita", "olej_norma",
    "obrazok_url", "datasheet_url", "aktivny", "datum_aktualizacie",
]


def build_record(i, supplier, sup_prefix):
    g = rnd.choices(GEN_FUNCS, weights=rnd.gen_w)[0]()
    voc = g["voc"]
    marza = rnd.uniform(*g["marza"])
    voc_dph = round(voc * (1 + VAT / 100), 2)
    moc = round(voc * marza, 2)
    moc_dph = round(moc * (1 + VAT / 100), 2)
    marza_pct = round((moc - voc) / voc * 100, 1)
    rabat = rnd.choice([0, 0, 0, 5, 10, 15])
    akcia = round(moc_dph * (1 - rabat / 100), 2) if rabat else ""
    objem = g.get("objem")
    cena_jednotka = round(moc_dph / objem, 2) if objem else ""
    status, qty, dod_txt, dod_dni = avail()
    code = f"{sup_prefix}-{CAT_CODE.get(g['kat'], 'GEN')}-{i:06d}"
    kompat = vehicle() if g["kompat"] else "Univerzálne"
    rok_od, rok_do = years_from_vehicle(kompat) if g["kompat"] else ("", "")
    l, w, h = g["dims"]
    n_oe = rnd.randint(1, 3) if g["oe"] else 0
    oe = ";".join(f"OE{rnd.randint(1000000, 9999999)}" for _ in range(n_oe))
    slug = code.lower()

    return {
        "riadok_id": i,
        "dodavatelsky_kod": code,
        "ean": gf.ean13(),
        "mpn": f"{g['znacka'][:3].upper()}{rnd.randint(10000, 999999)}",
        "oe_cisla": oe,
        "tecdoc_id": rnd.randint(10000, 99999),
        "znacka": g["znacka"], "vyrobca": g.get("vyrobca", g["znacka"]), "dodavatel": supplier,
        "kategoria": g["kat"], "podkategoria": g["sub"], "kategoria_kod": CAT_CODE.get(g["kat"], "GEN"),
        "nazov_produktu": g["nazov"], "kratky_popis": g.get("kratky", g["nazov"]),
        "dlhy_popis": g.get("dlhy", ""),
        "typ_variantu": g.get("variant_typ", g.get("pozicia", "")),
        "hodnota_variantu": g.get("variant_val", ""),
        "pozicia_montaze": g.get("pozicia", ""), "strana": g.get("strana", ""),
        "farba": g.get("farba", ""),
        "mena": "EUR", "dph_sadzba_pct": VAT,
        "voc_bez_dph": f"{voc:.2f}", "voc_s_dph": f"{voc_dph:.2f}",
        "moc_bez_dph": f"{moc:.2f}", "moc_s_dph": f"{moc_dph:.2f}",
        "marza_pct": f"{marza_pct:.1f}", "rabat_pct": rabat,
        "akciova_cena_s_dph": (f"{akcia:.2f}" if akcia != "" else ""),
        "cena_za_jednotku": (f"{cena_jednotka:.2f}" if cena_jednotka != "" else ""),
        "jednotka_ceny": g.get("jednotka", "€/ks"),
        "zaloha_za_diel": (f"{g['deposit']:.2f}" if g.get("deposit") else ""),
        "sklad_mnozstvo": qty, "sklad_lokalita": rnd.choice(WAREHOUSE),
        "dostupnost": status, "doba_dodania": dod_txt, "doba_dodania_dni": dod_dni,
        "min_objednavka": rnd.choice([1, 1, 1, 2, 4, 5, 10]),
        "objednavkovy_nasobok": rnd.choice([1, 1, 2, 4]),
        "ks_v_baleni": rnd.choice([1, 1, 1, 2, 4]),
        "balenie_typ": rnd.choice(PACKAGING), "expedicia_do": dod_txt,
        "hmotnost_netto_kg": f"{g['hmot']:.2f}",
        "hmotnost_brutto_kg": f"{g['hmot'] * rnd.uniform(1.05, 1.25):.2f}",
        "dlzka_mm": l, "sirka_mm": w, "vyska_mm": h,
        "objem_l": (f"{objem:.2f}" if objem else ""),
        "rozmery_text": f"{l}x{w}x{h} mm",
        "kompatibilita_vozidla": kompat, "rok_vyroby_od": rok_od, "rok_vyroby_do": rok_do,
        "norma_certifikat": g.get("norma", ""),
        "colny_kod_hs": HS_CODES.get(g["kat"], ""),
        "krajina_povodu": rnd.choice(ORIGIN),
        "stav_tovaru": g.get("stav", "Nový"), "zaruka_mesiace": g["zaruka"],
        "pneu_sezonnost": g.get("pneu_sezona", ""),
        "eu_stitok_palivo": g.get("eu_fuel", ""), "eu_stitok_prilnavost": g.get("eu_grip", ""),
        "eu_stitok_hluk_db": g.get("eu_noise", ""),
        "olej_viskozita": g.get("olej_visk", ""), "olej_norma": g.get("olej_norma", ""),
        "obrazok_url": f"https://cdn.{sup_prefix.lower()}.sk/img/{slug}.jpg",
        "datasheet_url": f"https://cdn.{sup_prefix.lower()}.sk/doc/{slug}.pdf",
        "aktivny": rnd.choice(["áno", "áno", "áno", "nie"]),
        "datum_aktualizacie": UPDATED,
    }


# ── 11 dodávateľov (názov, prefix, seed, váhy zamerania) ───────────────────
SUPPLIERS = [
    ("MotoDiely SK s.r.o.",        "MDS", 42,  None),
    ("AutoParts Slovakia s.r.o.",  "APS", 101, None),
    ("BrzdyPro s.r.o.",            "BPR", 102, [40, 8, 22, 3, 3, 4, 2, 2, 6, 10]),
    ("FilterCentrum s.r.o.",       "FLC", 103, [6, 42, 14, 8, 8, 3, 2, 3, 8, 6]),
    ("OlejExpert s.r.o.",          "OLX", 104, [4, 8, 8, 38, 26, 2, 1, 3, 6, 4]),
    ("PneuServis SK s.r.o.",       "PNS", 105, [4, 4, 6, 4, 3, 42, 24, 3, 6, 4]),
    ("ElektroAuto s.r.o.",         "ELA", 106, [6, 6, 10, 4, 4, 4, 2, 30, 8, 26]),
    ("DielyExpres s.r.o.",         "DEX", 107, [16, 12, 40, 6, 5, 5, 3, 4, 5, 4]),
    ("CarStyle s.r.o.",            "CST", 108, [4, 6, 8, 5, 5, 8, 6, 3, 45, 10]),
    ("EuroDiely a.s.",             "EUD", 109, None),
    ("MotoMarket s.r.o.",          "MMK", 110, None),
]


def generate_one(name, prefix, seed, weights):
    rnd.seed(seed)
    rnd.gen_w = weights if weights else DEFAULT_W
    fname = f"feed_{prefix.lower()}.tsv"
    with open(fname, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(COLUMNS)
        for i in range(1, gf.ROWS + 1):
            rec = build_record(i, name, prefix)
            w.writerow([rec[k] for k in COLUMNS])
    return fname


def main():
    print(f"Stĺpcov na feed: {len(COLUMNS)}\n")
    for name, prefix, seed, weights in SUPPLIERS:
        fname = generate_one(name, prefix, seed, weights)
        print(f"  ✓ {fname:24s} {name}")
    print(f"\nHotovo: {len(SUPPLIERS)} feedov × {gf.ROWS} SKU × {len(COLUMNS)} parametrov (TAB-oddeľované)")


if __name__ == "__main__":
    main()
