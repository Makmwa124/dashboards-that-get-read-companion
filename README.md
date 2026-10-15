# Dashboards That Get Read: companion files

Free practice files for the book **Dashboards That Get Read: Design Principles and Before-and-After Makeovers for Executive Dashboards** by Mathew Kariuki.

Everything here goes with the book's running example, Coastline Outfitters (a fictional outdoor retailer): the practice data, the code behind every chart and output in the book, the Power BI theme and DAX measures, the Tableau calculated fields, and the templates from the appendices.

## Download

Click the green **Code** button near the top of this page, then choose **Download ZIP**. Unzip it anywhere on your computer. You don't need a GitHub account.

## What's here

| Folder | What it contains |
|---|---|
| `data/` | Coastline Outfitters data, July 2024 to June 2026: `orders.csv` (65,560 orders), `targets.csv`, `service_monthly.csv` and `usage_log.csv`, plus the same tables as `coastline.xlsx` and `coastline.sqlite` |
| `code/` | `coastline.py` (shared helpers and the Chapter 6 palette), `figures.py` (draws every chart in the book), `make_data.py` (regenerates the data) |
| `code/chapters/` | The Python and SQL from each chapter, named by chapter (for example `ch08_variance.py`, `ch12_quality_checks.sql`) |
| `powerbi/` | `coastline_theme.json` (the report theme from Chapter 6) and `measures.dax` (the measures from Chapter 11) |
| `tableau/` | `calculated_fields.txt` (the Tableau equivalents from Chapter 11) |
| `templates/` | `dashboard_brief.docx`, `review_checklist.xlsx`, `chart_chooser.xlsx` and `region_scorecard.xlsx` (Chapter 9's formulas and conditional formatting) |
| `makeovers/` | Every before-and-after chart from the book at full size (300 dpi PNG) |

## Quick start

You don't need Python to use the book: open the data in Excel, Power BI or Tableau and follow along. If you do want to run the code:

1. Install Python 3.11 or later.
2. In a terminal, from this folder, install the packages: `pip install -r requirements.txt`
3. Redraw every chart: `python code/figures.py` (images are written to `makeovers/`)
4. Run a chapter's code, for example: `cd code/chapters` then `python ch08_variance.py`
5. Run the SQL checks from Chapter 12: `python code/chapters/run_sql.py code/chapters/ch12_quality_checks.sql`

For Power BI, load the CSV files, import `powerbi/coastline_theme.json` (Design ribbon > Import theme) and create the measures from `powerbi/measures.dax`. `code/chapters/ch11_check_dax.py` prints the values your measures should return.

## Get the book

- **eBook + practice files (PDF bundle with a cheat sheet):** [mathewkariuki.gumroad.com/l/dashboards-that-get-read](https://mathewkariuki.gumroad.com/l/dashboards-that-get-read)
- **Paperback and Kindle:** coming soon on Amazon

## About

Coastline Outfitters and all the people in its examples are fictional, and the data is generated. The files in this repository are free to use for learning. The book is © 2026 Mathew Kariuki.
