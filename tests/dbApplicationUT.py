from unitTestFunctions import * 

if __name__ == "__main__":
    
    correct_username = os.getenv("DBUSER")
    correct_password = os.getenv("DBPASS")

    ctdUnitTest = connectToDatabase_UT("connectToDatabase", "DbApplication.py")
    ctdUnitTest.addTestCase("Correct Credentials", "correct_username", correct_password, True)
    ctdUnitTest.addTestCase("Incorrect username", "fakeusername", "fjamq72f", False)
    ctdUnitTest.addTestCase("Incorrect password", "csci375team5", "fakepassword", False)
    ctdUnitTest.addTestCase("Invalid username format", 5, "fakepassword", False)
    ctdUnitTest.addTestCase("Invalid password format", "csci375team5", None, False)
    ctdUnitTest.addTestCase("Wrong username, bad pw format", "fakeusername", 11, False)
    ctdResult = ctdUnitTest.runTestCases(verbose=True)

    database = None
    dfdUnitTest = disconnectFromDatabase_UT("disconnectFromDatabase", "DbApplication.py")
    dfdUnitTest.addTestCase("None-type database", database, False)
    database2 = db.connectToDatabase("csci375team5", "fjamq72f")
    dfdUnitTest.addTestCase("Correct Database Object Provided", database2, True)
    dfdUnitTest.addTestCase("Database was not connected", database2, False)
    dfdResult = dfdUnitTest.runTestCases(verbose=True)

    print("RESULT UT CONNECT: ", ctdResult)
    print("RESULT UT Disconnect: ", dfdResult)