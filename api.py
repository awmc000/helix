# api.py (WIP)
# Author: Cassius Galdames
#
# Note: Currently set up for individual testing.
#  

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware # uncomment for UI integration
from contextlib import asynccontextmanager #This is for ensuring the database connection is opened on startup and closed before shutdown
from models import Answer, Question, Quiz, Course, Author
from typing import List, Dict
import os
import dbApplication as db_app
# import mysql.connector            // DB integration

db_connection = None

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
    return db_app.createQuiz(quiz.__dict__, db_connection)

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

    print(quiz_id)
    
    quiz = Quiz(**db_app.assembleQuiz([quiz_id], db_connection))
    return quiz

    # Hard Coded
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quizzes[quiz_id]

# Delete a quiz by ID
@app.delete("/quizzes/{quiz_id}", response_model=Quiz)
def delete_quiz(quiz_id: int):
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    deleted_quiz = quizzes.pop(quiz_id)
    return deleted_quiz

# Edit a quiz by ID
@app.put("/quizzes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: int, quiz: Quiz):
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz.quizID = quiz_id
    quizzes[quiz_id] = quiz
    return quiz

# Get all quizzes as a list
@app.get("/quizzes/", response_model=List[Quiz])
def get_all_quizzes():
    
    quizList = db_app.getQuizList(db_connection)
    quizClassList = []
    for quiz in quizList:
        quizClassList.append(Quiz(**quiz))
    return quizClassList
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
    question.questionID = db_app.createQuestion(temp.__dict__, db_connection)
    return question

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
@app.put("/quizzes/{quiz_id}/questions/{question_id}/answers/", response_model=Answer)
def update_answer(
    quiz_id: int,
    question_id: int, 
    optionNumber: int, 
    answer: Answer
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
            answer.optionNumber = optionNumber 
            question.AnswerKey[i] = answer  
            return answer
    raise HTTPException(status_code=404, detail="Answer not found")

# Delete an answer within the question "question_id"
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
    # Assign a quizID       // for unit testing - DB will handle
    # Note: courseID defaults to 0, and IDs start at 1 via this method
    max_id = max(courses.keys(), default=0)
    course.courseID = max_id + 1
    course.username = username
    courses[course.courseID] = course
    return course

# Edit a course by ID
@app.put("/courses/{course_id}", response_model=Course)
def update_course(
    course_id: int, 
    course: Course,
    username: str = Query(..., description="Username of the creator")
):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    course.username = username
    course.courseID = course_id
    courses[course_id] = course
    return course

# Delete a course by ID
@app.delete("/courses/{course_id}", response_model=Course)
def delete_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses.pop(course_id)

# Add a quiz to a course
@app.post("/courses/{course_id}/quizzes/{quiz_id}", response_model=Course)
def add_quiz_to_course(course_id: int, quiz_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    course = courses[course_id]
    quiz = quizzes[quiz_id]
    quiz.courseID = course_id
    return course

# Remove a quiz from a course
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
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return [quiz for quiz in quizzes.values() if quiz.courseID == course_id]

# Get link to a course
@app.get("/courses/{course_id}/link", response_model=Dict[str, str])
def get_course_link(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"link": f"http://localhost:3000/class/{course_id}"}


# Author Endpoints:

# Create an author entry
@app.post("/authors/", response_model=Author)
def create_author(author: Author):
    return author

# Delete an author entry
@app.delete("/authors/{username}", response_model=dict)
def delete_author(username: str):
    return {"message": f"Author {username} deleted"}
