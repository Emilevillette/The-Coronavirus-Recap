#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""
import json
import os
import time
from datetime import date

from Downloader import download_stats
from emailSender import send_email
from recap_generator import generate_recap


def main_function(test=True):
    download_stats(yesterday=True)
    path = download_stats() + "/"

    for file in os.scandir("User_data/Users"):
        with open(file, "r") as user:
            data = json.load(user)
        recap = generate_recap(
            "AA_RawDataProcessed.json", path, data["preferences"], "AA_DAILY_TOTAL.json", test_mode=False
        )
        check_for_abortion = send_email(
            data["language"],
            "Recap Coronavirus " + str(date.today()),
            recap,
            "coronarecap@gmail.com",
            data["email"],
            path,
            test_mode=test,
        )
        if check_for_abortion == "Aborted":
            break
        time.sleep(0.5)


if __name__ == "__main__":
    main_function(test=True)
