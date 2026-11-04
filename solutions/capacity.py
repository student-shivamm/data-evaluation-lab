"""Measure time above capacity over clipped, half-open reservations."""
def overloaded_minutes(reservations, window_start, window_end, capacity):
    changes = {}
    for row in reservations:
        start = max(row['start'], window_start)
        end = min(row['end'], window_end)
        if start >= end:
            continue
        changes[start] = changes.get(start, 0) + row['units']
        changes[end] = changes.get(end, 0) - row['units']
    load = total = 0
    previous = window_start
    for at, delta in sorted(changes.items()):
        if load > capacity:
            total += at - previous
        load += delta
        previous = at
    return total
