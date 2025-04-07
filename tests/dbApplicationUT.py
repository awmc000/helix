# File name: dbApplicationUT.py
# Last edited by Glen on April 3rd, 2025
# Last edited by Alex on April 7th, 2025 to add import
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.models import *

# Brief: Contains a test suite for functions in dbApplication.py

'''Description:
An example of a unit test for dbApplications.py. While it is common for a unit test suite to corrospond to a particular project file, it is not necessarily the case. An individual unit test file is just meant to be a repeatable set of tests to validate that the project still works as intended. 
'''

from unitTestFunctions import * 

def ctdTests(correctUsername, correctPassword):
    ctdUnitTest = connectToDatabase_UT("connectToDatabase", "DbApplication.py")
    ctdUnitTest.addTestCase("Correct Credentials", correct_username, correct_password, True)
    ctdUnitTest.addTestCase("Reversed Credentials", correct_password, correct_username, False)
    ctdUnitTest.addTestCase("Incorrect username", "fakeusername", correct_password, False)
    ctdUnitTest.addTestCase("Incorrect password", correct_username, "fakepassword", False)
    ctdUnitTest.addTestCase("Invalid username format", 5, "fakepassword", False)
    ctdUnitTest.addTestCase("Invalid password format", correct_username, None, False)
    ctdUnitTest.addTestCase("Wrong username, bad pw format", "fakeusername", 11, False)
    ctdResult = ctdUnitTest.runTestCases(verbose=True)

def dfdTests(correctUsername, correctPassword):
    database = None
    dfdUnitTest = disconnectFromDatabase_UT("disconnectFromDatabase", "DbApplication.py")
    dfdUnitTest.addTestCase("None-type database", database, False)
    database2 = db.connectToDatabase("csci375team5", "fjamq72f")
    dfdUnitTest.addTestCase("Correct Database Object Provided", database2, True)
    dfdUnitTest.addTestCase("Database was not connected", database2, False)
    dfdResult = dfdUnitTest.runTestCases(verbose=True)

if __name__ == "__main__":
    
    correct_username = os.getenv("DBUSER")
    correct_password = os.getenv("DBPASS")
    #ctdTests(correct_username, correct_password)
    #dfdTests(correct_username, correct_password)

    database = None
    database = db.connectToDatabase(correct_username,correct_password)
    if database.is_connected():
        print("Database Is Connected.")
    else:
        print("Database Is Not Connected.")

    author = Author(username="gbeatty", name="Glen Beatty", description="Pretty Cool Guy", emailAddress="fake@email.com")
    author2 = Author(username="gbeattddfasdy", name="Glen Beatty", description="Pretty Cool Guy", emailAddress="fake@email.com")
    try: 
        db.deleteAuthor(author, database)
        print("Hello World")
    except Exception as e:
        print(e)

    try: 
        db.deleteAuthor(author, database)
        print("Hello World")

    except Exception as e:
        print(e)

    print("Does gbeatty exist?: ", db.doesAuthorExist("gbeatty", database))
    db.createAuthor(author, database)
    
    print("Does gbeatty exist now?: ", db.doesAuthorExist("gbeatty", database))
    print("Results of username lookup:", db.getAuthorByUsername("gbeatty", database))
    #print(*db.getAuthorList(database), sep="\n")
    #print("Delete #1: ",db.deleteAuthor(author, database))

    #print("Delete #2: ", db.deleteAuthor(author2,database))
