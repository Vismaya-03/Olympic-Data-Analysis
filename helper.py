import numpy as np

def fetch_medal_tally(merged_df, year, country, season):

    medal_df = merged_df.drop_duplicates(
        subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]
    )

    # Normalize year
    if year != 'Overall':
        year = int(year)

    # -------------------------------
    # APPLY FILTERS
    # -------------------------------
    temp_df = medal_df.copy()

    if year != 'Overall':
        temp_df = temp_df[temp_df['Year'] == year]

    if season != 'Overall':
        temp_df = temp_df[temp_df['Season'] == season]

    # -------------------------------
    # CASE 1: COUNTRY NOT SELECTED → RANKING
    # -------------------------------
    if country == 'Overall':

        result = (
            temp_df
            .groupby('region')[['Gold','Silver','Bronze']]
            .sum()
            .sort_values(['Gold','Silver','Bronze'], ascending=False)
            .reset_index()
        )

        result['total'] = result['Gold'] + result['Silver'] + result['Bronze']
        result['rank'] = range(1, len(result) + 1)

        return result

    # -------------------------------
    # CASE 2: COUNTRY SELECTED → YEAR-WISE TREND
    # -------------------------------
    else:
        temp_df = temp_df[temp_df['region'] == country]

        result = (
            temp_df
            .groupby('Year')[['Gold','Silver','Bronze']]
            .sum()
            .sort_index()
            .reset_index()
        )

        result['total'] = result['Gold'] + result['Silver'] + result['Bronze']
        return result


def medal_tally(merged_df):
    medal_tally = merged_df.drop_duplicates(subset=["Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
    medal_tally=medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
    medal_tally["total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]

    return medal_tally

def country_year_season_list(merged_df):
    # Extracting the unique years from the dataframe
    year = merged_df['Year'].unique().tolist()
    year.sort()
    year.insert(0,"Overall")
 
    # Extracting the unique regions from the dataframe
    country = np.unique(merged_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,"Overall")

    # Extracting the unique season from the dataframe
    season = np.unique(merged_df['Season'].dropna().values).tolist()
    season.sort()
    season.insert(0,"Overall")

    return year, country, season

def data_over_time(merged_df, col_name):

    df = merged_df.drop_duplicates(["Year", col_name])

    result = (df.groupby("Year")[col_name].nunique().reset_index().rename(columns={"Year": "Edition", col_name: col_name}))
    return result


def most_successful(merged_df, sport):

    temp_df = merged_df.dropna(subset=['Medal'])

    if sport != "Overall":
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete
    top_athletes = (
        temp_df['Name']
        .value_counts()
        .reset_index(name='Medals')
        .rename(columns={'index': 'Name'})
        .head(15)
    )

    # Merge country and sport info
    top_athletes = top_athletes.merge(
        merged_df[['Name', 'region', 'Sport']],
        on='Name',
        how='left'
    )

    # Keep dominant sport per athlete
    top_athletes = (
        top_athletes
        .groupby(['Name', 'region', 'Medals'])['Sport']
        .agg(lambda x: x.value_counts().idxmax())
        .reset_index()
    )

    # SORT IN DESCENDING ORDER
    top_athletes = top_athletes.sort_values(
        by='Medals',
        ascending=False
    ).reset_index(drop=True)

    return top_athletes

def year_medal_tally(merged_df, country):
    temp_df = merged_df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df["region"]== country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()

    return final_df

def country_event_heatmap(merged_df, country):
    temp_df = merged_df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df["region"]== country]
    pivot = new_df.pivot_table(index='Sport', columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pivot

def most_successful_region(merged_df, country):

    temp_df = merged_df.dropna(subset=['Medal'])

   
    temp_df = temp_df[temp_df['region'] == country]

    # Count medals per athlete
    top_athletes = (
        temp_df['Name']
        .value_counts()
        .reset_index(name='Medals')
        .rename(columns={'index': 'Name'})
        .head(10)
    )

    # Merge country and sport info
    top_athletes = top_athletes.merge(
        merged_df[['Name', 'region', 'Sport']],
        on='Name',
        how='left'
    )

    # Keep dominant sport per athlete
    top_athletes = (
        top_athletes
        .groupby(['Name', 'Medals'])['Sport']
        .agg(lambda x: x.value_counts().idxmax())
        .reset_index()
    )

    # SORT IN DESCENDING ORDER
    top_athletes = top_athletes.sort_values(
        by='Medals',
        ascending=False
    ).reset_index(drop=True)

    return top_athletes

def weight_height(merged_df, sport):
    athlete_df = merged_df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport']== sport]
        return temp_df
    else:
        return athlete_df
    
def men_women(merged_df):
    athlete_df = merged_df.drop_duplicates(subset=['Name','region'])
    # Men vs Women participation
    men = athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex']=='F'].groupby('Year').count().reset_index()
    final = men.merge(women, on='Year')
    final.rename(columns={"Name_x": "Men","Name_y": "Women"},inplace=True)
    return final


    



