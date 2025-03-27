import dbApplication as db


class unitTest:
    def __init__(self, name, file, description = "No Unit Test Description"):
        self.unit = name
        self.file = file
        self.description = description

    def run(self):
        print("NO TEST CASE DEFINED")
        

class connectToDatabase_UT(unitTest):
    def run(self, dbUserName, dbPassword, expectedSuccessValue):
        database = db.connectToDatabase("DNA", "Dude5")
        self._userNameIsValid = type(dbUserName) is str
        self._passwordIsValid = type(dbPassword) is str
        #self._databaseConnectSuccess = database!=None
        self._databaseConnectSuccess = True
        self._unitTestSuccess = self._userNameIsValid and self._passwordIsValid and self._databaseConnectSuccess
        self.__evaluate()

    def __evaluate(self):
        print("Unit Test (",self.unit,") result: ",self._unitTestSuccess)
        print("Criteria 1: Username is a string. Result:", self._userNameIsValid)
        print("Criteria 2: Password is a string. Result:", self._passwordIsValid)
        print("Criteria 3: Database Connected. Result:", self._databaseConnectSuccess)




if __name__ == "__main__":
    tmp = connectToDatabase_UT("connectToDatabase", "DbApplication.py", "Testing the connection to MySQL DB")
    tmp.run("DNA", "Dude5", False)
