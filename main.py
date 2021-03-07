"""
Emile Villette - October 2020
Automatic daily email updates on the COVID-19 situation in Belgium
"""

import dailyDirectory
import downloadFile

# Get daily file path
path = dailyDirectory.daily_directory()
print(path)

#rows_to_skip
# Download today's files from https://corona.lmao.ninja/v2/countries?yesterday&sort
# Confirmed cases by date, age, sex and province
downloadFile.download_file('https://corona.lmao.ninja/v2/countries?yesterday&sort', 'RAW_DATA',
                           path)

