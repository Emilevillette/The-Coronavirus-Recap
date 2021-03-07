#!/usr/bin/env python3

"""
Sends email to unique mails, NOT meant for mass email sending.

Emile Villette - March 2021
"""
import yagmail


def send_email(subject, content, sender, recipient, OAUTH2):
    yag = yagmail.SMTP(sender, oauth2_file=OAUTH2)

    with yag:
        yag.send(recipient, subject, content)
