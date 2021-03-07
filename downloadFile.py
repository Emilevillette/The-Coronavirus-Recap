#!/usr/bin/env python3

"""
Emile Villette - October 2020

download a file from the internet and store it in a directory named "jj/mm/aa"
"""
import requests


def download_file(url, category, path):
    r = requests.get(url, stream=True)

    with open(path + "/" + category + '.coviddata', "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


