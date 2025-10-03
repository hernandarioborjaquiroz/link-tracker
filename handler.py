import os, json, time, uuid, hashlib
from datetime import datetime, timezone
import boto3

# --- Configuración DynamoDB ---
TABLE_NAME = os.environ.get("TABLE_NAME", "")
TTL_DAYS = int(os.environ.get("TTL_DAYS", "90"))

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# ---------- Utilidades ----------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _client_ip(headers: dict) -> str:
    h = headers or {}
    xff = h.get("x-forwarded-for") or h.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return h.get("x-real-ip") or h.get("X-Real-Ip") or "0.0.0.0"

def _link_id_from(url: str) -> str:
    if not url:
        return str(uuid.uuid4())
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:10]

def _json(body: dict, status: int = 200):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Cache-Control": "no-store",
            "Access-Control-Allow-Origin": "*",  # en prod: cámbialo por tu dominio
        },
        "body": json.dumps(body, ensure_ascii=False),
    }

# ---------- Handler ----------
def track_click(event, context):
    qs = (event or {}).get("queryStringParameters") or {}
    url = (qs.get("url") or "").strip()
    link_id = (qs.get("linkId") or "").strip() or _link_id_from(url)

    if not url and not link_id:
        return _json({"ok": False, "error": "Falta 'url' o 'linkId'."}, 400)

    headers = (event or {}).get("headers") or {}
    ip = _client_ip(headers)
    ua = headers.get("user-agent") or headers.get("User-Agent") or ""
    ref = headers.get("referer") or headers.get("Referer") or ""

    now_iso = _now_iso()
    ttl_unix = int(time.time()) + TTL_DAYS * 24 * 3600

    item = {
        "pk": f"LINK#{link_id}",   
        "sk": now_iso,             
        "url": url,
        "ip": ip,
        "userAgent": ua[:1024],
        "referrer": ref[:1024],
        "receivedAt": now_iso,
        "ttl": ttl_unix,           
    }

    table.put_item(Item=item)

    return _json({
        "ok": True,
        "linkId": link_id,
        "url": url,
        "storedAt": now_iso
    })
