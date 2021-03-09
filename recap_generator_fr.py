#!/usr/bin/env python3

"""
Daily recap generator (French version)

Emile Villette - March 2021
"""
import json
import locale


def generate_recap(recap_file, path, country_list, total):
    """

    :param total: the filename with the total cases in it
    :param recap_file: The recap file's name (with the extension) (string)
    :param path: the directory with the recap file in it (string)
    :param country_list: list of the countries with the ISO codes and the translations
    :return: recap, a string of the daily recap.
    """
    locale.setlocale(locale.LC_ALL, '')

    with open(path + recap_file, "r") as file:
        data = json.loads(file.read())

    case_sentence = "{}: {:n} morts et {:n} nouveaux cas.\n"
    vaccine_sentence = "  {:n} doses de vaccin administrées (+ {:n}).\n"

    recap = ""

    for country in range(len(data)):
        with open(path + "/vaccine/" + country_list[country][0] + "_VACCINE.coviddata", "r") as vaccine_file:
            vaccine_data = json.loads(vaccine_file.read())

        vaccine_delta = []
        for day in vaccine_data["timeline"].values():
            vaccine_delta.append(day)
        recap += case_sentence.format(country_list[country][1], data[country]["todayDeaths"],
                                      data[country]["todayCases"])
        recap += " " * len(country_list[country][1]) + vaccine_sentence.format(vaccine_delta[1],
                                                                               int(vaccine_delta[1]) - int(
                                                                                   vaccine_delta[0]))

    with open(path + total, 'r') as file2:
        total_cases = json.loads(file2.read())
    recap += "{:n} (+{:n}) cas et {:n} (+{:n}) morts dans le monde.\n".format(total_cases["cases"],
                                                                              total_cases["todayCases"],
                                                                              total_cases["deaths"],
                                                                              total_cases["todayDeaths"])

    return recap