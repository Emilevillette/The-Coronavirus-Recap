"""
Emile Villette - October 2020

Parse csv file into a python dictionary
"""
import pandas
import binarySearch


def read_csv(path, category, date, rows_to_skip):
    path = path + "/" + category + ".csv"
    with open(path) as csv_file:
        data = pandas.read_csv(csv_file, parse_dates=True)
        # print(data)
        for i in (data['DATE']):
            if i=="2020-03-03":
                print(type(i))


read_csv('data/2020-10-17', 'COVID19BE_CASES_AGESEX', '2020-03-01', 30053)
