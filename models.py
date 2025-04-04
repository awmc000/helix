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

'''
{
    'numOfResponses': 120,
    'meanScore': [2.5, 1.75, 3.0],
    'medianScore': [2, 2, 3],
    'leastCorrect': [('What is the capital of France?', 25)],
    'mostCorrect': [('2 + 2 equals?', 110)],
    'homogenous': ['Select the primary color.', 0.5],
    'heterogenous': ['Which programming language is fastest?', 2.2]
}

'''
class Analytics(BaseModel):
    quizID: int = 0
    numOfResponses: int = 0
    meanScore: List[float] = []
    leastCorrect: List = []
    mostCorrect: List = []
    homogenous: List = []
    heterogenous: List = []
