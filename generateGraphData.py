"""
Generate JSON data for chartjs graphs.

Emile Villette - April 2021
"""
import datetime
import json
import os

from dateutil.parser import *


def generate_graph_data():
    with open("languages/countries.json", "r") as countries_file:
        countries_data = json.load(countries_file)

    data_cases = {}
    data_cases_today = {}
    data_deaths = {}
    data_deaths_today = {}
    data_recovered = {}
    data_recovered_today = {}

    for country in countries_data["iso_codes"]:
        data_cases[country] = []
        data_deaths[country] = []
        data_recovered[country] = []
        data_cases_today[country] = []
        data_deaths_today[country] = []
        data_recovered_today[country] = []

    for file in os.scandir("data"):
        try:
            if isinstance(parse(file.name), datetime.date):
                for country in countries_data["iso_codes"]:
                    try:
                        with open(
                            f"data/{file.name}/{country}.json", "r"
                        ) as current_country:
                            current_data = json.load(current_country)
                        data_cases_today[country].append(
                            current_data["todayCases"])
                        data_cases[country].append(current_data["cases"])
                        data_deaths_today[country].append(
                            current_data["todayDeaths"])
                        data_deaths[country].append(current_data["deaths"])
                        data_recovered_today[country].append(
                            current_data["todayRecovered"]
                        )
                        data_recovered[country].append(
                            current_data["recovered"])
                    except FileNotFoundError:
                        print(f"No file named {country}, skipped entry.")
        except ParserError as e:
            print(f"{e} (Skipped non datetime file).")

    # TODO: Make a copy of those files in website directory
    with open("data/graph_data/graph_data_cases.json", "w") as write_data:
        json.dump(data_cases, write_data)

    with open("data/graph_data/graph_data_cases_today.json", "w") as write_data:
        json.dump(data_cases_today, write_data)

    with open("data/graph_data/graph_data_deaths.json", "w") as write_data:
        json.dump(data_deaths, write_data)

    with open("data/graph_data/graph_data_deaths_today.json", "w") as write_data:
        json.dump(data_deaths_today, write_data)

    with open("data/graph_data/graph_data_recovered.json", "w") as write_data:
        json.dump(data_recovered, write_data)

    with open("data/graph_data/graph_data_recovered_today.json", "w") as write_data:
        json.dump(data_recovered_today, write_data)


if __name__ == "__main__":
    generate_graph_data()
