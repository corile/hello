"""Fetch offers JSON from offer.love and extract offers for specific merchants.

This script provides:
- fetch_offers_json(url, timeout=10, retries=3): fetches JSON with simple retry logic
- get_offers_for_merchants(merchants, url=...): returns a dict mapping merchant -> offers list

Usage (CLI):
    python offer_fetcher.py --merchants hilton,parkhyatt

The script prefers the 'requests' library but falls back to urllib if requests isn't available.
"""
from __future__ import annotations

import json
import logging
import sys
import time
from typing import Dict, Iterable, List, Any

DEFAULT_URL = "https://api.offer.love/offers/get?key=offer-love-web"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Try to import requests; fall back to urllib
try:
    import requests  # type: ignore
    HAS_REQUESTS = True
except Exception:  # pragma: no cover - fallback
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error


def fetch_offers_json(url: str = DEFAULT_URL, timeout: int = 10, retries: int = 3, backoff: float = 1.0) -> dict:
    """Fetch the JSON from the offers endpoint with simple retry/backoff logic.

    Returns parsed JSON (dict). Raises an exception if all retries fail.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            logger.debug(f"Fetching offers JSON from {url} (attempt {attempt})")
            if HAS_REQUESTS:
                resp = requests.get(url, timeout=timeout)
                resp.raise_for_status()
                return resp.json()
            else:
                with urllib.request.urlopen(url, timeout=timeout) as fh:
                    data = fh.read()
                    return json.loads(data.decode("utf-8"))
        except Exception as exc:  # keep broad to catch network/JSON errors
            last_exc = exc
            logger.warning(f"Attempt {attempt} failed: {exc}")
            if attempt < retries:
                sleep_for = backoff * (2 ** (attempt - 1))
                logger.info(f"Retrying after {sleep_for:.1f}s...")
                time.sleep(sleep_for)
            else:
                logger.error("All retries exhausted while fetching offers JSON")
    raise last_exc  # type: ignore


def get_offers_for_merchants(merchants: Iterable[str], url: str = DEFAULT_URL) -> Dict[str, List[Any]]:
    """Return a mapping merchant (as provided) -> list of offers (possibly empty).

    Matching is done case-insensitively against keys inside JSON['offersData'].
    """
    merchants_list = [m.strip() for m in merchants if m and m.strip()]
    if not merchants_list:
        return {}

    data = fetch_offers_json(url)

    # Navigate to offersData key
    offers_data = data.get("offersData") if isinstance(data, dict) else None
    if offers_data is None:
        logger.error("offersData key not found in JSON response")
        return {m: [] for m in merchants_list}

    # Build case-insensitive lookup for keys in offers_data
    key_map = {k.lower(): k for k in offers_data.keys()} if isinstance(offers_data, dict) else {}

    result: Dict[str, List[Any]] = {}
    for merchant in merchants_list:
        lookup = merchant.lower()
        if lookup in key_map:
            real_key = key_map[lookup]
            result[merchant] = offers_data.get(real_key) or []
        else:
            # Try partial matches: some merchants might be prefixed/suffixed
            matches = [offers_data.get(k) for k in offers_data.keys() if lookup in k.lower()]
            # flatten and filter None
            flattened: List[Any] = []
            for m in matches:
                if isinstance(m, list):
                    flattened.extend(m)
                elif m is not None:
                    flattened.append(m)
            result[merchant] = flattened
    return result


def main(argv: List[str] | None = None) -> int:
    import argparse

    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="Fetch offer.love JSON and extract offers for given merchants")
    parser.add_argument("--merchants", "-m", required=True,
                        help="Comma-separated list of merchants (e.g. hilton,parkhyatt)")
    parser.add_argument("--url", "-u", default=DEFAULT_URL, help="Offers API URL")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout seconds")
    parser.add_argument("--retries", type=int, default=3, help="Number of fetch retries")
    args = parser.parse_args(argv)

    merchants = [m.strip() for m in args.merchants.split(",") if m.strip()]

    try:
        # fetch with the user-specified timeout/retries
        data = fetch_offers_json(url=args.url, timeout=args.timeout, retries=args.retries)
    except Exception as exc:
        logger.error(f"Failed to fetch offers JSON: {exc}")
        return 2

    # If user requested, extract only the merchants
    offers_map = get_offers_for_merchants(merchants, url=args.url)

    print(json.dumps(offers_map, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
