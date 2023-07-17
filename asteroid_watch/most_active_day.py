def most_active_day(df):
    """Get the day with the most asteroids in the given dataframe."""

    # Get the day with the most asteroids and the number of asteroids
    most_active_day = df['date'].value_counts().idxmax()

    # Get the number of asteroids on the most active day
    most_active_day_count = int(df['date'].value_counts().max())

    return {
        'date': most_active_day.strftime('%Y-%m-%d'),
        'count': most_active_day_count
    }