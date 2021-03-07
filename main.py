#!/usr/bin/env python3

"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""

import Downloader as dl
import recap_generator_fr as rgfr
import email_sender as email

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
    path = dl.download_stats(countries_to_track) + "/"
    recap_fr = rgfr.generate_recap("AA_Daily_recap.coviddata", path, countries_to_track)
    email.send_email("test", 'TRESDKLSJ', 'coronarecap@gmail.com', 'emilevillette@hotmail.fr', 'code_secret_client_247411167392-5qlr4h1jamrt1im9doekjlc032birac9.apps.googleusercontent.com.json')