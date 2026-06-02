#!/usr/bin/env python3
"""
Vygeneruje 11 HETEROGÉNNYCH feedov — každý od iného dodávateľa a s INOU schémou:
iné názvy stĺpcov, poradie, jazyk, oddeľovač, desatinný oddeľovač, formát dátumu,
EAN ako text, ceny so suffixom meny, vynechané/pridané stĺpce, počítaná marža.

Simuluje realitu: agent dostáva feedy v rôznych formátoch a musí ich normalizovať.

Spustenie:  python3 generate_varied.py
"""

import csv
import generate_feed as gf

VAT = gf.VAT

# ── Lokalizačné slovníky (kanonická SK hodnota → preklad) ──────────────────
AVAIL = {
    "en": {"Skladom": "In stock", "Na ceste": "Incoming", "Na objednávku": "On order", "Vypredané": "Sold out"},
    "cz": {"Skladom": "Skladem", "Na ceste": "Na cestě", "Na objednávku": "Na objednávku", "Vypredané": "Vyprodáno"},
    "de": {"Skladom": "Auf Lager", "Na ceste": "Unterwegs", "Na objednávku": "Auf Bestellung", "Vypredané": "Ausverkauft"},
}
LEAD = {
    "en": {"24 h": "24 h", "2–3 dni": "2–3 days", "7–14 dní": "7–14 days", "—": "—"},
    "cz": {"24 h": "24 h", "2–3 dni": "2–3 dny", "7–14 dní": "7–14 dní", "—": "—"},
    "de": {"24 h": "24 h", "2–3 dni": "2–3 Tage", "7–14 dní": "7–14 Tage", "—": "—"},
}


def fmt_date(iso, fmt):
    y, m, d = iso.split("-")
    return {"iso": iso, "dot": f"{d}.{m}.{y}", "slash": f"{d}/{m}/{y}"}[fmt]


def fmt_value(profile, key, rec):
    """Naformátuje kanonickú hodnotu podľa profilu dodávateľa (jazyk, desatinné, suffix...)."""
    dec = profile["decimal"]
    lang = profile["lang"]

    # počítaná marža (%) z čistej MOC voči VOC
    if key == "margin_pct":
        voc = float(rec["voc_bez_dph_eur"])
        moc_net = float(rec["moc_s_dph_eur"]) / (1 + VAT / 100)
        val = f"{(moc_net - voc) / voc * 100:.1f}"
        return val.replace(".", dec) + " %"

    val = str(rec[key])

    if key in ("voc_bez_dph_eur", "moc_s_dph_eur"):
        val = val.replace(".", dec) + profile.get("price_suffix", "")
    elif key == "hmotnost_kg":
        val = val.replace(".", dec)
    elif key == "ean" and profile.get("ean_quote"):
        val = "'" + val  # vodiaci apostrof → bunka ako text (Sheets/Excel)
    elif key == "datum_aktualizacie":
        val = fmt_date(val, profile["date_fmt"])
    elif key == "dostupnost" and lang in AVAIL:
        val = AVAIL[lang][val]
    elif key == "doba_dodania" and lang in LEAD:
        val = LEAD[lang][val]
    return val


# ── 11 profilov dodávateľov (názov, prefix, seed, váhy, schéma) ────────────
# columns = zoznam (hlavička_v_súbore, kanonický_kľúč). Vynechané kľúče = chýbajúci stĺpec.
PROFILES = [
    {
        "supplier": "MotoDiely SK s.r.o.", "prefix": "MDS", "seed": 42, "weights": None,
        "file": "feed_motodiely.csv", "delimiter": ",", "decimal": ".", "lang": "sk",
        "date_fmt": "iso", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("dodavatelsky_kod", "dodavatelsky_kod"), ("ean", "ean"), ("mpn", "mpn"),
            ("oe_cislo", "oe_cislo"), ("znacka", "znacka"), ("nazov_produktu", "nazov_produktu"),
            ("popis", "popis"), ("kategoria", "kategoria"), ("podkategoria", "podkategoria"),
            ("typ_variantu", "typ_variantu"), ("hodnota_variantu", "hodnota_variantu"),
            ("voc_bez_dph_eur", "voc_bez_dph_eur"), ("moc_s_dph_eur", "moc_s_dph_eur"),
            ("mena", "mena"), ("dph_sadzba_pct", "dph_sadzba_pct"),
            ("sklad_mnozstvo", "sklad_mnozstvo"), ("dostupnost", "dostupnost"),
            ("doba_dodania", "doba_dodania"), ("min_objednavka", "min_objednavka"),
            ("ks_v_baleni", "ks_v_baleni"), ("hmotnost_kg", "hmotnost_kg"),
            ("rozmery", "rozmery"), ("zaruka_mesiace", "zaruka_mesiace"),
            ("kompatibilita_vozidla", "kompatibilita_vozidla"), ("datum_aktualizacie", "datum_aktualizacie"),
        ],
    },
    {   # EN, štandardné e-commerce názvy, čiarka/bodka
        "supplier": "AutoParts Slovakia s.r.o.", "prefix": "APS", "seed": 101, "weights": None,
        "file": "feed_autoparts.csv", "delimiter": ",", "decimal": ".", "lang": "en",
        "date_fmt": "iso", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("sku", "dodavatelsky_kod"), ("barcode", "ean"), ("brand", "znacka"),
            ("product_name", "nazov_produktu"), ("description", "popis"),
            ("category", "kategoria"), ("subcategory", "podkategoria"),
            ("wholesale_price_excl_vat", "voc_bez_dph_eur"),
            ("retail_price_incl_vat", "moc_s_dph_eur"), ("currency", "mena"),
            ("vat_rate", "dph_sadzba_pct"), ("stock_qty", "sklad_mnozstvo"),
            ("availability", "dostupnost"), ("lead_time", "doba_dodania"),
            ("min_order_qty", "min_objednavka"), ("weight_kg", "hmotnost_kg"),
            ("warranty_months", "zaruka_mesiace"), ("vehicle_fit", "kompatibilita_vozidla"),
            ("updated_at", "datum_aktualizacie"),
        ],
    },
    {   # SK, bodkočiarka + desatinná čiarka, dátum DD.MM.RRRR (typický Excel export)
        "supplier": "BrzdyPro s.r.o.", "prefix": "BPR", "seed": 102,
        "weights": [40, 8, 22, 3, 3, 4, 2, 2, 6, 10],
        "file": "feed_brzdypro.csv", "delimiter": ";", "decimal": ",", "lang": "sk",
        "date_fmt": "dot", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("Kód", "dodavatelsky_kod"), ("EAN", "ean"), ("Výrobca", "znacka"),
            ("OE číslo", "oe_cislo"), ("Názov", "nazov_produktu"), ("Popis", "popis"),
            ("Kategória", "kategoria"), ("Cena bez DPH", "voc_bez_dph_eur"),
            ("Cena s DPH", "moc_s_dph_eur"), ("DPH %", "dph_sadzba_pct"),
            ("Sklad", "sklad_mnozstvo"), ("Dostupnosť", "dostupnost"),
            ("Dodanie", "doba_dodania"), ("Hmotnosť", "hmotnost_kg"),
            ("Vozidlo", "kompatibilita_vozidla"), ("Aktualizované", "datum_aktualizacie"),
        ],
    },
    {   # TAB-delimited, minimalistický feed
        "supplier": "FilterCentrum s.r.o.", "prefix": "FLC", "seed": 103,
        "weights": [6, 42, 14, 8, 8, 3, 2, 3, 8, 6],
        "file": "feed_filtercentrum.tsv", "delimiter": "\t", "decimal": ".", "lang": "sk",
        "date_fmt": "iso", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("kod", "dodavatelsky_kod"), ("ean", "ean"), ("mpn", "mpn"),
            ("nazov", "nazov_produktu"), ("znacka", "znacka"), ("kategoria", "kategoria"),
            ("nakup", "voc_bez_dph_eur"), ("predaj", "moc_s_dph_eur"),
            ("sklad", "sklad_mnozstvo"), ("dostupnost", "dostupnost"),
            ("dodanie", "doba_dodania"),
        ],
    },
    {   # CZ, bodkočiarka + desatinná čiarka
        "supplier": "OlejExpert s.r.o.", "prefix": "OLX", "seed": 104,
        "weights": [4, 8, 8, 38, 26, 2, 1, 3, 6, 4],
        "file": "feed_olejexpert.csv", "delimiter": ";", "decimal": ",", "lang": "cz",
        "date_fmt": "dot", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("Kód zboží", "dodavatelsky_kod"), ("EAN", "ean"), ("Značka", "znacka"),
            ("Název", "nazov_produktu"), ("Popis", "popis"), ("Kategorie", "kategoria"),
            ("Varianta", "hodnota_variantu"), ("Nákupní cena", "voc_bez_dph_eur"),
            ("Doporučená cena", "moc_s_dph_eur"), ("DPH", "dph_sadzba_pct"),
            ("Skladem", "sklad_mnozstvo"), ("Dostupnost", "dostupnost"),
            ("Dodací lhůta", "doba_dodania"), ("Hmotnost kg", "hmotnost_kg"),
            ("Balení", "ks_v_baleni"), ("Aktualizace", "datum_aktualizacie"),
        ],
    },
    {   # ceny so suffixom " €", EAN ako text, dátum DD/MM/RRRR
        "supplier": "PneuServis SK s.r.o.", "prefix": "PNS", "seed": 105,
        "weights": [4, 4, 6, 4, 3, 42, 24, 3, 6, 4],
        "file": "feed_pneuservis.csv", "delimiter": ",", "decimal": ".", "lang": "sk",
        "date_fmt": "slash", "price_suffix": " €", "ean_quote": True,
        "columns": [
            ("Item", "dodavatelsky_kod"), ("EAN", "ean"), ("Brand", "znacka"),
            ("Title", "nazov_produktu"), ("Rozmer", "hodnota_variantu"),
            ("Category", "kategoria"), ("Buy", "voc_bez_dph_eur"), ("Sell", "moc_s_dph_eur"),
            ("Qty", "sklad_mnozstvo"), ("Stav", "dostupnost"), ("ETA", "doba_dodania"),
            ("Weight", "hmotnost_kg"), ("Updated", "datum_aktualizacie"),
        ],
    },
    {   # UPPERCASE hlavičky, bodkočiarka
        "supplier": "ElektroAuto s.r.o.", "prefix": "ELA", "seed": 106,
        "weights": [6, 6, 10, 4, 4, 4, 2, 30, 8, 26],
        "file": "feed_elektroauto.csv", "delimiter": ";", "decimal": ",", "lang": "sk",
        "date_fmt": "dot", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("KOD", "dodavatelsky_kod"), ("EAN", "ean"), ("ZNACKA", "znacka"),
            ("NAZOV", "nazov_produktu"), ("POPIS", "popis"), ("KATEGORIA", "kategoria"),
            ("PODKATEGORIA", "podkategoria"), ("VOC", "voc_bez_dph_eur"),
            ("MOC", "moc_s_dph_eur"), ("MENA", "mena"), ("DPH", "dph_sadzba_pct"),
            ("SKLAD", "sklad_mnozstvo"), ("DOSTUPNOST", "dostupnost"),
            ("DODANIE", "doba_dodania"), ("ZARUKA_MES", "zaruka_mesiace"),
            ("DATUM", "datum_aktualizacie"),
        ],
    },
    {   # DE (nemecký) feed, bodkočiarka + desatinná čiarka
        "supplier": "DielyExpres s.r.o.", "prefix": "DEX", "seed": 107,
        "weights": [16, 12, 40, 6, 5, 5, 3, 4, 5, 4],
        "file": "feed_dielyexpres.csv", "delimiter": ";", "decimal": ",", "lang": "de",
        "date_fmt": "dot", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("Artikelnummer", "dodavatelsky_kod"), ("EAN", "ean"), ("Marke", "znacka"),
            ("OE_Nummer", "oe_cislo"), ("Bezeichnung", "nazov_produktu"),
            ("Kategorie", "kategoria"), ("EK_Preis", "voc_bez_dph_eur"),
            ("VK_Preis", "moc_s_dph_eur"), ("MwSt", "dph_sadzba_pct"),
            ("Bestand", "sklad_mnozstvo"), ("Verfuegbarkeit", "dostupnost"),
            ("Lieferzeit", "doba_dodania"), ("Gewicht_kg", "hmotnost_kg"),
            ("Fahrzeug", "kompatibilita_vozidla"), ("Aktualisiert", "datum_aktualizacie"),
        ],
    },
    {   # EN, s počítanou maržou namiesto MOC mena/dph stĺpcov
        "supplier": "CarStyle s.r.o.", "prefix": "CST", "seed": 108,
        "weights": [4, 6, 8, 5, 5, 8, 6, 3, 45, 10],
        "file": "feed_carstyle.csv", "delimiter": ",", "decimal": ".", "lang": "en",
        "date_fmt": "iso", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("sku", "dodavatelsky_kod"), ("ean", "ean"), ("brand", "znacka"),
            ("name", "nazov_produktu"), ("description", "popis"), ("category", "kategoria"),
            ("variant", "hodnota_variantu"), ("cost", "voc_bez_dph_eur"),
            ("price", "moc_s_dph_eur"), ("margin", "margin_pct"),
            ("stock", "sklad_mnozstvo"), ("availability", "dostupnost"),
            ("lead_time", "doba_dodania"), ("weight_kg", "hmotnost_kg"),
            ("updated", "datum_aktualizacie"),
        ],
    },
    {   # SK, bodkočiarka, iné poradie + EAN ako text
        "supplier": "EuroDiely a.s.", "prefix": "EUD", "seed": 109, "weights": None,
        "file": "feed_eurodiely.csv", "delimiter": ";", "decimal": ",", "lang": "sk",
        "date_fmt": "dot", "price_suffix": "", "ean_quote": True,
        "columns": [
            ("Názov produktu", "nazov_produktu"), ("Kód", "dodavatelsky_kod"),
            ("Čiarový kód", "ean"), ("Výrobca", "znacka"), ("OE", "oe_cislo"),
            ("Kategória", "kategoria"), ("Podkategória", "podkategoria"),
            ("Popis", "popis"), ("VOC bez DPH", "voc_bez_dph_eur"),
            ("MOC s DPH", "moc_s_dph_eur"), ("Sadzba DPH", "dph_sadzba_pct"),
            ("Na sklade", "sklad_mnozstvo"), ("Stav", "dostupnost"),
            ("Doba dodania", "doba_dodania"), ("Min. odber", "min_objednavka"),
            ("Hmotnosť (kg)", "hmotnost_kg"), ("Záruka (mes.)", "zaruka_mesiace"),
            ("Vozidlo", "kompatibilita_vozidla"), ("Dátum", "datum_aktualizacie"),
        ],
    },
    {   # SK skrátené názvy, čiarka/bodka
        "supplier": "MotoMarket s.r.o.", "prefix": "MMK", "seed": 110, "weights": None,
        "file": "feed_motomarket.csv", "delimiter": ",", "decimal": ".", "lang": "sk",
        "date_fmt": "slash", "price_suffix": "", "ean_quote": False,
        "columns": [
            ("kod", "dodavatelsky_kod"), ("ean", "ean"), ("mpn", "mpn"),
            ("vyrobca", "znacka"), ("nazov", "nazov_produktu"), ("popis", "popis"),
            ("kat", "kategoria"), ("subkat", "podkategoria"), ("var", "hodnota_variantu"),
            ("cena_nakup", "voc_bez_dph_eur"), ("cena_predaj", "moc_s_dph_eur"),
            ("dph", "dph_sadzba_pct"), ("ks_sklad", "sklad_mnozstvo"),
            ("dostupnost", "dostupnost"), ("dodanie", "doba_dodania"),
            ("hmot", "hmotnost_kg"), ("rozmer", "rozmery"), ("auto", "kompatibilita_vozidla"),
            ("upd", "datum_aktualizacie"),
        ],
    },
]


def generate_one(p):
    gf.random.seed(p["seed"])
    gf.SUPPLIER = p["supplier"]
    gf.CODE_PREFIX = p["prefix"]
    gf.gen_weights = p["weights"] if p["weights"] else [w for _, w in gf.GENERATORS]

    headers = [h for h, _ in p["columns"]]
    with open(p["file"], "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=p["delimiter"])
        w.writerow(headers)
        for i in range(1, gf.ROWS + 1):
            rec = gf.build_record(i)
            w.writerow([fmt_value(p, key, rec) for _, key in p["columns"]])
    return len(headers)


def main():
    for p in PROFILES:
        ncols = generate_one(p)
        d = {",": "čiarka", ";": "bodkočiarka", "\t": "TAB"}[p["delimiter"]]
        print(f"  ✓ {p['file']:28s} {p['supplier']:28s} {ncols:2d} st. | "
              f"{p['lang']} | {d} | des '{p['decimal']}'")
    print(f"\nHotovo: {len(PROFILES)} heterogénnych feedov × {gf.ROWS} SKU")


if __name__ == "__main__":
    main()
