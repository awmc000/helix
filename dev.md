# dev notes
## Purpose of this document

- Collect concise information about things we need to do in this project
- Document how things work and what assumptions are made
    - Like a technical spec

## Table of Contents

- Plan

- Development Environment
    - Setting up
- Frontend HTML + JS (View Layer)
- REST API (Business Layer)
- Data Layer
- Security & Encryption
- Information Passing Schemas
- Timers
- Metrics

## Plan

| Week          | Target            |
|---------------|-------------------|
| Week 1        | Students can do quizzes, instr can view results. |
| Week 2        | Instr can create quizzes and view analytics      |
| Week 3        | Buffer, Testing, other stretch features

## Development Environment
### Setting up the environment

To create a python virtual environment

```bash
python -m venv .venv
```

To enter a virtual environment
```
source .venv/bin/activate
```

To install everything that's in a requirements.txt

```bash
pip install -r requirements.txt
```

To activate a venv such that you are "in" that venv

```bash
source .venv/bin/activate
```


To install packages (requests is just for example)

```bash
pip install requests
```

etc.

To create a requirements.txt so that anybody can recreate the environment

```bash
pip freeze > requirements.txt
```

## Frontend HTML & JS
- The frontend is contained a single page and elements are drawn 
or hidden depending on the **screen state** of the application.
- Screen states represent:
    - Responding to a quiz
    - Creating a quiz
    - Creating a course
    - Editing instructor profile (for instructors only, naturally)
- The frontend functions get data by POST and GET requests
to the API.
- They make these requests asynchronously using the Javascript
function `fetch()`.
- There is other state information like global variables tracking
the current quiz and question.
- These global state variables will live in the `appState` global 
object to clean things up a bit.
- Until the endpoints are ready in the API, Http requests have been
marked as TODO, and interactions implemented with local data (you can
add questions but they will be gone if you refresh, etc.)
- DOM nodes / HTML tags are created, modified, and deleted by scripts, 
and they are identified by ID.
### Responding to Quizzes
- Information stored as global state includes:
    - List of available quizzes, only the info needed to fetch them.
    - A copy of the current quiz.
    - A variable tracking current question index, used for creating, editing
    and responding to quizzes.
- When the page is loaded, `setup()` is run.
- `setup()` fetches a list of available quizzes.
- Until a quiz is selected, filler text is shown.
- Once a quiz is selected and fetched, it is loaded in to be completed.
- Each time the user hits next or prev, their answer is updated by a POST request
to the API.
## Rest API

### Example Requests
#### Create Course as curl
```
curl -X POST '127.0.0.1:8000/courses/' \
  --url-query 'username=awmc2000' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "courseID": -1,
  "username": "awmc2000",
  "courseName": "Intro to Textile Arts",
  "courseDescription": "Beginner sewing and embroidery"
}'
```


## Data Layer
- The data layer is implemented as a Python module which the API can use to encapsulate interactions with the database
## Information Passing Schemas

### Python

- Dictionaries in Python are objects in JSON
- Lists in Python are lists in JSON
- Notation is very similar

```python
answer = {
    'optionNumber': -1,
    'optDescription': 'Red',
    'scoreValue': -1,
}

question = {
    'questionID': -1,
    'prompt': 'What is the first colour in the rainbow?',
    'durationMins': -1,
    'durationSecs': -1,
    'answers': [answer],
}

quiz = {
    'name': 'Preschool Graduation Exam NO RETAKES',
    'asynchronous': True,
    'label': 'quiz1',
    'description': 'A quiz of some kind',
    'durationMins': -1,
    'durationSecs': -1,
    'questionList': [question],
}
```

Analytics - schema from `dbApplication.py`

```python
result = dict(numOfResponses = count[0], meanScore = mean, medianScore = median, leastCorrect = minCorrect, mostCorrect = maxCorrect, homogenous = leastVariance, heterogenous = mostVariance)

{
    'numOfResponses': 120,
    'meanScore': [2.5, 1.75, 3.0],
    'medianScore': [2, 2, 3],
    'leastCorrect': [('What is the capital of France?', 25)],
    'mostCorrect': [('2 + 2 equals?', 110)],
    'homogenous': ['Select the primary color.', 0.5],
    'heterogenous': ['Which programming language is fastest?', 2.2]
}

```

### Javascript and JSON

The following code block outlines how quizzes, questions, and 
answers are represented in JSON. This is how they are passed
between the frontend and the API.

```js
const quiz = {
    'name': 'Preschool Graduation Exam NO RETAKES',
    'asynchronous': true,
    'label': 'quiz1',
    'description': 'A quiz of some kind',
    'durationMins': -1,
    'durationSecs': -1,
    'questionList': [
        question,        
    ]
};

const question = {
    'questionID': -1,
    'prompt': 'What is the first colour in the rainbow?',
    'durationMins': -1,
    'durationSecs': -1,
    'answers': [
        answer,
    ],
};

const answer = {
    'optionNumber': -1,
    'optDescription': 'Red',
    'scoreValue': -1,
};
```

Answers being sent from frontend to API have this form:
```js
{ 'quizID': -1, 'questionID': -1, 'choices': []} // chose nothing
{ 'quizID': -1, 'questionID': -1, 'choices': [1, 2] } // chose 1 and 2
{ 'quizID': -1, 'questionID': -1, 'choices': [1, 2, 3, 4] } // chose all
```

## Timers
- Expiry time is part of the data the frontend gets when retrieving a quiz.
- Frontend will create a timer based on this information.
- That a response is on time is checked by API after it is submitted
- A response is sent back indicating whether it is on time or too late.
- There must be a significant tolerance to allow for slow connections etc.
- Client can ping server to see if question is open?
- Whether a client is allowed to see and respond to a question could also
be determined by whether the instructor has stepped to that question
synchronously.

## Metrics
- Computed mostly (...?) by business layer
- Mean score
- Median score
- Question with fewest correct answers
- Question with most correct answers
- Questions with most homogenous answers
- Questions with most heterogenous answers