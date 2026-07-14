# The DHS hiring surge in ICE & CBP: how big, did it stick, who's leaving?

**Analyst memo · data through May 2026 · every figure is reproduced in `dhs_hiring_surge.ipynb`**

**Bottom line.** The 2025 DHS surge was overwhelmingly an **ICE** event, concentrated in **Sept 2025–Jan 2026** and in **entry immigration-enforcement officer jobs**. It did put people on the payroll — ICE grew about 46% — but the peak was brief: the same people are now leaving. About **one in four surge hires has already left within roughly 5–8 months**, mostly by quitting — and that is before their first year is even up, already past what comparable CBP law-enforcement classes shed over a *full* year (~10–11%).

**Source.** OPM/EHRI records for hires, departures, and monthly headcount, read directly from the HuggingFace dataset `impactproject/opm-ehri-data`. ICE = agency code `HSBB`, CBP = `HSBD`. Each record is a *count of people*, not one named individual — see caveats.

---

### 1. The surge was ICE, and it was big but brief · *notebook §1*
ICE normally hires about 700–1,300 people a year. In **2025 it hired 10,322** — roughly **8× normal** — with about **9,970 of those in Sept 2025–Jan 2026** alone, peaking in December, then falling back to normal monthly levels. It is about 99.6% genuine new hires, **not** transfers from other agencies (transfers = 0.4%). **CBP's increase was modest** (2025 was about 1.2× its baseline); its ramp is smaller, later, and Border-Patrol-focused. The disputed "surge" is real, and it is almost entirely ICE.

### 1b. It is unlike anything in ICE's history · *notebook §1b*
Extending the series back to 2006, ICE's previous *annual* hiring record was about **1,966 (2009)**; 2025's 10,322 is about **5× ICE's all-time record and 8× its recent norm**. The **2017 executive order directing 10,000 new ICE officers produced no visible surge** — hiring stayed at about 700–1,300/year. The only comparable buildup in this data is **CBP in 2007–2009** (about 7,000–9,000 hires/year, the Bush-era Border Patrol expansion) — precisely the kind of rapid buildup that historically loses a quarter or more of new hires early (§4b). ICE is now running that experiment for the first time, at record scale.

### 2. It reached the payroll — then started reversing · *notebook §2*
ICE headcount went from **20,848 (Aug 2025) to 30,461 (Jan 2026)**, a roughly 46% jump. But it has since **fallen to 29,219 (May 2026), down 1,242 (−4%) from the peak**, even though some hiring continued. CBP rose gradually (63k→69k) with no reversal. So for ICE, the answer to "how many stayed" is: the workforce did grow about 9,600, but the gain is already eroding.

### 3. Who the surge hires are — a job profile · *notebook §3*
With no person IDs, we identify the surge hires by the **jobs they were hired into**, scoring every attribute by how sharply surge hires differ from normal ICE hires. The surge is unmistakable in job and pay plan: **job series 1801** (*General Inspection, Investigation, Enforcement, and Compliance* — the ICE deportation / immigration-enforcement officer series) is about 64% of surge hires vs 20% normally (**3.2× as common**); with **1811** (*Criminal Investigation*) the two are about 87%. **About 68% are on the `GL` entry law-enforcement pay plan** at grades **GL-05/07/09**. Secondary tells: term (non-permanent) appointments are about 3× as common, and the age mix skews unusually **older**. **Work location is redacted for about 98% of these hires** — we can't map them, which itself confirms they are law-enforcement officers. Profile = **GL pay plan + series 1801/1811**. Because ICE had almost no one in these jobs before the surge, any jump in departures from them *is* the surge hires — with no reliance on length of service.

### 4. The leavers are the surge hires — and they're quitting, not being let go · *notebook §4*
Departures from these jobs ran a flat **27–46 per year (2018–2024)**, then jumped to **730 (2025)** and **1,058 in the first five months of 2026** — about 50–60× the prior norm, beginning the same month hiring did. Of those exits, about **71% are voluntary quits and about 26% are involuntary terminations** (expired term appointments plus some probationary removals; the data lumps the two together). The dominant pattern is people **taking the job and then leaving on their own**.

### 4b. About one in four is already gone — roughly 2× a comparable group · *notebook §4b*
Watching the whole group's exits against its own hires, **1,733 of 7,033 surge hires (24.6%) had left by May 2026** — within about 5–8 months, and still climbing because hiring stopped while exits continue. We can't yet state an ICE *first-year* rate: the cohort's first year isn't over, and annualizing a partial year would mislead. But that ~25% in 5–8 months already exceeds what CBP's comparable entry classes shed over a **full** first year — about **10–11%** for **Border Patrol (series 1896-GL, *Border Patrol Enforcement*)** and **CBP Officer (series 1895, *Customs and Border Protection*)** in 2023–24 — and is closing on the roughly **29%** that CBP's own **2019–21** rapid-hire Border Patrol classes lost across a full year. Rapid immigration-enforcement hiring reliably produces heavy early loss; ICE 2025 is tracking the bad end of that history, with months still to run.

---

### What the data can't say (caveats) · *notebook §5, checked in §0*
- **Counts, not people.** We match *departing* jobs to *hiring* jobs; we can't prove a specific leaver was a specific fall-2025 hire. The match is tight only because these GL entry jobs were nearly empty before the surge (~900 people). The group we track cleanly is the ~68% who are entry LE officers (GL-1801/1811); GS officers and attorneys can't be isolated the same way.
- **Length of service ≠ time in the job.** The service figure is *total federal service*; about 30% of 2025 ICE new hires arrived with 3+ years of prior service — a mix of veterans (military credit) and prior federal civilians (rehires), **not transfers**. That is exactly why we define the group by job and grade, not by length of service.
- **Headcount and flow don't reconcile** — hires minus departures lags the headcount change by about 15–20% (timing plus provisional late reporting), so we use headcount for *levels* and departures for *exits*, never chained. The "headcount is declining" finding rests on complete point-in-time headcount snapshots, not on provisional flows.
- **Involuntary exits can't be fully split** (term-appointment expiration vs. removal for cause); **work location is redacted** for about 98% of these LE hires (hidden as a value, not dropped — totals stay complete); and the elevated departures are **not** a buyout-program artifact (those programs hit senior incumbents; the surge hires came afterward and show 71% quits and essentially no retirements).

**Method checked (notebook §0):** ICE=HSBB / CBP=HSBD confirmed as the only ICE/CBP codes, stable 2008–2026; monthly files confirmed to *add* new actions, so summing across files and grouping by the effective-date field is required (single-file totals undercount the December surge by about 64%) and does not double-count; redaction preserves totals; headcount de-duplicated to one snapshot per file.

*Reproduce: `python src/extract.py` and `python src/history.py` (pull the data → `data/`), then run `dhs_hiring_surge.ipynb`. The surge-hire definition and windows are in `src/surge.py`.*
