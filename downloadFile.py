#!/usr/bin/env python3

"""
Emile Villette - October 2020

download a file from the internet and store it in a directory specified by the user
"""
from time import sleep

import requests


def download_file(url, file_extension, category, path, case_file=False, failed=0):
    """downloads a file from the internet and stores it in the specified directory.

    :param failed: Number of time the connection has failed, only called by function itself
    :param case_file: defines whether the file to download is a covid general case file
    :param url: A string that is The URL to download from
    :param file_extension: a string that is the file extension to store the file in (MUST include a "," in the beginning
    :param category: a string that specifies the name of the file
    :param path: The path on the local machine (string)
    :return: None
    """
    try:
        # Get content from the desired webpage
        r = requests.get(url, stream=True)
        if case_file:
            request_json = r.json()
            if request_json["todayCases"] == 0 and request_json["todayDeaths"] == 0:
                del request_json
                return True

        # Store acquired content in file in the desired path
        with open(path + "/" + category + file_extension, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except ConnectionError and ConnectionAbortedError as e:
        if failed > 10:
            raise ConnectionError(
                "Connection failed, please ensure you have a valid internet connection."
            )
        else:
            new_failed = failed + 1
            print(
                "Connection failed: retrying, {} tries left before throwing an Error".format(
                    str(10 - failed)
                )
            )
            sleep(0.5)
            download_file(
                url, file_extension, category, path, case_file=False, failed=new_failed
            )
