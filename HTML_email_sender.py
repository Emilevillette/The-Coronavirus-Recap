from translator import trans
from datetime import date

def sendHTMLemail(language, user):
    email = ""
    with open("email/email0.html", "r") as styles:
        email += styles.read()
    with open("email/email1.html", "r") as header:
        header_data = header.read()

    newsletter = trans("Daily Corona Recap newsletter", "en", language)
    browser = trans("View in browser", "en", language)
    title = f"Corona recap {date.today()}"
    greeting = trans(f"Hello, {user.split('@')[0]}", "en", language)
    introduction = trans("Here is your daily COVID-19 recap (according to your chosen countries):", "en", "fr")

    email += header_data.format(newsletter, browser, title, greeting, introduction)

if __name__=="__main__":
    sendHTMLemail("fr", "emilevillette@hotmail.fr")
