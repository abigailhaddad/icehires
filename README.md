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
- `data/hf_file_map.json` — deduped max-version HuggingFace file list the extracts read from (committed;
  `src/extract.py` and `src/history.py` read it but don't regenerate it). `data/*.parquet` are the
  extracts themselves — git-ignored, rebuilt by `python src/extract.py`.

## Method
This analysis rests on six assumptions about the data, each verified directly against the raw files
in the notebook's **§0**.

- **Files add, they don't restate.** OPM's monthly files are incremental — each one is mostly that
  month's actions plus a trickle of late-reported earlier ones (December 2025, the peak surge month,
  was only ~30% complete in its own file). A clean per-month series means summing across every file
  and grouping by when the action took effect, not by which file reported it — one file per month
  would badly undercount the surge.
- **Agency codes are stable and exclusive.** ICE = `HSBB`, CBP = `HSBD`, unchanged back to 2008.
  Lookalikes — USCIS (`HSAB`), DOJ immigration courts (`DJ12`) — are separate agencies and excluded.
- **Redaction hides values, not people.** A masked field (like work location) is relabeled, not
  dropped, so headcount and job totals still include everyone.
- **Surge hires are identified by job, not length of service.** The profile is pay plan `GL` + job
  series 1801/1811. Length of service mixes genuine new hires with rehires and veterans who arrive
  carrying years of prior federal credit, so it can't do this cleanly.
- **The departures we attribute to the surge cohort aren't mostly the ~1,500 people who already held
  these jobs before the surge, just leaving at their normal pace.** We can't prove that outright — there
  are no person IDs — but this job group's own attrition rate in the two years before the surge (2023–24,
  the years its headcount is large enough to trust) was about 7% a year. Applied to the group's actual
  size going into the surge (1,511 people, Aug 2025), that's roughly 5% of what we count as surge-cohort
  departures. The rest has to be the surge hires themselves.
- **Headcount for this job slice fell more than hires-minus-departures explains** — down 1,822 since
  the January peak, vs. 738 accounted for by flow, a 59% gap (ICE overall has a smaller, 20% version
  of the same gap). Checked and ruled out: promotion into GS-paid roles, a mass-transfer recoding
  event, reclassification to another pay plan. The decline is broad across every age bracket and
  grade, not concentrated in a small cell, so it isn't people dropping out of the data. The mechanism
  for the rest is unresolved — but nothing found points toward the departure count being too high.
- **A higher base-group attrition rate doesn't erase the headline number.** The bound above assumes
  the ~1,500 pre-existing job holders kept leaving at their flat 2023-24 rate (~7%/year). Triple that
  rate to ~21%/year — never seen in this job group — and the cohort-exit figure only drops a few
  points. It would take a ~143%/year rate, more than the whole group leaving, to explain all tracked
  departures without any surge-hire exits at all.
- **This job group's own separations land later than a typical month.** Only ~52% of its eventual
  departures show up in the event month's own file, versus ~99% for a typical ICE+CBP separation.
  Projecting that lag onto the still-thin recent months puts current attrition closer to ~31% than the
  raw ~28% figure quoted below — if anything, that makes the headline number too low, not too high.

## Headline findings
The surge was overwhelmingly **ICE** (2025: ~8× normal hiring, ~5.3× ICE's all-time prior peak of 1,966 in
2009 — the 2017 "hire 10,000 officers" order produced nothing like it), concentrated in **Sept 2025–Jan
2026** in **entry immigration-enforcement officer roles** (series 1801/1811, GL plan). ICE headcount grew
~46% (20.9k→30.5k) then slipped ~5% by Jul 2026. The leavers are the surge hires themselves (see
Method for how we identify them), and **more than 1 in 4 has already left, ~69% by voluntary quit** —
before the cohort's first year is even up, against this same job group's own ~7%-a-year normal rate
before the surge, and already past what comparable CBP entry classes shed over a *full* year (~10–11%),
closing on CBP's worst rapid-hire surges (~29% in 2019–21). It isn't just fast growth: CBP's own entry
officer jobs also grew substantially over this same window (headcount roughly doubled) without a
comparable spike in attrition — what's different about ICE is the shape of the growth, not the growth
itself.

![Monthly new hires, ICE vs CBP](figures/monthly_hires.png)
![Share of the ICE surge hires who have already left](figures/cohort_exited.png)
