# models.py (WIP)
# Author: Cassius Galdames
#
# Note: Based on the Quiz, Question, & Answer 
#       Dictionaries by Trevor in the Discord.

from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    optionNumber: int
    optDescription: str
    scoreValue: int

class Question(BaseModel):
    questionID: int
    prompt: str
    wasAsked: bool
    durationMins: int
    durationSecs: int
    Answers: List[Answer]

class Quiz(BaseModel):
    quizID: int
    name: str
    asynchronous: bool
    label: str
    description: str
    durationMins: int
    questionList: List[Question]
