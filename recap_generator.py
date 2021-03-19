#!/usr/bin/env python3

"""
Daily recap generator (French version)

Emile Villette - March 2021
"""
import json
import locale


def generate_recap(recap_file, path, user_data, total):
    """

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

    user_cases = user_data["countries"].split(",")

    with open("languages/countries.json", "r") as countries_file:
        countries_data = json.load(countries_file)

    # Open json file with the language data in it, according to the user's preferred language
    with open("languages/EN.json", "r", encoding="utf-8") as language_file:
        language_data = json.load(language_file)
        case_sentence = language_data["cases"] + "\n"
        critical_sentence = language_data["critical"] + "\n"
        vaccine_sentence = language_data["vaccine"] + "\n\n"

    # Empty string for the daily recap
    recap = ""

    for country in range(len(user_cases)):
        with open(
            path + "vaccine/" + user_cases[country] + "_VACCINE.json", "r"
        ) as vaccine_file:
            vaccine_data = json.loads(vaccine_file.read())

        vaccine_delta = []
        for day in vaccine_data["timeline"].values():
            vaccine_delta.append(day)

        recap += case_sentence.format(
            countries_data["couples"][user_cases[country]],
            data[user_cases[country]]["todayDeaths"],
            data[user_cases[country]]["todayCases"],
        )
        recap += critical_sentence.format(
            data[user_cases[country]]["critical"])
        if int(vaccine_delta[1]) - int(vaccine_delta[0]) > 0:
            recap += " " * len(user_data[country][1]) + vaccine_sentence.format(
                vaccine_delta[1], int(vaccine_delta[1]) - int(vaccine_delta[0])
            )
        else:
            recap += "\n"

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

    recap += "\n" + language_data["vaccine_warning"]

    return recap
