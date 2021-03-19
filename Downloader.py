#!/usr/bin/env python3

"""
Downloads the daily covid stats from Worldometer.

N.B.: If run multiple times in a day, updates the existing ".coviddata" files.

Emile Villette - March 2021
"""
import json
import os

import directoryManager
import downloadFile


def download_stats(yesterday=False):
    """Downloads COVID stats from https://www.disease.sh/

    :param yesterday: download yesterday's data
    :return: None
    """

    if yesterday:
        url_yesterday = "?yesterday=true"
        path = directoryManager.daily_directory(yesterday=True)
    else:
        url_yesterday = ""
        # Get daily file path
        path = directoryManager.daily_directory()

    if os.path.exists(path + "/vaccine/AA_properties.json"):
        with open(path + "/vaccine/AA_properties.json", "r") as properties_check:
            vaccine_properties = json.load(properties_check)
            if vaccine_properties["downloaded"]:
                vaccine_is_downloaded = True
    else:
        vaccine_is_downloaded = False

    # Recap file
    recap_countries_to_request = ""

    # Download today's files from https://disease.sh/v3/covid-19/countries
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/countries" + url_yesterday,
        ".json",
        "AA_RawData",
        path,
    )

    with open(path + "/AA_RawData.json", "r") as AA_process:
        AA_data = json.load(AA_process)

    AA = {}
    for i in AA_data:
        AA[i["countryInfo"]["iso2"]] = i
    with open(path + "/AA_RawDataProcessed.json", "w") as AA_processed:
        json.dump(AA, AA_processed)

    with open("languages/countries.json", "r") as country_file:
        country_list = json.load(country_file)

    for country in country_list["iso_codes"]:
        # Get the ISO_code from the user's desired country list
        iso_code = country

        if os.path.exists(path + "/" + iso_code + ".json"):

            with open(path + "/" + iso_code + ".json") as update_check:
                update_data = json.load(update_check)

            if update_data["todayCases"] == 0 and update_data["todayDeaths"] == 0:
                downloadFile.download_file(
                    "https://disease.sh/v3/covid-19/countries/"
                    + iso_code
                    + url_yesterday,
                    ".json",
                    iso_code,
                    path,
                )

        else:
            # Download the "country"'s daily data
            downloadFile.download_file(
                "https://disease.sh/v3/covid-19/countries/" + iso_code + url_yesterday,
                ".json",
                iso_code,
                path,
            )

        # Download the "country"'s vaccine data in the last two days.
        if not vaccine_is_downloaded:
            downloadFile.download_file(
                "https://disease.sh/v3/covid-19/vaccine/coverage/countries/{}?lastdays=2".format(iso_code),
                ".json",
                iso_code + "_VACCINE",
                path + "/vaccine",
            )

        # AA_DAILY_Recap requires country ISO codes to be separated by a comma in the URL.
        recap_countries_to_request += iso_code + ","

    # Remove the most right comma from the recap_countries_to_request
    recap_countries_to_request.rstrip(",")

    # Download the user's selected countries data in one singles file for archiving.
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/countries/"
        + recap_countries_to_request
        + url_yesterday,
        ".json",
        "AA_DAILY_Recap",
        path,
    )

    # Daily GLOBAL (the whole world without per-country details)
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/all" + url_yesterday,
        ".json",
        "AA_DAILY_TOTAL",
        path
    )

    # Download per country GLOBAL vaccine stats in the two last days
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/vaccine/coverage/countries/?lastdays=2",
        ".json",
        "AA_DAILY_TOTAL_VACCINE",
        path + "/vaccine",
    )

    # Download GLOBAL Vaccine data (the whole world without per-country details)
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/vaccine/coverage?lastdays=2",
        ".json",
        "AA_DAILY_TOTAL_GLOBAL_VACCINE",
        path + "/vaccine",
    )

    if not vaccine_is_downloaded:
        with open(path + "/vaccine/AA_properties.json", "w") as vaccine_downloaded:
            vaccine_downloaded.write('{"downloaded": 1}')

    return path
