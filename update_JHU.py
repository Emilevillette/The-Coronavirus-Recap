"""
Pull data from the John Hopkins University GitHub - https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data

Emile Villette - March 2021
"""
import downloadFile
import pandas
from datetime import timedelta, datetime
from dateutil.parser import parse
import directoryManager
import json
import os
import progressbar


def update_raw():
    def match_country_info() -> dict:
        with open("data/2021-03-31/AA_RawDataProcessed.json", "r") as reference_file:
            reference_data = json.load(reference_file)
        # print(reference_data[current_data["countryInfo"]["iso2"]], current_data["countryInfo"]["iso2"])
        current_data["country"] = cases["Country/Region"][j]
        current_data["countryInfo"]["iso2"] = str(
            countries_info["inverted_couples"][cases["Country/Region"][j]])
        current_data["countryInfo"][
            'flag'] = f"""https://disease.sh/assets/img/flags/{current_data["countryInfo"]["iso2"]}.png"""
        current_data["countryInfo"]["lat"] = str(cases["Lat"][j])
        current_data["countryInfo"]["long"] = str(cases["Long"][j])
        current_data["countryInfo"]["iso3"] = reference_data[current_data["countryInfo"]["iso2"]]["countryInfo"]["iso3"]
        current_data["countryInfo"]["_id"] = reference_data[current_data["countryInfo"]["iso2"]]["countryInfo"]["_id"]
        current_data["population"] = reference_data[current_data["countryInfo"]["iso2"]]["population"]
        current_data["continent"] = reference_data[current_data["countryInfo"]["iso2"]]["continent"]
        return current_data

    downloadFile.download_file(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
        ".csv", "JHU_time_series_cases", "data/JHU_DATA/")
    downloadFile.download_file(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
        ".csv", "JHU_time_series_deaths", "data/JHU_DATA/")
    downloadFile.download_file(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
        ".csv", "JHU_time_series_recovered", "data/JHU_DATA/")

    with open('languages/countries.json', "r") as countries_file:
        countries_info = json.load(countries_file)

    cases = pandas.read_csv("data/JHU_DATA/JHU_time_series_cases.csv")
    deaths = pandas.read_csv("data/JHU_DATA/JHU_time_series_deaths.csv")
    recovered = pandas.read_csv("data/JHU_DATA/JHU_time_series_recovered.csv")

    example = {"updated": 0, "country": "country_full_name",
               "countryInfo": {"_id": 0, "iso2": "CY", "iso3": "CTY", "lat": 0, "long": 0,
                               "flag": "https://disease.sh/assets/img/flags/CT.png"}, "cases": 0, "todayCases": 0,
               "deaths": 0, "todayDeaths": 0, "recovered": 0, "todayRecovered": 0, "active": 0, "critical": 0,
               "casesPerOneMillion": 0, "deathsPerOneMillion": 0, "tests": 0, "testsPerOneMillion": 0, "population": 0,
               "continent": "continent", "oneCasePerPeople": 0, "oneDeathPerPeople": 0, "oneTestPerPeople": 0,
               "activePerOneMillion": 0, "recoveredPerOneMillion": 0, "criticalPerOneMillion": 0}

    progress_widgets = [
        progressbar.FormatLabel(""),
        progressbar.Percentage(),
        " ",
        progressbar.Bar(marker="█", left="[", right="]", fill="░"),
        " ",
        progressbar.AdaptiveETA(),
    ]

    for progression in progressbar.progressbar(range(4, len(cases.columns.values[4:-14])), widgets=progress_widgets):
        i = cases.columns.values[progression]

        directoryManager.daily_directory(choose_date=parse(i).date())
        for j in range(len(cases)):
            if cases["Country/Region"][j] not in countries_info["EN"]:
                continue
            elif os.path.isfile(
                    f"""data/{parse(i).date()}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json"""):
                with open(
                        f"""data/{parse(i).date()}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json""",
                        "r") as current_country:
                    current_data = json.load(current_country)
                progress_widgets[0] = progressbar.FormatLabel(f"{i}: ")
                current_data["updated"] = unix_time_millis(parse(i))
                current_data["cases"] += int(cases[i][j])
                current_data["deaths"] += int(deaths[i][j])
                try:
                    current_data["recovered"] += int(recovered[i][j])
                except KeyError:
                    pass
                try:
                    with open(
                            f"""data/{str(parse(i).date() - timedelta(days=1))}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json""",
                            "r") as yesterday_file:
                        yesterday_data = json.load(yesterday_file)

                    current_data["todayCases"] = current_data["cases"] - yesterday_data["cases"]
                    current_data["todayDeaths"] = current_data["deaths"] - yesterday_data["deaths"]
                    current_data["todayRecovered"] = current_data["recovered"] - yesterday_data["recovered"]
                except FileNotFoundError:
                    current_data["todayCases"] = 0
                    current_data["todayDeaths"] = 0
                    current_data["todayRecovered"] = 0
                current_data = match_country_info()
                current_data["casesPerOneMillion"] = (current_data["cases"] / current_data["population"]) * 1000000
                if current_data["cases"] != 0:
                    current_data["casesPerOneMillion"] = (current_data["cases"] / current_data["population"]) * 1000000
                    current_data["oneCasePerPeople"] = int(round(current_data["population"] / current_data["cases"]))
                if current_data["deaths"] != 0:
                    current_data["deathsPerOneMillion"] = (current_data["deaths"] / current_data[
                        "population"]) * 1000000
                    current_data["oneDeathPerPeople"] = int(round(current_data["population"] / current_data["deaths"]))
                current_data["recoveredPerOneMillion"] = (current_data["recovered"] / current_data[
                    "population"]) * 1000000
                with open(
                        f"""data/{parse(i).date()}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json""",
                        "w") as current_country2:
                    json.dump(current_data, current_country2)

                with open(
                        f"""data/{parse(i).date()}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json""",
                        'w') as new_country:
                    json.dump(current_data, new_country)
            else:
                current_data = example.copy()
                progress_widgets[0] = progressbar.FormatLabel(f"{i}: ")
                current_data["updated"] = unix_time_millis(parse(i))
                current_data["cases"] = int(cases[i][j])
                current_data["deaths"] = int(deaths[i][j])

                try:
                    current_data["recovered"] = int(recovered[i][j])
                except KeyError:
                    current_data["recovered"] = 0

                try:
                    with open(
                            f"""data/{str(parse(i).date() - timedelta(days=1))}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json""",
                            "r") as yesterday_file:
                        yesterday_data = json.load(yesterday_file)
                    current_data["todayCases"] = current_data["cases"] - yesterday_data["cases"]
                    current_data["todayDeaths"] = current_data["deaths"] - yesterday_data["deaths"]
                    current_data["todayRecovered"] = current_data["recovered"] - yesterday_data["recovered"]
                except FileNotFoundError:
                    current_data["todayCases"] = 0
                    current_data["todayDeaths"] = 0
                    current_data["todayRecovered"] = 0
                current_data = match_country_info()
                if current_data["cases"] != 0:
                    current_data["casesPerOneMillion"] = (current_data["cases"] / current_data["population"]) * 1000000
                    current_data["oneCasePerPeople"] = int(round(current_data["population"] / current_data["cases"]))
                if current_data["deaths"] != 0:
                    current_data["deathsPerOneMillion"] = (current_data["deaths"] / current_data[
                        "population"]) * 1000000
                    current_data["oneDeathPerPeople"] = int(round(current_data["population"] / current_data["deaths"]))
                current_data["recoveredPerOneMillion"] = (current_data["recovered"] / current_data[
                    "population"]) * 1000000
                with open(
                        f"""data/{parse(i).date()}/{countries_info["inverted_couples"][cases["Country/Region"][j]]}.json""",
                        "w") as current_country2:
                    json.dump(current_data, current_country2)


def unix_time_millis(dt):
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000.0)


if __name__ == "__main__":
    update_raw()
