import mysql.connector
from mysql.connector import Error
import math
import statistics
import json


# Opens a connection to the database
# Requires no Parameters
# Returns the database connection object
def connectToDatabase (username, password):
    database = None
    try:
        database = mysql.connector.connect(
            #host= "dolphin.csci.viu.ca",
            host= "localhost",
            user= username,
            password= password,
            database= "csci375team5_quizdb"
        )
    except Error as e:
        raise Exception (e)
        return None

    return database
        

# Closes the connection from the database
# Requires a database object as a paramater
# Returns nothing
def disconnectFromDatabase (database):
    if(database is None):
        raise Exception ("Error in disconnectFromDatabase in dbApplication.py. Database is None-type.")
        return False

    if(database.is_connected()==False):
        raise Exception ("Error in disconnectFromDatabase in dbApplication.py. Database was not connected.")
        return False
    
    database.close()
    if(database.is_connected()):
        raise Exception ("Error in disconnectFromDatabase in dbApplication.py. Database connection did not close.")
        return False

    else:
        return True


# Retrieves data from the database coresponding to the sql query it is fed
# sqlQuery is the Sql query to be executed
# params is the list of parameters to the sql query (if any)
# database is the database connection
# Returns the result set if successful, otherwise nothing
def retrieveFromDatabase (sqlQuery, params, database):
    
    try:
        if(database.is_connected()):
            cursor = database.cursor()
            cursor.execute(sqlQuery, params)
            return cursor.fetchall()
        
        return None

    except Error as e:
        print("Error: ", e)
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
        if(database.is_connected()):
            cursor = database.cursor()
            cursor.execute(sqlQuery, values)
            database.commit()
            cursor.close()
            return True
        return None
        
    except Error as e:
        print("Error: ", e)
        return None


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
# Returns a Quiz dictonary if sucessful, None otherwise
def assembleQuiz (quizID, database) :

    questions = []
    results = retrieveFromDatabase("SELECT questionID, prompt, durationMinutes, durationSeconds FROM Question WHERE quizID = %s;", quizID, database)
    if(not results):
        return None
    
    for row in results:
        ident, desc, mins, secs = row
        Question = dict(questionID = ident, prompt = desc, durationMins = mins, durationSecs = secs, answers = [])
        questions.append(Question)


    answer = []
    for question in questions:
        questionID = [question["questionID"]]
        results2 = retrieveFromDatabase("SELECT optionNumber, optionDescription, scoreValue FROM AnswerKey WHERE questionID = %s;", questionID, database)
        if(results2):
            for row in results2:
                number, optDescription, value = row
                Answer = dict(optionNumber = number, description = optDescription, scoreValue = value)
                answer.append(Answer)
            if(not answer):
                print("Error:  Every question must have at least one answer!")
                return None
            question["answers"] = answer
            answer = []

        else: return None
        
    results3 = retrieveFromDatabase("SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizID = %s;", quizID, database)
    if(not results3):
        print(results3)
        return None
    
    for row in results3:
        quizName, availableAsync, quizLabel, quizDescription, minutes = row

    Quiz = dict(quizName = quizName, availableAsync = availableAsync, label = quizLabel, quizDescription = quizDescription, durationMins = minutes, questionList = questions)

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
    results = retrieveFromDatabase("SELECT quizID, quizName FROM Quiz", None, database)
    if(not results):
        return None
    
    for row in results:
        quizID, quizName = row
        nameIDPair = dict(quizID = quizID, quizName = quizName)
        quizList.append(nameIDPair)
    return quizList


# Creates a quizList with the follwing schema
#       "quizID" -> The id of the quiz to retrieve its details
#       "quizName" -> The name of the quiz
#
# courseID is the course that the resulting quizzes are associated with
# database is the database object to connect to
# Returns a quizList dictonary
def getQuizListFromCourse(courseID, database):
    quizList = []
    results = retrieveFromDatabase("SELECT quizID, quizName FROM Quiz WHERE courseID = %s", courseID, database)
    if(not results):
        return None
    
    for row in results:
        quizID, quizName = row
        nameIDPair = dict(quizID = quizID, quizName = quizName)
        quizList.append(nameIDPair)
    return quizList


# Creates a quizList with the follwing schema
#       "quizName" -> The name of the quiz
#       "availableAsync" -> a boolean value determining if the quiz is Asynchronous
#       "label" -> A keyword to search the quiz by
#       "quizDescription" -> A description on what the quiz covers, or in reality whatever the author feels like
#       "durationMins" -> The length of the quiz in minutes
#
# username is the quiz creators username
# database is the database object to connect to
# Returns a quizList dictonary
def getQuizListFromAuthor(username, database):
    quizList = []
    results = retrieveFromDatabase("SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz NATURAL JOIN Course WHERE courseID = Course.courseID AND Course.username = %s;", username, database)
    if(not results):
        return None
    
    for row in results:
        quizName, availableAsync, label, quizDescription, durationMinutes = row
        nameIDPair = dict(quizName = quizName, availableAsync = availableAsync, label = label, quizDescription =  quizDescription, durationMinutes = durationMinutes)
        quizList.append(nameIDPair)
    return quizList


# Takes the answer dictonary from the users response to a quiz question, and adds it to the database
# answer is the answers python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def processAnswer(answer, database):
    return updateDatabase("INSERT INTO Answers (questionID, optionNumber) VALUES (%s, %s) ON DUPLICATE KEY UPDATE optionNumber = VALUES(optionNumber);", list(answer.values()), database)


# Takes the answerKey object and adds the values of it to the database
# answerKey is the answerKey python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createAnswerKey(answerKey, database):
    return updateDatabase("INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (%s, %s, %s, %s);", list(answerKey.values()), database)


# Takes the question object and adds the values of it to the database
# question is the question python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createQuestion(question, database):
    return updateDatabase("INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (%s, %s, %s, %s)", list(question.values()), database)


# Takes the quiz object and adds the values of it to the database
# quiz is the quiz python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createQuiz(quiz, database):
    return updateDatabase("INSERT INTO Quiz (courseID, quizName, availableAsync, label, quizDescription, durationMinutes) VALUES (%s, %s, %s, %s, %s, %s)", list(quiz.values()), database)


# Takes the course object and adds the values of it to the database
# course is the course python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createCourse(course, database):
    return updateDatabase("INSERT INTO Course (username, courseName, courseDescription) VALUES (%s, %s, %s)", list(course.values()), database)


# Takes the author object and adds the values of it to the database
# author is the author python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createAuthor(author, database):
    return updateDatabase("INSERT INTO Author (username, name, authorDescription, emailAddress) VALUES (%s, %s, %s, %s)", list(author.values()), database)


# Processes specific analytics for the quiz specifed by quizID in the following format:
#
# Returns the results as a ptython dictonary in the following format:
#       "numOfResponses" -> A list showing the number of people who responded to each question
#       "meanScore" -> A list containing the mean score for each question
#       "medianScore" -> A list containing the median score for each question
#       "leastCorrect" -> A 2 element list where the first element is the number of people who got the question correct, the 2nd element is the question prompt
#       "mostCorrect" -> A 2 element list where the first element is the number of people who got the question correct, the 2nd element is the question prompt
#       "homogenous" -> A 2 element list where the first element is the question prompt, and the 2nd element is the Variance in the results 
#       "heterogenous" -> A 2 element list where the first element is the question prompt, and the 2nd element is the Variance in the results 
#
# quizID is the identifier for the quiz you want aggregate results for
# database is the database connection
# Returns The results in the above format if sucessful, otherwise None
def createAnalytics(quizID, database):
    quiz = assembleQuiz(quizID, database)
    if(not quiz):
        return None
    

    count = []
    answers = []
    scorePerQuestion = []
    scorePerResponse = []

    for question in quiz["questionList"]:
        questionID = [question["questionID"]]
        count.append(retrieveFromDatabase("SELECT COUNT(*) FROM Answers WHERE questionID = %s;", questionID, database))
        answers.append(retrieveFromDatabase("SELECT COUNT(optionNumber) FROM Answers WHERE questionID = %s GROUP BY optionNumber;", questionID, database))
        scorePerQuestion.append(retrieveFromDatabase("SELECT SUM(scoreValue) FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;", questionID, database))
        scorePerResponse.append(retrieveFromDatabase("SELECT scoreValue FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;", questionID, database))

    mean = []
    median = []

    i = 0
    scorePerResponse = fixData(scorePerResponse)
    answers = fixData(answers)
    
    for row in answers:
        while(len(row) < 4):
            row.append(0)

    print(answers)
    i = 0
    variance = []
    for question in quiz["questionList"]:
        # For some reason this is returned as a list of 1 object lists, of tuples where the second value is None
        mean.append(scorePerQuestion[i][0][0] / count[i][0][0])
        median.append(statistics.median(scorePerResponse[i]))
        variance.append(statistics.variance(answers[i]))
        i = i+1
    
    count = fixData(count)
    count = fixData([count])

    minCorrect = retrieveFromDatabase("WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID) SELECT MIN(correct) AS minCorrect, prompt FROM (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question NATURAL JOIN correctAnswers JOIN Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) AS counts GROUP BY prompt ORDER BY correct ASC LIMIT 1;", quizID, database)
    maxCorrect = retrieveFromDatabase("WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID) SELECT MAX(correct) AS maxCorrect, prompt FROM (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question NATURAL JOIN correctAnswers JOIN Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) AS counts GROUP BY prompt ORDER BY correct DESC LIMIT 1;", quizID, database)

    minVariance = min(variance)
    prompt = quiz["questionList"][variance.index(minVariance)]["prompt"]
    leastVariance = [prompt, minVariance]
    
    maxVariance = max(variance)
    prompt = quiz["questionList"][variance.index(maxVariance)]["prompt"]
    mostVariance = [prompt, maxVariance]

    result = dict(numOfResponses = count[0], meanScore = mean, medianScore = median, leastCorrect = minCorrect, mostCorrect = maxCorrect, homogenous = leastVariance, heterogenous = mostVariance)
    return result

# Fixes some obscure problem I had where data was coming back from the sql statements in one element tuples
# list is the list to be fixed
# returns the fixed list
def fixData (list):
    i = 0
    for row in list:
        j = 0
        for col in row:
            list[i][j] = col[0]
            j += 1
        i += 1
    return list


# Creates a list of quizzes that all share the same quiz name or label if no quiz names are named that way. Each quiz in the list is in the following format
#       "quizID" -> the unique identifier of the quiz
#       "quizName" -> the name of the quiz
#       "availableAsync" -> a boolean value determining if the quiz can be done asynchronously
#       "label" -> a search keyword used for looking up quizzes
#       "quizDescription" -> The description of what the quiz is about
#       "durationMinutes" -> The maximum duration of the entire quiz
#
# string is the search string for the quiz
# database is the database object where the quiz will be searched for 
def searchForQuiz (string, database):
    results = retrieveFromDatabase("SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizName SOUNDS LIKE %s;", string, database)

    if(not results):
        results = retrieveFromDatabase("SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE label SOUNDS LIKE %s;", string, database)
    
    if(not results):
        return None
    
    quizList = []
    for row in results:
        ident, name, asyncronous, lab, desc, duration = row
        quiz = dict(quizID = ident, quizName = name, availableAsync = asyncronous, label = lab, quizDescription = desc, durationMinutes = duration)
        quizList.append(quiz)
    
    return quizList
