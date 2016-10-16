import json

file = open("data.json", "r")
jsonString = ""
for line in file:
    jsonString += line

jsonFile = json.loads(jsonString)

