#!/usr/bin/env python3

"""
create directory every day named "aaaa-mm-jj"

Emile Villette - March 2021
"""
import os
from datetime import date, timedelta


def daily_directory(path="", yesterday=False, choose_date=date.today()):
    """Creates a directory named "aaaa-mm-jj" in /data/aaaa-mm-jj.

    :param choose_date: choose the date (datetime)
    :param yesterday: return yesterday's path
    :param path: a string specifying the path where to create the daily path (defaults as ../data/aaaa-mm-jj
    :return: the path (as a string)
    """
    if yesterday:
        today = path + "data/" + str(choose_date.today() - timedelta(days=1))
    elif choose_date:
        today = path + "data/" + str(choose_date)
    else:
        today = path + "data/" + str(choose_date.today())

    if not os.path.exists(today):
        # Create main folder
        os.makedirs(today)
        # Create vaccine sub-folder
        os.makedirs(today + "/vaccine")
    return today
