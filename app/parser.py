import re
from typing import List, Dict, Any

price_re = re.compile(r'(\d+\.\d{2}|\d+,\d{2}|\d+)')

def _normalize_number(s: str) -> float:
    s = s.replace(',', '.')
    try:
        return float(re.search(r'\d+(\.\d+)?', s).group())
    except:
        return None

def parse_receipt_text(text: str) -> List[Dict[str, Any]]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    items = []
    for line in lines:
        if re.search(r'\b(total|subtotal|tax|change|cash|visa|mastercard|balance|amount)\b', line.lower(), re.I):
            continue
        parts = line.rsplit(' ', 2)
        candidate_price = None
        if parts:
            m = re.search(r'(\d+[.,]\d{2})\s*$', line)
            if m:
                candidate_price = _normalize_number(m.group(1))
            else:
                token = parts[-1]
                if price_re.match(token):
                    candidate_price = _normalize_number(token)
        if candidate_price:
            desc = line.replace(str(parts[-1]), '').strip()
            items.append({"desc": desc, "price": candidate_price})
    if not items:
        for line in lines:
            m = re.search(r'(.+?)\s+(\d+[.,]\d{2})', line)
            if m:
                items.append({"desc": m.group(1).strip(), "price": _normalize_number(m.group(2))})
    return items