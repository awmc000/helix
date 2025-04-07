# File name: unitTestFunctions.py
# Last edited by Glen on April 3rd, 2025

# Brief: Contains classes necessary to create suites of unit tests. 

''' Description:
This file contains the classes and functions necessary to create and run suites of unit tests. This file is not meant to be called directly and does not contain a main method. 

Classes and methods will be called in separate unit test files. For example, a set of tests meant to validate the functionality of dbApplications.py is contained in dbApplicationUT.py. The goal of this structure is to allow unit tests to be easily compartmentalized. A series of tests could be used to test a particular file or component of the application. A larger test could be constructed to validate all functionality on the server-side and could be run before major updates are pushed. 

A base unitTest class is defined and then extended upon for each unit test. Where possible, each derived class of unitTest corrosponds to a particular function or class that is being tested. 
'''

# Necessary to obtain system username/password and to include files from parent directory.
import sys

sys.path.append("..")

from data import dbApplication as db


# Base unitTest class. Typically not used directly.
class unitTest:

    # Called to initialize unitTest object. 
    # Param testName is the name of the unit test.
    # param file is the file containing the unit being tested (eg: dbApplication.py)
    def __init__(self, testName, file):

        self.testName = testName
        self.file = file

        # Empty list to contain all test cases for a particular unit test.
        self.testCases = []
        self.numTestCases = 0 # Tracks how many cases there are. 
    
    # Print function to allow for (hopefully) readable output.
    # Param char is simply the character to be printed.
    # Param qty is the number of times the char should be printed, which defaults to 100.
    def _lineBreak(self, char, qty = 100):
        line = ""
        for x in range(qty):
            line = line + char
        print(line)


# ***** Begin unit tests for dbApplication.py *****

# Unit test class for connectToDatabase function.
class connectToDatabase_UT(unitTest):

    # runTestCase function runs an individual test case, based on the provided paramaters. This method can be called directly to test an individual test case, but is also called to test all test cases by runTestCases method.

    # Param caseName is the name of the test case (eg: "Bad password").
    # Param dbUsername is the username to test.
    # Param dbPassword is the password to test.
    # Param expectedSuccessValue is the expected outcome of the test. For example, a correct username and password would be expected to return true.
    # Param verbose specifies whether the detailed results of the test should be printed. If this argument is omitted or a false value specified, only brief results will be printed. 

    def runTestCase(self, caseName, dbUsername, dbPassword, expectedSuccessValue, verbose = False):
        
        # Verify that username and password are of the correct type (string).
        usernameIsValid = type(dbUsername) is str
        passwordIsValid = type(dbPassword) is str

        #Initialize database to None type and create empty list to store errors. 
        database = None
        errors = []

        # Try to connect to the database.
        try:
            database = db.connectToDatabase(dbUsername, dbPassword)

        # If dbApplication.py throws an exception, store it.
        except Exception as e:
            errors.append(e)

        # Boolean to store whether the database connected successfully or not. 
        databaseConnectSuccess = database!=None

        # If DB connected, we need to disconnect as well.
        if(databaseConnectSuccess):
            db.disconnectFromDatabase(database)
        
        # Determine the total success value of this test case (only true if all tests pass)
        unitTestSuccess = usernameIsValid and passwordIsValid and databaseConnectSuccess

        # Print the results of the test case
        self._lineBreak('*')
        print("Testing case:", caseName,) 
        if(unitTestSuccess == expectedSuccessValue):
            print("Test passed (expected", expectedSuccessValue," - Result:",unitTestSuccess,")")
        else:
            print("Test failed (expected", expectedSuccessValue," - Result:",unitTestSuccess,")")

        if(verbose):  
            print("\tCriteria 1: Username is a string. Result:", usernameIsValid)
            print("\tCriteria 2: Password is a string. Result:", passwordIsValid)
            print("\tCriteria 3: Database Connected. Result:", databaseConnectSuccess,"\n")
            if(len(errors)>0):
                print("\tRaised Errors:")
                for e in errors:
                    print("\t-", e)

        # Return true if the test case result matched the expected result. This still returns true if a test was expected to fail and did fail. Similarly, if a test was expected to fail and passed false is returned.
        return unitTestSuccess == expectedSuccessValue

    # addTestCase function adds a testCase to be tested later using runTestCases function. 
    # Param name is a name assigned to a given test case, and is used to identify the result of each test case.
    def addTestCase(self, name, userName, password, expectedSuccess):
        self.numTestCases += 1
        self.testCases.append([self.numTestCases,name,userName,password,expectedSuccess,])

    # Helper function, primarily used in development of test case suites. Is not called when running individual or series of test cases.
    def printTestCases(self):
        self._lineBreak("^")
        print("Printing all test cases for unit test:", self.testName)
        print(*self.testCases, sep="\n")

    # Function used to call all test cases previously added using the addTestCase method.
    # Param verbose specifices whether brief or long-form results should be printed.
    def runTestCases(self, verbose = False):
        self._lineBreak('=')
        print("Running", self.numTestCases, "test cases for unit test:",self.testName)
        self._lineBreak('=')

        numPassedTests = 0
        for case in self.testCases:
            if(self.runTestCase(case[1],case[2],case[3],case[4], verbose)):
                numPassedTests+=1
        print("")
        print("Results for Unit Test",self.testName,": Passed",numPassedTests,"of",self.numTestCases,"test cases.")
        self._lineBreak("-")
        print("\n")
        if(numPassedTests<self.numTestCases):
            return False
        else:
            return True

class disconnectFromDatabase_UT(unitTest):

    def runTestCase(self, caseName, database, expectedSuccessValue, verbose = False):
        
        errors = []
        disconnectSuccess = False
        try:
            disconnectSuccess= db.disconnectFromDatabase(database)
        except Exception as e:
            errors.append(e)
        unitTestSuccess = disconnectSuccess
        self._lineBreak('*')
        print("Testing case:", caseName,) 
        if(unitTestSuccess == expectedSuccessValue):
            print("Test passed (expected", expectedSuccessValue," - Result:",unitTestSuccess,")")
        else:
            print("Test failed (expected", expectedSuccessValue," - Result:",unitTestSuccess,")")

        if(verbose):  
                print("\tCriteria 1: Database disconnected. Result:", disconnectSuccess)
                if(len(errors)>0):
                    print("\tRaised Errors:")
                    for e in errors:
                        print("\t-", e)
        return unitTestSuccess == expectedSuccessValue

            
    def addTestCase(self,name, database, expectedSuccess):
        self.numTestCases += 1
        self.testCases.append([self.numTestCases,name,database,expectedSuccess,])


    def printTestCases(self):
        self._lineBreak("^")
        print("Printing all test cases for unit test:", self.testName)
        print(*self.testCases, sep="\n")

    def runTestCases(self, verbose = False):
        self._lineBreak('=')
        print("Running", self.numTestCases, "test cases for unit test:",self.testName)
        self._lineBreak('=')

        numPassedTests = 0
        for case in self.testCases:
            if(self.runTestCase(case[1],case[2],case[3], verbose)):
                numPassedTests+=1
        print("")
        print("Results for Unit Test",self.testName,": Passed",numPassedTests,"of",self.numTestCases,"test cases.")
        self._lineBreak("-")
        print("\n")
        if(numPassedTests<self.numTestCases):
            return False
        else:
            return True


