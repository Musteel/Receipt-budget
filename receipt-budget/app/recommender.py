from app.db import get_conn
from collections import defaultdict

def suggest_savings(receipt_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT description, price, category FROM items WHERE receipt_id =?', (receipt_id,))
    rows = c.fetchall()
    conn.close()

    recs = []
    for desc, price, cat in rows:
        s = desc.lower()
        if any(k in s for k in ["subscription", "monthly", "renewal", "membership", "spotify", "netflix"]):
            recs.append({
                "type": "subscription",
                desc: desc,
                "current_monthly": price,
                "suggestion": "Consider if you still need this subscription. You might save money by cancelling unused services."
            })
        if price and price > 50 and cat in ("restaurants", "groceries"):
            recs.append({
                "type": "swap",
                "description": desc,
                "amount": price,
                "suggestion": f"Consider buying store-brand or bulk - estimated saving ~{round(price*0.2,2)}."
            })
    return recs