"""Render the two standalone charts embedded in memo.md, into figures/.
Same data and styling as the corresponding notebook cells (§1 and §4b)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import surge
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.ticker as mtick, matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"; FIG.mkdir(exist_ok=True)
con = surge.con()
q = lambda s: con.execute(s).df()
ACC, SEP = surge.ACC, surge.SEP

C_ICE, C_CBP, C_EXIT, SPAN = "#2166ac", "#e08214", "#c0392b", "#fdd9a0"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "savefig.bbox": "tight", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#bbbbbb",
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlepad": 10,
    "axes.labelcolor": "#444", "axes.labelsize": 10, "xtick.color": "#444", "ytick.color": "#444",
    "axes.grid": True, "axes.axisbelow": True, "grid.color": "#dddddd", "grid.linewidth": 0.7,
    "legend.frameon": False,
})
def comma_y(ax): ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x:,.0f}"))
def date_x(ax):
    loc = mdates.AutoDateLocator(); ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

# ---- Figure 1: monthly new hires, ICE vs CBP ----
m = q(f"""
  SELECT event_ym,
    SUM(CASE WHEN agy_code='{surge.ICE}' AND {surge.NEW_HIRE} THEN count END) AS ICE,
    SUM(CASE WHEN agy_code='{surge.CBP}' AND {surge.NEW_HIRE} THEN count END) AS CBP
  FROM '{ACC}' WHERE event_ym >= '202301' GROUP BY 1 ORDER BY 1
""")
m["date"] = pd.to_datetime(m.event_ym, format="%Y%m")
fig, ax = plt.subplots(figsize=(8.5, 3.6))
ax.axvspan(pd.Timestamp("2025-09-01"), pd.Timestamp("2026-01-31"), color=SPAN, alpha=.7, zorder=0,
           label="ICE surge window (Sep 2025 – Jan 2026)")
ax.plot(m.date, m.ICE, marker="o", ms=4, lw=2, color=C_ICE, label="ICE")
ax.plot(m.date, m.CBP, marker="o", ms=4, lw=2, color=C_CBP, label="CBP")
ax.set(title="Monthly new hires: ICE vs CBP", ylabel="New hires per month")
comma_y(ax); date_x(ax); ax.legend(loc="upper left"); fig.tight_layout()
fig.savefig(FIG / "monthly_hires.png"); plt.close(fig)

# ---- Figure 2: cumulative share of the surge cohort who have separated ----
c = q(f"""
  WITH h AS (SELECT event_ym, SUM(count) hires FROM '{ACC}' WHERE agy_code='{surge.ICE}' AND {surge.NEW_HIRE} AND {surge.SURGE_FP} GROUP BY 1),
       s AS (SELECT event_ym, SUM(count) exits FROM '{SEP}' WHERE agy_code='{surge.ICE}' AND {surge.SURGE_FP} GROUP BY 1)
  SELECT m.event_ym,
    ROUND(100.0*SUM(COALESCE(exits,0)) OVER w / NULLIF(SUM(COALESCE(hires,0)) OVER w,0),1) AS pct
  FROM (SELECT event_ym FROM h UNION SELECT event_ym FROM s) m
  LEFT JOIN h USING(event_ym) LEFT JOIN s USING(event_ym)
  WHERE m.event_ym >= '202509' WINDOW w AS (ORDER BY m.event_ym) ORDER BY m.event_ym
""")
c["date"] = pd.to_datetime(c.event_ym, format="%Y%m")
fig, ax = plt.subplots(figsize=(8.5, 3.4))
ax.plot(c.date, c.pct, marker="o", ms=5, lw=2, color=C_EXIT)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.set(title="Share of the ICE surge hires who have already left",
       ylabel="Departures ÷ hires, running total"); date_x(ax); fig.tight_layout()
fig.savefig(FIG / "cohort_exited.png"); plt.close(fig)

print("wrote", FIG / "monthly_hires.png", "and", FIG / "cohort_exited.png")
