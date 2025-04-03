import sys
import os 

sys.path.append("..")

import dbApplication as db

class unitTest:
    def __init__(self, testName, file):
        self.testName = testName
        self.file = file
        self.testCases = []
        self.numTestCases = 0
    
    def _lineBreak(self, char, qty = 100):
        line = ""
        for x in range(qty):
            line = line + char
        print(line)


class connectToDatabase_UT(unitTest):
    def runTestCase(self, caseName, dbUsername, dbPassword, expectedSuccessValue, verbose = False):
        
        usernameIsValid = type(dbUsername) is str
        passwordIsValid = type(dbPassword) is str
        database = None
        errors = []
        try:
            database = db.connectToDatabase(dbUsername, dbPassword)
        except Exception as e:
            errors.append(e)
        databaseConnectSuccess = database!=None
        if(databaseConnectSuccess):
            db.disconnectFromDatabase(database)
        unitTestSuccess = usernameIsValid and passwordIsValid and databaseConnectSuccess
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
        return unitTestSuccess == expectedSuccessValue

            
    def addTestCase(self, name, userName, password, expectedSuccess):
        self.numTestCases += 1
        self.testCases.append([self.numTestCases,name,userName,password,expectedSuccess,])


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


