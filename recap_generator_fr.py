#!/usr/bin/env python3

"""
Daily recap generator (French version)

Emile Villette - March 2021
"""
import json
import locale


def generate_recap(recap_file, path, country_list):
    """

    :param recap_file: The recap file's name (with the extension) (string)
    :param path: the directory with the recap file in it (string)
    :param country_list: list of the countries with the ISO codes and the translations
    :return: recap, a string of the daily recap.
    """
    locale.setlocale(locale.LC_ALL, '')

    with open(path + recap_file, "r") as file:
        data = json.loads(file.read())

    sentence = "{}: {:n} morts et {:n} nouveaux cas\n"
    recap = ""

    for country in range(len(data)):
        recap += sentence.format(country_list[country][1], data[country]["todayDeaths"], data[country]["todayCases"])

    return recap
