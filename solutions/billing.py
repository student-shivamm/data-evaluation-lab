"""Aggregate successful logical operations after collapsing delivery retries."""
def net_cents(events):
    # The caller may pass a generator. Materialize once; do not mutate rows.
    chosen = {}
    for event in events:
        if event['status'] != 'succeeded':
            continue
        key = (event['account'], event['operation'])
        previous = chosen.get(key)
        if previous is None or (event['received_at'], event['delivery_id']) < (
                previous['received_at'], previous['delivery_id']):
            chosen[key] = event
    totals = {}
    for event in chosen.values():
        sign = 1 if event['kind'] == 'charge' else -1
        account = event['account']
        totals[account] = totals.get(account, 0) + sign * event['amount_cents']
    return totals
