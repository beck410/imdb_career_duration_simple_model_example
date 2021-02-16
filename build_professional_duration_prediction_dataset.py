from functools import reduce
import pandas as pd
import numpy as np

from constants import (
    IMDB_DATASETS,
    DATASETS_DIR
)


def get_imdb_dataframe(file_name):
    file_path = "{}/{}.tsv.gz".format(DATASETS_DIR, file_name)
    return pd.read_csv(file_path, sep='\t')

def merge_df_datasets(df_mappings):
    # one for loop instead of three
    title_df_list = [
        df_mappings[x] for x in df_mappings
        if 'tconst' in df_mappings[x].columns and 'nconst' not in df_mappings[x].columns
    ]

    main_df_list = [
        df_mappings[x] for x in df_mappings
        if 'tconst' in df_mappings[x].columns and 'nconst' in df_mappings[x].columns
    ]

    name_df_list = [
        df_mappings[x] for x in df_mappings
        if 'nconst' in df_mappings[x].columns and 'tconst' not in df_mappings[x].columns
    ]

    title_df_list.extend(main_df_list)
    print("join title datasets...")

    df = reduce(lambda left,right: pd.merge(left,right, on='tconst',
                                            how='left'), title_df_list)
    print("join title and name datasets...")
    # create list with df + name_df_list
    df = reduce(lambda left,right: pd.merge(left,right,on='nconst',
                                            how='left'), [df] + name_df_list)

    df = pd.merge(df,df_mappings['title_akas'],left_on='tconst', right_on='titleId', how='left')


def get_final_df_mapping():
    imdb_df_mapping = {}

    for dataset in IMDB_DATASETS:
        df = get_imdb_dataframe(dataset['dataset'])
        drop_columns = set(df.columns).difference(set(dataset['columns']))
        imdb_df_mapping[dataset['dataset']] = df.drop(drop_columns, 1)

    return imdb_df_mapping

def save_staging_data_to_csv(df):
    print('saving staging data...')
    file_path = '{}/{}.csv'.format(DATASETS_DIR, 'staging_features')
    df.to_csv(file_path)
    print('staging features saved to csv')

def build_features_dataset(stage_df):
    # filter data
    df = stage_df.loc[stage_df['averageRating'].notnull()] # remove rows where title has no ratings
    df = df.loc[df['startYear'] != '\\N']
    df = df.loc[df['titleType'].isin(['movie'])]

    # sanitize data
    df['language'] = df['language'].replace(['\\N'], 'unknown')
    df['region'] = df['region'].replace(['\\N'], 'unknown')
    df['genres'] = df['genres'].apply(lambda x: str(x).split(',')).apply(tuple)
    df['language'].fillna(value='unknown').astype('string')
    df['region'].fillna(value='unknown').astype('string')
    df['language'] = df['language'].apply(lambda x: str(x).split(',')).apply(tuple)
    df['region'] = df['region'].apply(lambda x: str(x).split(',')).apply(tuple)
    df['primaryProfession'] = df['primaryProfession'].apply(lambda x: str(x).split(',')).apply(tuple)

    # add fields
    df = df \
        .assign(startYear = pd.to_numeric(df['startYear'])) \
        .assign(ratingScore = (df['averageRating']/df['numVotes']).astype(float))

    # aggregates
    df = df.groupby(["nconst", "primaryProfession"]) \
      .agg({
        "primaryProfession": ['first'],
        "titleId": [np.size], # num_media_jobs
        "genres": [np.sum], # genres,
        "ratingScore": [np.mean, np.average], # average/mean rating scores
        "startYear": ['min', 'max'],
        "language": [np.sum],
        "region": [np.sum]
      })

    df.columns = ['primaryProfession', 'title__sum', 'genres__sum', 'ratingScore__mean', 'ratingScore__avg', 'startYear__min', 'startYear__max', 'language__sum', 'region__sum']

    # additional features
    df = df.assign(careerDuration= df['startYear__max'] - df['startYear__min'].astype(int))
    df['language__sum'] = df['language__sum'].apply(lambda x: set(x))
    df['language__size'] = df['language__sum'].apply(lambda x: len(x))
    df['region__sum'] = df['region__sum'].apply(lambda x: set(x))
    df['region__size'] = df['region__sum'].apply(lambda x: len(x))

    # filter final dataset
    df = df.loc[df['startYear__max'] != 2021]



def load_staging_data_from_csv():
    file_path = '{}/{}.csv'.format(DATASETS_DIR, 'staging_features')
    return pd.read_csv(file_path)
