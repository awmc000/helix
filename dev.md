# dev notes
## Purpose of this document

- Collect concise information about things we need to do in this project
- Document how things work and what assumptions are made
    - Like a technical spec

## Table of Contents

- Development Environment
    - Setting up

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


To install packages

```bash
pip fastapi[standard]
pip requests
```

etc.

To create a requirements.txt so that anybody can recreate the environment

```bash
pip freeze > requirements.txt
```