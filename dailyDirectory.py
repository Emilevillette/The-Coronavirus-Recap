#!/usr/bin/env python3

"""
create directory everyday named "aaaa-mm-jj"
"""
import os
from datetime import date


def daily_directory():
    today = 'data/' + str(date.today())

    if not os.path.exists(today):
        os.makedirs(today)
    return today
