#!/usr/bin/env python3
"""
Detailed automotive product feeds ready for DIRECT PASTE into Google Sheets.

Format: TAB-separated (.tsv) → open file, Ctrl/Cmd+A, Cmd+C, paste into A1.
Google Sheets auto-splits into columns (no import dialog).

~67 parameters per product. 11 different suppliers, 10 000 SKU each.
Market SK, currency EUR, VAT 23%. All labels and content in English.

Run:  python3 generate_rich.py
"""

import csv
import generate_feed as gf

rnd = gf.random
VAT = gf.VAT
VEHICLES = gf.VEHICLES
UPDATED = gf.UPDATED


# ── Reference data ─────────────────────────────────────────────────────────
ORIGIN = ["Germany", "Czechia", "Poland", "Italy", "France", "Spain",
          "Slovakia", "Turkey", "Japan", "China"]
WAREHOUSE = ["BA-01 Bratislava", "ZA-02 Zilina", "KE-03 Kosice",
             "DC-PRG Prague", "DC-VIE Vienna"]
PACKAGING = ["Box", "Blister", "Film wrap", "Plastic container", "Boxed set"]

HS_CODES = {
    "Braking system": "8708.30", "Filters": "8421.23", "Spare parts": "8708.99",
    "Fluids": "3819.00", "Tires": "4011.10", "Wheels": "8708.70",
    "Electrical": "8507.10", "Accessories": "8708.29", "Lighting & visibility": "8512.20",
}
CAT_CODE = {
    "Braking system": "BRK", "Filters": "FLT", "Spare parts": "PRT",
    "Fluids": "FLU", "Tires": "TYR", "Wheels": "RIM",
    "Electrical": "BAT", "Accessories": "ACC", "Lighting & visibility": "LGT",
}


def price(lo, hi):
    return round(rnd.uniform(lo, hi), 2)


def vehicle():
    mk, gen = rnd.choice(VEHICLES)
    return f"{mk} {gen}"


def years_from_vehicle(v):
    """Extracts 'year from–to' from the compatibility string (e.g. '2007-2013')."""
    for tok in v.replace("–", "-").split():
        if "-" in tok and tok[:4].isdigit():
            a, _, b = tok.partition("-")
            return a, (b if b.isdigit() else "")
    return "", ""


def avail():
    status = rnd.choices(["In stock", "Incoming", "On order", "Sold out"],
                         weights=[60, 12, 25, 3])[0]
    qty = {"In stock": rnd.randint(5, 480), "Incoming": rnd.randint(0, 40),
           "On order": 0, "Sold out": 0}[status]
    days = {"In stock": 1, "Incoming": 3, "On order": rnd.choice([7, 10, 14]),
            "Sold out": 0}[status]
    txt = {"In stock": "24 h", "Incoming": "2–3 days",
           "On order": f"{days} days", "Sold out": "—"}[status]
    return status, qty, txt, days


# ── Category generators (return a detailed attribute dict) ──────────────────
def brakes():
    sub, brands, pos, lo, hi = rnd.choice([
        ("Brake discs", ["Brembo", "ATE", "TRW", "Bosch", "Zimmermann"], "Front/Rear axle", 18, 75),
        ("Brake pads", ["Brembo", "ATE", "TRW", "Ferodo", "Bosch"], "Front/Rear axle", 22, 68),
        ("Brake caliper", ["TRW", "ATE", "Cifam"], "Wheel hub", 45, 160),
        ("Brake shoes", ["TRW", "Bosch", "Febi"], "Rear axle", 24, 55),
    ])
    b = rnd.choice(brands)
    dia = rnd.choice([256, 280, 288, 300, 312, 330])
    deposit = price(20, 60) if sub == "Brake caliper" else 0
    return dict(
        kat="Braking system", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}, diameter {dia} mm",
        dlhy=f"{sub} by {b} with {dia} mm diameter. Approved to ECE R90, "
             f"anti-corrosion coating, balanced for low noise.",
        voc=price(lo, hi), marza=(1.30, 1.55), zaruka=24, oe=True, kompat=True,
        hmot=round(rnd.uniform(0.8, 9.5), 2), dims=(dia, dia, rnd.randint(18, 90)),
        norma="ECE R90", pozicia=pos, strana=rnd.choice(["Left", "Right", ""]),
        deposit=deposit,
    )


def filters():
    sub, brands, lo, hi = rnd.choice([
        ("Oil filter", ["Mann-Filter", "Mahle", "Bosch", "Hengst"], 4, 16),
        ("Air filter", ["Mann-Filter", "Mahle", "Bosch", "Filtron"], 6, 28),
        ("Cabin filter", ["Mann-Filter", "Bosch", "Mahle"], 5, 24),
        ("Fuel filter", ["Mann-Filter", "Bosch", "Mahle", "Hengst"], 8, 35),
    ])
    b = rnd.choice(brands)
    typ = rnd.choice(["Standard", "Activated carbon", "High flow"])
    return dict(
        kat="Filters", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}, type {typ}",
        dlhy=f"{sub} {b} ({typ}). Precise fitment geometry, high filtration "
             f"efficiency and long service life per manufacturer intervals.",
        voc=price(lo, hi), marza=(1.35, 1.60), zaruka=24, oe=True, kompat=True,
        hmot=round(rnd.uniform(0.1, 1.4), 2), dims=(rnd.randint(60, 300), rnd.randint(60, 250), rnd.randint(30, 120)),
        norma="ISO 4548", variant_typ="Filter type", variant_val=typ,
    )


def oils():
    b = rnd.choice(["Castrol", "Mobil", "Shell", "Valvoline", "Liqui Moly"])
    visk = rnd.choice(["0W-20", "0W-30", "5W-30", "5W-40", "10W-40", "15W-40"])
    bal = rnd.choice([1, 4, 5, 20])
    base = {1: (6, 14), 4: (24, 52), 5: (28, 64), 20: (95, 210)}[bal]
    voc = price(*base)
    acea = rnd.choice(["A3/B4", "C2", "C3", "A5/B5"])
    api = rnd.choice(["SN", "SP", "SN PLUS"])
    return dict(
        kat="Fluids", sub="Engine oil", znacka=b, vyrobca=b,
        nazov=f"Engine oil {b} {visk} {bal} L",
        kratky=f"Synthetic oil {b} {visk}, {bal} L pack",
        dlhy=f"Fully synthetic engine oil {b} {visk}. ACEA {acea}, API {api} "
             f"standards, VW/MB/BMW approvals. {bal} L pack.",
        voc=voc, marza=(1.20, 1.45), zaruka=0, oe=False, kompat=False,
        hmot=round({1: 1.0, 4: 3.8, 5: 4.7, 20: 18.5}[bal], 1),
        dims=(rnd.randint(90, 300), rnd.randint(90, 300), rnd.randint(120, 400)),
        objem=float(bal), jednotka="€/L", norma=f"ACEA {acea} / API {api}",
        variant_typ="Viscosity/Pack", variant_val=f"{visk} / {bal} L",
        olej_visk=visk, olej_norma=f"ACEA {acea}, API {api}",
    )


def fluids():
    sub, brands, vol, lo, hi, norma = rnd.choice([
        ("Coolant", ["Febi", "Liqui Moly", "Castrol"], 1.5, 6, 18, "G12++"),
        ("Brake fluid", ["ATE", "Bosch", "TRW"], 0.5, 5, 14, "DOT 4"),
        ("AdBlue", ["BASF", "Liqui Moly"], 10, 9, 22, "ISO 22241"),
        ("Washer fluid", ["Sheron", "Liqui Moly"], 3, 3, 9, "—"),
    ])
    b = rnd.choice(brands)
    return dict(
        kat="Fluids", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b} {vol} L", kratky=f"{sub} {b}, {vol} L, {norma}",
        dlhy=f"{sub} {b}, {norma} standard, {vol} L pack. Ready to use, "
             f"compliant with vehicle manufacturer specifications.",
        voc=price(lo, hi), marza=(1.25, 1.50), zaruka=0, oe=False, kompat=False,
        hmot=round(vol * rnd.uniform(1.0, 1.1), 2),
        dims=(rnd.randint(90, 250), rnd.randint(90, 250), rnd.randint(150, 400)),
        objem=float(vol), jednotka="€/L", norma=norma,
        variant_typ="Pack", variant_val=f"{vol} L",
    )


def tires():
    b = rnd.choice(["Continental", "Michelin", "Goodyear", "Barum", "Matador", "Sava", "Bridgestone"])
    w = rnd.choice([175, 185, 195, 205, 215, 225, 235]); pr = rnd.choice([45, 50, 55, 60, 65])
    di = rnd.choice([15, 16, 17, 18]); li = rnd.randint(88, 99); si = rnd.choice(["H", "V", "W", "T"])
    size = f"{w}/{pr} R{di}"; season = rnd.choice(["Summer", "Winter", "All-season"])
    fuel = rnd.choice(["B", "C", "D", "E"]); grip = rnd.choice(["A", "B", "C"]); noise = rnd.randint(68, 73)
    return dict(
        kat="Tires", sub=f"{season} tire", znacka=b, vyrobca=b,
        nazov=f"{b} {size} {li}{si} {season.lower()}",
        kratky=f"{season} tire {b} {size} {li}{si}",
        dlhy=f"{season} tire {b} {size}, load index {li}, speed rating {si}. "
             f"EU label: fuel {fuel}, wet grip {grip}, noise {noise} dB.",
        voc=price(38, 165), marza=(1.18, 1.40), zaruka=24, oe=False, kompat=False,
        hmot=round(rnd.uniform(7.0, 12.5), 1), dims=(di * 25 + 100, w, w),
        norma="ECE R30", pneu_rozmer=f"{size} {li}{si}", pneu_sezona=season,
        eu_fuel=fuel, eu_grip=grip, eu_noise=noise,
        variant_typ="Size", variant_val=f"{size} {li}{si}",
    )


def wheels():
    b = rnd.choice(["Borbet", "Alcar", "Ronal", "Dezent", "OE"])
    typ = rnd.choice(["Alloy wheel", "Steel wheel"]); di = rnd.choice([15, 16, 17, 18])
    w = rnd.choice([6.0, 6.5, 7.0, 7.5, 8.0]); pcd = rnd.choice(["5x112", "5x114.3", "4x100", "5x108"])
    et = rnd.choice([35, 40, 45, 48, 50])
    return dict(
        kat="Wheels", sub=typ, znacka=b, vyrobca=b,
        nazov=f"{typ} {b} {w}Jx{di} {pcd} ET{et}",
        kratky=f"{typ} {b} {w}Jx{di}, {pcd}, ET{et}",
        dlhy=f"{typ} {b}, {w}Jx{di}, PCD {pcd}, ET{et}. Certified (TUV), suitable "
             f"for all-year use, painted finish.",
        voc=price(28, 140), marza=(1.25, 1.55), zaruka=24, oe=False, kompat=False,
        hmot=round(rnd.uniform(6.5, 13.0), 1), dims=(di * 25 + 50, di * 25 + 50, int(w * 25)),
        norma="TUV / ECE", variant_typ="Size", variant_val=f"{w}Jx{di} {pcd} ET{et}",
    )


def batteries():
    b = rnd.choice(["Varta", "Exide", "Bosch", "Banner"]); cap = rnd.choice([44, 54, 60, 70, 74, 80, 95])
    cca = cap * rnd.choice([9, 10, 11])
    return dict(
        kat="Electrical", sub="Car battery", znacka=b, vyrobca=b,
        nazov=f"Car battery {b} {cap} Ah 12V {cca}A",
        kratky=f"Car battery {b} {cap} Ah, cranking {cca} A",
        dlhy=f"Starter battery {b} {cap} Ah, 12 V, cranking current {cca} A. "
             f"Maintenance-free, suitable for start-stop vehicles.",
        voc=price(48, 165), marza=(1.20, 1.40), zaruka=24, oe=False, kompat=True,
        hmot=round(rnd.uniform(11.0, 22.0), 1), dims=(242, 175, 190),
        deposit=price(8, 15), norma="EN 50342", variant_typ="Capacity", variant_val=f"{cap} Ah",
    )


def other_parts():
    sub, brands, lo, hi, repas = rnd.choice([
        ("Shock absorber", ["Sachs", "Bilstein", "KYB", "Monroe"], 35, 130, False),
        ("Clutch kit", ["Sachs", "LuK", "Valeo"], 95, 320, False),
        ("Water pump", ["SKF", "Gates", "Hepu"], 28, 95, False),
        ("Wheel bearing", ["SKF", "FAG", "SNR"], 22, 88, False),
        ("Spark plug", ["NGK", "Denso", "Bosch"], 3, 14, False),
        ("Ignition coil", ["Bosch", "NGK", "Beru"], 25, 75, False),
        ("Timing belt kit", ["Gates", "INA", "Contitech"], 55, 180, False),
        ("Alternator", ["Bosch", "Valeo", "Denso"], 90, 280, True),
        ("Starter motor", ["Bosch", "Valeo", "Denso"], 80, 240, True),
    ])
    b = rnd.choice(brands)
    return dict(
        kat="Spare parts", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}",
        dlhy=f"{sub} {b}. Precise fitment to OE specification, proven reliability "
             f"and durability. {'Remanufactured part with refundable core deposit.' if repas else ''}".strip(),
        voc=price(lo, hi), marza=(1.30, 1.55), zaruka=24, oe=True, kompat=True,
        hmot=round(rnd.uniform(0.3, 12.0), 2),
        dims=(rnd.randint(50, 400), rnd.randint(50, 300), rnd.randint(30, 250)),
        stav=("Remanufactured" if repas else "New"),
        deposit=(price(25, 90) if repas else 0),
        pozicia=rnd.choice(["Front axle", "Rear axle", "Engine", ""]),
        strana=rnd.choice(["Left", "Right", "", "Set"]),
    )


def accessories():
    sub, brands, lo, hi = rnd.choice([
        ("Rubber mats (set)", ["Petex", "Rezaw-Plast", "Frogum"], 12, 45),
        ("Textile mats (set)", ["Petex", "AutoMega"], 9, 32),
        ("Seat covers (set)", ["Kegel", "Petex"], 25, 95),
        ("Car shampoo", ["Sonax", "Meguiar's", "K2"], 4, 18),
        ("Phone holder", ["Cellularline", "Baseus"], 6, 24),
        ("Jump leads", ["Bottari", "K2"], 9, 38),
        ("Roof box", ["Thule", "Hapro"], 180, 520),
        ("Snow chains", ["Pewag", "Konig"], 35, 120),
    ])
    b = rnd.choice(brands); color = rnd.choice(["Black", "Grey", "Beige", "—"])
    return dict(
        kat="Accessories", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}, {color.lower()}",
        dlhy=f"{sub} {b}. Quality build, easy installation, universal or "
             f"model-specific design.",
        voc=price(lo, hi), marza=(1.35, 1.70), zaruka=12, oe=False, kompat=False,
        hmot=round(rnd.uniform(0.1, 9.0), 2),
        dims=(rnd.randint(50, 600), rnd.randint(50, 400), rnd.randint(20, 300)),
        farba=color, variant_typ="Design", variant_val=rnd.choice(["Universal", color, "Set"]),
    )


def bulbs_wipers():
    sub, brands, lo, hi = rnd.choice([
        ("H7 bulb", ["Osram", "Philips", "Bosch"], 2, 12),
        ("LED bulb", ["Osram", "Philips"], 14, 48),
        ("Wiper blade (set)", ["Bosch", "Valeo", "SWF"], 8, 32),
    ])
    b = rnd.choice(brands)
    return dict(
        kat="Lighting & visibility", sub=sub, znacka=b, vyrobca=b,
        nazov=f"{sub} {b}", kratky=f"{sub} {b}",
        dlhy=f"{sub} {b}. High luminosity / perfect wiping, long service life, "
             f"road-legal (ECE).",
        voc=price(lo, hi), marza=(1.30, 1.60), zaruka=12, oe=False, kompat=True,
        hmot=round(rnd.uniform(0.05, 0.8), 2),
        dims=(rnd.randint(40, 700), rnd.randint(20, 60), rnd.randint(20, 60)),
        norma="ECE R37/R112", variant_typ="Pack", variant_val=rnd.choice(["1 pc", "2 pcs (pair)", "Set"]),
    )


GENERATORS = [
    (brakes, 14), (filters, 12), (other_parts, 18), (oils, 8), (fluids, 6),
    (tires, 12), (wheels, 6), (batteries, 4), (accessories, 12), (bulbs_wipers, 8),
]
GEN_FUNCS = [g for g, _ in GENERATORS]
DEFAULT_W = [w for _, w in GENERATORS]


# ── Assemble the detailed record (~67 parameters) ──────────────────────────
COLUMNS = [
    "row_id", "supplier_sku", "ean", "mpn", "oe_numbers", "tecdoc_id",
    "brand", "manufacturer", "supplier",
    "category", "subcategory", "category_code",
    "product_name", "short_description", "long_description",
    "variant_type", "variant_value", "fitment_position", "side", "color",
    "currency", "vat_rate_pct", "wholesale_price_excl_vat", "wholesale_price_incl_vat",
    "retail_price_excl_vat", "retail_price_incl_vat",
    "margin_pct", "discount_pct", "sale_price_incl_vat", "unit_price", "price_unit",
    "core_deposit",
    "stock_qty", "warehouse_location", "availability", "lead_time", "lead_time_days",
    "min_order_qty", "order_multiple", "units_per_pack", "packaging_type", "dispatch_within",
    "net_weight_kg", "gross_weight_kg", "length_mm", "width_mm", "height_mm",
    "volume_l", "dimensions_text",
    "vehicle_compatibility", "year_from", "year_to", "standard_certification",
    "hs_customs_code", "country_of_origin", "condition", "warranty_months",
    "tire_season", "eu_label_fuel", "eu_label_grip", "eu_label_noise_db",
    "oil_viscosity", "oil_standard",
    "image_url", "datasheet_url", "active", "updated_at",
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
    kompat = vehicle() if g["kompat"] else "Universal"
    rok_od, rok_do = years_from_vehicle(kompat) if g["kompat"] else ("", "")
    l, w, h = g["dims"]
    n_oe = rnd.randint(1, 3) if g["oe"] else 0
    oe = ";".join(f"OE{rnd.randint(1000000, 9999999)}" for _ in range(n_oe))
    slug = code.lower()

    return {
        "row_id": i,
        "supplier_sku": code,
        "ean": gf.ean13(),
        "mpn": f"{g['znacka'][:3].upper()}{rnd.randint(10000, 999999)}",
        "oe_numbers": oe,
        "tecdoc_id": rnd.randint(10000, 99999),
        "brand": g["znacka"], "manufacturer": g.get("vyrobca", g["znacka"]), "supplier": supplier,
        "category": g["kat"], "subcategory": g["sub"], "category_code": CAT_CODE.get(g["kat"], "GEN"),
        "product_name": g["nazov"], "short_description": g.get("kratky", g["nazov"]),
        "long_description": g.get("dlhy", ""),
        "variant_type": g.get("variant_typ", g.get("pozicia", "")),
        "variant_value": g.get("variant_val", ""),
        "fitment_position": g.get("pozicia", ""), "side": g.get("strana", ""),
        "color": g.get("farba", ""),
        "currency": "EUR", "vat_rate_pct": VAT,
        "wholesale_price_excl_vat": f"{voc:.2f}", "wholesale_price_incl_vat": f"{voc_dph:.2f}",
        "retail_price_excl_vat": f"{moc:.2f}", "retail_price_incl_vat": f"{moc_dph:.2f}",
        "margin_pct": f"{marza_pct:.1f}", "discount_pct": rabat,
        "sale_price_incl_vat": (f"{akcia:.2f}" if akcia != "" else ""),
        "unit_price": (f"{cena_jednotka:.2f}" if cena_jednotka != "" else ""),
        "price_unit": g.get("jednotka", "€/pc"),
        "core_deposit": (f"{g['deposit']:.2f}" if g.get("deposit") else ""),
        "stock_qty": qty, "warehouse_location": rnd.choice(WAREHOUSE),
        "availability": status, "lead_time": dod_txt, "lead_time_days": dod_dni,
        "min_order_qty": rnd.choice([1, 1, 1, 2, 4, 5, 10]),
        "order_multiple": rnd.choice([1, 1, 2, 4]),
        "units_per_pack": rnd.choice([1, 1, 1, 2, 4]),
        "packaging_type": rnd.choice(PACKAGING), "dispatch_within": dod_txt,
        "net_weight_kg": f"{g['hmot']:.2f}",
        "gross_weight_kg": f"{g['hmot'] * rnd.uniform(1.05, 1.25):.2f}",
        "length_mm": l, "width_mm": w, "height_mm": h,
        "volume_l": (f"{objem:.2f}" if objem else ""),
        "dimensions_text": f"{l}x{w}x{h} mm",
        "vehicle_compatibility": kompat, "year_from": rok_od, "year_to": rok_do,
        "standard_certification": g.get("norma", ""),
        "hs_customs_code": HS_CODES.get(g["kat"], ""),
        "country_of_origin": rnd.choice(ORIGIN),
        "condition": g.get("stav", "New"), "warranty_months": g["zaruka"],
        "tire_season": g.get("pneu_sezona", ""),
        "eu_label_fuel": g.get("eu_fuel", ""), "eu_label_grip": g.get("eu_grip", ""),
        "eu_label_noise_db": g.get("eu_noise", ""),
        "oil_viscosity": g.get("olej_visk", ""), "oil_standard": g.get("olej_norma", ""),
        "image_url": f"https://cdn.{sup_prefix.lower()}.example/img/{slug}.jpg",
        "datasheet_url": f"https://cdn.{sup_prefix.lower()}.example/doc/{slug}.pdf",
        "active": rnd.choice(["yes", "yes", "yes", "no"]),
        "updated_at": UPDATED,
    }


# ── 11 suppliers (name, prefix, seed, focus weights) ───────────────────────
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
    print(f"Columns per feed: {len(COLUMNS)}\n")
    for name, prefix, seed, weights in SUPPLIERS:
        fname = generate_one(name, prefix, seed, weights)
        print(f"  ✓ {fname:24s} {name}")
    print(f"\nDone: {len(SUPPLIERS)} feeds × {gf.ROWS} SKU × {len(COLUMNS)} parameters (TAB-separated)")


if __name__ == "__main__":
    main()
