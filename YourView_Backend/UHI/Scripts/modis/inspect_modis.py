"""
inspect_modis.py
----------------
Sanity check for MOD11A2 HDF files:
- Lists subdatasets
- Reads LST_Day_1km (+ LST_Night_1km if enabled)
- Applies a simple QC mask
- Converts to °C
- Prints quick stats
- NOW ALSO writes results to a CSV so you can see what a summary table will look like
"""

import os
import re
import csv
import numpy as np
from osgeo import gdal

RAW_DATA_DIR = "/Users/abhi/Documents/Uni/Sem 4/5120/YourView/UHI/Data/Raw_Data/UHI Data/MOD11A2_061-20250825_060433"
SAMPLE_COUNT = 3
CHECK_NIGHT = True

def list_hdf_files(raw_dir: str):
    hdfs = sorted(f for f in os.listdir(raw_dir) if f.lower().endswith(".hdf"))
    if not hdfs:
        raise FileNotFoundError(f"No .hdf files found in {raw_dir}")
    return hdfs

def pick_subdataset(subdatasets, suffix: str) -> str:
    for name, _desc in subdatasets:
        if name.endswith(suffix):
            return name
    raise RuntimeError(f"Subdataset not found: {suffix}")

def ayear_doy_from_filename(fname: str) -> str:
    m = re.search(r"\.A(\d{4})(\d{3})\.", fname)
    if m:
        return f"{m.group(1)}-DOY{m.group(2)}"
    return fname

def apply_qc_and_scale(lst_raw: np.ndarray, qc_raw: np.ndarray) -> np.ndarray:
    lst = lst_raw.astype("float32")
    fill_mask = (lst_raw == 0)
    good_mask = (qc_raw & 0b11) == 0
    mask = (~fill_mask) & good_mask
    lst = lst * 0.02 - 273.15
    lst[~mask] = np.nan
    return lst

def main():
    hdfs = list_hdf_files(RAW_DATA_DIR)
    sample = hdfs[:SAMPLE_COUNT]

    first_path = os.path.join(RAW_DATA_DIR, sample[0])
    print(f"🔎 Inspecting HDF container:\n  {first_path}\n")

    ds0 = gdal.Open(first_path)
    subs0 = ds0.GetSubDatasets()
    print("📦 Subdatasets found (first file):")
    for name, desc in subs0:
        print("  ", name)
    print()

    print(f"Processing the first {len(sample)} file(s) with QC masking…\n")

    # Collect rows to later write to CSV
    rows = []
    header = ["filename", "label", "day_mean", "day_min", "day_max", "day_valid_pct"]
    if CHECK_NIGHT:
        header += ["night_mean", "night_min", "night_max", "night_valid_pct"]

    for fname in sample:
        file_path = os.path.join(RAW_DATA_DIR, fname)
        label = ayear_doy_from_filename(fname)
        ds = gdal.Open(file_path)
        subs = ds.GetSubDatasets()

        # Daytime
        lst_day_name = pick_subdataset(subs, ":MODIS_Grid_8Day_1km_LST:LST_Day_1km")
        qc_day_name  = pick_subdataset(subs, ":MODIS_Grid_8Day_1km_LST:QC_Day")
        lst_day_raw = gdal.Open(lst_day_name).ReadAsArray()
        qc_day_raw  = gdal.Open(qc_day_name).ReadAsArray()
        lst_day_c   = apply_qc_and_scale(lst_day_raw, qc_day_raw)
        day_min = float(np.nanmin(lst_day_c)) if np.isfinite(lst_day_c).any() else float("nan")
        day_max = float(np.nanmax(lst_day_c)) if np.isfinite(lst_day_c).any() else float("nan")
        day_mean = float(np.nanmean(lst_day_c)) if np.isfinite(lst_day_c).any() else float("nan")
        day_valid = float(np.isfinite(lst_day_c).mean() * 100)

        night_stats = []
        if CHECK_NIGHT:
            lst_night_name = pick_subdataset(subs, ":MODIS_Grid_8Day_1km_LST:LST_Night_1km")
            qc_night_name  = pick_subdataset(subs, ":MODIS_Grid_8Day_1km_LST:QC_Night")
            lst_night_raw = gdal.Open(lst_night_name).ReadAsArray()
            qc_night_raw  = gdal.Open(qc_night_name).ReadAsArray()
            lst_night_c   = apply_qc_and_scale(lst_night_raw, qc_night_raw)
            nt_min = float(np.nanmin(lst_night_c)) if np.isfinite(lst_night_c).any() else float("nan")
            nt_max = float(np.nanmax(lst_night_c)) if np.isfinite(lst_night_c).any() else float("nan")
            nt_mean = float(np.nanmean(lst_night_c)) if np.isfinite(lst_night_c).any() else float("nan")
            nt_valid = float(np.isfinite(lst_night_c).mean() * 100)
            night_stats = [nt_mean, nt_min, nt_max, nt_valid]

        print(
            f"{label}  day mean={day_mean:.2f}°C "
            f"(min={day_min:.2f}, max={day_max:.2f}, valid={day_valid:.1f}%)"
            + (f" | night mean={night_stats[0]:.2f}°C (min={night_stats[1]:.2f}, max={night_stats[2]:.2f}, valid={night_stats[3]:.1f}%)" if CHECK_NIGHT else "")
        )

        row = [fname, label, day_mean, day_min, day_max, day_valid] + night_stats
        rows.append(row)

    # -----------------------------------------------------------------
    # Write everything we computed into a CSV file for inspection
    # -----------------------------------------------------------------
    out_csv = os.path.join(
        "/Users/abhi/Documents/Uni/Sem 4/5120/YourView/UHI/Data/Processed_Data",
        "modis_inspect_summary.csv"
    )
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    # Open the CSV file for writing
    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)

        # Write the header row with column names
        writer.writerow(header)

        # Write all the collected rows of statistics
        writer.writerows(rows)

    print(f"\n Summary written to: {out_csv}")
    print("Open it in Excel, Numbers, or VS Code to see what the database-ready table might look like.")

if __name__ == "__main__":
    main()