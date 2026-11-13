"""Find a Tokyo cash equity or request its daily candles."""
import json
import os
import re
import sys
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "catalog"
    code = (sys.argv[2] if len(sys.argv) > 2 else "7203").strip().upper().removeprefix("TSE:")
    if not re.fullmatch(r"[0-9](?:[0-9]{3}|[0-9]{2}[ACDFGHJKLMNPRSTUWXY]|[ACDFGHJKLMNPRSTUWXY][0-9]{2})", code):
        raise SystemExit("Supply a four-character Tokyo Stock Exchange code, e.g. 7203.")
    symbol = "TSE:" + code
    if mode == "catalog":
        request = Request("https://www.zafeed.com/api/v1/public/symbols", headers={"User-Agent": "ZaFeed-Tokyo-Example/1.0"})
        with urlopen(request, timeout=15) as response:
            rows = json.load(response)["data"]
        result = [row for row in rows if row["m"].upper() == "JP" and row["api"] == symbol]
    elif mode == "candles":
        base = urlsplit(os.environ.get("ZAFEED_HTTP_BASE_URL", ""))
        key = os.environ.get("ZAFEED_API_KEY")
        if base.scheme != "https" or not base.hostname or base.username is not None or not key:
            raise SystemExit("Set the assigned HTTPS origin and Japan market Key.")
        query = urlencode(dict(market="JP", symbol=symbol, interval="1d", limit=10))
        request = Request(f"https://{base.netloc}/v1/klines?{query}", headers={"X-API-Key": key})
        with build_opener(RejectRedirects()).open(request, timeout=15) as response:
            result = json.load(response)
    else:
        raise SystemExit("Choose catalog or candles.")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
