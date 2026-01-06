import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Loading the athlete_events dataset into the environment
athlete = pd.read_csv("athlete_events.csv")

# Loading the noc_regions dataset into the environment
regions = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(athlete, regions)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio('Select an Option',
                 ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete Analysis'))


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    year, country, season = helper.country_year_season_list(df)
    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)
    selected_season = st.sidebar.selectbox("Select Season", season)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country,selected_season)
    if selected_year == "Overall" and selected_country == "Overall" and selected_season == "Overall":
        st.title("Overall Medal Tally")
    elif selected_year == "Overall" and selected_country != "Overall" and selected_season != "Overall":
        st.title(f"{selected_country} Medal Tally ({selected_season} Olympics – All Years)")

    elif selected_year != "Overall" and selected_country == "Overall" and selected_season == "Overall":
        st.title(f"Medal Tally – {selected_year} Olympics")

    elif selected_year == "Overall" and selected_country != "Overall" and selected_season == "Overall":
        st.title(f"{selected_country} Overall Olympic Medal Tally")

    elif selected_year == "Overall" and selected_country == "Overall" and selected_season != "Overall":
        st.title(f"{selected_season} Olympics Medal Tally (All Years)")

    elif selected_year != "Overall" and selected_country != "Overall" and selected_season == "Overall":
        st.title(f"{selected_country} Medal Tally – {selected_year} Olympics")

    elif selected_year != "Overall" and selected_country == "Overall" and selected_season != "Overall":
        st.title(f"Medal Tally – {selected_year} {selected_season} Olympics")

    else:
        st.title(f"{selected_country} Medal Tally – {selected_year} {selected_season} Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]
    cities =  df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nation = df['region'].unique().shape[0]

    
    st.markdown("## Top Olympic Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Editions", value=editions)

    with col2:
        st.metric(label="Host Cities", value=cities)

    with col3:
        st.metric(label="Sports", value=sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Events", value=events)

    with col2:
        st.metric(label="Nations", value=nation)

    with col3:
        st.metric(label="Athletes", value=athletes)


    nations = helper.data_over_time(df, "region")
    fig = px.line(nations,x="Edition",y="region",markers=True)
    st.markdown("## Participation over the Years")
    st.plotly_chart(fig, use_container_width=True)

    events = helper.data_over_time(df, "Event")
    fig = px.line(events,x="Edition",y="Event",markers=True)
    st.markdown("## Events over the Years")
    st.plotly_chart(fig, use_container_width=True)

    athletes = helper.data_over_time(df, "Name")
    fig = px.line(athletes,x="Edition",y="Name", markers=True)
    st.markdown("## Athletes over the Years")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## No.of Events over the Years")
    fig, ax = plt.subplots(figsize=(20,20))
    x =df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year', values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select a sport", sport_list)

    # Dynamic title
    if selected_sport == "Overall":
        st.markdown("## Most Successful Athletes (Overall)")
    else:
        st.markdown(f"## Most Successful Athletes in {selected_sport}")

    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.markdown("## Country-wise Analysis ")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_nation = st.sidebar.selectbox("Select a Country", country_list)
    country_df = helper.year_medal_tally(df,selected_nation)
    fig = px.line(country_df,x="Year",y="Medal",markers=True)
    st.subheader(f"{selected_nation} – Medal Tally over the Years")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"{selected_nation} – Success in each Sport")
    pivot = helper.country_event_heatmap(df, selected_nation)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pivot, annot=True)
    st.pyplot(fig)

    st.subheader(f"{selected_nation} – Top 10 Decorated Athletes")
    top10 = helper.most_successful_region(df,selected_nation)
    st.table(top10)

if user_menu == 'Athlete Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 =athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 =athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 =athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.markdown("## Age Distribution of the Medalist ")
    st.plotly_chart(fig, use_container_width=True)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']== sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    st.markdown("## Age Distribution of Gold Medalist for each Sport ")
    st.plotly_chart(fig, use_container_width=True)

    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    st.markdown("## Height vs Weight ")
    selected_sport = st.selectbox("Select a sport", sport_list)
    temp_df = helper.weight_height(df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(
    x='Weight',
    y='Height',
    data=temp_df,
    hue=temp_df['Medal'],
    style=temp_df['Sex']
)
    st.pyplot(fig)

    st.markdown("## Men vs Women Participation")
    final = helper.men_women(df)
    fig = px.line(final, x="Year", y=["Men","Women"])
    st.plotly_chart(fig)



