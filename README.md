# ICE / CBP hiring-surge analysis (OPM EHRI)

Did the 2025 DHS hiring surge — especially at ICE and CBP — actually put officers on the payroll, and
are they staying? Built from OPM/EHRI records for hires, departures, and monthly headcount
(`impactproject/opm-ehri-data` on HuggingFace), read directly with DuckDB.

## Deliverables
- **`dhs_hiring_surge.ipynb`** — the analysis, start to finish (charts + tables inline).
- **`memo.md`** — one-page memo, every figure cross-referenced to a notebook section.

## Reproduce
```bash
pip install duckdb pandas matplotlib nbformat nbconvert jupyter
python src/extract.py          # pull the ICE+CBP slice (2018→) -> data/*.parquet
python src/history.py          # long-run 2006-2017 hiring + agency-code stability audit -> data/*.csv
jupyter nbconvert --to notebook --execute --inplace dhs_hiring_surge.ipynb
```

## Layout
- `src/extract.py` — DuckDB query over the HuggingFace parquet; caches a small ICE+CBP
  extract to `data/` (hires & departures 2018→, headcount 2022→).
- `src/history.py` — pulls 2006–2017 ICE/CBP new-hire history and a reproducible agency-code stability
  audit (`data/ice_cbp_hires_history.csv`, `data/agency_code_audit.csv`).
- `src/surge.py` — shared constants: ICE=`HSBB`, CBP=`HSBD`, the surge-hire profile
  (GL pay plan + job series 1801/1811), and the analysis windows.
- `data/hf_file_map.json` — deduped max-version HuggingFace file list the extracts read from.

## Method
OPM's monthly files are incremental — each one carries mostly that month's actions plus a trickle of
late-reported earlier ones (December 2025, the peak surge month, was only ~30% complete in its own
file). So a clean per-month series needs summing across every file and grouping by the date an action
took effect, not by which file reported it — one file per month would undercount the surge badly.
Redaction hides values like work location but keeps the person in the totals. ICE (`HSBB`) and CBP
(`HSBD`) are the only matching agency codes, stable back to 2008 — lookalikes like USCIS (`HSAB`) and
DOJ immigration courts (`DJ12`) are excluded. Surge hires are identified by job (pay plan `GL`, series
1801/1811), not length of service, since service years mix genuine new hires with rehires and veterans
carrying years of prior federal credit. All four of these are checked live against the data in the
notebook's **§0**, not just asserted.

## Headline findings
The surge was overwhelmingly **ICE** (2025: ~8× normal hiring, ~5.3× ICE's all-time prior peak of 1,966 in
2009 — the 2017 "hire 10,000 officers" order produced nothing like it), concentrated in **Sept 2025–Jan
2026** in **entry immigration-enforcement officer roles** (series 1801/1811, GL plan). ICE headcount grew
~46% (20.9k→30.5k) then slipped ~5% by Jul 2026. The leavers are the surge hires themselves —
identified by job, not length of service — and **more than 1 in 4 has already left, ~69% by
voluntary quit** — before the cohort's first year is even up, already past what comparable CBP entry
classes shed over a *full* year (~10–11%), and closing on CBP's worst rapid-hire surges (~29% in
2019–21).

![Monthly new hires, ICE vs CBP](figures/monthly_hires.png)
![Share of the ICE surge hires who have already left](figures/cohort_exited.png)
