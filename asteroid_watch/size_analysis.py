def size_analysis(df):
    """Get the largest, smallest, and average size of asteroids in the given dataframe."""
    # date,absolute_magnitude_h,id,neo_reference_id,nasa_jpl_url,is_potentially_hazardous_asteroid,is_sentry_object,name,links.self,estimated_diameter.feet.estimated_diameter_min,estimated_diameter.feet.estimated_diameter_max,estimated_diameter.kilometers.estimated_diameter_min,estimated_diameter.kilometers.estimated_diameter_max,estimated_diameter.meters.estimated_diameter_min,estimated_diameter.meters.estimated_diameter_max,estimated_diameter.miles.estimated_diameter_min,estimated_diameter.miles.estimated_diameter_max

    # Get the largest asteroid by name and size
    largest = df.loc[df['estimated_diameter.meters.estimated_diameter_max'].idxmax()]

    # Get the smallest asteroid by name and size
    smallest = df.loc[df['estimated_diameter.meters.estimated_diameter_max'].idxmin()]

    # Get the average size of asteroids
    average = df['estimated_diameter.meters.estimated_diameter_max'].mean()

    return {
        'unit': 'meters',
        'largest': {
            'name': largest['name'],
            'size': round(largest['estimated_diameter.meters.estimated_diameter_max'])
        },
        'smallest': {
            'name': smallest['name'],
            'size': round(smallest['estimated_diameter.meters.estimated_diameter_max'])
        },
        'average': round(average)
    }