def PrevDayChange(df, base, target, period):
    """
    Function to compute the ratio of change from the previous trading day

    Args :
        df : Pandas DataFrame
        base : String indicating the column name from which the SMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the number of days to look back on during percentage calculation

    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """
    if target not in df.columns:
        df[target] = df[base] / df[base].shift(period) - 1
    return df
