# helpers.py – shared helper functions for the dashboard

DEFAULT_LOCATION = [30.2672, -97.7431]  # Austin, Texas

def get_breed_column(dframe):
    """Return the best breed column available in the dataframe."""
    if "breed_outcome" in dframe.columns:
        return "breed_outcome"
    if "breed_intake" in dframe.columns:
        return "breed_intake"
    if "breed" in dframe.columns:
        return "breed"
    return None


def get_outcome_type_column(dframe):
    """Return the outcome_type column name if it exists."""
    if "outcome_type" in dframe.columns:
        return "outcome_type"
    return None

def group_small_slices(df, column, threshold=0.05):
    """
    Groups categories that represent less than 'threshold' proportion
    into an 'Other' category.
    """
    if column not in df.columns:
        return df

    counts = df[column].value_counts(normalize=True)

    small_slices = counts[counts < threshold].index.tolist()
    if not small_slices:
        return df

    df[column] = df[column].apply(lambda x: "Other" if x in small_slices else x)
    return df

def get_age_column(df):
    if "age_in_years" in df.columns:
        return "age_in_years"
    if "age_upon_outcome_in_weeks" in df.columns:
        return "age_upon_outcome_in_weeks"
    return None