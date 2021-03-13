#!/usr/bin/env python3

"""
Downloads the daily covid stats from Worldometer.

N.B.: If run multiple times in a day, updates the existing ".coviddata" files.

Emile Villette - March 2021
"""
import directoryManager
import downloadFile


def download_stats(countries_to_track, yesterday=False):
    """

    :param yesterday: download yesterday's data
    :param countries_to_track: the list of the countries to track in the form [["COUNTRY ISO CODE", "Country name],...]
    :return: None
    """

    if yesterday:
        url_yesterday = "?yesterday=true"
        path = directoryManager.daily_directory(yesterday=True)
    else:
        url_yesterday = ""
        # Get daily file path
        path = directoryManager.daily_directory()

    # Recap file
    recap_countries_to_request = ""

    # Download today's files from https://disease.sh/v3/covid-19/countries
    downloadFile.download_file('https://disease.sh/v3/covid-19/countries' + url_yesterday, '.json', 'AA_RawData', path)

    for country in range(len(countries_to_track)):
        # Get the ISO_code from the user's desired country list
        ISO_code = countries_to_track[country][0]

        # Download the "country"'s daily data
        downloadFile.download_file('https://disease.sh/v3/covid-19/countries/' + ISO_code + url_yesterday, ".json",
                                   ISO_code, path)

        # Download the "country"'s vaccine data in the last two days.
        downloadFile.download_file(
            "https://disease.sh/v3/covid-19/vaccine/coverage/countries/" + ISO_code + "?lastdays=2",
            ".json", ISO_code + "_VACCINE", path + "/vaccine")

        # AA_DAILY_Recap requires country ISO codes to be separated by a comma in the URL.
        recap_countries_to_request += ISO_code + ","

    # Remove the most right comma from the recap_countries_to_request
    recap_countries_to_request.rstrip(",")

    # Download the user's selected countries data in one singles file for archiving.
    downloadFile.download_file('https://disease.sh/v3/covid-19/countries/' + recap_countries_to_request + url_yesterday,
                               ".json", "AA_DAILY_Recap", path)

    # Daily GLOBAL (the whole world without per-country details)
    downloadFile.download_file('https://disease.sh/v3/covid-19/all' + url_yesterday, ".json", "AA_DAILY_TOTAL", path)

    # Download per country GLOBAL vaccine stats in the two last days
    downloadFile.download_file('https://disease.sh/v3/covid-19/vaccine/coverage/countries/?lastdays=2', ".json",
                               "AA_DAILY_TOTAL_VACCINE", path + "/vaccine")

    # Download GLOBAL Vaccine data (the whole world without per-country details)
    downloadFile.download_file('https://disease.sh/v3/covid-19/vaccine/coverage?lastdays=2', ".json",
                               "AA_DAILY_TOTAL_GLOBAL_VACCINE", path + "/vaccine")

    return path
