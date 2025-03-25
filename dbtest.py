import dbApplication as db

# Connect/disconnect to database test
#Invlaid

database = db.connectToDatabase("DNA", "Dude5")

print(database)

if(database):
    db.disconnectFromDatabase(database)
else: print("\n\nTest1 Passed\n\n")

#valid
username = "you"
password = "wish"

database = db.connectToDatabase(username, password)

print(database)

db.disconnectFromDatabase(database)

if(database):
    print("\n\nTest2 Passed\n\n")

# updateDatabase tests

database = db.connectToDatabase(username, password)

# Invalid Data
values = []
if(not db.updateDatabase("INSERT INTO Author (username, name, authorDescription, emailaddress) VALUES (%s, %s, %s, %s);", values, database)):
    print("\n\nTest3 Passed\n\n")

# Valid Data
values = ["user", "name", "desc", "email"]
if(db.updateDatabase("INSERT INTO Author (username, name, authorDescription, emailaddress) VALUES (%s, %s, %s, %s);", values, database)):
    print("\n\nTest4 Passed\n\n")

# Duplicate Data
if(not db.updateDatabase("INSERT INTO Author (username, name, authorDescription, emailaddress) VALUES (%s, %s, %s, %s);", values, database)):
    print("\n\nTest5 Passed\n\n")

# Invalid FK reference
values = ["username", "name", "desc"]
if(not db.updateDatabase("INSERT INTO Course (username, courseName, courseDescription) VALUES (%s, %s, %s);", values, database)):
    print("\n\nTest6 Passed\n\n")

# Valid FK reference
values = ["user", "name", "desc"]
if(db.updateDatabase("INSERT INTO Course (username, courseName, courseDescription) VALUES (%s, %s, %s);", values, database)):
    print("\n\nTest7 Passed\n\n")

# retrieveFromDB tests
# TO DO
