"""Point-in-time features with separate event and availability clocks."""
def features_at(observations, queries):
    observations = list(observations)
    result = []
    for query in queries:
        eligible = [row for row in observations
                    if row['entity'] == query['entity']
                    and row['event_at'] <= query['at']
                    and row['available_at'] <= query['at']]
        latest = max(eligible,
                     key=lambda row: (row['event_at'], row['available_at'], row['revision']),
                     default=None)
        result.append(None if latest is None else latest['value'])
    return result
