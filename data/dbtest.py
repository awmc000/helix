from data import dbApplication as db
import os

# If you are using this file, please run init.sql first as the tests require the ID's of the data it creates





# Connect/disconnect to database test
#Invlaid

try:
    database = db.connectToDatabase("DNA", "Dude5")
    db.disconnectFromDatabase(database)
except:
    print("\n\nTest1 Passed\n\n")



#valid
username = os.getenv("DBUSER")
password = os.getenv("DBPASS")

print(username, " ", password)

database = db.connectToDatabase(username, password)

print(database)

db.disconnectFromDatabase(database)

if(database):
    print("\n\nTest2 Passed\n\n")

# updateDatabase tests
#       createAuthor tests
database = db.connectToDatabase(username, password)

# Invalid Data
values = {}
if(not db.createAuthor(values, database)):
    print("\n\nTest3 Passed\n\n")

# Valid Data
values = {"username": "user", "name": "name", "authorDescription": "desc",  "emailAddress": "email"}
if(db.createAuthor(values, database)):
    print("\n\nTest4 Passed\n\n")

# Duplicate Data
if(not db.createAuthor(values, database)):
    print("\n\nTest5 Passed\n\n")

#       createCourse Tests
# Invalid FK reference
values = {"username": "username","courseName": "name","courseDescription": "desc"}
if(not db.createCourse(values, database)):
    print("\n\nTest6 Passed\n\n")

# Valid FK reference
values = {"username": "user","courseName": "name","courseDescription": "desc"}
if(db.createCourse(values, database)):
    print("\n\nTest7 Passed\n\n")

# Since Create _____ uses the same undelying code (updateDatabase) These are just testing the Sql statements
#       createQuiz Tests
values = {"courseID": 2,"quizName": "name","availableAsync": 1,"label": "label","quizDescription": "desc","durationMinutes": 9}
if(db.createQuiz(values, database)):
    print("\n\nTest8 Passed\n\n")

# retrieveFromDB tests
#       getQuizList Test

# Query With No Parameters
result = db.getQuizList(database)
if(result):
    print(result)
    print("\n\nTest9 Passed\n\n")

#       getQuizListFromAuthor Test
# Query With Parameters
values = ["user"]
result = db.getQuizListFromAuthor(values, database)
if(result):
    print(result)
    print("\n\nTest10 Passed\n\n")

# Invalid data
values = ["user", "idk"]
result = db.getQuizListFromAuthor(values, database)
if(not result):
    print("\n\nTest11 Passed\n\n")

#       getQuizListFromCourse Test

values = [2]
result = db.getQuizListFromCourse(values, database)
if(result):
    print(result)
    print("\n\nTest12 Passed\n\n")


# assembleQuiz Tests

# Assemble quiz with no questions
values = [1]
quiz = db.assembleQuiz(values, database)
if(not quiz):
    print("\n\nTest13 Passed\n\n")

#       createQuestion Tests
values = {"quizID": 1,"prompt": "(1) Is SelfNotAccept accepted by SelfNotAccept?","durationMinutes": 1,"durationSeconds": 0}
if(db.createQuestion(values, database)):
    print("\n\nTest14 Passed\n\n")

# Assemble quiz with a question but no answers
values = [1]
quiz = db.assembleQuiz(values, database)
if(not quiz):
    print("\n\nTest15 Passed\n\n")

#       CreateAnswerKey tests
values = {"questionID": 1,"optionNumber": 1,"optionDescription": "Yes","scoreValue": 0}
if(db.createAnswerKey(values, database)):
    print("\n\nTest16 Passed\n\n")

# Assemble a valid quiz (Albeit a stupid one as there is only one option)
values = [1]
quiz = db.assembleQuiz(values, database)
if(quiz):
    print(quiz)
    print("\n\nTest17 Passed\n\n")

# Quiz with question with multiple options
values = {"questionID": 1,"optionNumber": 2,"optionDescription": "No","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 1,"optionNumber": 3,"optionDescription": "undecidable","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 1,"optionNumber": 4,"optionDescription": "unrecognizable","scoreValue": 1}
db.createAnswerKey(values, database)

values = [1]
quiz = db.assembleQuiz(values, database)
if(quiz):
    print(quiz)
    print("\n\nTest18 Passed\n\n")

# Quiz with multiple questions with mutliple options
values = {"quizID": 1,"prompt": "(2) Is SelfNotAccept accepted by SelfNotAccept?","durationMinutes": 1,"durationSeconds": 0}
db.createQuestion(values, database)
values = {"quizID": 1,"prompt": "(3) Is SelfNotAccept accepted by SelfNotAccept?","durationMinutes": 1,"durationSeconds": 0}
db.createQuestion(values, database)
values = {"quizID": 1,"prompt": "(4) Is SelfNotAccept accepted by SelfNotAccept?","durationMinutes": 1,"durationSeconds": 0}
db.createQuestion(values, database)
values = {"quizID": 1,"prompt": "(5) Is SelfNotAccept accepted by SelfNotAccept?","durationMinutes": 1,"durationSeconds": 0}
db.createQuestion(values, database)

#   Q2
values = {"questionID": 2,"optionNumber": 1,"optionDescription": "Yes","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 2,"optionNumber": 2,"optionDescription": "No","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 2,"optionNumber": 3,"optionDescription": "undecidable","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 2,"optionNumber": 4,"optionDescription": "unrecognizable","scoreValue": 1}
db.createAnswerKey(values, database)

#   Q3
values = {"questionID": 3,"optionNumber": 1,"optionDescription": "Yes","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 3,"optionNumber": 2,"optionDescription": "No","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 3,"optionNumber": 3,"optionDescription": "undecidable","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 3,"optionNumber": 4,"optionDescription": "unrecognizable","scoreValue": 1}
db.createAnswerKey(values, database)

#   Q4
values = {"questionID": 4,"optionNumber": 1,"optionDescription": "Yes","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 4,"optionNumber": 2,"optionDescription": "No","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 4,"optionNumber": 3,"optionDescription": "undecidable","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 4,"optionNumber": 4,"optionDescription": "unrecognizable","scoreValue": 1}
db.createAnswerKey(values, database)

#   Q5
values = {"questionID": 5,"optionNumber": 1,"optionDescription": "Yes","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 5,"optionNumber": 2,"optionDescription": "No","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 5,"optionNumber": 3,"optionDescription": "undecidable","scoreValue": 0}
db.createAnswerKey(values, database)

values = {"questionID": 5,"optionNumber": 4,"optionDescription": "unrecognizable","scoreValue": 1}
db.createAnswerKey(values, database)

values = [1]
quiz = db.assembleQuiz(values, database)
if(quiz):
    print(quiz)
    print("\n\nTest19 Passed\n\n")

# Python to JSON
json = db.pythonToJSON(quiz)
if(json):
    print(quiz)
    print("\n\nTest20 Passed\n\n")

# JSON to Python
python = db.jsonToPython(json)
if(python):
    print(quiz)
    print("\n\nTest21 Passed\n\n")

# Process Answer Tests
# Valid data
values = {"questionID": 1, "optionNumber": 1}
if(db.processAnswer(values, database)):
    print("\n\nTest22 Passed\n\n")

# Invalid Question num
values = {"questionID": 8, "optionNumber": 1}
if(not db.processAnswer(values, database)):
    print("\n\nTest23 Passed\n\n")

# Invalid Question num
values = {"questionID": 1, "optionNumber": 9}
if(not db.processAnswer(values, database)):
    print("\n\nTest24 Passed\n\n")

# Create Analytics Tests
# Inserting Data
# Q1: 50% option 1 50% option 2
# Q2: 25% each
# Q3: 25% option 3 75% option 4
# Q4: 100% option 2
# Q5: 100% option 4

values = {"questionID": 1, "optionNumber": 1}
db.processAnswer(values, database)
values = {"questionID": 1, "optionNumber": 2}
db.processAnswer(values, database)
db.processAnswer(values, database)

values = {"questionID": 2, "optionNumber": 1}
db.processAnswer(values, database)
values = {"questionID": 2, "optionNumber": 2}
db.processAnswer(values, database)
values = {"questionID": 2, "optionNumber": 3}
db.processAnswer(values, database)
values = {"questionID": 2, "optionNumber": 4}
db.processAnswer(values, database)

values = {"questionID": 3, "optionNumber": 3}
db.processAnswer(values, database)
values = {"questionID": 3, "optionNumber": 4}
db.processAnswer(values, database)
db.processAnswer(values, database)
db.processAnswer(values, database)

values = {"questionID": 4, "optionNumber": 2}
db.processAnswer(values, database)
db.processAnswer(values, database)
db.processAnswer(values, database)
db.processAnswer(values, database)

values = {"questionID": 5, "optionNumber": 4}
db.processAnswer(values, database)
db.processAnswer(values, database)
db.processAnswer(values, database)
db.processAnswer(values, database)

print(db.createAnalytics([1], database))
print("\n\nTest25 Passed\n\n")

# searchForQuiz tests
# Not a valid quizname or label

values = ["PinkFluffyUnicorns"]
quizList = db.searchForQuiz(values, database)
if(not quizList):
    print("\n\nTest26 Passed\n\n")

# search by quizname
values = ["name"]
quizList = db.searchForQuiz(values, database)
if(quizList):
    print(quizList)
    print("\n\nTest27 Passed\n\n")

# search by quiz label
values = ["label"]
quizList = db.searchForQuiz(values, database)
if(quizList):
    print(quizList)
    print("\n\nTest28 Passed\n\n")

#
values = {"courseName": "name","courseDescription": "desc", "courseID": 1}
if(db.updateCourse(values, database)):
    print("\n\nTest29 Passed\n\n")

"""
values = {"courseID": 2,"quizName": "name2","availableAsync": 1,"label": "label","quizDescription": "desc","durationMinutes": 9}
if(db.createQuiz(values, database)):
    print("\n\nTest30 Passed\n\n")"""