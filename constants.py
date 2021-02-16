import os

IMDB_DATASETS = [
    {
        'dataset': 'name_basics',
        'url': 'https://datasets.imdbws.com/name.basics.tsv.gz',
        'columns': ['nconst', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
    },
    {
        'dataset': 'title_akas',
        'url': 'https://datasets.imdbws.com/title.akas.tsv.gz',
        'columns': ['titleId', 'region', 'language']
    },
    {
        'dataset': 'title_basics',
        'url': 'https://datasets.imdbws.com/title.basics.tsv.gz',
        'columns': ['tconst', 'titleType', 'primaryTitle', 'isAdult', 'startYear', 'endYear', 'genres']
    },
    {
        'dataset': 'title_crew',
        'url': 'https://datasets.imdbws.com/title.crew.tsv.gz',
        'columns': ['tconst', 'directors', 'writers']
    },
    {
        'dataset': 'title_principals',
        'url':'https://datasets.imdbws.com/title.principals.tsv.gz',
        'columns': ['tconst', 'nconst', 'category', 'job']
    },
    {
        'dataset': 'title_ratings',
        'url': 'https://datasets.imdbws.com/title.ratings.tsv.gz',
        'columns': ['tconst', 'averageRating', 'numVotes']
    }
]

DATASETS_DIR = '{}/datasets'.format(os.getcwd())
