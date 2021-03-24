"""
Add a user into the database and generate a unique UUID.

Emile Villette - March 2021
"""

import json
import os
import uuid


def add_user_in_db(email, language, preferences_countries):
    user_unique_id = uuid.uuid5(uuid.NAMESPACE_URL, email)
    path = "{}/{}.json".format("Users", user_unique_id)

    if os.path.isfile(path):
        return "E-mail already registered, please log in to modify preferences"
    with open(path, "w") as user:
        with open("exampleuserfile/userdata.json", "r") as template_file:
            template = json.load(template_file)

        template["uuid"], template["email"], template["language"] = (
            str(user_unique_id),
            email,
            language,
        )
        # USER PREFERENCES ENCODING TBI
        template["preferences"]["countries"] = preferences_countries

        user.write(str(template).replace("'", '"'))

        return True
