#!/usr/bin/env python3

"""
Sends email to unique mails, NOT meant for mass email sending.

Emile Villette - March 2021
"""
import json

import yagmail

import translator


def send_email(language, subject, content, sender, recipient):
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

    new_content = (
            language_data["email_header"].format(
                recipient.split("@")[0]) + "\n" + content
    )

    translated_content = translator.trans(new_content, "en", language)
    print(translated_content)

    with yagmail.SMTP(sender) as yag:
        pass
        yag.send(recipient, subject, translated_content)
    yag.close()
