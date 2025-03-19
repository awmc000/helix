import mysql.connector
from mysql.connector import Error

# Opens a connection to the database
# Requires no Parameters
# Returns the database connection object
def connectToDatabase ():

    loggedIn = False
    while(not loggedIn):
        print("Enter your database username: ")
        username = input()
        print("Enter your password: ")
        password = input()

        try:
            database = mysql.connector.connect(
                host= "localhost",
                user= username,
                password= password,
                database= "csci375team5_quizdb"
            )
        except Error as e:
            print("Error: {e}")

        loggedIn = True

    return database

# Closes the connection from the database
# Requires a database object as a paramater
# Returns nothing
def disconnectFromDatabase (database):
    database.close()

# Retrieves data from the database coresponding to the sql query it is fed
# sqlQuery is the Sql query to be executed
# params is the list of parameters to the sql query (if any)
# database is the database connection
# Returns the result set if successful, otherwise nothing
def retrieveFromDatabase (sqlQuery, params, database):
    
    try:
        if(database.isConnected()):
            cursor = database.cursor()
            cursor.execute(sqlQuery, params)
            return cursor.fetchall()
        
        return None

    except Error as e:
        print("Error: {e}")
        return None

    finally:
        cursor.close()

# Updates the values to the database according to the sqlQuery (added / removed)
# sqlQuery is the Sql query to be executed
# values is the list of values to be updated in the database
# database is the database connection
# Returns True if sucessful, otherwise None
def updateDatabase (sqlQuery, values, database):
    try:
        if(database.isConnected()):
            cursor = database.cursor
            cursor.execute(sqlQuery, values)
            database.commit()
            cursor.close()
            return True
        return None
        
    except Error as e:
        print("Error: {e}")


        