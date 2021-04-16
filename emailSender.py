#!/usr/bin/env python3

"""
Sends email to unique mails, NOT meant for mass email sending.

Emile Villette - March 2021
"""
import json
import os

import yagmail

import translator


def send_email(
    language,
    subject,
    content,
    sender,
    recipient,
    path,
    oauth2_userfile,
    first_email=False,
    test_mode=False,
):
    """Send an email through Gmail.

    :param first_email: is this the first email?
    :param oauth2_userfile: file with OAUTH2 google information. See Yagmail doc for more info.
    :param path: path where the data is stored
    :param test_mode: if set to True, doesn't send emails
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
            mail_data = {"mails_sent": False}

    new_content = (
        language_data["email_header"].format(
            recipient.split("@")[0]) + "\n" + content
    )

    translated_content = translator.trans(new_content, "en", language)
    print(translated_content)

    if not test_mode:
        with yagmail.SMTP(sender, oauth2_file=oauth2_userfile) as yag:
            if mail_data["mails_sent"]:
                if first_email:
                    print(
                        "WARNING : E-mails have already been sent today but test mode is disabled, please confirm "
                        "before proceeding."
                    )
                    confirmation = input(
                        "Write 'yes' to proceed (type anything else to cancel) > "
                    )
                else:
                    confirmation = "yes"
                if confirmation == "yes":
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
