import mysql.connector
from mysql.connector import Error
import statistics
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
    results = retrieveFromDatabase("SELECT questionID, prompt, durationMinutes, durationSeconds FROM Question WHERE quizID = %s;", quizID, database)
    for row in results:
        ident, desc, asked, mins, secs = row
        Question = dict(questionID = ident, prompt = desc, durationMins = mins, durationSecs = secs, answers = [])
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
    for row in results:
        quizID, quizName = row
        nameIDPair = dict(id = quizID, name = quizName)
        quizList.append(nameIDPair)
    return quizList


# Takes the answer dictonary and updates the database with the corresponding key/value pairs:
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
    newList = list(answerKey.values())
    return updateDatabase("INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (%s, %s, %s, %s);", newList, database)


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
    return updateDatabase("INSERT INTO Quiz (courseID, name, availableAsync, label, quizDescription, durationMinutes) VALUES (%s, %s, %s, %s, %s, %s)", list(quiz.values()), database)


# Takes the course object and adds the values of it to the database
# course is the course python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createCourse(course, database):
    return updateDatabase("INSERT INTO Course (username, name, courseDescription) VALUES (%s, %s, %s)", list(course.values()), database)


# Takes the author object and adds the values of it to the database
# author is the author python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createAuthor(author, database):
    return updateDatabase("INSERT INTO Author (name, authorDescription, emailaddress) VALUES (%s, %s, %s)", list(author.values()), database)


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

    count = []
    scorePerQuestion = []
    scorePerResponse = []

    for question in quiz["questionList"]:
        count.append(retrieveFromDatabase("SELECT COUNT(*) FROM Answers WHERE questionID = %s;", question["questionID"], database))
        scorePerQuestion.append(retrieveFromDatabase("SELECT SUM(scoreValue) FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;", question["questionID"], database))
        scorePerResponse.append(retrieveFromDatabase("SELECT scoreValue FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;", question["questionID"], database))

    mean = []
    median = []

    for i in quiz["questionList"]:
        mean.append(scorePerQuestion[i] // count[i])
        median.append(statistics.median(scorePerResponse[i]))

    minCorrect = retrieveFromDatabase("WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID) SELECT MIN(correct) AS minCorrect, prompt FROM (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question JOIN correctAnswers ON Answers.attemptID = correctAnswers.attemptID JOIN Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) AS counts GROUP BY prompt;", quizID, database)
    maxCorrect = retrieveFromDatabase("WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID) SELECT MAX(correct) AS maxCorrect, prompt FROM (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question JOIN correctAnswers ON Answers.attemptID = correctAnswers.attemptID JOIN Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) AS counts GROUP BY prompt;", quizID, database)
    leastVariance = retrieveFromDatabase("WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID), attemptCount AS (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question JOIN correctAnswers ON Answers.attemptID = correctAnswers.attemptID Join Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) SELECT prompt, VARIANCE(correct) AS variance FROM attemptCount GROUP BY prompt ORDER BY variance ASC LIMIT 1;", quizID, database)
    mostVariance = retrieveFromDatabase("WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID), attemptCount AS (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question JOIN correctAnswers ON Answers.attemptID = correctAnswers.attemptID Join Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) SELECT prompt, VARIANCE(correct) AS variance FROM attemptCount GROUP BY prompt ORDER BY variance DESC LIMIT 1;", quizID, database)

    result = dict(numOfResponses = count, meanScore = mean, medianScore = median, leastCorrect = minCorrect, mostCorrect = maxCorrect, homogenous = leastVariance, heterogenous = mostVariance)
    return result