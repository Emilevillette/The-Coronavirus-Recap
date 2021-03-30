# The Coronavirus Recap

Coronavirus Tracker using the **disease.sh** API. \
Data sourced from Worldometers and the European Center for Disease Control (CEDC)

## What is the Coronavirus Recap?

The Coronavirus Recap is a backend and frontend tool that aims to provide customized analytics for the COVID-19
pandemic.

## Features

- A daily mailing list that provides a given country set's Covid-related cases, deaths, critical patients and vaccination numbers
- Translation of the above-mentioned content in any language using the googletrans API
- **OAUTH2** authentication with Google Gmail and the Python Yagmail library. **No need** to _"Enable less secure apps"_!
- A database of the users where each user is referred to with a **UUID5** generated from its email address. **No information is kept** except the E-mail and the user's preferences.
- Logging of each country's Daily Covid information. Updated multiple times a day.

## Requirements
- Python 3.9 (might work for older versions of Python but this hasn't been tested)
- Python's package installer pip
- The Python Yagmail library: ``pip install yagmail``
- The Python Googletrans library (**NOTE**: as of March 2021, you MUST install Googletrans version **3.0.1a**, older versions have a critical bug preventing this project from functioning normally): ``pip install googletrans==3.0.1a``

