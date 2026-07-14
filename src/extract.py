"""Serverside-query ICE (HSBB) + CBP (HSBD) accessions, separations, and employment
from the impactproject/opm-ehri-data HuggingFace dataset and cache small local extracts.

Each monthly OPM "dynamics" file is incremental: it is dominated by actions whose
effective month equals the file month, plus a decaying tail of late-reported prior-month
actions. So the authoritative event-month series is built by summing `count` across ALL
files grouped by `personnel_action_effective_date_yyyymm`. We keep row-level cells here
so the notebook can slice by category / tenure / series; it does the grouping.
"""
import json
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://huggingface.co/datasets/impactproject/opm-ehri-data/resolve/main"
ICE_CBP = ("HSBB", "HSBD")  # HSBB = ICE, HSBD = CBP

file_map = json.load(open(ROOT / "data" / "hf_file_map.json"))


def urls(kind, min_ym):
    m = file_map[kind]
    return [f"{BASE}/{m[ym]}" for ym in sorted(m) if ym >= min_ym]


def url_list(us):
    return "[" + ",".join(f"'{u}'" for u in us) + "]"


def run():
    con = duckdb.connect()
    con.execute("SET enable_progress_bar=false;")
    agy = "('" + "','".join(ICE_CBP) + "')"

    # ---- Accessions (new hires / transfers in), 2018-01 onward ----
    us = urls("accessions", "201801")
    print(f"accessions: reading {len(us)} remote files ...", flush=True)
    con.execute(f"""
        COPY (
          SELECT personnel_action_effective_date_yyyymm AS event_ym,
                 agency_subelement_code AS agy_code, agency_subelement AS agency,
                 accession_category, accession_category_code,
                 appointment_type, pay_plan, pay_plan_code,
                 occupational_series, occupational_series_code, occupational_category,
                 grade, age_bracket, length_of_service_years, work_schedule,
                 duty_station_state_abbreviation AS duty_state,
                 duty_station_city AS duty_city, duty_station_code AS duty_code,
                 count::INT AS count,
                 regexp_extract(filename, '_(\\d{{6}})_v', 1) AS file_ym
          FROM read_parquet({url_list(us)}, union_by_name=true, filename=true)
          WHERE agency_subelement_code IN {agy}
        ) TO '{ROOT/'data'/'acc_ice_cbp.parquet'}' (FORMAT parquet);
    """)

    # ---- Separations (departures), 2018-01 onward ----
    us = urls("separations", "201801")
    print(f"separations: reading {len(us)} remote files ...", flush=True)
    con.execute(f"""
        COPY (
          SELECT personnel_action_effective_date_yyyymm AS event_ym,
                 agency_subelement_code AS agy_code, agency_subelement AS agency,
                 separation_category, separation_category_code,
                 pay_plan, pay_plan_code,
                 occupational_series, occupational_series_code, occupational_category,
                 grade, age_bracket, length_of_service_years, work_schedule,
                 duty_station_state_abbreviation AS duty_state,
                 duty_station_city AS duty_city, duty_station_code AS duty_code,
                 count::INT AS count,
                 regexp_extract(filename, '_(\\d{{6}})_v', 1) AS file_ym
          FROM read_parquet({url_list(us)}, union_by_name=true, filename=true)
          WHERE agency_subelement_code IN {agy}
        ) TO '{ROOT/'data'/'sep_ice_cbp.parquet'}' (FORMAT parquet);
    """)

    # ---- Employment (point-in-time headcount), 2022-01 onward, aggregated ----
    us = urls("employment", "202201")
    print(f"employment: reading {len(us)} remote files ...", flush=True)
    con.execute(f"""
        COPY (
          SELECT snapshot_yyyymm AS snapshot_ym,
                 agency_subelement_code AS agy_code, agency_subelement AS agency,
                 occupational_series, occupational_series_code,
                 pay_plan, pay_plan_code, work_schedule,
                 SUM(count::INT) AS count
          FROM read_parquet({url_list(us)}, union_by_name=true)
          WHERE agency_subelement_code IN {agy}
          GROUP BY 1,2,3,4,5,6,7,8
        ) TO '{ROOT/'data'/'emp_ice_cbp.parquet'}' (FORMAT parquet);
    """)

    for f in ("acc_ice_cbp", "sep_ice_cbp", "emp_ice_cbp"):
        n = con.execute(f"SELECT COUNT(*) FROM '{ROOT/'data'/(f+'.parquet')}'").fetchone()[0]
        print(f"  {f}: {n:,} rows")


if __name__ == "__main__":
    run()
