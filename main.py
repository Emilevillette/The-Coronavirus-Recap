#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""
from translator import trans
from Downloader import download_stats
from recap_generator import generate_recap
from emailSender import send_email
from datetime import date

countries_to_track = [
    ["IT", "Italy"],
    ["ES", "Spain"],
    ["FR", "France"],
    ["BE", "Belgium"],
    ["US", "United States"],
    ["CA", "Canada"],
    ["UK", "United Kingdoms"],
    ["NL", "The Netherlands"],
    ["DE", "Germany"],
    ["PT", "Portugal"],
    ["LU", "Luxembourg"],
    ["IN", "India"],
    ["BR", "Brazil"],
    ["ZA", "South Africa"],
    ["MA", "Morocco"],
    ["PL", "Poland"],
    ["CH", "Switzerland"],
    ["DK", "Denmark"],
    ["SE", "Sweden"],
    ["MX", "Mexico"],
    ["AT", "Austria"],
    ["GR", "Greece"],
    ["IL", "Israel"],
    ["TR", "Turkey"],
    ["IR", "Iran"],
    ["CO", "Colombia"],
    ["PE", "Peru"],
    ["RO", "Romania"],
    ["UA", "Ukraine"],
    ["CL", "Chili"]
]

if __name__ == "__main__":
    download_stats(countries_to_track, yesterday=True)
    path = download_stats(countries_to_track) + "/"
    recap = generate_recap("AA_Daily_recap.json", path, countries_to_track, 'AA_DAILY_TOTAL.json')
    send_email("fr", "Recap Coronavirus " + str(date.today()), recap, 'coronarecap@gmail.com',
               'aurore.idee@gmail.com')
