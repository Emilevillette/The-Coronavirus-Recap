#!/usr/bin/env python3

"""
Daily recap generator (French version)

Emile Villette - March 2021
"""
import json
import locale
import os
from datetime import date, timedelta


def generate_recap(recap_file, path, user_data, total, yesterday_missing, uuid, test_mode=False):
    """

    :param test_mode: test mode
    :param yesterday_missing: user's yesterday missing data
    :param total: the filename with the total cases in it
    :param recap_file: The recap file's name (with the extension) (string)
    :param path: the directory with the recap file in it (string)
    :param user_data: file of the user with the preferences
    :return: recap, a string of the daily recap.
    """
    # Set locale separator to the local preference
    locale.setlocale(locale.LC_ALL, "")

    # Open json file with list of chosen countries
    with open(path + recap_file, "r") as file:
        data = json.loads(file.read())

    with open("languages/countries.json", "r") as countries_file:
        countries_data = json.load(countries_file)

    # Open json file with the language data in it, according to the user's preferred language
    with open("languages/EN.json", "r", encoding="utf-8") as language_file:
        language_data = json.load(language_file)
        yesterday_sentence = language_data["yesterday_missed_data"] + "\n\n"

    # Initialize recap
    recap = ""

    recap = generate_per_country_recap(recap, path, user_data, language_data, countries_data, data, test_mode, uuid)

    with open(path + total, "r") as total_file:
        total_cases = json.loads(total_file.read())

    recap += (
            language_data["global_cases"].format(
                total_cases["cases"],
                total_cases["todayCases"],
                total_cases["deaths"],
                total_cases["todayDeaths"],
            )
            + "\n"
    )

    with open(
            path + "/vaccine/" + "AA_DAILY_TOTAL_GLOBAL_VACCINE.json", "r"
    ) as vaccine_total_file:
        total_vaccine = json.loads(vaccine_total_file.read())

    total_vaccine_data = []

    for global_vaccine in total_vaccine.values():
        total_vaccine_data.append(global_vaccine)

    if int(total_vaccine_data[1]) - int(total_vaccine_data[0]) > 0:
        recap += (
                language_data["global_vaccine"].format(
                    total_vaccine_data[1],
                    int(total_vaccine_data[1]) - int(total_vaccine_data[0]),
                )
                + "\n"
        )

    if len(yesterday_missing) > 0:
        recap += "\n\n" + yesterday_sentence
        new_path = f"data/{str(date.today() - timedelta(days=1))}/"
        recap += generate_per_country_recap(recap, new_path, user_data, language_data, countries_data,
                                            yesterday_missing, test_mode, uuid, treating_missing=True)

    return recap


def generate_per_country_recap(recap, path, user_data, language_data, countries_data, data, test_mode, uuid,
                               treating_missing=False):
    today_missing_countries = []

    user_cases = user_data["countries"].split(",")
    user_vaccine = user_data["vaccine detail"].split(",")
    user_critical = user_data["critical"].split(",")
    user_100k = user_data["active cases per 100k"].split(",")
    user_recovered = user_data["recovered today"].split(",")

    case_sentence = language_data["cases"] + "\n"
    critical_sentence = language_data["critical"] + "\n"
    vaccine_sentence = language_data["vaccine"] + "\n"
    no_data_sentence = language_data["no_data"] + "\n"

    with open(f"{path}/AA_to_download.json", "r") as missing_data_file:
        missing_countries = json.load(missing_data_file)

    for country in range(len(user_cases)):
        if os.path.isfile(f"{path}/vaccine/{user_cases[country]}_VACCINE.json"):
            with open(
                    path + "vaccine/" + user_cases[country] + "_VACCINE.json", "r"
            ) as vaccine_file:
                vaccine_data = json.loads(vaccine_file.read())

        vaccine_delta = []
        for day in vaccine_data["timeline"].values():
            vaccine_delta.append(day)

        if user_cases[country] not in missing_countries:
            recap += case_sentence.format(
                countries_data["couples"][user_cases[country]],
                data[user_cases[country]]["todayDeaths"],
                data[user_cases[country]]["todayCases"],
            )
        else:
            recap += no_data_sentence.format(countries_data["couples"][user_cases[country]])
            today_missing_countries.append(user_cases[country])

        if user_cases[country] in user_critical:
            recap += critical_sentence.format(
                data[user_cases[country]]["critical"])

        if os.path.isfile(f"{path}/vaccine/{user_cases[country]}_VACCINE.json") and (
                user_cases[country] in user_vaccine
        ):
            if int(vaccine_delta[1]) - int(vaccine_delta[0]) > 0:
                recap += vaccine_sentence.format(
                    vaccine_delta[1], int(
                        vaccine_delta[1]) - int(vaccine_delta[0])
                )
        recap += "\n"

        if not treating_missing and not test_mode:
            with open(f"User_data/Users/{uuid}.json", "r") as read_user_data:
                old_data = json.load(read_user_data)
            old_data["yesterday_missing"] = today_missing_countries
            with open(f"User_data/Users/{uuid}.json", "w") as write_user_data:
                json.dump(old_data, write_user_data)

    return recap
