#!/usr/bin/env bash
set -euo pipefail

echo "===== GIT / REPO ====="
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "${ROOT}" ]; then
  echo "Not inside a git repo."
  exit 1
fi
echo "Repo root: ${ROOT}"
echo "Current dir: $(pwd)"
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "Remotes:"
git remote -v | sed 's/^/  /'
echo "Recent commits:"
git --no-pager log --oneline -n 5 | sed 's/^/  /'

echo
echo "===== TOP-LEVEL CONTENTS ====="
ls -la "${ROOT}"

echo
echo "===== .gitignore (first 80 lines if present) ====="
if [ -f "${ROOT}/.gitignore" ]; then
  nl -ba "${ROOT}/.gitignore" | head -n 80
else
  echo "No .gitignore at repo root"
fi

echo
echo "===== UHI structure (depth 3) ====="
if [ -d "${ROOT}/UHI" ]; then
  if command -v tree >/dev/null 2>&1; then
    tree -L 3 "${ROOT}/UHI"
  else
    echo "(tip: brew install tree)"
    find "${ROOT}/UHI" -maxdepth 3 -print
  fi
else
  echo "UHI folder not found"
fi

echo
echo "===== Look for HDF files under repo (first 5) ====="
HDF_COUNT=$(find "${ROOT}" -type f -name "*.hdf" | wc -l | tr -d ' ')
echo "Total .hdf files: ${HDF_COUNT}"
find "${ROOT}" -type f -name "*.hdf" | sort | head -n 5

FIRST_HDF=$(find "${ROOT}" -type f -name "*.hdf" | sort | head -n 1 || true)
if [ -n "${FIRST_HDF}" ]; then
  echo
  echo "===== gdalinfo on first HDF (subdatasets header only) ====="
  if command -v gdalinfo >/dev/null 2>&1; then
    gdalinfo "${FIRST_HDF}" | sed -n '1,120p'
  else
    echo "gdalinfo not found in PATH"
  fi
fi

echo
echo "===== GDAL / Python environment ====="
if command -v gdalinfo >/dev/null 2>&1; then
  gdalinfo --version
else
  echo "gdalinfo not found"
fi

if command -v conda >/dev/null 2>&1; then
  echo "Conda envs:"
  conda info --envs
fi

if command -v python >/dev/null 2>&1; then
  python - <<'PY'
try:
    from osgeo import gdal
    print("Python GDAL version:", gdal.VersionInfo())
except Exception as e:
    print("Python GDAL import failed:", e)
PY
else
  echo "python not found in PATH"
fi

echo
echo "===== Guess your MODIS RAW and PROCESSED folders ====="
guess_raw=$(find "${ROOT}" -type d -iname "*MOD11A2*" | head -n 1 || true)
guess_proc="${ROOT}/UHI/Data/Processed_Data/MODIS"
echo "RAW guess:       ${guess_raw:-not found}"
echo "PROCESSED guess: ${guess_proc}"
echo
echo "Done."
