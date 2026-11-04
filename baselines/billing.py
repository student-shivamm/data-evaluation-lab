"""Wrong: a pending delivery reserves the key and hides later success."""
def net_cents(events):
    seen = set()
    totals = {}
    for event in sorted(events, key=lambda row: (row['received_at'], row['delivery_id'])):
        key = (event['account'], event['operation'])
        if key in seen:
            continue
        seen.add(key)
        if event['status'] != 'succeeded':
            continue
        sign = 1 if event['kind'] == 'charge' else -1
        account = event['account']
        totals[account] = totals.get(account, 0) + sign * event['amount_cents']
    return totals
