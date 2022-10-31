from turtle import color
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

#处理读取数据
df = pd.read_csv('songs.csv')

df.isnull().sum()
df.drop_duplicates(inplace=True)
df.year.unique()
df_years_drop = df[(df['year'] <2000) | (df['year'] > 2019)].index
df = df.drop(df_years_drop)

#两个十年
df8 = df.loc[df['year'] < 2010].groupby('genre').sum().sort_values(by='popularity', ascending=False).head(10).reset_index(drop=False)[['genre', 'popularity']].groupby('genre').sum().sort_values(by='popularity', ascending=False)
df9 = df.loc[df['year'] > 2009].groupby('genre').sum().sort_values(by='popularity', ascending=False).head(10).reset_index(drop=False)[['genre', 'popularity']].groupby('genre').sum().sort_values(by='popularity', ascending=False)
fig1, ax = plt.subplots(1, 2, figsize=(20,10))
df8.popularity.plot.barh(ax=ax[0], color='lightgreen') 
df9.popularity.plot.barh(ax=ax[1], color='lightgreen') 
ax[0].set_xlabel('Popularity')
ax[1].set_xlabel('Popularity')
lables1 = df8.index
ax[0].set_yticklabels(lables1, rotation=30)
lables2 = df9.index
ax[1].set_yticklabels(lables2, rotation=30)
for size in ax[0].get_yticklabels():   #获取x轴上所有坐标，并设置字号
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')
for size in ax[0].get_xticklabels():   #获取x轴上所有坐标，并设置字号
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')    
for size in ax[1].get_yticklabels():   #获取x轴上所有坐标，并设置字号
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')
for size in ax[1].get_xticklabels():   #获取x轴上所有坐标，并设置字号
    size.set_fontname('Times New Roman')   
    size.set_fontsize('20')  

#popularity top10的歌手
df1 = df.groupby('artist').sum().sort_values('popularity', ascending=False).head(10)
top_10_artists = df1.reset_index(drop=False)

#The popularity of top 10 Artists柱状图
fig3 = plt.figure(figsize = (15, 5))
plt.bar(top_10_artists['artist'], top_10_artists['popularity'], width = 0.4, color='lightgreen')
plt.xlabel("Artists", size=15)
plt.ylabel("Popularity", size=15)
plt.title('The popularity of top 10 Artists', color='black', fontsize=20)


#可舞性和力量
fig2, ax = plt.subplots(1, 2, figsize=(15,5))
df.danceability.plot.hist(ax=ax[0], bins=30, color='lightgreen') 
df.energy.plot.hist(ax=ax[1], bins=30, color='lightgreen') 
ax[0].set_xlabel('Danceability')
ax[1].set_xlabel('Energy')


#歌曲的平均播放时长：折线图

def second_to_hms(s):
    """change s to hms"""
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    hms = "%02d:%02d:%02d" % (hours, minutes, seconds)
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


df6 = get_avarage_duration(df.loc[lambda x: (2000 < x['year']) & (x['year'] < 2020)])

chart = (
    alt.Chart(df6, title=f"The average duration of each year")
    .mark_line(point=alt.OverlayMarkDef(color="turquoise", size=80), color='lightgreen')
    .encode(
        x=alt.X("year", title="Year", axis=alt.Axis(tickMinStep=1), scale=alt.Scale(domain=[2000, 2020]), sort=alt.EncodingSortField(field="year", order="ascending")),
        y=alt.Y("duration_ms", title="Average duration", scale=alt.Scale(zero=False), axis=alt.Axis(formatType="timeUnit", format="hh:mm:ss"),sort=alt.EncodingSortField(field="duration_ms", order="descending")),
        order='year',
        tooltip=[
            alt.Tooltip(field="year", type="nominal", title="Year"),
            alt.Tooltip(field="duration_ms", type="nominal", title="Average duration"),
        ],

    )
)


#top 10歌手的average popularity
i = 0
avg_list=[]
while i < 10:
    average_popularity = top_10_artists['popularity'][i]/len(df[df.artist == top_10_artists['artist'][i]])
    avg_list.append(average_popularity)
    i += 1
top_10_artists['average_popularity'] = avg_list
df7 = pd.DataFrame({
    'artist':top_10_artists['artist'],
    'average_popularity': top_10_artists['average_popularity']  
})


fig4 = plt.figure(figsize=(15, 5))
plt.xlabel('Artist', size=15)
plt.ylabel('Average popularity', size=15)
plt.title('The average popularity of top 10 artists', fontsize=20) 
plt.scatter(x=top_10_artists['artist'], y=top_10_artists['average_popularity'], color='turquoise', s=100)

#翻页
page_filter = st.sidebar.radio(
    "Choose the page",
    ('The change of popularity of different genres', 
    'Danceability & Energy', 
    'The change of duration', 
    'The top 10 artists in 20 years',
    'Generate a random playlist')
)
if page_filter == 'The change of popularity of different genres':
    st.header("The change of popularity of different genres between 2000-2009 and 2010-2019")
    st.pyplot(fig=fig1)
elif page_filter == 'Danceability & Energy':
    st.header('The importance of danceability and energy to songs clicks')
    st.pyplot(fig=fig2)
elif page_filter == 'The change of duration':
    st.header('The change of average duration of songs each year')
    st.altair_chart(chart, use_container_width=True)
elif page_filter == 'The top 10 artists in 20 years':
    st.header('The top 10 artists from 2000-2019')
    st.pyplot(fig=fig3)
    st.pyplot(fig=fig4)
    #交互1：点哪个歌手，就出现他的歌
    top_10_artists_list = []
    for i in top_10_artists['artist']:
        top_10_artists_list.append(i)

    artist_filter = st.radio(
        "Choose one of the top 10 artists",
        ('Rihanna', 'Eminem', 'Drake', 'Calvin Harris', 'David Guetta', 'Britney Spears', 'Taylor Swift', 'Katy Perry', 'Beyoncé', 'Chris Brown')
    )

    i = 0
    while i < 10:
        if artist_filter == top_10_artists_list[i]:
            songslist = df.loc[(df.artist == top_10_artists_list[i])]['song']
        i += 1

    songs = []
    for i in songslist:
        songs.append(i)

    df2 = pd.DataFrame({
        'songs': songs    
    })
    df2.index = np.arange(1, len(df2)+1)
    st.write(df2)
    
elif page_filter == 'Generate a random playlist':
    st.header('Generate a random playlist')
    #交互2：对于最受欢迎的5种风格，可以选取用户感兴趣的，随机生成歌单
    df3 = df.groupby('genre').sum().sort_values('popularity', ascending=False).head(5)
    top_5_genres = df3.reset_index(drop=False)

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
     
    df4 = pd.DataFrame({
        'recommendation_songs': random_recommendation   
    })
    df4.index = np.arange(1, len(df4)+1)
    st.write(df4)

