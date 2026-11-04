"""Wrong: counts overloaded ticks rather than elapsed time between events."""
def overloaded_minutes(reservations, window_start, window_end, capacity):
    total = 0
    for minute in range(window_start, window_end):
        load = sum(row['units'] for row in reservations
                   if row['start'] <= minute <= row['end'])
        if load > capacity:
            total += 1
    return total
