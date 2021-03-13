#!/usr/bin/env python3

"""
create directory every day named "aaaa-mm-jj"

Emile Villette - March 2021
"""
import os
from datetime import date, timedelta


def daily_directory(path="", yesterday=False):
    """Creates a directory named "aaaa-mm-jj" in /data/aaaa-mm-jj

    :param yesterday: return yesterday's path
    :param path: a string specifying the path where to create the daily path (defaults as ../data/aaaa-mm-jj
    :return: the path (as a string)
    """
    if yesterday:
        today = path + 'data/' + str(date.today() - timedelta(days=1))
    else:
        today = path + 'data/' + str(date.today())

    if not os.path.exists(today):
        # Create main folder
        os.makedirs(today)
        # Create vaccine sub-folder
        os.makedirs(today + "/vaccine")
    return today


def create_directory(path):
    """Create a directory

    :param path: directory path
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path)
