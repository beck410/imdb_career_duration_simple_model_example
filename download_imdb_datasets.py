import io
import requests
import zipfile

from constants import (
    IMDB_DATASETS,
    DATASETS_DIR
)


def download_datasets():
    for dataset in IMDB_DATASETS:
        file_path = '{}/{}.tsv.gz'.format(DATASETS_DIR, dataset['dataset'])

        _download_url(dataset['url'], file_path)
        print('{} dataset downloaded'.format(dataset['dataset']))

def _download_url(url, save_path, chunk_size=128):
    response = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(response.content)
