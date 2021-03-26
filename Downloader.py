#!/usr/bin/env python3

"""
Downloads the daily covid stats from Worldometer.

N.B.: If run multiple times in a day, updates the existing json files.

Emile Villette - March 2021
"""
import json
import os
import time
import sys

import directoryManager
import downloadFile

import progressbar


def download_stats(yesterday=False):
    """Downloads COVID stats from https://www.disease.sh/

    :param yesterday: download yesterday's data
    :return: None
    """
    start_time = time.time()

    if yesterday:
        url_yesterday = "?yesterday=true"
        path = directoryManager.daily_directory(yesterday=True)
    else:
        url_yesterday = ""
        # Get daily file path
        path = directoryManager.daily_directory()

    vaccine_data_confirmed = []
    if os.path.exists(path + "/vaccine/AA_properties.json"):
        with open(path + "/vaccine/AA_properties.json", "r") as properties_check:
            vaccine_properties = json.load(properties_check)
    else:
        vaccine_properties = []

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
        unprocessed_data = json.load(AA_process)

    processed_json = {}
    for i in unprocessed_data:
        processed_json[i["countryInfo"]["iso2"]] = i
    with open(path + "/AA_RawDataProcessed.json", "w") as AA_processed:
        json.dump(processed_json, AA_processed)

    with open("languages/countries.json", "r") as country_file:
        country_list = json.load(country_file)

    if os.path.exists("{}/AA_to_download.json".format(path)):
        with open("{}/AA_to_download.json".format(path), "r") as checker:
            country_list["iso_codes"] = json.load(checker)

    # countries that have not given their daily numbers (yet)
    no_numbers_countries = []

    # Progress bar to monitor clearly download state
    progress_widgets = [progressbar.FormatLabel(""), progressbar.Percentage(), " ",
                        progressbar.Bar(marker="█", left="[", right="]", fill="░"), " ", progressbar.AdaptiveETA(),
                        progressbar.FormatLabel("")]

    for i in progressbar.progressbar(range(len(country_list["iso_codes"])), redirect_stdout=True,
                                     widgets=progress_widgets):
        # Get the ISO_code from the user's desired country list
        iso_code = country_list["iso_codes"][i]

        progress_widgets[0] = progressbar.FormatLabel('Processing country {}: '.format(iso_code))

        if os.path.exists(path + "/" + iso_code + ".json"):

            check = downloadFile.download_file(
                "https://disease.sh/v3/covid-19/countries/" + iso_code + url_yesterday,
                ".json",
                iso_code,
                path,
                case_file=True,
            )
            if check:
                no_numbers_countries.append(iso_code)
                progress_widgets[-1] = progressbar.FormatLabel(" | {}: No data".format(iso_code))
            else:
                progress_widgets[-1] = progressbar.FormatLabel(" | {}: OK".format(iso_code))

        else:
            # Download the "country"'s daily data
            check = downloadFile.download_file(
                "https://disease.sh/v3/covid-19/countries/" + iso_code + url_yesterday,
                ".json",
                iso_code,
                path,
                case_file=True,
            )
            if check:
                no_numbers_countries.append(iso_code)
                progress_widgets[-1] = progressbar.FormatLabel(" | {}: No data".format(iso_code))
            else:
                progress_widgets[-1] = progressbar.FormatLabel(" | {}: OK".format(iso_code))

        # Download the "country"'s vaccine data in the last five days.
        if not iso_code in vaccine_properties:
            days_ago = 5
            for tries in range(4):
                try_vaccine_data = downloadFile.download_file(
                    "https://disease.sh/v3/covid-19/vaccine/coverage/countries/{}?lastdays={}".format(iso_code,
                                                                                                      days_ago),
                    ".json",
                    iso_code + "_VACCINE",
                    path + "/vaccine",
                    vaccine_file=True,
                )
                if not try_vaccine_data:
                    vaccine_data_confirmed.append(iso_code)
                    break
                else:
                    days_ago += 1

        # AA_DAILY_Recap requires country ISO codes to be separated by a comma in the URL.
        recap_countries_to_request += iso_code + ","

    with open(path + "/vaccine/AA_properties.json", "w") as vaccine_check:
        json.dump(vaccine_data_confirmed, vaccine_check)

    with open(
            "{}/AA_to_download.json".format(path), "w"
    ) as updated_no_numbers_countries:
        json.dump(no_numbers_countries, updated_no_numbers_countries)

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
        path,
    )

    # Download per country GLOBAL vaccine stats in the two last days
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/vaccine/coverage/countries/?lastdays=5",
        ".json",
        "AA_DAILY_TOTAL_VACCINE",
        path + "/vaccine",
    )

    # Download GLOBAL Vaccine data (the whole world without per-country details)
    downloadFile.download_file(
        "https://disease.sh/v3/covid-19/vaccine/coverage?lastdays=5",
        ".json",
        "AA_DAILY_TOTAL_GLOBAL_VACCINE",
        path + "/vaccine",
    )

    print(
        "------- Process took %s seconds to execute -------"
        % (time.time() - start_time)
    )
    return path
