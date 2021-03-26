#!/usr/bin/env python3

"""
Sends email to unique mails, NOT meant for mass email sending.

Emile Villette - March 2021
"""
import json
import os

import yagmail

import translator


def send_email(language, subject, content, sender, recipient, path, test_mode=False):
    """Send an email.

    :param language: user's preferred language (ISO code, string)
    :param subject: Email subject
    :param content: Email content
    :param sender: sender email
    :param recipient: receiver email
    :return: None
    """
    with open("languages/en.json", "r", encoding="utf-8") as language_file:
        language_data = json.load(language_file)

    if os.path.exists(path + "AA_mails_sent.json"):
        with open(path + "AA_mails_sent.json", "r") as mail_file:
            mail_data = json.load(mail_file)
    else:
        with open(path + "AA_mails_sent.json", "w") as mail_file:
            json.dump({"mails_sent": False}, mail_file)

    new_content = (
        language_data["email_header"].format(
            recipient.split("@")[0]) + "\n" + content
    )

    translated_content = translator.trans(new_content, "en", language)
    print(translated_content)

    with yagmail.SMTP(sender) as yag:
        if test_mode:
            pass
        else:
            if mail_data["mails_sent"]:
                print(
                    "/!\ WARNING /!\ : E-mails have already been sent today but test mode is disabled, please confirm before proceeding."
                )
                confirmation = input(
                    "Write 'yes' to proceed (type anything else to cancel) ? > "
                )
                if confirmation == "Yes":
                    with open(path + "AA_mails_sent.json", "w") as log_mails_sent:
                        json.dump({"mails_sent": True}, log_mails_sent)
                    yag.send(recipient, subject, translated_content)
                else:
                    print("Email sending canceled by user: operation aborted")
                    return "Aborted"
            else:
                with open(path + "AA_mails_sent.json", "w") as log_mails_sent:
                    json.dump({"mails_sent": True}, log_mails_sent)
                yag.send(recipient, subject, translated_content)
    yag.close()
