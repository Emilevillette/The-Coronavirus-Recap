#!/usr/bin/env python3

"""
create directory every day named "aaaa-mm-jj"

Emile Villette - March 2021
"""
import os
from datetime import date


def daily_directory(path=""):
    """Creates a directory named "aaaa-mm-jj" in /data/aaaa-mm-jj

    :param path: a string specifying the path where to create the daily path (defaults as ../data/aaaa-mm-jj
    :return: the path (as a string)
    """
    today = path + 'data/' + str(date.today())

    if not os.path.exists(today):
        os.makedirs(today)
    return today
