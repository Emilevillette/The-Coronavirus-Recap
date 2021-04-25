from translator import trans
from datetime import date

import gmail_sender


def send_HTML_email(language, user, recap, sender, test_mode=False):
    email = ""
    with open("emaildata/email0.html", "r", encoding="UTF-8") as styles:
        email += styles.read()
    with open("emaildata/email1.html", "r", encoding="UTF-8") as header:
        header_data = header.read()
    with open("emaildata/email4.html", "r", encoding="UTF-8") as footer:
        footer_data = footer.read()

    to_be_translated = []

    newsletter = "Daily newsletter"
    browser = "View in browser"
    title = f"{date.today()}"
    name = user.split("@")[0]
    if "." in name:
        name = name.replace(".", " ").capitalize()
    else:
        name = name.capitalize()
    greeting = f"Hello, {name}"
    introduction = "Here is your daily COVID-19 recap (according to your chosen countries):"

    to_be_translated.append(newsletter)
    to_be_translated.append(browser)
    to_be_translated.append(title)
    to_be_translated.append(greeting)
    to_be_translated.append(introduction)

    email_without_css = ""
    email_without_css += header_data
    email_without_css += recap
    email_without_css += footer_data

    to_be_translated.append("Thank you!")
    to_be_translated.append(
        "Thank you for trusting The Corona Recap and beta testing it. Since I work all on my own, I make slow but "
        "steady progress. Please contact me if you have suggestions (French/English only).")
    to_be_translated.append("Emile Villette, founder")
    to_be_translated.append("Contact me")
    to_be_translated.append("Email:")

    translation_raw = ""
    for element in range(len(to_be_translated)):
        to_be_translated[element] = to_be_translated[element].replace("\n", "")
        translation_raw += to_be_translated[element] + "\n"

    translated = trans(translation_raw, "en", language).split("\n")
    email_without_css = email_without_css.format(*translated)
    email += email_without_css

    print(email)
    if not test_mode:
        gmail_sender.send_email(sender, user, f"Corona Recap {date.today()}", email)
