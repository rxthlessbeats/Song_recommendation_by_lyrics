import webbrowser
import urllib.parse

import pandas as pd
import numpy as np
from datetime import date,datetime

def song_recommend(user_happy_rating=0.1, user_energetic_rating=0.1, year=2018):
    song_lyrics_df = pd.read_csv('D:/python training/Text mining/en_lyrics_scale.csv')
    song_lyrics_df['chart_date'] = song_lyrics_df['chart_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    # song_lyrics_df = pd.read_excel('D:/python training/Text mining/en_lyrics_scale.xlsx')
    
    for d in np.arange(0, 1, 0.01):
    # Filter dataset by user input
        song_lyrics_filtered_df = song_lyrics_df[(song_lyrics_df['sentiment']>=user_happy_rating-d) & (song_lyrics_df['sentiment']<=user_happy_rating+d)]
        song_lyrics_filtered_df = song_lyrics_df[(song_lyrics_df['cluster_distance']>=user_energetic_rating-d) & (song_lyrics_df['cluster_distance']<=user_energetic_rating+d)]
        song_lyrics_filtered_df = song_lyrics_filtered_df[(song_lyrics_filtered_df['chart_date']>=date(year-1, 12, 31)) & (song_lyrics_filtered_df['chart_date']<=date(year+1, 1, 1))]

        if song_lyrics_filtered_df.empty == False:
            break
    
    
    song_lyrics_filtered_df = song_lyrics_filtered_df.reset_index(drop=True)
    
    # If no song found, recommend most happy and energetic song
    if song_lyrics_filtered_df.empty:
        selected_df = song_lyrics_df[(song_lyrics_df['chart_date']>=date(year-1, 12, 31)) & (song_lyrics_df['chart_date']<=date(year+1, 1, 1))]
        selected_df = selected_df.reset_index(drop=True)
        min = 100
        for i in range(len(selected_df)):
            if (selected_df['sentiment'][i] - user_happy_rating)**2 + (selected_df['cluster_distance'][i] - user_energetic_rating)**2 < min:
                min = (selected_df['sentiment'][i] - user_happy_rating)**2 + (selected_df['cluster_distance'][i] - user_energetic_rating)**2
                selected = [selected_df['song_name'][i], selected_df['artist_name'][i]]
    
    else:
        min = 100
        for i in range(len(song_lyrics_filtered_df)):
            if (song_lyrics_filtered_df['sentiment'][i] - user_happy_rating)**2 + (song_lyrics_filtered_df['cluster_distance'][i] - user_energetic_rating)**2 < min:
                min = (song_lyrics_filtered_df['sentiment'][i] - user_happy_rating)**2 + (song_lyrics_filtered_df['cluster_distance'][i] - user_energetic_rating)**2
                selected = [song_lyrics_filtered_df['song_name'][i], song_lyrics_filtered_df['artist_name'][i]]
                
    song_name = selected[0]
    artist_name = selected[1]

    # Constructing the search query
    query = song_name + " " + artist_name
    query_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)

    # Opening the first search result in a new window with autoplay enabled
    webbrowser.open_new(query_url)
    
song_recommend()