# models.py (WIP)
# Author: Cassius Galdames 
#    

from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    optionNumber: int = 0
    description: str = ""
    scoreValue: int = 0

class Question(BaseModel):
    questionID: int = 0
    prompt: str = ""
    durationMins: int = 0
    durationSecs: int = 0
    answers: List[Answer] = []

class Quiz(BaseModel):
    quizID: int = 0
    courseID: int = 0
    quizName: str = ""
    availableAsync: bool = False
    label: str = ""
    quizDescription: str = ""
    durationMins: int = 0
    questionList: List[Question] = []

class Course(BaseModel):
    courseID: int = 0
    username: str
    courseName: str = ""
    courseDescription: str = ""

class Author(BaseModel):
    username: str
    name: str = ""
    description: str = ""
    emailAddress: str = ""
