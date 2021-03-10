#!/usr/bin/env python3

"""
Sends email to unique mails, NOT meant for mass email sending.

Emile Villette - March 2021
"""
import yagmail


def send_email(subject, content, sender, recipient):
    new_content = "Chèr(e) {},\n Voici votre récap quotidien sur la situation pandémique dans les pays que vous avez " \
                  "demandés:\n".format(recipient.split("@")[0]) + content
    with yagmail.SMTP(sender) as yag:
        yag.send(recipient, subject, new_content)
    yag.close()
