#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""
import json
import os
from datetime import date
import time

from Downloader import download_stats
from emailSender import send_email
from recap_generator import generate_recap

if __name__ == "__main__":
    download_stats(yesterday=True)
    path = download_stats() + "/"

    for file in os.scandir("User_data/Users"):
        with open(file, "r") as user:
            data = json.load(user)
        recap = generate_recap(
            "AA_RawDataProcessed.json", path, data["preferences"], "AA_DAILY_TOTAL.json"
        )
        send_email(
            data["language"],
            "Recap Coronavirus " + str(date.today()),
            recap,
            "coronarecap@gmail.com",
            data["email"],
            test_mode=True
        )
        time.sleep(0.5)
