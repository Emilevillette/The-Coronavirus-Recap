"""
Translate a text using Google Translate

Emile Villette - March 2021
"""
# IMPORTANT, AS OF 16/03/2021 you have to use VERSION 3.1.0a or the api won't be functional. Install it with
# pip install googletrans==3.1.0a BE CAREFUL, version 4 rc1 HAS A CRITICAL BUG
import googletrans


def trans(text, origin_lan, target_lan):
    """Translates text.

    :param text: text to translate
    :param origin_lan: text's language
    :param target_lan: target language
    :return: translated text
    """
    transl = googletrans.Translator()
    return transl.translate(text, dest=target_lan, src=origin_lan).text
