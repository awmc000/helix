# dev notes
## Purpose of this document

- Collect concise information about things we need to do in this project
- Document how things work and what assumptions are made
    - Like a technical spec

## Table of Contents

- Plan

- Development Environment
    - Setting up
- How things work
    - Frontend HTML + JS (View Layer)
    - REST API (Business Layer)
    - Data Layer
    - Security & Encryption

## Plan

| Week          | Target            |
|---------------|-------------------|
| Week 1        | Students can do quizzes, instr can view results. |
| Week 2        | Instr can create quizzes and view analytics      |
| Week 3        | Buffer / TBD / Testing

## Development Environment
### Setting up the environment

To create a python virtual environment

```bash
python -m venv .venv
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
## How Things Work
### Frontend HTML & JS
- The frontend is contained a single page and elements are drawn 
or hidden depending on the **state** of the application.
- States include:
    - Responding to a quiz
    - Creating a quiz
    - Creating a course
- The frontend functions get data by POST and GET requests
to the API.
- They make these requests asynchronously using the Javascript
function `fetch()`.
### Rest API
- todo
### Data Layer
- The data layer is implemented as a Python module which the API can use to encapsulate interactions with the database
### Security & Encryption
- Passwords are sent to the API already unreadable.
- Encrypt with a public key, decrypt with private key
- We will backburner password encryption for now
- **Don't look at me like that, huge corporations store
passwords in plaintext!!!!**