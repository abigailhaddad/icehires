"""Shared constants and helpers for the DHS/ICE hiring-surge analysis.

The notebook and the memo both import from here so every cited number comes from
one definition of "the surge cohort" and one set of query windows.
"""
from pathlib import Path
import duckdb

DATA = Path(__file__).resolve().parent.parent / "data"
ACC = str(DATA / "acc_ice_cbp.parquet")
SEP = str(DATA / "sep_ice_cbp.parquet")
EMP = str(DATA / "emp_ice_cbp.parquet")

ICE, CBP = "HSBB", "HSBD"

# The ICE surge cohort fingerprint, derived empirically in the notebook:
# entry law-enforcement officers hired onto the GL pay plan in series
# 1801 (deportation/enforcement officer) and 1811 (criminal investigator).
SURGE_FP = "pay_plan_code = 'GL' AND occupational_series_code IN ('1801','1811')"
NEW_HIRE = "accession_category LIKE 'NEW HIRE%'"

# Windows. Event months are `personnel_action_effective_date_yyyymm`.
BASELINE_YEARS = ("2018", "2024")   # pre-surge normal
SURGE_WINDOW = ("202509", "202601")  # ICE burst: Sep 2025 - Jan 2026
LATEST_MONTH = "202605"              # most recent data (provisional)


def con():
    c = duckdb.connect()
    c.execute("SET enable_progress_bar=false;")
    return c


def dbl(col):
    return f"TRY_CAST({col} AS DOUBLE)"
