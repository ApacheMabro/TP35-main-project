import os
import uuid
from typing import Optional

import boto3
from botocore.config import Config

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from mangum import Mangum

# =========================
# Load environment variables
# (On Lambda, prefer runtime env vars; load_dotenv is harmless locally.)
# =========================


AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
S3_BUCKET = os.getenv("S3_BUCKET")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # Default 10 MB

# Sightengine credentials (put these in env)
SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")     # e.g., '706094766'
SIGHTENGINE_SECRET = os.getenv("SIGHTENGINE_SECRET") # e.g., 'DabU23Ntfj9DNE3yuTjhwHPCAYJr5C6c'

if not S3_BUCKET:
    raise RuntimeError("Missing S3_BUCKET env var")
if not SIGHTENGINE_USER or not SIGHTENGINE_SECRET:
    raise RuntimeError("Missing Sightengine credentials (SIGHTENGINE_USER / SIGHTENGINE_SECRET)")

# =========================
# Initialize AWS S3 client
# =========================
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(s3={"addressing_style": "virtual"})
)

# Optional: pre-flight check to fail fast if bucket is not accessible
try:
    s3.head_bucket(Bucket=S3_BUCKET)
except Exception as e:
    raise RuntimeError(f"Unable to access S3 bucket '{S3_BUCKET}': {e}")

# =========================
# FastAPI app
# =========================
# app = FastAPI(title="Image Uploader to S3 (with Nudity Check)", version="1.1.1")
app = FastAPI(title="Image Uploader to S3 (with Nudity Check)", version="1.1.1", root_path="/default")

# CORS (tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Constants
# =========================
# Allow only JPEG and PNG (server-side verification via magic bytes)
ALLOWED_CONTENT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

# Decision thresholds for nudity-2.1 (conservative defaults)
# If any of these probabilities exceeds the threshold, we reject the image.
NUDITY_THRESHOLDS = {
    "sexual_activity": 0.50,  # explicit sexual acts
    "sexual_display": 0.50,   # explicit display of sexual organs
    "erotica": 0.80,          # erotic but less explicit
    # "suggestive": 0.90,     # optional: add if you want to reject suggestive content too
}

# Sightengine networking tuneables
SIGHTENGINE_CONNECT_TIMEOUT = float(os.getenv("SIGHTENGINE_CONNECT_TIMEOUT", "8"))   # seconds
SIGHTENGINE_READ_TIMEOUT    = float(os.getenv("SIGHTENGINE_READ_TIMEOUT", "45"))    # seconds
SIGHTENGINE_TOTAL_RETRIES   = int(os.getenv("SIGHTENGINE_TOTAL_RETRIES", "3"))
SIGHTENGINE_BACKOFF_FACTOR  = float(os.getenv("SIGHTENGINE_BACKOFF_FACTOR", "0.6"))

def _requests_session_with_retries() -> requests.Session:
    """Create a requests session with sane retries for transient network errors."""
    retry = Retry(
        total=SIGHTENGINE_TOTAL_RETRIES,
        backoff_factor=SIGHTENGINE_BACKOFF_FACTOR,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["POST"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    s = requests.Session()
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

def detect_image_type(data: bytes) -> Optional[str]:
    """
    Detect image type via magic bytes.
    Returns canonical content-type ('image/jpeg' or 'image/png') or None if unsupported.
    """
    if len(data) >= 3 and data[0:3] == b"\xFF\xD8\xFF":
        return "image/jpeg"  # JPEG starts with FF D8 FF
    if len(data) >= 8 and data[0:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"   # PNG starts with 89 50 4E 47 0D 0A 1A 0A
    return None

def check_image_with_sightengine(bytes_data: bytes, filename: str, content_type: str) -> None:
    """
    Call Sightengine 'nudity-2.1'. Raise 400 if disallowed; 502/504 if moderation service fails/timeouts.
    """
    url = "https://api.sightengine.com/1.0/check.json"
    files = {"media": (filename or "upload", bytes_data, content_type or "application/octet-stream")}
    data = {
        "models": "nudity-2.1",
        "api_user": SIGHTENGINE_USER,
        "api_secret": SIGHTENGINE_SECRET,
    }

    session = _requests_session_with_retries()
    try:
        resp = session.post(
            url,
            files=files,
            data=data,
            timeout=(SIGHTENGINE_CONNECT_TIMEOUT, SIGHTENGINE_READ_TIMEOUT),
        )
    except requests.Timeout as e:
        # read/write/overall timeout -> 504 Gateway Timeout to indicate upstream slowness
        raise HTTPException(status_code=504, detail=f"Moderation timeout: {e}")
    except requests.RequestException as e:
        # other network issues
        raise HTTPException(status_code=502, detail=f"Moderation service unavailable: {e}")

    # parse JSON
    try:
        result = resp.json()
    except ValueError:
        raise HTTPException(status_code=502, detail="Moderation service returned invalid JSON")

    if resp.status_code != 200:
        err = (result.get("error", {}) or {}).get("message") if isinstance(result, dict) else None
        raise HTTPException(status_code=502, detail=f"Moderation service error: {err or 'unknown'}")

    nudity = (result or {}).get("nudity", {})
    if not isinstance(nudity, dict) or not nudity:
        raise HTTPException(status_code=400, detail="Upload rejected: content analysis failed")

    for label, threshold in NUDITY_THRESHOLDS.items():
        score = float(nudity.get(label, 0.0))
        if score >= threshold:
            raise HTTPException(status_code=400, detail="Upload rejected: image contains disallowed content")

# =========================
# Healthcheck
# =========================
@app.get("/health")
def health():
    return {"ok": True}

# =========================
# Upload endpoint
# =========================
@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(..., description="multipart/form-data field name = file"),
    folder: Optional[str] = Form(default="YourWindow", description="Optional S3 subfolder, e.g., 'uploads/'")
):
    # 1) Read into memory with size limit
    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File too large (> {MAX_FILE_SIZE} bytes)")

    # 2) Enforce JPEG/PNG only using magic bytes (do not trust client headers)
    detected_ct = detect_image_type(contents)
    if detected_ct not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only JPG and PNG are allowed")

    # 3) Run Sightengine moderation BEFORE uploading to S3
    check_image_with_sightengine(contents, file.filename or "upload", detected_ct)

    # 4) Build safe S3 key (prefix folder if provided)
    ext = ALLOWED_CONTENT_TYPES[detected_ct]
    safe_folder = (folder or "").strip().lstrip("/")
    if safe_folder and not safe_folder.endswith("/"):
        safe_folder += "/"
    key = f"{safe_folder}{uuid.uuid4().hex}{ext}"

    # 5) Upload to S3 (private) after passing moderation
    try:
        put_resp = s3.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=contents,
            ContentType=detected_ct,   # use detected content type
            Metadata={"original-filename": file.filename or ""},
        )
        etag = put_resp.get("ETag", "").replace('"', "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {e}")

    # 6) Generate a presigned URL for temporary access (1 hour)
    presigned_url = None
    try:
        presigned_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": key},
            ExpiresIn=3600  # 1 hour
        )
    except Exception:
        # Ignore if presigning fails; we still return the key/etag
        pass

    return {
        "bucket": S3_BUCKET,
        "key": key,
        "content_type": detected_ct,
        "size": len(contents),
        "etag": etag,
        "presigned_url": presigned_url,
        "moderation": "passed",
    }

# ============ Lambda entry ============
handler = Mangum(app)

