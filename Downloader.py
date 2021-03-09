#!/usr/bin/env python3

"""
Downloads the daily covid stats from Worldometer.

N.B.: If run multiple times in a day, updates the existing ".coviddata" files.

Emile Villette - March 2021
"""
import dailyDirectory
import downloadFile


def download_stats(countries_to_track):
    """

    :param countries_to_track: the list of the countries to track in the form [["COUNTRY ISO CODE", "Country name],...]
    :return: None
    """
    # Get daily file path
    path = dailyDirectory.daily_directory()

    # Recap file
    recap_countries_to_request = ""

    # Download today's files from https://disease.sh/v3/covid-19/countries
    downloadFile.download_file('https://disease.sh/v3/covid-19/countries', '.coviddata', 'AA_RawData', path)

    for country in range(len(countries_to_track)):
        ISO_code = countries_to_track[country][0]
        downloadFile.download_file('https://disease.sh/v3/covid-19/countries/' + ISO_code, ".coviddata", ISO_code, path)
        downloadFile.download_file(
            "https://disease.sh/v3/covid-19/vaccine/coverage/countries/" + ISO_code + "?lastdays=2",
            ".coviddata", ISO_code + "_VACCINE", path + "/vaccine")

        recap_countries_to_request += ISO_code + ","

    recap_countries_to_request.rstrip(",")
    downloadFile.download_file('https://disease.sh/v3/covid-19/countries/' + recap_countries_to_request,
                               ".coviddata", "AA_DAILY_Recap", path)

    downloadFile.download_file('https://disease.sh/v3/covid-19/all', ".coviddata", "AA_DAILY_TOTAL", path)

    downloadFile.download_file('https://disease.sh/v3/covid-19/vaccine/coverage/countries/?lastdays=2', ".coviddata",
                               "AA_DAILY_TOTAL_VACCINE", path + "/vaccine")

    return path
