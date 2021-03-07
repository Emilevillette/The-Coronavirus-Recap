#!/usr/bin/env python3

"""
Daily recap generator (French version)

Emile Villette - March 2021
"""
import json
import locale


def generate_recap(recap_file, path, country_list):
    locale.setlocale(locale.LC_ALL, '')

    with open(path + recap_file, "r") as file:
        data = json.loads(file.read())

    sentence = "{}: {:n} morts et {:n} nouveaux cas\n"
    recap = ""

    for country in range(len(data)):
        recap += sentence.format(country_list[country][1], data[country]["todayDeaths"], data[country]["todayCases"])

    return recap
