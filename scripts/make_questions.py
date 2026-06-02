#!/usr/bin/env python3
"""
Generates 100 realistic customer questions about OUT-OF-STOCK products, matchable
to a real product across all 11 feeds, evenly distributed.

v2 changes:
- Multilingual shuffle: each question is written in one of SK/CZ/EN/DE/PL (round-robin).
- `language` column added.
- `customer_email` column: alternates between the two real test inboxes.
- ~1 in 6 questions is symptom/implicit (does NOT name the part) to exercise the
  agent's inference (e.g. "piska pri brzdeni" -> brake pads).

Each question is built from a real feed row where availability is 'On order' /
'Incoming' and stock_qty = 0 — so a matching product + price + lead time exists as
ground truth (kept in expected_* columns).

Output: questions/customer_questions.csv (RFC4180, UTF-8). Run: python3 scripts/make_questions.py
"""

import csv
import glob
import os
import random

random.seed(2024)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS = sorted(glob.glob(os.path.join(REPO, "feeds", "feed_*.tsv")))
OUT = os.path.join(REPO, "questions", "customer_questions.csv")
TOTAL = 100

LANGS = ["sk", "cz", "en", "de", "pl"]
EMAILS = ["marekmicuda1@gmail.com", "dominik@fronc.eu"]

# Explicit-part templates, per language: {desc} product, {veh} vehicle.
TPL_VEHICLE = {
    "sk": "Dobry den, potrebujem {desc} na moje {veh}. Aktualne to nie je skladom - kolko to stoji a ako rychlo viete dodat?",
    "cz": "Dobry den, sháním {desc} pro {veh}. Momentálně nedostupné - jaká je cena a dodací lhůta?",
    "en": "Hi, I need {desc} for my {veh}. It's currently out of stock - what's the price and how soon can you deliver?",
    "de": "Hallo, ich brauche {desc} für meinen {veh}. Derzeit nicht auf Lager - wie viel kostet es und wie schnell lieferbar?",
    "pl": "Dzien dobry, potrzebuje {desc} do {veh}. Obecnie niedostepne - jaka cena i czas dostawy?",
}
TPL_UNIVERSAL = {
    "sk": "Dobry den, chcel by som objednat {desc}. Nie je to skladom - prosim o cenu a dodaciu lehotu.",
    "cz": "Dobry den, rad bych objednal {desc}. Není skladem - prosím o cenu a dodací lhůtu.",
    "en": "Hi, I'd like to order {desc}. It's out of stock - please quote the price and lead time.",
    "de": "Hallo, ich möchte {desc} bestellen. Nicht auf Lager - bitte Preis und Lieferzeit angeben.",
    "pl": "Dzien dobry, chcialbym zamowic {desc}. Brak na stanie - prosze o cene i czas dostawy.",
}

# Symptom/implicit templates by category -> language. Part is NOT named (inference test).
TPL_SYMPTOM = {
    "Braking system": {
        "sk": "Auto mi piska a vrzga ked brzdim na {veh}. Co s tym potrebujem? Asi to nie je skladom - cena a dodanie?",
        "cz": "Pri brzdění to na {veh} pískne a skřípe. Co budu potřebovat? Asi nedostupné - cena a dodání?",
        "en": "There's a squealing/grinding noise when I brake on my {veh}. What do I need? Probably out of stock - price and delivery?",
        "de": "Beim Bremsen quietscht und schleift es bei meinem {veh}. Was brauche ich? Vermutlich nicht auf Lager - Preis und Lieferung?",
        "pl": "Podczas hamowania piszczy i zgrzyta w {veh}. Czego potrzebuje? Pewnie brak na stanie - cena i dostawa?",
    },
    "Electrical": {
        "sk": "Moje {veh} rano nestartuje, baterka asi vybita. Co potrebujem? Nie je skladom - cena a dodanie?",
        "cz": "Moje {veh} ráno nenastartuje, baterka asi vybitá. Co potřebuji? Není skladem - cena a dodání?",
        "en": "My {veh} won't start in the morning, the battery seems dead. What do I need? It's out of stock - price and delivery?",
        "de": "Mein {veh} springt morgens nicht an, die Batterie scheint leer. Was brauche ich? Nicht auf Lager - Preis und Lieferung?",
        "pl": "Moje {veh} nie odpala rano, akumulator chyba padl. Czego potrzebuje? Brak na stanie - cena i dostawa?",
    },
    "Lighting & visibility": {
        "sk": "Na {veh} mi zhasla zarovka v svetlometu, potrebujem nahradu. Nie je skladom - cena a dodanie?",
        "cz": "Na {veh} mi zhasla žárovka ve světlometu, potřebuji náhradu. Není skladem - cena a dodání?",
        "en": "A headlight bulb burned out on my {veh}, I need a replacement. Out of stock - price and delivery?",
        "de": "Eine Scheinwerferlampe an meinem {veh} ist durchgebrannt, ich brauche Ersatz. Nicht auf Lager - Preis und Lieferung?",
        "pl": "W {veh} przepalila sie zarowka w reflektorze, potrzebuje wymiany. Brak na stanie - cena i dostawa?",
    },
}


def descriptor(row):
    cat, brand, name, sub = row["category"], row["brand"], row["product_name"], row["subcategory"]
    if cat in ("Tires", "Wheels", "Electrical", "Fluids"):
        return name
    variant = row.get("variant_value", "").strip()
    if variant and cat in ("Filters", "Accessories", "Lighting & visibility"):
        return f"{sub} ({brand}, {variant})"
    return f"{sub} by {brand}"


def make_question(row, idx, lang):
    veh = row["vehicle_compatibility"]
    cat = row["category"]
    # Symptom/implicit phrasing whenever the category + vehicle support it and on a
    # 1-in-3 cadence (exercises the agent's inference; part is not named).
    if idx % 3 == 0 and veh and veh != "Universal" and cat in TPL_SYMPTOM:
        return TPL_SYMPTOM[cat][lang].format(veh=veh), True
    desc = descriptor(row)
    if veh and veh != "Universal":
        return TPL_VEHICLE[lang].format(desc=desc, veh=veh), False
    return TPL_UNIVERSAL[lang].format(desc=desc), False


def main():
    base, extra = divmod(TOTAL, len(FEEDS))
    counts = [base + (1 if i < extra else 0) for i in range(len(FEEDS))]

    sampled = []
    for fn, n in zip(FEEDS, counts):
        rows = list(csv.DictReader(open(fn, encoding="utf-8"), delimiter="\t"))
        pool = [r for r in rows
                if r["availability"] in ("On order", "Incoming") and r["stock_qty"] == "0"]
        picks = random.sample(pool, n)
        for r in picks:
            r["_feed"] = os.path.basename(fn)
        sampled.append(picks)

    ordered = []
    i = 0
    while len(ordered) < TOTAL:
        for feed_picks in sampled:
            if i < len(feed_picks):
                ordered.append(feed_picks[i])
                if len(ordered) == TOTAL:
                    break
        i += 1

    cols = [
        "question_id", "language", "customer_email", "customer_question", "implicit",
        "expected_supplier", "expected_feed_file", "expected_sku",
        "expected_product_name", "expected_brand", "expected_category",
        "expected_vehicle", "expected_variant",
        "availability", "expected_lead_time", "expected_price_incl_vat", "currency",
    ]
    n_implicit = 0
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for idx, r in enumerate(ordered, 1):
            lang = LANGS[(idx - 1) % len(LANGS)]
            email = EMAILS[(idx - 1) % len(EMAILS)]
            q, implicit = make_question(r, idx, lang)
            n_implicit += int(implicit)
            w.writerow([
                f"Q{idx:03d}", lang, email, q, "yes" if implicit else "no",
                r["supplier"], r["_feed"], r["supplier_sku"],
                r["product_name"], r["brand"], r["category"],
                r["vehicle_compatibility"], r.get("variant_value", ""),
                r["availability"], r["lead_time"],
                r["retail_price_incl_vat"], r["currency"],
            ])
    print(f"Done: {TOTAL} questions -> {OUT}  ({n_implicit} implicit/symptom-based)")


if __name__ == "__main__":
    main()
