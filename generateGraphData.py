"""
Generate JSON data for chartjs graphs.

Emile Villette - April 2021
"""
import datetime
import json
import os
from shutil import copy2
from math import log

from dateutil.parser import *


def generate_graph_data():
    with open("languages/countries.json", "r") as countries_file:
        countries_data = json.load(countries_file)

    data_cases = {}
    data_cases_today = {}
    data_cases_log = {}
    data_deaths = {}
    data_deaths_today = {}
    data_deaths_log = {}
    data_recovered = {}
    data_recovered_today = {}
    data_recovered_log = {}

    for country in countries_data["iso_codes"]:
        data_cases[country] = {}
        data_deaths[country] = {}
        data_recovered[country] = {}
        data_cases_today[country] = {}
        data_deaths_today[country] = {}
        data_recovered_today[country] = {}
        data_cases_log[country] = {}
        data_deaths_log[country] = {}
        data_recovered_log[country] = {}

    for file in os.scandir("data"):
        try:
            if isinstance(parse(file.name), datetime.date):
                for country in countries_data["iso_codes"]:
                    try:
                        filename = file.name
                        with open(
                                f"data/{filename}/{country}.json", "r"
                        ) as current_country:
                            current_data = json.load(current_country)
                        data_cases_today[country][filename] = current_data[
                            "todayCases"
                        ]
                        data_cases[country][filename] = current_data["cases"]
                        data_deaths_today[country][filename] = current_data[
                            "todayDeaths"
                        ]
                        data_deaths[country][filename] = current_data["deaths"]
                        data_recovered_today[country][filename] = current_data[
                            "todayRecovered"
                        ]
                        data_recovered[country][filename] = current_data["recovered"]

                        if data_cases[country][filename] > 0:
                            data_cases_log[country][filename] = log(data_cases[country][filename])
                        else:
                            data_cases_log[country][filename] = None
                        if data_deaths[country][filename] > 0:
                            data_deaths_log[country][filename] = log(data_deaths[country][filename])
                        else:
                            data_deaths_log[country][filename] = None
                        if data_recovered[country][filename] > 0:
                            data_recovered_log[country][filename] = log(data_recovered[country][filename])
                        else:
                            data_recovered_log[country][filename] = None
                    except FileNotFoundError:
                        print(f"No file named {country}, skipped entry.")
        except ParserError as e:
            print(f"{e} (Skipped non datetime file).")

    # TODO: Make a copy of those files in website directory
    with open("data/graph_data/graph_data_cases.json", "w") as write_data:
        json.dump(data_cases, write_data)
    copy2(
        "data/graph_data/graph_data_cases.json", "website/static/graph_data_cases.json"
    )

    with open("data/graph_data/graph_data_cases_today.json", "w") as write_data:
        json.dump(data_cases_today, write_data)
    copy2(
        "data/graph_data/graph_data_cases_today.json",
        "website/static/graph_data_cases_today.json",
    )

    with open("data/graph_data/graph_data_deaths.json", "w") as write_data:
        json.dump(data_deaths, write_data)
    copy2(
        "data/graph_data/graph_data_deaths.json",
        "website/static/graph_data_deaths.json",
    )

    with open("data/graph_data/graph_data_deaths_today.json", "w") as write_data:
        json.dump(data_deaths_today, write_data)
    copy2(
        "data/graph_data/graph_data_deaths_today.json",
        "website/static/graph_data_deaths_today.json",
    )

    with open("data/graph_data/graph_data_recovered.json", "w") as write_data:
        json.dump(data_recovered, write_data)
    copy2(
        "data/graph_data/graph_data_recovered.json",
        "website/static/graph_data_recovered.json",
    )

    with open("data/graph_data/graph_data_recovered_today.json", "w") as write_data:
        json.dump(data_recovered_today, write_data)
    copy2(
        "data/graph_data/graph_data_recovered_today.json",
        "website/static/graph_data_recovered_today.json",
    )

    with open("data/graph_data/graph_data_cases_log.json", "w") as write_data:
        json.dump(data_cases_log, write_data)
    copy2("data/graph_data/graph_data_cases_log.json",
          "website/static/graph_data_cases_log.json")

    with open("data/graph_data/graph_data_deaths_log.json", "w") as write_data:
        json.dump(data_deaths_log, write_data)
    copy2("data/graph_data/graph_data_deaths_log.json",
          "website/static/graph_data_deaths_log.json")

    with open("data/graph_data/graph_data_recovered_log.json", "w") as write_data:
        json.dump(data_recovered_log, write_data)
    copy2("data/graph_data/graph_data_recovered_log.json",
          "website/static/graph_data_recovered_log.json")


if __name__ == "__main__":
    generate_graph_data()
