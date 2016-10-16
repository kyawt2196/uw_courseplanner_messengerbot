import json
from pymongo import MongoClient

client = MongoClient("mongodb://straw:berry@ds031965.mlab.com:31965/mixfruitdb")

file = open("data.json", "r")
jsonString = ""
for line in file:
    jsonString += line

jsonFile = json.loads(jsonString)

db = client.courses

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
    for classList in jsonFile[dept]:
        for className in classList:
            for attr in className:
                if (attr == 'meetings'):
                    if (len(attr) == 1):

                        start = 'to be arranged'
                        end = 'to be arranged'
                        days = 'to be arranged'
                        instructor = 'to be arranged'
                        link = 'to be arranged'
                    else:
                        start = attr['start']
                        end = attr['end']
                        days = attr['day']
                        link = 'to be arranged'

                if (attr == 'status'):
                    if (className[attr] == ''):
                        isOpen = False
                    else:
                        isOpen = True
                
                if (attr == 'major'):
                    prefix = className[attr]

                if (attr == 'SLN'):
                    sln = className[attr]

                if (attr == 'professor'):
                    instructor = className[attr]

                if (attr == 'courseName'):
                    nameOfclassName = className[attr]

                if (attr == 'courseName'):
                    number = className[attr]

                isSection = True
                isWriting = False
            
            result = db.insert_one(
                {'sln':sln, 'prefix':prefix, 'number':number, 'nameOfclassName':nameOfclassName, 
                'days':days, 'start':start, 'end':end, 'isSection':isSection, 'instructor':instructor, 
                'isOpen':isOpen, 'generalEd':generalEd, 'isWriting':isWriting, 'link':link}
            )

            print(result)

