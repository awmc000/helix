# Helix

## Setup
### Frontend Setup

Serve `index.html`, `style.css`, and `viewLayer.js` on
the Dolphin web server.

Make sure to clear any cached older versions of the page!

It has been in rapid development so it is essential you
are not navigating an older, cached version.

### API Setup

**The API will not run on Windows. It runs on Linux and 
whether it would work on other Unixes is unknown.**

Do the following on a cub system.

Create a python virtual environment.

```bash
python -m venv .venv
```

Enter the virtual environment.
```
source .venv/bin/activate
```

Install dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

Activate a venv such that you are "in" that venv

```bash
source .venv/bin/activate
```

### Database Setup and Launching API

Execute the contents of `Init.sql` on a MySQL database
to configure the tables.

At least one author, course, and quiz need to be made manually
using SQL queries for the application to behave.

Run commands to set `DBUSER` and `DBPASS` to a database user
and password with sufficient access before running the API.


```sh
export DBUSER='youruser'
export DBPASS='yourpass'
fastapi dev api.py
```

Finally, the host needs to be set, according to whether the
production Dolphin database or a local database is being used.

For production usage, it should be set to use Dolphin, but
if that is not the case, go to approximately line 14 in `dbApplication.py`.

It should look like this:

```python
def connectToDatabase (username, password):
    database = None
    try:
        database = mysql.connector.connect(
            # host= "dolphin.csci.viu.ca",
            host= "localhost",
            user= username,
            password= password,
            database= "csci375team5_quizdb",
            auth_plugin= "mysql_native_password"
        )
    except Error as e:
        raise Exception (e)

    return database
```

Set the host parameter to `dolphin.csci.viu.ca`, likely by
uncommenting what's already there and commenting out or removing
what you don't want to use, if it looks like above.

The instructor will be supplied credentials separately, not
part of this repository.


## If you are running the API on the same machine you are browsing on

Works as is.

## If you are running the API on a cub machine and want to access it from another

Set the global constant variable `apiAddress` in `viewLayer.js` to
the local IP plus port of whichever cub you are running the API on.

## Known Issues
- There must be at least one quiz and therefore one course
and author for the frontend to render properly.
- Login is faked out for proof of concept.
- Analytics are presented in an unpolished manner. Raw JSON is stuffed in a table.