user = "felix.gaudin@gmail.com"
if "." in user[:-3]:
    name = user.split("@")[0]
    namelst = name.split(".")
    name = ""
    for element in namelst:
        name += element.capitalize() + " "
else:
    name = user.split("@")[0]
    name = name.capitalize()
print(name)