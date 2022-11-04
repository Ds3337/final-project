import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import altair as alt
from streamlit_echarts import st_echarts  
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts

df = pd.read_csv('songs.csv')       
df.isnull().sum()       # Check for missing data
df.drop_duplicates(inplace=True)        # Eliminate duplicate data
# Years other than the 20 years are excluded for comparison.
df.year.unique()
df_years_drop = df[(df['year'] < 2000) | (df['year'] > 2019)].index
df = df.drop(df_years_drop)

# Bar charts of the popularity of different genres over two decades.
df1 = df.loc[df['year'] < 2010].groupby('genre').sum().sort_values(by='popularity', ascending=False).head(10)[['popularity']]
df2 = df.loc[df['year'] > 2009].groupby('genre').sum().sort_values(by='popularity', ascending=False).head(10)[['popularity']]
fig1, ax = plt.subplots(1, 2, figsize=(20,10))
df1.popularity.plot.barh(ax=ax[0], color='lightgreen') 
df2.popularity.plot.barh(ax=ax[1], color='lightgreen') 
ax[0].set_xlabel('Popularity', size=15)
ax[1].set_xlabel('Popularity', size=15)
ax[0].set_ylabel('Genre', size=15)
ax[1].set_ylabel('')
lables1 = df1.index
ax[0].set_yticklabels(lables1, rotation=30)
lables2 = df2.index
ax[1].set_yticklabels(lables2, rotation=30)
ax[0].set_title('Popularity of different genres in 2000-2009', fontsize=20)
ax[1].set_title('Popularity of different genres in 2010-2019', fontsize=20)
for size in ax[0].get_yticklabels():   
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')
for size in ax[0].get_xticklabels():   
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')    
for size in ax[1].get_yticklabels():   
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')
for size in ax[1].get_xticklabels():   
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')  

# The top 10 artists in terms of popularity.
df3 = df.groupby('artist').sum().sort_values('popularity', ascending=False).head(10)
top_10_artists = df3.reset_index(drop=False)

# A bar chart of the popularity of the 10 artists.
fig2 = plt.figure(figsize=(15,5))
plt.bar(top_10_artists['artist'], top_10_artists['popularity'], width=0.4, color='lightgreen')
plt.xlabel("Artists", size=15)
plt.ylabel("Popularity", size=15)
plt.title('The popularity of top 10 Artists', color='black', fontsize=20)

# A scatter plot of the average popularity of the 10 artists.
i = 0
avg_list = []
while i < 10:
    average_popularity = top_10_artists['popularity'][i] / len(df[df.artist == top_10_artists['artist'][i]])
    avg_list.append(average_popularity)
    i += 1
top_10_artists['average_popularity'] = avg_list
df4 = pd.DataFrame({
    'artist': top_10_artists['artist'],
    'average_popularity': top_10_artists['average_popularity']  
})

fig3 = plt.figure(figsize=(15, 5))
plt.xlabel('Artist', size=15)
plt.ylabel('Average popularity', size=15)
plt.title('The average popularity of top 10 artists', fontsize=20) 
plt.scatter(x=top_10_artists['artist'], y=top_10_artists['average_popularity'], color='turquoise', s=100)

# The distribution of dancability and energy.
fig4, ax = plt.subplots(1, 2, figsize=(15,5))
df.danceability.plot.hist(ax=ax[0], bins=30, color='lightgreen') 
df.energy.plot.hist(ax=ax[1], bins=30, color='lightgreen') 
ax[0].set_xlabel('Danceability')
ax[1].set_xlabel('Energy')
ax[0].set_title('The distribution of danceability', fontsize=20)
ax[1].set_title('The distribution of energy', fontsize=20)

# A line chart showing the average duration of the songs in the two decades.
def second_to_hms(s):
    """change s to hms"""
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    hms = '%02d:%02d:%02d' % (hours, minutes, seconds)
    return hms
def get_avarage_duration(df):
    years = {}
    for i in range(0, len(df)):
        if df.iloc[i]['year'] in years:
            years[df.iloc[i]['year']].append(df.iloc[i]['duration_ms'])
        else:
            years[df.iloc[i]['year']] = [df.iloc[i]['duration_ms']]
   
    years2 = {}
    for i in years:
        if years[i]:
            years2[i] = int(sum(years[i]) / len(years[i]))
        else:
            years2[i] = 0

    res = []
    for i in years2:
        res.append({
            "year": int(i),
            "duration_ms": second_to_hms(int(years2[i]) // 1000)
        })
    return pd.DataFrame(res)

df5 = get_avarage_duration(df.loc[lambda x: (2000 < x['year']) & (x['year'] < 2020)])

fig5 = (
    alt.Chart(df5, title=f'The average duration of songs each year')
    .mark_line(point=alt.OverlayMarkDef(color='turquoise', size=80), color='lightgreen')
    .encode(
        x=alt.X('year', 
        title='Year', 
        axis=alt.Axis(tickMinStep=1), 
        scale=alt.Scale(domain=[2000, 2020]), 
        sort=alt.EncodingSortField(field='year', order='ascending')),
        y=alt.Y('duration_ms', 
        title='Average duration', 
        scale=alt.Scale(zero=False), 
        axis=alt.Axis(formatType='timeUnit', format='hh:mm:ss'),
        sort=alt.EncodingSortField(field='duration_ms', order='descending')),
        order='year',
        tooltip=[
            alt.Tooltip(field="year", type="nominal", title="Year"),
            alt.Tooltip(field="duration_ms", type="nominal", title="Average duration"),
        ],
    )
)

# Interaction1: Users can choose the page they want to study by radio.
st.sidebar.header('Catalog')
page_filter = st.sidebar.radio(
    'Choose the page',
    ('Homepage',
    'Dataset description',
    'What are the changes in the popularity of different genres?', 
    'Something about danceability and energy', 
    'Average duration of songs is changing', 
    'The top 10 artists with popularity',
    'Generate a random playlist')
)
if page_filter == 'Homepage':
    st.title('Homepage')
    st.markdown('## ***Production life has changed dramatically from 2000 to 2019. As an important force over the cultural field, how have people\'s preferences for music changed in these two decades?***')
    st.image('homepage.png')
elif page_filter == 'Dataset description':
    st.title('Dataset description')
    st.markdown('## ***Origin: Top Hits Spotify from 2000-2019(Kaggle)***')
    st.markdown('### [Top Hits Spotify from 2000-2019 | Kaggle](https://www.kaggle.com/datasets/paradisejoy/top-hits-spotify-from-20002019)')
    st.markdown('#### This dataset contains audio statistics of the nearly top 2000 songs on Spotify from 2000-2019. The data contains about 18 columns each describing the song and it\'s qualities.')
    st.write(df)
elif page_filter == 'What are the changes in the popularity of different genres?':
    st.title('What are the changes in the popularity of different genres?')
    st.pyplot(fig=fig1)
    st.markdown('#### It can be seen from the chart that pop music has the highest number of hits in both decades, while the ranking of popularity of the rest are constantly changing.')
    st.markdown('#### Since there are multiple style elements in one genre, we believe that the changes in the popularitiy of the genres are caused by changes in people\'s preferences for style elements. ')   
    st.markdown('#### For example: R&B——Dance/Electronic')    
elif page_filter == 'Something about danceability and energy':
    st.title('The importance of danceability and energy to songs clicks')
    st.pyplot(fig=fig4)
    st.markdown('#### The danceability and energy of these songs are concentrated on high values.')
    st.markdown('#### It may due to the emergence of various boy bands and girl groups now, people prefer songs that can be used as dance music.')
elif page_filter == 'Average duration of songs is changing':
    st.title('The change of average duration of songs each year')
    st.altair_chart(fig5, use_container_width=True)
    st.markdown('#### There is a shortening trend in song duration over these two decades.')
    st.markdown('#### It may because of :')
    st.markdown('#### - The era of fragmentation')
    st.markdown('#### - Rise of various short video apps')
    st.markdown('#### - Listeners\' preference to listen to music at double speed')
    st.markdown('#### - ……')
    
elif page_filter == 'The top 10 artists with popularity':
    st.title('The top 10 artists from 2000-2019')
    st.markdown('## ***Total popularity VS Average popularity***')
    st.pyplot(fig=fig2)
    st.pyplot(fig=fig3)
    st.markdown('#### There is no completely positive correlation between the average popularity and the total popularity of the aritists. This may be because total popularity is related to the number of songs an artist has.')
    st.markdown('#### For a artist like Taylor Swift, even though she doesn\'t have higher total popularity, the average popularity of her songs is pretty high, which means each of her songs is a hit.')
# Interation2: Users can choose one of the top 10 artists by radio.
    top_10_artists_list = []
    for i in top_10_artists['artist']:
        top_10_artists_list.append(i)
    st.markdown('## ***Do you want to know about the songs of the artists? Choose one of the 10 artists you are interested in!***')
    artist_filter = st.radio(
        'Choose one artist',
        ('Rihanna', 
        'Eminem', 
        'Drake', 
        'Calvin Harris', 
        'David Guetta', 
        'Britney Spears', 
        'Taylor Swift', 
        'Katy Perry', 
        'Beyoncé', 
        'Chris Brown')
    )

# Interaction3: Users can choose to know the songs whose popularity are above the number they choose by a slider.
    st.markdown('### You can set the popularity value of the songs')
    songs_filter = st.slider(
    'Choose the bottom line of the popularity value of the songs you want to know', 0, 60, 89
    )

    i = 0
    while i < 10:
        if artist_filter == top_10_artists_list[i]:
            songslist = df.loc[(df.artist == top_10_artists_list[i])][['song','popularity']]
        i += 1

    df6 = songslist[songslist.popularity >= songs_filter]['song']
    st.markdown('### Here are the songs whose popularity value are higher than the value you chose:')
    st.write(df6)
    
elif page_filter == 'Generate a random playlist':
    st.title('Generate a random playlist')

# Interaction4：For the five most popular genres, users can choose one of them, then we will generate a playlist of 10 songs for them.
    st.markdown('## ***The top 5 genres of the songs***')
    df7 = df.groupby('genre').sum().sort_values('popularity', ascending=False).head(5)
    top_5_genres = df7.reset_index(drop=False)
    
    fig5 = plt.figure(figsize=(15,5))
    plt.bar(top_5_genres['genre'], top_5_genres['popularity'], width=0.4, color='lightgreen')
    plt.xlabel('Genre', size=15)
    plt.ylabel('Popularity', size=15)
    plt.title('The popularity of top 5 genres', color='black', fontsize=20)
    st.pyplot(fig=fig5)

    st.markdown('## ***Do you want to own your exclusive playlist?***')
    genre_filter = st.selectbox( 
        'Choose the genre type you are most interested in:', 
        top_5_genres.genre.unique() 
    )

    top_5_genres_list = []
    for i in top_5_genres['genre']:
        top_5_genres_list.append(i)

    songslist2 = []
    i = 0
    while i < 5:
        if genre_filter == top_5_genres_list[i]:
            for p in df.loc[(df.genre == top_5_genres_list[i])]['song']:
                songslist2.append(p)
        i += 1
    random_recommendation = random.sample(songslist2, 10)
     
    df8 = pd.DataFrame({
        'recommendation_songs': random_recommendation   
    })
    df8.index = np.arange(1, len(df8)+1)
    st.markdown('### Here are the 10 songs we recommend for you:')
    st.write(df8)
    