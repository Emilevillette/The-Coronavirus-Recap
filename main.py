#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""

from Downloader import download_stats
from recap_generator_fr import generate_recap
from emailSender import send_email
from datetime import date

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
    ["CL", "Chili"]
]

if __name__ == "__main__":
    path = download_stats(countries_to_track) + "/"
    recap_fr = generate_recap("FR", "AA_Daily_recap.coviddata", path, countries_to_track, 'AA_DAILY_TOTAL.coviddata')
    print(recap_fr)
    # send_email("Recap Coronavirus " + str(date.today()), recap_fr, 'coronarecap@gmail.com',
    #           'aurore.idee@gmail.com')
