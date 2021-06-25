import pandas as pd
import random


def prepare_data(file_path='./data/Thu_Jun_24_18.55.29_2021_data.csv'):
    '''read file drop duplicate and sort by frequency'''
    df = pd.read_csv(file_path)
    df.drop(df.columns[0], axis=1, inplace=True)
    df['frequency'] = df['content'].map(df['content'].value_counts())
    return df.drop_duplicates().sort_values(df.columns[1], axis=0, ascending=False)


def pick_random(df, numbers=10):
    '''return list of random song from df'''
    return random.sample(df['content'].tolist(), numbers)


def most_played(df, top_k=5):
    '''return list of most played song'''
    return df['content'].tolist()[:top_k]
