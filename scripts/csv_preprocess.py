import os
import pandas as pd
from datetime import datetime

PROJECT_PATH = '/project/bigdata-final-project-iu-2024'
DATA_LOCATION = os.path.join(PROJECT_PATH, 'data')
MOVIE_PATH = os.path.join(DATA_LOCATION, 'movies.csv')
NEW_MOVIE_PATH = os.path.join(DATA_LOCATION, 'new_movies.csv')


def preprocess_movie_csv():
    # read data
    data_path = MOVIE_PATH
    data = pd.read_csv(data_path)
    # genres to list
    data.genres = data.genres.apply(lambda x: x.split('|'))
    # create new dataframe
    new_df_movie = {'movieId': [], 'title': []}
    new_df_ganres = {'recordId': [], 'movieId': [], 'genre': []}
    for _, elem in data.iterrows():
        new_df_movie['movieId'].append(elem.movieId)
        new_df_movie['title'].append(elem.title)
        for genre in elem.genres:
            idx = len(new_df_ganres['recordId'])
            new_df_ganres['recordId'].append(idx)
            new_df_ganres['movieId'].append(elem.movieId)
            new_df_ganres['genre'].append(genre)
    new_df_movie = pd.DataFrame.from_dict(new_df_movie)
    new_df_ganres = pd.DataFrame.from_dict(new_df_ganres)
    # save result
    new_data_movie_path = NEW_MOVIE_PATH
    new_data_genres_path = os.path.join(DATA_LOCATION, 'ganres.csv')
    new_df_movie.to_csv(new_data_movie_path, index=False)
    new_df_ganres.to_csv(new_data_genres_path, index=False)


def create_recordId_column():
    files = ['links.csv', 'ratings.csv', 'tags.csv']
    for f in files:
        data_path = os.path.join(DATA_LOCATION, f)
        data = pd.read_csv(data_path)
        data["recordId"] = range(len(data))
        data.to_csv(data_path, index=False)


def convert_timestamp():
    files = ['ratings.csv', 'tags.csv']
    for f in files:
        # YYYY-MM-DD HH:MM:SS
        data_path = os.path.join(DATA_LOCATION, f)
        df = pd.read_csv(data_path)
        df['timestamp'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %I:%M:%S"))
        df.to_csv(data_path, index=False)

        
preprocess_movie_csv()
create_recordId_column()
convert_timestamp()

