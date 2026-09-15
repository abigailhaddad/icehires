# The DHS hiring surge in ICE & CBP: how big, did it stick, who's leaving?

**Analyst memo · data through Jul 2026 · every figure is reproduced in `dhs_hiring_surge.ipynb`**

**Bottom line.** The 2025 DHS surge was overwhelmingly an **ICE** event, concentrated in **Sept 2025–Jan 2026** and in **entry immigration-enforcement officer jobs**. It did put people on the payroll — ICE grew about 46% — and headcount has since slipped further (about 5% off its January peak) as those hires begin to leave. **More than one in four of the ~7,200 entry-officer surge hires has already left** — mostly by quitting — before their first year is even up, already past what comparable CBP law-enforcement classes shed over a *full* year (~10–11%).

**Source.** OPM/EHRI records for hires, departures, and monthly headcount, read directly from the HuggingFace dataset `impactproject/opm-ehri-data`. ICE = agency code `HSBB`, CBP = `HSBD`. Each record is a *count of people*, not one named individual — see caveats.

---

### 1. The surge was ICE, and it was big but brief · *notebook §1*
ICE normally hires about 700–1,350 people a year. In **2025 it hired 10,474** — roughly **8× normal** — and the burst was tightly concentrated: about **10,133 hires fell in the five months Sept 2025–Jan 2026** alone, peaking in December, then falling back to normal monthly levels. It is about 99.6% genuine new hires, **not** transfers from other agencies (transfers = 0.4%). **CBP's increase was modest** (2025 was about 1.2× its 2024 level); its ramp is smaller, later, and Border-Patrol-focused.

![Monthly new hires, ICE vs CBP — a sharp, brief ICE burst in Sept 2025–Jan 2026 (shaded); CBP barely moves.](figures/monthly_hires.png){width=6in}

### 1b. The biggest hiring year in ICE's history · *notebook §1b*
Extending the series back to 2006, ICE's previous *annual* hiring record was about **1,966 (2009)**; 2025's 10,474 is about **5.3× ICE's all-time record and 8× its recent norm**. The **2017 executive order directing 10,000 new ICE officers produced no visible surge** — hiring stayed near 700–1,300/year. The only comparable buildup in this data is **CBP in 2007–2009** (about 7,000–9,000 hires/year, the Bush-era Border Patrol expansion); and CBP's most recent rapid entry-officer push, in 2019–21, lost nearly 30% of new hires within the first year (§4b).

### 2. It reached the payroll — then kept edging down · *notebook §2*
ICE headcount went from **20,848 (Aug 2025) to 30,461 (Jan 2026)**, a roughly 46% jump. It has since **slipped to 28,861 (Jul 2026), down 1,600 (−5.3%) from the peak**, even though some hiring continued — a larger decline than it looked a couple of months ago (−4% as of May), consistent with the surge cohort continuing to leave (§4). CBP rose gradually (67.3k→70.3k since Aug 2025) with no reversal. So the ICE workforce is still far above its pre-surge level — up roughly 8,000 since August even after the slip — but the ~5% decline from January's peak is real, and §§3–4 show it is the surge hires themselves leaving.

### 3. Who the surge hires are — a job profile · *notebook §3*
With no person IDs, we identify the surge hires by the **jobs they were hired into**, comparing them with normal ICE hiring. The surge is unmistakable in job and pay plan: **job series 1801** (*General Inspection, Investigation, Enforcement, and Compliance* — the ICE deportation / immigration-enforcement officer series) is about 64% of surge hires vs 20% normally (**3.2× as common**); with **1811** (*Criminal Investigation*) the two are about 87%. **About 68% are on the `GL` entry law-enforcement pay plan** at grades **GL-05/07/09**. Other markers: term (non-permanent) appointments are about 3× as common, and the age mix skews unusually **older**. Profile = **GL pay plan + series 1801/1811**. Because ICE had almost no one in these jobs before the surge, any jump in departures from them *is* the surge hires.

### 4. The leavers are the surge hires — and they're mostly quitting, not being let go · *notebook §4*
Departures from these jobs ran a flat **27–46 per year (2018–2024)**, then jumped to **739 (2025)** and **1,303 in just the first seven months of 2026** — already 76% more than *all* of 2025, in barely half the year — about 50–60× the prior norm, beginning the same month hiring did. Of those exits, about **69% are voluntary quits and about 27% are involuntary terminations** (expired term appointments plus some probationary removals; the data lumps the two together).

### 4b. More than one in four is already gone — before the first year is up · *notebook §4b*
Watching the whole group's exits against its own hires, **1,987 of 7,214 surge hires (27.5%) had left by Jul 2026**, and still climbing because hiring stopped while exits continue. We can't yet state an ICE *first-year* rate: the group's first year isn't over for the cohort as a whole (the earliest arrivals, from Sept 2025, have only about ten months in; later arrivals less), and annualizing a partial year would mislead. But that ~28% already exceeds what CBP's comparable entry classes shed over a **full** first year — about **10–11%** for **Border Patrol (series 1896-GL, *Border Patrol Enforcement*)** and **CBP Officer (series 1895, *Customs and Border Protection*)** in 2023–24 — and is closing on the roughly **29%** that CBP's own **2019–21** rapid-hire Border Patrol classes lost across a full year. ICE's early loss is already near the high end of that range, with its first year not yet complete.

![Cumulative share of the ~7,200 entry-officer surge hires who had separated, by month — more than one in four within the first year, and still climbing.](figures/cohort_exited.png){width=6in}

---

### What the data can't say (caveats) · *notebook §5, checked in §0*
- **Counts, not people.** We match *departing* jobs to *hiring* jobs; we can't prove a specific leaver was a specific fall-2025 hire. The match is tight only because these GL entry jobs held few people before the surge (~1,500 in Aug 2025, small next to the ~7,200 hired into them). The group we track cleanly is the ~68% who are entry law-enforcement officers (GL-1801/1811); the higher-grade officers and attorneys can't be isolated the same way.
- **Length of service is not time in the job.** The service figure is *total federal service*; about 30% of 2025 ICE new hires arrived with 3+ years of prior service — a mix of veterans (military credit) and prior federal civilians (rehires), **not transfers**. This is why we define the group by job and grade, not by length of service.
- **Headcount and flow don't reconcile** — hires minus departures lags the headcount change by about 15–20% (timing plus provisional late reporting), so we use headcount for *levels* and departures for *exits*, never chained. The "headcount is declining" finding rests on complete point-in-time headcount snapshots, not on provisional flows.
- **Involuntary exits can't be fully split** (term-appointment expiration vs. removal for cause), and the elevated departures are **not** a buyout-program artifact: the separations `drp_indicator` field flags **none** of the 1,987 cohort departures (and none of the ~4,100 ICE departures in the window) as deferred-resignation-program exits.

**Method checked (notebook §0):** ICE=HSBB / CBP=HSBD confirmed as the only ICE/CBP codes, stable 2008–2026; monthly files confirmed to *add* new actions, so summing across files and grouping by the effective-date field is required (a single file holds only ~30% of December's hires, so one-file-per-month undercounts that surge month by ~70%) and does not double-count; redaction preserves totals; headcount de-duplicated to one snapshot per file.

*Reproduce: `python src/extract.py` and `python src/history.py` (pull the data → `data/`), then run `dhs_hiring_surge.ipynb`. The surge-hire definition and windows are in `src/surge.py`.*
