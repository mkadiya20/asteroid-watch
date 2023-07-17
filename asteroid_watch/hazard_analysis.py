def hazard_analysis(df):
    """Get the total number of hazardous asteroids and non-hazardous asteroids in the given dataframe."""

    # Get the number of hazardous asteroids
    hazardous = int(df[df['is_potentially_hazardous_asteroid'] == True].shape[0])

    # Get the number of non-hazardous asteroids
    non_hazardous = int(df[df['is_potentially_hazardous_asteroid'] == False].shape[0])

    return {
        'hazardous': hazardous,
        'non_hazardous': non_hazardous,
        'ratio': round(hazardous / non_hazardous, 2)
    }