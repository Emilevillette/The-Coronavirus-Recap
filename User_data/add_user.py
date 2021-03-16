"""
Add a user into the database and generate a unique UUID.

Emile Villette - March 2021
"""

import uuid
import json
import os


# from user_settings import modify_user


def add_user_in_db(email, language, preferences):
    user_unique_id = uuid.uuid5(uuid.NAMESPACE_URL, email)
    path = "{}/{}.json".format("Users", user_unique_id)

    if os.path.isfile(path):
        return "E-mail already registered, please log in to modify preferences"
    else:
        with open(path, "w") as user:
            with open("exampleuserfile/userdata.json", "r") as template_file:
                template = json.load(template_file)

            template["uuid"], template["email"], template["language"] = str(user_unique_id), email, language
            # USER PREFERENCES ENCODING TBI
            user.write(str(template))

            return True
