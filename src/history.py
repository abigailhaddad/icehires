"""Pull long-run ICE/CBP new-hire history (2006-2017) to put the 2025 surge in context, and emit a
reproducible agency-code stability audit. Reads raw HF files with per-year retries (HF can be flaky).
Writes data/ice_cbp_hires_history.csv and data/agency_code_audit.csv.
"""
import sys, json, time
sys.path.insert(0, "src")
import surge
import pandas as pd

con = surge.con()
B = "https://huggingface.co/datasets/impactproject/opm-ehri-data/resolve/main"
fm = json.load(open("data/hf_file_map.json"))


def urls(kind, y0, y1):
    return [f"{B}/{fm[kind][ym]}" for ym in sorted(fm[kind])
            if ym.endswith(("01","02","03","04","05","06","07","08","09","10","11","12"))
            and y0 <= ym[:4] <= y1]


def read_retry(sql, tries=5):
    for i in range(tries):
        try:
            df = con.execute(sql).df()
            if len(df) == 0 and i < tries - 1:   # HF sometimes returns empty on soft-throttle
                time.sleep(6); continue
            return df
        except Exception:
            if i == tries - 1: raise
            time.sleep(6)


# ---- Historical ICE/CBP new-hire totals, one year of files at a time ----
hist = []
for yr in [str(y) for y in range(2006, 2018)]:
    us = urls("accessions", yr, yr)
    lst = "[" + ",".join(f"'{u}'" for u in us) + "]"
    try:
        d = read_retry(f"""
          SELECT substr(personnel_action_effective_date_yyyymm,1,4) AS year,
                 agency_subelement_code AS agy, SUM(count::INT) AS new_hires
          FROM read_parquet({lst}, union_by_name=true)
          WHERE agency_subelement_code IN ('HSBB','HSBD')
            AND accession_category LIKE 'NEW HIRE%'
            AND substr(personnel_action_effective_date_yyyymm,1,4) = '{yr}'
          GROUP BY 1,2
        """)
        hist.append(d); print(f"{yr}: {len(us)} files -> {dict(zip(d.agy, d.new_hires))}", flush=True)
    except Exception as e:
        print(f"{yr}: FAILED {str(e)[:60]}", flush=True)

if hist:
    out = pd.concat(hist, ignore_index=True)
    out.to_csv("data/ice_cbp_hires_history.csv", index=False)
    print("saved data/ice_cbp_hires_history.csv", len(out), "rows")

# ---- Agency-code stability audit (only ICE/CBP-named DHS subelements per year) ----
aud = []
for ym in ["200806","201206","201606","201806","202006","202206","202406","202506"]:
    try:
        d = read_retry(f"""SELECT '{ym[:4]}' AS year, agency_subelement_code AS code,
             agency_subelement AS agency_name, SUM(count::INT) AS accessions
             FROM read_parquet('{B}/{fm['accessions'][ym]}')
             WHERE regexp_matches(upper(agency_subelement), 'IMMIGRATION|CUSTOMS|BORDER')
             GROUP BY 1,2,3 ORDER BY 2""")
        aud.append(d); print(f"audit {ym}: ok", flush=True)
    except Exception as e:
        print(f"audit {ym}: FAILED {str(e)[:60]}", flush=True)
if aud:
    a = pd.concat(aud, ignore_index=True)
    a.to_csv("data/agency_code_audit.csv", index=False)
    print("saved data/agency_code_audit.csv"); print(a.to_string(index=False))

# ---- Occupational-series names (USAJOBS public codelist; no API key needed) ----
# https://developer.usajobs.gov/api-reference/get-codelist-occupationalseries
import urllib.request
try:
    req = urllib.request.Request("https://data.usajobs.gov/api/codelist/occupationalseries",
                                 headers={"User-Agent": "icehires-research"})
    cl = json.load(urllib.request.urlopen(req, timeout=60))["CodeList"][0]["ValidValue"]
    occ = pd.DataFrame({"code": [v["Code"] for v in cl],
                        "name": [(v.get("Value") or "").replace(" And ", " and ") for v in cl]})
    occ.sort_values("code").to_csv("data/occ_series_names.csv", index=False)
    print("saved data/occ_series_names.csv", len(occ), "series")
except Exception as e:
    print("occ-series codelist pull FAILED:", str(e)[:80])
