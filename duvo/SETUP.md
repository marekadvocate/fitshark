# One-time setup — Google Sheets

The agent reads two Google Sheets. Create them once, then paste their URLs into
`MCP_CREATE_PROMPT.md` (two `<...>` placeholders) and into `ASSIGNMENT_SOP.md`.

> Create both sheets in the **same Google account** whose Sheets connection you'll pin in
> Duvo. Default in the prompt: `marekpodhorsky1993@gmail.com` (its Sheets **and** Gmail are
> both connected, so one identity reads the sheets and sends the mail). If you'd rather use
> `dominikfroncik@gmail.com` for the sheets, pin that Sheets connection instead.

## 1. Questions sheet
1. New Google Sheet → name it `Fitshark — Customer Questions`.
2. Rename the first tab to **`Questions`**.
3. **File → Import → Upload** `duvo/questions_sheet.csv` → *Replace current sheet* →
   separator *Comma* → *Import*. (100 rows, all `status = Pending`, recipient already set to
   dominikfronc@gmail.com.)
4. Copy the sheet URL → this is `<QUESTIONS_SHEET_URL>`.

## 2. Catalog sheet
1. New Google Sheet → name it `Fitshark — Product Catalog`.
2. Rename the first tab to **`Catalog`**.
3. **File → Import → Upload** `duvo/catalog.csv` → *Replace current sheet* → separator
   *Comma* → *Import*. (110,000 rows × 15 columns; the import may take a minute.)
4. Add a second tab named **`Scratch`** (the agent writes QUERY lookups into `Scratch!A1`).
5. Copy the sheet URL → this is `<CATALOG_SHEET_URL>`.

> The Catalog is the searchable product DB. The agent never loads it into context — it runs
> a `=QUERY(...)` against it and reads back only the matched row, so 110k rows is fine.

## 3. Fill the placeholders
In `MCP_CREATE_PROMPT.md` and `ASSIGNMENT_SOP.md`, replace:
- `<QUESTIONS_SHEET_URL>` → the Questions sheet URL
- `<CATALOG_SHEET_URL>` → the Catalog sheet URL

## 4. Create the agent
Run the prompt in `MCP_CREATE_PROMPT.md` from a Duvo-MCP-connected client.

## 5. Run + approve
Open the assignment in Duvo → **Start Work**. For each question an **approval** appears in the
**Activity Inbox** (and Slack/Teams if enabled) showing the drafted email — Approve to send to
dominikfronc@gmail.com, or Deny to skip. Watch progress in the Questions sheet `status` column.
