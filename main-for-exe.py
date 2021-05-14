#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily emaildata updates on the COVID-19 situation in Belgium
"""
import json
import os
import time

from Downloader import download_stats
from HTML_email_sender import send_HTML_email
from recap_generator import generate_recap
from generateGraphData import generate_graph_data


def main_function(test=True):
    download_stats(yesterday=True)
    path = download_stats() + "/"
    # generate_graph_data()

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

        send_HTML_email(data["language"], data["email"], recap, "coronarecap@gmail.com", test_mode=test)

        print(
            """
        ---------------------------------------------------------
        """
        )
        time.sleep(0.5)


if __name__ == "__main__":
    main_function(test=False)
