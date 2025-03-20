import mysql.connector
from mysql.connector import Error
import json


# Opens a connection to the database
# Requires no Parameters
# Returns the database connection object
def connectToDatabase (username, password):
    loggedIn = False

    try:
        database = mysql.connector.connect(
            host= "localhost",
            user= username,
            password= password,
            database= "csci375team5_quizdb"
        )
    except Error as e:
        print("Error: {e}")
        
    loggedIn = True

# Closes the connection from the database
# Requires a database object as a paramater
# Returns nothing
def disconnectFromDatabase (database):
    database.close()


# Retrieves data from the database coresponding to the sql query it is fed
# sqlQuery is the Sql query to be executed
# params is the list of parameters to the sql query (if any)
# database is the database connection
# Returns the result set if successful, otherwise nothing
def retrieveFromDatabase (sqlQuery, params, database):
    
    try:
        if(database.isConnected()):
            cursor = database.cursor()
            cursor.execute(sqlQuery, params)
            return cursor.fetchall()
        
        return None

    except Error as e:
        print("Error: {e}")
        return None

    finally:
        cursor.close()


# Updates the values to the database according to the sqlQuery (added / removed)
# sqlQuery is the Sql query to be executed
# values is the list of values to be updated in the database
# database is the database connection
# Returns True if sucessful, otherwise None
def updateDatabase (sqlQuery, values, database):
    try:
        if(database.isConnected()):
            cursor = database.cursor
            cursor.execute(sqlQuery, values)
            database.commit()
            cursor.close()
            return True
        return None
        
    except Error as e:
        print("Error: {e}")


# Creates a quiz dictonary associated with the quizID provided with the following schema:
#
# Quiz Dictonary:
#       "name" -> The name of the quiz
#       "asynchronous" -> a boolean value determining if the quiz can be done asychronously
#       "label" -> The label attached to this quiz
#       "description" -> The description of this quiz
#       "durationMins" -> the duration in minutes that this quiz will allow
#       "questionList" -> a list of question disctonaries associated with this quiz (described below)
#
# Question Dictonary:
#       "questionID" -> The identifier of the question
#       "prompt" -> The actual question being asked
#       "wasAsked" -> A boolean Value determining if the question was asked. Still unsure why this is in the database
#       "durationMins" -> An integer with the time limit of the quiz in minutes
#       "durationSecs" -> An integer with the time limit of the quiz in seconds
#       "Answers" -> A list of Answer dictonaries associated with this question (described below)
# 
# Answer Dictonary:
#       "optionNumber" -> The identifier of the option for the question
#       "optDescription" -> The actual option text
#       "scoreValue" -> The amount of points you get for answering this option 
#
# quizID is the Idnetifier of the quiz you want to retrieve form the database
# database is the database object you want to get the quiz from
# Returns a Quiz dictonary
def assembleQuiz (quizID, database) :

    questions = []
    results = retrieveFromDatabase("SELECT questionID, prompt, wasAsked, durationMinutes, durationSeconds FROM Question WHERE quizID = %s;", quizID, database)
    for row in results:
        ident, desc, asked, mins, secs = row
        Question = dict(questionID = ident, prompt = desc, wasAsked = asked, durationMins = mins, durationSecs = secs, answers = [])
        questions.append(Question)


    answer = []
    for i in questions:
        questionID = questions[i]["questionID"]
        results2 = retrieveFromDatabase("SELECT optionNumber, optionDescription, scoreValue FROM AnswerKey WHERE questionID = %s;", questionID, database)
        for row in results2:
            number, optDescription, value = row
            Answer = dict(optionNumber = number, description = optDescription, scoreValue = value)
            answer.append(Answer)
        questions[i]["answers"] = answer[i]

    quizName, availableAsync, quizLabel, quizDescription, minutes = retrieveFromDatabase("SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizID = %s;", quizID, database)
    Quiz = dict(name = quizName, asynchronous = availableAsync, label = quizLabel, description = quizDescription, durationMins = minutes, questionList = questions)

    return Quiz


# Converts any python object into a related javascript one
# someObject is the item to be converted
# returns the JSON object
def pythonToJSON(someObject):
    return json.dumps(someObject)


# Converts a JSON object to a python one
# someObject is the JSON object
# return the python equivalent to the object
def jsonToPython(someObject):
    return json.loads(someObject) 

# Creates a quizList with the follwing schema
#       "quizID" -> The id of the quiz to retrieve its details
#       "quizName" -> The name of the quiz
#
# database is the database object to connect to
# Returns a quizList dictonary
def getQuizList(database):
    quizList = []
    results = retrieveFromDatabase("SELECT quizID, quizName FROM Quiz",[], database)
    for row in results:
        quizID, quizName = row
        nameIDPair = dict(id = quizID, name = quizName)
        quizList.append(nameIDPair)
    return quizList


    
