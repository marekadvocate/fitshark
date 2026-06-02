# fitshark

Testovacie dátové feedy automobilového sortimentu pre vývoj a testovanie agentov.

## Prehľad

`feeds/` obsahuje **11 syntetických dodávateľských feedov**, každý od iného (fiktívneho) dodávateľa.
Slúžia ako vstupné dáta pre agenta, ktorý spracúva produktové feedy z Google Sheets.

> ⚠️ Všetky dáta sú **vygenerované / syntetické** — fiktívni dodávatelia, náhodné kódy, EAN aj ceny.
> Značky výrobcov (Bosch, Brembo, Mann-Filter…) a modely vozidiel sú reálne len pre realistickosť feedu.

### Parametre

- **11 feedov × 10 000 SKU** (1 riadok = 1 SKU/variant)
- **67 stĺpcov** na produkt
- Trh SK, mena EUR, DPH 23 %
- Formát **TSV (TAB-oddeľované)** — pripravené na priame vloženie do Google Sheets

### Zoznam feedov

| Súbor | Dodávateľ | Zameranie |
|---|---|---|
| `feed_mds.tsv` | MotoDiely SK s.r.o. | plný sortiment |
| `feed_aps.tsv` | AutoParts Slovakia s.r.o. | plný sortiment |
| `feed_bpr.tsv` | BrzdyPro s.r.o. | brzdy |
| `feed_flc.tsv` | FilterCentrum s.r.o. | filtre |
| `feed_olx.tsv` | OlejExpert s.r.o. | oleje / kvapaliny |
| `feed_pns.tsv` | PneuServis SK s.r.o. | pneumatiky + disky |
| `feed_ela.tsv` | ElektroAuto s.r.o. | batérie + osvetlenie |
| `feed_dex.tsv` | DielyExpres s.r.o. | náhradné diely |
| `feed_cst.tsv` | CarStyle s.r.o. | autodoplnky |
| `feed_eud.tsv` | EuroDiely a.s. | plný sortiment |
| `feed_mmk.tsv` | MotoMarket s.r.o. | plný sortiment |

### Skupiny parametrov (67 stĺpcov)

Identita (kód, EAN, MPN, OE čísla, TecDoc) · značka/zaradenie · texty (názov, krátky/dlhý popis) ·
varianty (typ, hodnota, pozícia montáže, strana, farba) · ceny (VOC/MOC bez aj s DPH, marža %, rabat,
akciová cena, cena za jednotku, záloha za repas. diel) · sklad a logistika · fyzické rozmery a hmotnosť ·
automotive (kompatibilita vozidla, roky výroby, normy, HS colný kód, krajina pôvodu, stav nový/repas) ·
EÚ štítok pneumatík · normy olejov · médiá a meta.

## Vloženie do Google Sheets

1. Otvor `feeds/feed_<prefix>.tsv` → **Cmd/Ctrl+A → Cmd/Ctrl+C**
2. V Google Sheets klikni na bunku **A1** → **Cmd/Ctrl+V**
3. TAB-oddeľovač sa automaticky rozhodí do 67 stĺpcov.

Ak sa čísla zobrazia ako text: *Súbor → Nastavenia → Miestne nastavenie* (feedy majú desatinnú bodku, ISO dátum).

## Generovanie

`scripts/` obsahuje generátory (Python 3, bez závislostí):

```bash
cd scripts
python3 generate_rich.py   # aktuálne: 11 feedov × 67 parametrov (TSV)
```

- `generate_rich.py` — aktuálny generátor (67-stĺpcový TSV)
- `generate_feed.py` — pôvodné jadro generátorov kategórií
- `generate_varied.py` — variant s heterogénnymi schémami (SK/EN/CZ/DE, rôzne oddeľovače) na test normalizácie

Generovanie je deterministické (pevný seed na dodávateľa) — opakované spustenie dá identické feedy.
