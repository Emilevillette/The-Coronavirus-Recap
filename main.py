#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""
from datetime import date

from Downloader import download_stats
from emailSender import send_email
from recap_generator import generate_recap
from translator import trans

countries_to_track = [
    ["IT", "Italie"],
    ["ES", "Espagne"],
    ["FR", "France"],
    ["BE", "Belgique"],
    ["US", "Etats-Unis"],
    ["CA", "Canada"],
    ["UK", "Royaume-Uni"],
    ["NL", "Pays-Bas"],
    ["DE", "Allemagne"],
    ["PT", "Portugal"],
    ["LU", "Luxembourg"],
    ["IN", "Inde"],
    ["BR", "Brésil"],
    ["ZA", "Afrique du sud"],
    ["MA", "Morocco"],
    ["PL", "Pologne"],
    ["CH", "Suisse"],
    ["DK", "Danemark"],
    ["SE", "Suède"],
    ["MX", "Mexique"],
    ["AT", "Austria"],
    ["GR", "Grèce"],
    ["IL", "Israel"],
    ["TR", "Turquie"],
    ["IR", "Iran"],
    ["CO", "Colombie"],
    ["PE", "Pérou"],
    ["RO", "Roumanie"],
    ["UA", "Ukraine"],
    ["CL", "Chili"],
]

if __name__ == "__main__":
    download_stats(countries_to_track, yesterday=True)
    path = download_stats(countries_to_track) + "/"
    recap = generate_recap(
        "FR", "AA_Daily_recap.json", path, countries_to_track, "AA_DAILY_TOTAL.json"
    )
    print(recap)
    # send_email("FR", "Recap Coronavirus " + str(date.today()), recap, 'coronarecap@gmail.com',
    #           'aurore.idee@gmail.com')
