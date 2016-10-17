import json
from pymongo import MongoClient

client = MongoClient("mongodb://straw:berry@ds031965.mlab.com:31965/mixfruitdb")

file = open("data.json", "r")
jsonString = ""
for line in file:
    jsonString += line

jsonFile = json.loads(jsonString)

collection = client.mixfruitdb.courses

isOpen = ''
sln = ''
prefix = ''
number = ''
nameOfclassName = ''
days = ''
start = ''
end = ''
isSection = ''
instructor = ''
generalEd = ''
isWriting = ''
link = ''

for dept in jsonFile:
    for classObj in jsonFile[dept]:
        # class object is another dictionary
        for attr in classObj:
            if (attr == 'meetings'):
                if ('to be arranged' in classObj[attr]):
                    start = 'to be arranged'
                    end = 'to be arranged'
                    days = 'to be arranged'
                    instructor = 'to be arranged'
                    link = 'to be arranged'
                else:
                    start = classObj[attr]['start']
                    end = classObj[attr]['end']
                    days = classObj[attr]['day']
                    link = 'to be arranged'

            if (attr == 'status'):
                if (classObj[attr] == ''):
                    isOpen = False
                else:
                    isOpen = True

            if (attr == 'major'):
                prefix = classObj[attr]

            if (attr == 'SLN'):
                sln = int(classObj[attr])

            if (attr == 'professor'):
                instructor = classObj[attr]

            if (attr == 'courseName'):
                nameOfclassName = classObj[attr]

            if (attr == 'courseNumber'):
                number = int(classObj[attr])

            isSection = True
            isWriting = False

        result = collection.insert_one(
            {'sln':sln, 'prefix':prefix, 'number':number, 'nameOfclassName':nameOfclassName,
            'days':days, 'start':start, 'end':end, 'isSection':isSection, 'instructor':instructor,
            'isOpen':isOpen, 'generalEd':generalEd, 'isWriting':isWriting, 'link':link}
        )

        print(result)

