"""
Add a user into the database and generate a unique UUID.

Emile Villette - March 2021
"""

import uuid
import json
import os
from user_settings import modify_user


def add_user_in_db(email, preferences):
    user_unique_id = uuid.uuid5(uuid.NAMESPACE_URL, email)

    if os.path.isfile('./{0}.json'.format(str(user_unique_id))):
        pass
    else:
        with open("userdata.json", "w") as file:
            data = json.load(file)
