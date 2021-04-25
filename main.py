#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily emaildata updates on the COVID-19 situation in Belgium
"""
import json
import os
import time
from datetime import date

from Downloader import download_stats
from HTML_email_sender import send_HTML_email
from recap_generator import generate_recap


def main_function(test=True):
    download_stats(yesterday=True)
    path = download_stats() + "/"

    files = os.listdir("User_data/Users")

    for file in files:
        with open("User_data/Users/" + file, "r") as user:
            data = json.load(user)

        recap = generate_recap(
            "AA_RawDataProcessed.json",
            path,
            data["preferences"],
            "AA_DAILY_TOTAL.json",
            data["yesterday_missing"],
            data["uuid"],
            data["language"],
            test_mode=False,
        )

        if file == files[0]:
            first_email = True
        else:
            first_email = False

        send_HTML_email(data["language"], data["email"], recap, "coronarecap@gmail.com", test_mode=test)

        print(
            """
        ---------------------------------------------------------
        """
        )
        time.sleep(0.5)


if __name__ == "__main__":
    while True:
        test = input("Test mode (True or False)? >")
        if test in ["True", "true"]:
            test = True
            break
        elif test in ["False", "false"]:
            test = False
            break
        else:
            print("Invalid entry, try again")

    main_function(test=test)
