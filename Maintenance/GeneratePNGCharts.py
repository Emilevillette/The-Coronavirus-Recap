"""
Generate PNG graphs for emails.

Emile Villette - April 2021
"""
import js2py
from datetime import date
import os


def generate_data(cases=(False, 0), deaths=(False, 0), recovered=(False, 0), cases_per_100k=(False, 0),
                  deaths_per_100k=(False, 0), recovered_per_100k=(False, 0)):
    today = date.today()
    if today not in os.listdir("../data/"):
        raise FileNotFoundError(f"NO DIRECTORY FOR date '{today}'.")
    else:
        with open(f"data/{today}/AA_RawDataProcessed.json", "r") as data_file:
            data = data_file.read()
        if cases[0]:
            top_cases = [["Country", 0]] * cases[1]
            for country in data:
                tmp_cases = country["todayCases"]
                if tmp_cases > top_cases[0][1]:
                    for top in range(1, len(top_cases) + 1):
                        if top == len(top_cases) + 1:
                            top_cases[-1] = [country["country"], tmp_cases]

                        if tmp_cases > top_cases[top][1]:
                            pass
                        elif tmp_cases <= top_cases[top][1]:
                            top_cases[top - 1] = [country["country"], tmp_cases]
