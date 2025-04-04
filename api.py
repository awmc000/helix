# api.py (WIP)
# Author: Cassius Galdames
#
# Note: Currently set up for individual testing.
#  

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware # uncomment for UI integration
from contextlib import asynccontextmanager #This is for ensuring the database connection is opened on startup and closed before shutdown
from models import Answer, Question, Quiz, Course, Author, Analytics
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
    return db_app.createQuiz([quiz.courseID, quiz.quizName, quiz.availableAsync, quiz.label, quiz.quizDescription, quiz.durationMins], db_connection)

    # hard coded
    # Assign a quizID       // for unit testing - DB will handle
    # Note: quizID defaults to 0, and IDs start at 1 via this method
    max_id = max(quizzes.keys(), default=0)
    quiz.quizID = max_id + 1
    quizzes[quiz.quizID] = quiz
    return quiz

# Get a quiz by ID
@app.get("/quizzes/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int):

    # DB Connection
    
    quiz = db_app.assembleQuiz([quiz_id], db_connection) # Works
    return quiz

    # Hard Coded
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quizzes[quiz_id]

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
    updateStatus = db_app.updateQuiz([quiz.courseID, quiz.quizName, quiz.availableAsync, quiz.label, quiz.quizDescription, quiz.durationMins, quiz.quizID], db_connection)
    if(not updateStatus):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return updateStatus

    # Hard Coded
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz.quizID = quiz_id
    quizzes[quiz_id] = quiz
    return quiz

# Get all quizzes as a list
@app.get("/quizzes/", response_model=List[Quiz])
def get_all_quizzes():
    
    # Database
    quizList = db_app.getQuizList(db_connection) # Works
    quizClassList = []
    for quiz in quizList:
        quizClassList.append(Quiz(**quiz))
    return quizClassList

    # Hard Coded
    return list(quizzes.values())


# Question Endpoints:

# Create a question within the quiz "quiz_id"
@app.post("/quizzes/{quiz_id}/questions/", response_model=Question)
def create_question(
    quiz_id: int,
    question: Question,
):
    
    # DB Connection
    temp = question
    temp.questionID = quiz_id # The questionID will be created by the db, but the db needs the quiz ID for the question
    result = db_app.createQuestion(temp.__dict__, db_connection)
    if(result):
        question.questionID = result
        return question
    raise HTTPException(status_code=404, detail="Quiz not found")

    # Hard Coded
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Assign a questionID       // for unit testing - DB will handle
    max_id = max([q.questionID for q in quizzes[quiz_id].questionList], default=0)
    question.questionID = max_id + 1  # Modify the input question
    quizzes[quiz_id].questionList.append(question)
    return question

# Update a question within the quiz "quiz_name"
@app.put("/quizzes/{quiz_id}/questions/{question_id}", response_model=Question)
def update_question(quiz_id: int, question_id: int, question: Question):
    # Database
    updateStatus = db_app.updateQuestion([quiz_id, question.prompt, question.durationMins, question.durationSecs, question_id])
    if(not updateStatus):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return updateStatus

    # Hard Coded
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Update questionID     // for unit testing
    for i, q in enumerate(quizzes[quiz_id].questionList):
        if q.questionID == question_id:
            question.questionID = question_id  # Preserve ID
            quizzes[quiz_id].questionList[i] = question  # Update with provided data
            return question
    raise HTTPException(status_code=404, detail="Question not found")

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
    answerList = [question_id, answer.optionNumber, answer.optDescription, answer.scoreValue]
    result = db_app.createAnswerKey(answerList, db_connection)
    if(result):
        return result
    raise HTTPException(status_code=404, detail="Question not found")

    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    quiz = quizzes[quiz_id]
    question_id_list = [q.questionID for q in quiz.questionList]
    if question_id not in question_id_list:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question = next(q for q in quiz.questionList if q.questionID == question_id)

    # Assign an optionNumber       // for unit testing - DB will handle
    max_num = max([q.optionNumber for q in question.AnswerKey], default=0)
    answer.optionNumber = max_num + 1 
    question.AnswerKey.append(answer)
    return answer

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

    # Hard Coded
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
            answer.optionNumber = optionNumber 
            question.AnswerKey[i] = answer  
            return answer
    raise HTTPException(status_code=404, detail="Answer not found")

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
    status = db_app.createCourse([course.username, course.courseName, course.courseDescription], db_connection)
    if(not status):
        raise HTTPException(status_code=500, detail="Couldn't Create a Course")
    return status

    # Hard Coded
    # Assign a quizID       // for unit testing - DB will handle
    # Note: courseID defaults to 0, and IDs start at 1 via this method
    max_id = max(courses.keys(), default=0)
    course.courseID = max_id + 1
    course.username = username
    courses[course.courseID] = course
    return course

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
    
    # Hard Coded
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    course.username = username
    course.courseID = course_id
    courses[course_id] = course
    return course

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

    # Hard Coded
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    course = courses[course_id]
    quiz = quizzes[quiz_id]
    quiz.courseID = course_id
    return course

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
    quizClassList = []
    for quiz in quizList:
        quizClassList.append(Quiz(**quiz))
    return quizClassList

    # Hard coded
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return [quiz for quiz in quizzes.values() if quiz.courseID == course_id]

# Get link to a course
@app.get("/courses/{course_id}/link", response_model=Dict[str, str])
def get_course_link(course_id: int):
    # Database
    if(db_app.retrieveFromDatabase("SELECT courseName FROM Quiz WHERE courseID = %s", [course_id], db_connection)):
        return {"link": f"http://localhost:3000/class/{course_id}"}
    raise HTTPException(status_code=404, detail="Course not found")

    # Hard coded
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"link": f"http://localhost:3000/class/{course_id}"}


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
    results = db_app.createAnalytics([quizID], db_connection)
    if(not results):
        raise HTTPException(status_code=404, detail="Quiz not found or no analytics to create for said quiz")
    return results

    return {
        'numOfResponses': 120,
        'meanScore': [2.5, 1.75, 3.0],
        'medianScore': [2, 2, 3],
        'leastCorrect': [('What is the capital of France?', 25)],
        'mostCorrect': [('2 + 2 equals?', 110)],
        'homogenous': ['Select the primary color.', 0.5],
        'heterogenous': ['Which programming language is fastest?', 2.2]
    }


""" Code for put for the responses to the quiz
    Technically could also work for post

    if(answer.attemptID == 0):
        result = db_app.processAnswer([answer.questionID, answer.optionNumber], db_connection)
        if(result):
            return result
        raise HTTPException(status_code=404, detail="Question not found")
    else:
        result = db_app.updateAnswer([answer.attemptID, answer.questionID, answer.optionNumber])
        if(result):
            return result
        raise HTTPException(status_code=404, detail="Question not found")
        """