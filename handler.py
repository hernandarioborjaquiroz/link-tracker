import os, json, time, datetime, boto3

dynamo = boto3.resource('dynamodb')
TABLE = os.environ.get('TABLE_NAME', 'link-tracker-dev-clicks')
TTL_DAYS = int(os.environ.get('TTL_DAYS', '90'))

def _json(body, status=200, extra_headers=None):
    h = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}
    if extra_headers: h.update(extra_headers)
    return {"statusCode": status, "headers": h, "body": json.dumps(body, ensure_ascii=False)}

def track_click(event, _):
    qs = (event or {}).get("queryStringParameters") or {}
    url = (qs.get("url") or "").strip()
    link_id = (qs.get("linkId") or "").strip() or "default"

    now_s = int(time.time()); now_ms = int(time.time()*1000)
    item = {
        "pk": f"LINK#{link_id}",
        "sk": f"TS#{now_ms}",
        "url": url,
        "userAgent": (event.get("headers") or {}).get("user-agent",""),
        "ip": (event.get("requestContext") or {}).get("http",{}).get("sourceIp",""),
        "ttl": now_s + TTL_DAYS*86400,
    }

    print(f"TABLE={TABLE} about to SAVE: {item}")
    dynamo.Table(TABLE).put_item(Item=item)
    print("SAVED OK")

    iso = datetime.datetime.utcfromtimestamp(now_ms/1000).isoformat()+"Z"
    return _json({"ok": True, "linkId": link_id, "url": url, "storedAt": iso})
