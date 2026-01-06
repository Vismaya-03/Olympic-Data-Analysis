import pandas as pd

def preprocess(athlete, regions):
    # Merging the two dataframes based on regions
    merged_df = athlete.merge(regions, on='NOC',how='left')
    # Dropping the duplicate values from the merged dataframe
    merged_df.drop_duplicates(inplace=True)
    # One-Hot encoding of medals
    merged_df = pd.concat([merged_df,pd.get_dummies(merged_df['Medal'])],axis=1)

    return merged_df