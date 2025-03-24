# api.py (WIP)
# Author: Cassius Galdames
#
# Note: Currently set up for individual testing.
#       Will have to make additions in order to
#       properly connect and integrate with database.

from fastapi import FastAPI, HTTPException
from models import Quiz, Question, Answer
from typing import List, Dict
# import dbApplication              // will uncomment for 
# import mysql.connector            // DB integration

app = FastAPI()

# Test values:     // will replace with connection to DB
quizzes: Dict[str, Quiz] = {}  # Key: quiz name, Value: Quiz object
courses: Dict[str, List[str]] = {}  # Key: course name, Value: list of quiz names

@app.get("/")
def read_root():
    return {"message": "This is Helix API"}


# Quiz Endpoints:

# Create a quiz
@app.post("/quizzes/", response_model=Quiz)
def create_quiz(quiz: Quiz):
    if any(q.name == quiz.name for q in quizzes.values()):
        raise HTTPException(status_code=400, detail="Quiz already exists")
    
    # Assign a quizID       // for unit testing - DB will handle
    max_id = max(quizzes.keys(), default=0) 
    quiz.quizID = max_id + 1
    quizzes[quiz.quizID] = quiz
    return quiz

# Get a quiz by name
@app.get("/quizzes/{quiz_name}", response_model=Quiz)
def get_quiz(quiz_name: str):
    if quiz_name not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quizzes[quiz_name]

# Delete a quiz by name
@app.delete("/quizzes/{quiz_name}", response_model=Quiz)
def delete_quiz(quiz_name: str):
    if quiz_name not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    deleted_quiz = quizzes.pop(quiz_name)
    
    # Also delete from courses if present
    for course_quizzes in courses.values():
        if quiz_name in course_quizzes:
            course_quizzes.remove(quiz_name)
    return deleted_quiz


# Question/Answer Endpoints:

# Create a question within the quiz "quiz_name"
@app.post("/quizzes/{quiz_name}/questions/", response_model=Question)
def create_question(quiz_name: str, question: Question):
    if quiz_name not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Assign a questionID       // for unit testing - DB will handle
    max_id = max([q.questionID for q in quizzes[quiz_name].questionList], default=0)
    question.questionID = max_id + 1
    quizzes[quiz_name].questionList.append(question)
    return question

# Update a question within the quiz "quiz_name"
@app.put("/quizzes/{quiz_name}/questions/{question_id}", response_model=Question)
def update_question(quiz_name: str, question_id: int, question: Question):
    if quiz_name not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Update questionID     // for unit testing
    for i, q in enumerate(quizzes[quiz_name].questionList):
        if q.questionID == question_id:
            question.questionID = question_id
            quizzes[quiz_name].questionList[i] = question
            return question
    raise HTTPException(status_code=404, detail="Question not found")

# Delete a question within the quiz "quiz_name"
@app.delete("/quizzes/{quiz_name}/questions/{question_id}", response_model=Question)
def delete_question(quiz_name: str, question_id: int):
    if quiz_name not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    for i, q in enumerate(quizzes[quiz_name].questionList):
        if q.questionID == question_id:
            deleted_question = quizzes[quiz_name].questionList.pop(i)
            return deleted_question
    raise HTTPException(status_code=404, detail="Question not found")


# Course Endpoints:

# Create a course
@app.post("/courses/{course_name}")
def create_course(course_name: str):
    if course_name in courses:
        raise HTTPException(status_code=400, detail="Course already exists")
    courses[course_name] = []
    return {"message": f"Course {course_name} created"}

# Delete a course by name
@app.delete("/courses/{course_name}", response_model=Quiz)
def delete_course(course_name: str):
    if course_name not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    deleted_course = courses.pop(course_name)
    return deleted_course

# Add a quiz to the course "course_name"
@app.post("/courses/{course_name}/quizzes/{quiz_name}")
def add_quiz_to_course(course_name: str, quiz_name: str):
    if course_name not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    if quiz_name not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz_name not in courses[course_name]:
        courses[course_name].append(quiz_name)
    return {"message": f"Quiz {quiz_name} added to {course_name}"}

# Get quizzes in a course
@app.get("/courses/{course_name}/quizzes", response_model=List[str])
def get_course_quizzes(course_name: str):
    if course_name not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_name]
