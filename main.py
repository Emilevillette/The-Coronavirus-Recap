"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""

import dailyDirectory
import downloadFile

# Get daily file path
path = dailyDirectory.daily_directory()
print(path)

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

# Download today's files from https://corona.lmao.ninja/v2/countries?yesterday&sort
downloadFile.download_file('https://corona.lmao.ninja/v2/countries?yesterday&sort', 'AA_RawData', path)

for country in countries_to_track:
    downloadFile.download_file('https://corona.lmao.ninja/v2/countries/' + country[0] + "?yesterday", country[0], path)
