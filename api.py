# api.py (WIP)
# Author: Cassius Galdames
#
# Note: Currently set up for individual testing.
#  

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware # uncomment for UI integration
from contextlib import asynccontextmanager #This is for ensuring the database connection is opened on startup and closed before shutdown
from models import Answer, Question, Quiz, Course, Author, Analytics, Response
from typing import List, Dict
import os
import dbApplication as db_app
import pdb
# import mysql.connector            // DB integration

# global database connection object
db_connection = None


# Allows the database to be connected to and disconnected from only at the start and end of the program respectively
@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_connection
    db_connection = db_app.connectToDatabase(os.getenv("DBUSER"), os.getenv("DBPASS"))

    yield

    db_app.disconnectFromDatabase(db_connection)

app = FastAPI(lifespan=lifespan)

# UI integration
# CORS configuration for frontend
app.add_middleware(
   CORSMiddleware,
#    allow_origins=["http://localhost:3000"],
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

# Test values:     // will replace with connection to DB
quizzes: Dict[int, Quiz] = {}  # Key: quiz id, Value: Quiz object
courses: Dict[int, Course] = {}  # Key: course id, Value: list of courses

# Quiz Endpoints:

# Create a quiz
@app.post("/quizzes/", response_model=Quiz)
def create_quiz(
    quiz: Quiz,  # Request body with quiz details from frontend
    username: str = Query(..., description="Username of the creator")
):
    # DB Connection
    # breakpoint()
    createdQuiz = db_app.createQuiz(
        [quiz.courseID, quiz.quizName, 
         quiz.availableAsync, quiz.label, 
         quiz.quizDescription, quiz.durationMins], 
        db_connection)
    # On success, createdQuiz is of the form [(6,)]
    # Put the new ID in the quiz and send that back.
    quiz.quizID = createdQuiz[0][0]
    # breakpoint()
    return {
        "quizID": quiz.quizID,
        "courseID": quiz.courseID,
        "quizName": quiz.quizName,
        "availableAsync": quiz.availableAsync,
        "label": quiz.label,
        "quizDescription": quiz.quizDescription,
        "durationMins": quiz.durationMins,
        "questionList": quiz.questionList
    }

# Get a quiz by ID
@app.get("/quizzes/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int):

    # DB Connection
    
    # breakpoint()
    quiz = db_app.assembleQuiz([quiz_id], db_connection) # Works
    return quiz

# Delete a quiz by ID | Deletion has been moved to a stretch feature
@app.delete("/quizzes/{quiz_id}", response_model=Quiz)
def delete_quiz(quiz_id: int):
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    deleted_quiz = quizzes.pop(quiz_id)
    return deleted_quiz

# Edit a quiz by ID
@app.put("/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, quiz: Quiz):
    # Database
    # breakpoint()
    updateStatus = db_app.updateQuiz([quiz.courseID, quiz.quizName, quiz.availableAsync, quiz.label, quiz.quizDescription, quiz.durationMins, quiz.quizID], db_connection)
    
    if(not updateStatus):
        raise HTTPException(status_code=404, detail="Quiz not found")
    # If we got here, then `quiz` has been sent to the database succesfully
    # However, this is still kind of bad practice
    # Really, we should be retrieving it from the DBMS again
    # That way we would be 100% sure that we avoid having a different value in the API than the DB!
    return quiz

# Get all quizzes as a list
@app.get("/quizzes/", response_model=List[Quiz])
def get_all_quizzes():
    quizList = db_app.getQuizList(db_connection) # Works
    quizClassList = []
    for quiz in quizList:
        if quiz:
            quizClassList.append(Quiz(**quiz))
    return quizClassList


# Question Endpoints:

# Create a question within the quiz "quiz_id"
@app.post("/quizzes/{quiz_id}/questions/", response_model=Question)
def create_question(
    quiz_id: int,
    question: Question,
):
    
    # DB Connection
    # breakpoint()
    if(question.questionID == -1):
        result = db_app.createQuestion([quiz_id, question.prompt, question.durationMins, question.durationSecs], db_connection)
        question.questionID = result
    else:
        result = db_app.updateQuestion([quiz_id, question.prompt, question.durationMins, question.durationSecs, question.questionID], db_connection)

    if(result):
        updatedAnswerKey = []
        for row in question.answers:
            answer = db_app.createAnswerKey([question.questionID, row.optionNumber, row.description, row.scoreValue], db_connection)[0]
            updatedAnswerKey.append(dict(questionID = answer[0], optionNumber = answer[1],  optionDescription = answer[2], scoreValue = answer[3]))

        question.answers = updatedAnswerKey
        questionData = {
            'questionID': question.questionID,
            'prompt': question.prompt,
            'durationMins': question.durationMins,
            'durationSecs': question.durationSecs,
            'answers': question.answers,
        }

        return questionData



# Update a question within the quiz "quiz_name"
@app.put("/quizzes/{quiz_id}/questions/{question_id}", response_model=Question)
def update_question(quiz_id: int, question_id: int, question: Question):
    # Database
    updateStatus = db_app.updateQuestion([quiz_id, question.prompt, question.durationMins, question.durationSecs, question_id])
    if(not updateStatus):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return updateStatus

# Delete a question within the quiz "quiz_id"
@app.delete("/quizzes/{quiz_id}/questions/{question_id}", response_model=Question)
def delete_question(quiz_id: int, question_id: int):
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    for i, q in enumerate(quizzes[quiz_id].questionList):
        if q.questionID == question_id:
            return quizzes[quiz_id].questionList.pop(i)
    raise HTTPException(status_code=404, detail="Question not found")


# Answer Endpoints:

# Create an answer within the question "question_id"
@app.post("/quizzes/{quiz_id}/questions/{question_id}/answers/", response_model=Answer)
def create_answer(
    quiz_id: int,
    question_id: int,
    answer: Answer
):
    answerList = [question_id, answer.optionNumber, answer.description, answer.scoreValue]
    result = db_app.createAnswerKey(answerList, db_connection)
    if(result):
        return result
    raise HTTPException(status_code=404, detail="Question not found")


# Update an answer within the question "question_id"
@app.put("/quizzes/{quiz_id}/questions/{question_id}/answers/", response_model=Answer) # Waiting on Team members response to proceed
def update_answer(
    quiz_id: int,
    question_id: int, 
    optionNumber: int, 
    answer: Answer
):
    # Database
    result = db_app.updateAnswerKey([question_id, answer.optionNumber, answer.description, answer.scoreValue], db_connection)
    if(result):
        return result
    raise HTTPException(status_code=404, detail="Question not found")

# Delete an answer within the question "question_id" | deleting data is a stretch feature. Keep your secrets out of the quizzes for now
@app.delete("/quizzes/{quiz_id}/questions/{question_id}/answers/", response_model=Answer)
def delete_answer(
    quiz_id: int,
    question_id: int, 
    optionNumber: int
):
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = quizzes[quiz_id]
    question_id_list = [q.questionID for q in quiz.questionList]
    if question_id not in question_id_list:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question = next(q for q in quiz.questionList if q.questionID == question_id)
    
    # Update optionNumber     // for unit testing
    for i, q in enumerate(question.AnswerKey):
        if q.optionNumber == optionNumber:
            return question.AnswerKey.pop(i)
    raise HTTPException(status_code=404, detail="Answer not found")


# Course Endpoints:

# Create a course
@app.post("/courses/", response_model=Course)
def create_course(
    course: Course, 
    username: str = Query(..., description="Username of the creator")
):
    # Database
    # breakpoint()
    newID = db_app.createCourse([username, course.courseName, course.courseDescription], db_connection)
    if(not newID):
        raise HTTPException(status_code=500, detail="Couldn't Create a Course")
    course.courseID = newID[0][0]
    return {
            'courseID': course.courseID,
            'username': course.username,
            'courseName': course.courseName,
            'courseDescription': course.courseDescription,
        }

#Get a course List
@app.get("/courses/", response_model=List[Course])
def get_course_list():

    # This function returns tuples with no keys. 
    # We will make a dictionary with keys and values compliant with `models.py`
    # from the tuples.

    raw_course_list = db_app.getCourseListFromAuthor(db_connection)
    courses = []
    for rc in raw_course_list:
        # see Course class in `models.py` for schema
        course = {
            'courseID': rc[0],
            'username': rc[1],
            'courseName': rc[2],
            'courseDescription': rc[3],
        }
        courses.append(course) 

    # Returns list of objects
    return courses

# Edit a course by ID
@app.put("/courses/{course_id}", response_model=Course)
def update_course(
    course_id: int, 
    course: Course,
    username: str = Query(..., description="Username of the creator")
):
    # Database
    status = db_app.updateCourse([course_id, username, course.courseName, course.courseDescription], db_connection)
    if(not status):
        raise HTTPException(status_code=404, detail="Course not found")
    return db_app.getCourse([course_id], db_connection)

# Delete a course by ID | Deleting data is a stretch feature
@app.delete("/courses/{course_id}", response_model=Course)
def delete_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses.pop(course_id)

# Add a quiz to a course
@app.post("/courses/{course_id}/quizzes/{quiz_id}", response_model=Course)
def add_quiz_to_course(course_id: int, quiz_id: int):
    # Database
    status = db_app.addQuizToCourse([course_id, quiz_id], db_connection)
    if(not status):
        raise HTTPException(status_code=404, detail="Course or Quiz not found")
    return status

# Remove a quiz from a course | deleting is a stretch feature. Also this violates a FK constraint
@app.delete("/courses/{course_id}/quizzes/{quiz_id}", response_model=Course)
def remove_quiz_from_course(course_id: int, quiz_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = quizzes[quiz_id]
    if quiz.courseID != course_id:
        raise HTTPException(
            status_code=400,
            detail=f"Quiz not associated with Course"
        )
    
    quiz.courseID = 0  
    return courses[course_id]

# Get all quizzes in a course as a list
@app.get("/courses/{course_id}/quizzes", response_model=List[Quiz])
def get_course_quizzes(course_id: int):

    # Database
    quizList = db_app.getQuizListFromCourse([course_id], db_connection) # Probably Works
    if(not quizList):
        raise HTTPException(status_code=404, detail="Course not found")
    return quizList

# Get link to a course
@app.get("/courses/{course_id}/link", response_model=Dict[str, str])
def get_course_link(course_id: int):
    # Database
    if(db_app.retrieveFromDatabase("SELECT courseName FROM Quiz WHERE courseID = %s", [course_id], db_connection)):
        return {"link": f"http://localhost:3000/class/{course_id}"}
    raise HTTPException(status_code=404, detail="Course not found")


# Author Endpoints:

# Create an author entry
@app.post("/authors/", response_model=Author)
def create_author(author: Author):
    if(not db_app.createAuthor([author.username, author.name, author.description, author.emailAddress], db_connection)):
        raise HTTPException(status_code=500, detail="Could not create a user")
    return author

# Delete an author entry | delete is a stretch feature
@app.delete("/authors/{username}", response_model=dict)
def delete_author(username: str):
    return {"message": f"Author {username} deleted"}

# Analytics Endpoint

# Get analytics object for quiz id
@app.get("/analytics/{quizID}", response_model=Analytics)
def get_analytics(quizID: int, username: str):
    # breakpoint()
    results = db_app.createAnalytics([quizID], db_connection)
    if(not results):
        raise HTTPException(status_code=404, detail="Quiz not found or no analytics to create for said quiz")
    return results

    # return {
    #     'numOfResponses': 120,
    #     'meanScore': [2.5, 1.75, 3.0],
    #     'medianScore': [2, 2, 3],
    #     'leastCorrect': [('What is the capital of France?', 25)],
    #     'mostCorrect': [('2 + 2 equals?', 110)],
    #     'homogenous': ['Select the primary color.', 0.5],
    #     'heterogenous': ['Which programming language is fastest?', 2.2]
    # }

# Get the next available attemptID
@app.get("/startattempt")
def get_next_attempt_id():
    # breakpoint()
    nextID = db_app.getMaxAttempt(db_connection)
    
    if not nextID:
        return {
            "attemptID": -1,
        }
    
    if nextID:
        return {
            "attemptID": nextID + 1
        }

# Submit a response to a quiz question
@app.post("/respond", response_model=Response)
def submit_response(response: Response):
    
    # First, get a new attemptID if needed.
    # The frontend will be waiting to grab this back
    # and use it for subequent responses to all questions 
    # in the same quiz in the same attempt.
    if(response.attemptID == -1):
        response.attemptID = get_next_attempt_id()["attemptID"]
        
    # Insert ANSWER or update if it exists
    db_app.submitAnswer([response.attemptID, response.questionID, response.optionNumber], db_connection)
    
    # Now return the response as it is
    return response