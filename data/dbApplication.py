from typing import List
import mysql.connector
from mysql.connector import Error
import statistics
import json


# Opens a connection to the database
# Requires no Parameters
# Returns the database connection object
def connectToDatabase (username, password):
    database = None
    try:
        database = mysql.connector.connect(
            host= "localhost",
            #host= "dolphin.csci.viu.ca",
            user= username,
            password= password,
            database= "csci375team5_quizdb",
            auth_plugin= "mysql_native_password"
        )
    except Error as e:
        raise Exception (e)

    return database
        

# Closes the connection from the database
# Requires a database object as a paramater
# Returns nothing
def disconnectFromDatabase (database):
    if(database is None):
        raise Exception ("Error in disconnectFromDatabase in dbApplication.py. Database is None-type.")

    if(database.is_connected()==False):
        raise Exception ("Error in disconnectFromDatabase in dbApplication.py. Database was not connected.")
    
    database.close()
    if(database.is_connected()):
        raise Exception ("Error in disconnectFromDatabase in dbApplication.py. Database connection did not close.")

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
#       "quizID" -> The identifier of the quiz
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
    
    if results:
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
        
    results3 = retrieveFromDatabase("SELECT courseID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizID = %s;", quizID, database)
    if(not results3):
        print(results3)
        return None
    
    for row in results3:
        courseID, quizName , availableAsync , quizLabel , quizDescription , minutes = row

    Quiz = dict(quizID = quizID[0] , courseID = courseID, quizName = quizName , availableAsync = availableAsync , label = quizLabel , quizDescription = quizDescription , durationMins = minutes , questionList = questions)

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
#       "quizID" -> The identifier of the quiz
#       "name" -> The name of the quiz
#       "asynchronous" -> a boolean value determining if the quiz can be done asychronously
#       "label" -> The label attached to this quiz
#       "description" -> The description of this quiz
#       "durationMins" -> the duration in minutes that this quiz will allow
#       "questionList" -> a list of question disctonaries associated with this quiz (described below)
#
# database is the database object to connect to
# Returns a quizList dictonary
def getQuizList(database):
    quizList = []
    results = retrieveFromDatabase("SELECT quizID FROM Quiz", None, database)
    # breakpoint()
    if(not results):
        return None
    
    # results is a list of tuples with a single element in each
    # so we need to unwrap it
    for row in results:
        quizID = [row[0]]
        quizList.append(assembleQuiz(quizID, database))
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
    results = retrieveFromDatabase("SELECT quizID FROM Quiz WHERE courseID = %s", courseID, database)
    if(not results):
        return None
    
    for row in results:
        quizID = row
        quizList.append(assembleQuiz(quizID, database))
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
    results = retrieveFromDatabase("SELECT courseID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz NATURAL JOIN Course WHERE courseID = Course.courseID AND Course.username = %s;", username, database)
    if(not results):
        return None
    
    for row in results:
        courseID, quizName, availableAsync, label, quizDescription, durationMinutes = row
        nameIDPair = dict(courseID = courseID, quizName = quizName, availableAsync = availableAsync, label = label, quizDescription =  quizDescription, durationMinutes = durationMinutes)
        quizList.append(nameIDPair)
    return quizList

def getCourseListFromAuthor (database):
    return retrieveFromDatabase("SELECT * FROM Course", [], database)


def getCourse(courseIDParam, database):
    results = retrieveFromDatabase("SELECT * FROM Course WHERE courseID = %s;", courseIDParam, database)
    if(not results):
        return None
    
    for row in results:
        courseID, username, courseName, courseDescription = row
    course = dict(courseID = courseID, username = username, courseName = courseName, courseDescription =  courseDescription)
    return course

# Gets max attempt ID
# API will add 1 to this and send to frontend
# Frontend will use that value as attemptID for all answers to questions in a certain quiz
# Frontend gets a new attemptID every time a quiz is started.
def getMaxAttempt(database):
    results = retrieveFromDatabase("SELECT MAX(attemptID) FROM Answers;", [], database)
    if not results:
        return None
    
    # Should be a list with a single tuple in it
    return results[0][0]

# Answer is a list of the form [attemptID, questionID, optionNumber]
# database is the database connection
# Returns True if sucessful, otherwise None
def submitAnswer(answer, database):
    sqlQuery = '''
        INSERT INTO Answers (attemptID, questionID, optionNumber)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        optionNumber = VALUES(optionNumber);
    '''
    status = updateDatabase(sqlQuery, answer, database)
    
    # Return success or failure
    if status:
        return True
    else:
        return False

# Takes the answer dictonary from the users response to a quiz question, and adds it to the database
# answer is the answers python object that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
# !! Deprecated by submitAnswer !!
def processAnswer(answer, database):
    # TODO: Can you please modify this function to somehow return the attemptID which is assigned by DBMS?
    status = updateDatabase("INSERT INTO Answers (questionID, optionNumber) VALUES (%s, %s);", answer, database)
    if(status):
        return retrieveFromDatabase("Select attemptID from Answers ORDER BY attemptID DESC LIMIT 1;", [], database)


# Takes the answerKey object and adds the values of it to the database
# answerKey is the answerKey python object that contains the answers you want to upload to the db
# database is the database connection
# Returns the updated answerKey if sucessful, otherwise None
def createAnswerKey(answerKey, database):
    if(updateDatabase("INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE optionDescription = VALUES(optionDescription), scoreValue = VALUES(scoreValue);", answerKey, database)):
        results = retrieveFromDatabase("SELECT * FROM AnswerKey WHERE questionID = %s AND optionNumber = %s;", [answerKey[0], answerKey[1]], database)
        # Need to unwrap results or it will not conform to the response model
        returnList = []
        for row in results:
            returnList.append(row)
        return returnList

# Takes the question object and adds the values of it to the database
# question is the question list that contains the data of the question you want to upload to the db
# database is the database connection
# Returns the questionID if sucessful, otherwise None
def createQuestion(question, database):
    if(updateDatabase("INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (%s, %s, %s, %s);", question, database)):
        # Need to unwrap questionID or it will not conform to the response model
        return retrieveFromDatabase("Select questionID from Question ORDER BY questionID DESC LIMIT 1;", [], database)[0][0]

# Takes the question object and updates the values of it to the database
# question is the question list that contains the answers you want to upload to the db
# database is the database connection
# Returns the True if sucessful, otherwise None
def updateQuestion(question, database):
    return updateDatabase("UPDATE Question SET quizID = %s, prompt = %s, durationMinutes = %s, durationSeconds = %s WHERE questionID = %s", question, database)

# Takes the quiz object and adds the values of it to the database
# quiz is the quiz list that contains the answers you want to upload to the db
# database is the database connection
# Returns the QuizID if sucessful, otherwise None
def createQuiz(quiz, database):
    if(updateDatabase("INSERT INTO Quiz (courseID, quizName, availableAsync, label, quizDescription, durationMinutes) VALUES (%s, %s, %s, %s, %s, %s);", quiz, database)):
        return retrieveFromDatabase("Select quizID from Quiz ORDER BY quizID DESC LIMIT 1;", [], database)

# Takes the quiz object and adds the values of it to the database
# quiz is the quiz list that contains the values you want to upload to the db
# database is the database connection
# Returns the QuizID if sucessful, otherwise None
def updateQuiz(quiz, database):
    return updateDatabase("UPDATE Quiz SET courseID = %s, quizName = %s, availableAsync = %s, label = %s, quizDescription = %s, durationMinutes = %s WHERE quizID = %s", quiz, database)

# Takes the course object and adds the values of it to the database
# course is the course's list that contains the values you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createCourse(course, database):
    updateDatabase("INSERT INTO Course (username, courseName, courseDescription) VALUES (%s, %s, %s);", course, database)
    return getNewCourseID(course, database)

def getNewCourseID(course, database):
    return retrieveFromDatabase("SELECT courseID FROM Course WHERE courseName = %s AND username = %s", [course[1], course[0]], database)

# Updates a course row in the database with the specifed courseID
# course is the course's list that contains the answers you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def updateCourse(course, database):
    return updateDatabase("INSERT INTO Course (courseID, username, courseName, courseDescription) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE courseName = VALUES(courseName), courseDescription = VALUES(courseDescription);", course, database)

# Updates an answer row in the database with the specifed attemptID
# answer is the answer's list that contains the values you want to upload to the db
# database is the database connection
# Returns the updated Answer as a list with a single tuple if sucessful, otherwise None
# !! Deprecated by submitAnswer !!
def updateAnswer(answer, database):
    updateDatabase("INSERT INTO Answers (attemptID, questionID, optionNumber) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE optionNumber = VALUES(optionNumber);", answer, database)
    return retrieveFromDatabase("Select attemptID, questionID, optionNumber from Answers WHERE attemptID = %s LIMIT 1;", [answer[0]], database)

# Updates an answer row in the database with the specifed attemptID
# answer is the answer's list that contains the values you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def updateAnswerKey(answerKey, database):
    return updateDatabase("INSERT INTO Answer (questionID, optionNumber, optionDescription, scoreValue) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE optionDescription = VALUES(optionDescription), scoreValue = VALUES(scoreValue);", answerKey, database)

# Adds the quiz in quizID to course in courseID
# values is a list of the courseID, then the quizID
# database is the database connection
# Returns True if sucessful, otherwise None
def addQuizToCourse(values, database):
    return updateDatabase("UPDATE Quiz SET courseID = %s WHERE quizID = %s;", values, database)

# Takes the author object and adds the values of it to the database
# author is the author list that contains the author attributes(?) you want to upload to the db
# database is the database connection
# Returns True if sucessful, otherwise None
def createAuthor(author, database):
    return updateDatabase("INSERT INTO Author (username, name, authorDescription, emailAddress) VALUES (%s, %s, %s, %s);", author, database)


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
    

    # Number of responses by question.
    count: List[int] = []
    
    # List of lists: Number of responses that chose each option for that question.
    answers: List[List[int]] = []
    
    # Sum of scores for each question in the quiz. 
    scorePerQuestion: List[int] = []
    
    # Score that each response to each question got.
    scorePerResponse: List[List[int]] = []

    for question in quiz["questionList"]:
        takeQuestionMetrics(database, count, answers, scorePerQuestion, scorePerResponse, question)

    # Pad the answers to each question to 4.
    for row in answers:
        while(len(row) < 4):
            row.append(0)

    i = 0

    mean = []
    median = []
    variance = []

    for question in quiz["questionList"]:
        if count[i] > 0:
            mean.append(scorePerQuestion[i] / count[i])
            median.append(statistics.median(scorePerResponse[i]))
            variance.append(statistics.variance(answers[i]))
        else:
            mean.append(0)
            median.append(0)
            variance.append(0)
        i = i+1
    
    minCorrect = findMinCorrect(quizID, database)
    
    maxCorrect = findMaxCorrect(quizID, database)

    minVariance = min(variance) if variance else 0
    prompt = quiz["questionList"][variance.index(minVariance)]["prompt"] if variance else 'n/a'
    leastVariance = [prompt, minVariance]
    
    maxVariance = max(variance) if variance else 0
    prompt = quiz["questionList"][variance.index(maxVariance)]["prompt"] if variance else 'n/a'
    mostVariance = [prompt, maxVariance]

    result = {
        'quizID': quizID,
        'numOfResponses': count[0] if count[0] and count[0] > 0 else 0,
        'meanScore': mean,
        'medianScore': median,
        'leastCorrect': minCorrect if minCorrect else [],
        'mostCorrect': maxCorrect if maxCorrect else [],
        'homogenous': leastVariance,
        'heterogenous': mostVariance
    }

    return result

# Helper to createAnalytics
def takeQuestionMetrics(database, count, answers, scorePerQuestion, scorePerResponse, question):
    questionID = [question["questionID"]]
        
    # Part 1 - Number of answers to this question
    # Answers to this question
    answersToThis = retrieveFromDatabase("SELECT COUNT(*) FROM Answers WHERE questionID = %s;", questionID, database)
        
    # Unwrap list containing single tuple
    answersToThis = answersToThis[0][0]
        
    count.append(answersToThis)
        
    # Part 2 - Number of answers with each option
    answersByOption = retrieveFromDatabase("SELECT COUNT(optionNumber) FROM Answers WHERE questionID = %s GROUP BY optionNumber;", questionID, database)
        
    # Unwrap list containing tuples with a single value
    answersByOption = [ x[0] for x in answersByOption ]
        
    answers.append(answersByOption)
        
    # Part 3 - Score per question? Sum of all scores
    thisSpq = retrieveFromDatabase("SELECT SUM(scoreValue) FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;", questionID, database)
    if thisSpq and thisSpq[0] and thisSpq[0][0]:
        thisSpq = int(thisSpq[0][0])
    else:
        thisSpq = 0
    scorePerQuestion.append(thisSpq)
        
    # Part 4 - Score per response?
    thisSpr = retrieveFromDatabase("SELECT scoreValue FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;", questionID, database)
    thisSpr = [ x[0] for x in thisSpr ]
    scorePerResponse.append(thisSpr)

# Helper to createAnalytics
def findMaxCorrect(quizID, database):
    maxCorrectQuery = '''
        WITH correctAnswers AS (
            SELECT attemptID
            FROM Answers
            NATURAL JOIN AnswerKey
            WHERE scoreValue > 0
            GROUP BY attemptID
        )
        SELECT MAX(correct) AS maxCorrect, prompt
        FROM (
            SELECT prompt,
                COUNT(DISTINCT correctAnswers.attemptID) AS correct
            FROM Answers
            NATURAL JOIN Question
            NATURAL JOIN correctAnswers
            JOIN Quiz ON Quiz.quizID = Question.quizID
            WHERE Quiz.quizID = %s
            GROUP BY prompt
        ) AS counts
        GROUP BY prompt
        ORDER BY correct DESC
        LIMIT 1;
    '''
    maxCorrect = retrieveFromDatabase(maxCorrectQuery, quizID, database)
    return maxCorrect

# Helper to createAnalytics
def findMinCorrect(quizID, database):
    minCorrectQuery = '''
        WITH correctAnswers AS (
            SELECT attemptID
            FROM Answers
            NATURAL JOIN AnswerKey
            WHERE scoreValue > 0
            GROUP BY attemptID
        )
        SELECT MIN(correct) AS minCorrect, prompt
        FROM (
            SELECT prompt,
                COUNT(DISTINCT correctAnswers.attemptID) AS correct
            FROM Answers
            NATURAL JOIN Question
            NATURAL JOIN correctAnswers
            JOIN Quiz ON Quiz.quizID = Question.quizID
            WHERE Quiz.quizID = %s
            GROUP BY prompt
        ) AS counts
        GROUP BY prompt
        ORDER BY correct ASC
        LIMIT 1;
    '''
    minCorrect = retrieveFromDatabase(minCorrectQuery, quizID, database)
    return minCorrect

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

# Returns True if quiz with given ID is async, False if not
def quiz_is_async(quizID, database):
    results = retrieveFromDatabase(
        '''
            SELECT IFNULL(
                (SELECT availableAsync FROM Quiz WHERE quizID = %s LIMIT 1),
                0
            ) AS availableAsync;
        ''',
        [quizID],
        database)
    return results[0][0] == 1
