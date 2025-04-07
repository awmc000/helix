CREATE DATABASE csci375team5_quizdb;

USE csci375team5_quizdb;

DROP TABLE IF EXISTS csci375team5_quizdb.Answers;
DROP TABLE IF EXISTS csci375team5_quizdb.AnswerKey;
DROP TABLE IF EXISTS csci375team5_quizdb.Question;
DROP TABLE IF EXISTS csci375team5_quizdb.Quiz;
DROP TABLE IF EXISTS csci375team5_quizdb.Course;
DROP TABLE IF EXISTS csci375team5_quizdb.Author;

DROP TRIGGER IF EXISTS SetAttemptId;




CREATE TABLE csci375team5_quizdb.Author (
    username varchar(32),
    name varchar(128) NOT NULL,
    authorDescription varchar(1024),
    emailAddress varchar(512),
    PRIMARY KEY (username)
);

CREATE TABLE csci375team5_quizdb.Course (
    courseID int AUTO_INCREMENT,
    username varchar(32),
    courseName varchar(128) NOT NULL,
    courseDescription varchar(1024),
    PRIMARY KEY (courseID),
    FOREIGN KEY (username) REFERENCES Author(username)
);

CREATE TABLE csci375team5_quizdb.Quiz (
    courseID int,
    quizID int AUTO_INCREMENT,
    quizName varchar(128) NOT NULL,
    availableAsync bit,
    quizDescription varchar(1024),
    label varchar(256),
    durationMinutes integer,
    PRIMARY KEY (quizID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

CREATE TABLE csci375team5_quizdb.Question (
    questionID integer AUTO_INCREMENT,
    quizID integer,
    prompt varchar(1024) NOT NULL,
    durationMinutes integer,
    durationSeconds integer,
    PRIMARY KEY (questionID),
    FOREIGN KEY (quizID) REFERENCES Quiz(quizID)
);

CREATE TABLE csci375team5_quizdb.AnswerKey(
    questionID integer,
    optionNumber integer,
    optionDescription varchar(1024) NOT NULL,
    scoreValue integer,
    FOREIGN KEY (questionID) REFERENCES Question(questionID),
    PRIMARY KEY (questionID, optionNumber)
);

CREATE TABLE csci375team5_quizdb.Answers (
    attemptID int,
    questionID int,
    optionNumber integer,
    PRIMARY KEY (attemptID, questionID),
    FOREIGN KEY (questionID, optionNumber) REFERENCES AnswerKey(questionID, optionNumber)
);


INSERT INTO Author (username, name, authorDescription, emailaddress) VALUES ('scaresothers', 'Sarah Carruthers', 'Yes all of these questions are from the quizzes on VIU learn', 'Sarah.carruthers@viu.ca');

INSERT INTO Course (username, courseName, courseDescription) VALUES ('scaresothers', 'csci375', 'Systems Analysis and Design');

INSERT INTO Quiz (courseID, quizName, availableAsync, label, quizDescription, durationMinutes) VALUES (1, 'csci375 Study Guide', 1, 'review', 'Note: This quiz does not cover everything', 30);

-- Question 1
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following Activities might take place in Core Process 1?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (1, 1, 'Identifying Metrics', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (1, 2, 'Cost Benefit Analysis', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (1, 3, 'Creating A Work Breakdown Structure', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (1, 4, 'Creating an ER Diagram', 0);

-- Question 2
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which is the best example of Buisness Process Automation?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (2, 1, 'Replacing a restaurants delivery service with uber eats', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (2, 2, 'Redesigning a payment System to replace entering a pin with tap to pay', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (2, 3, 'Redesigning the cafeteria to let users order and pay ahead of time, and pickup their food', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (2, 4, 'Buying your boss a Tesla so he doesnt have to drive to work anymore', 0);

-- Question 3
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which is the best example of Buisness Process Improvement?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (3, 1, 'Replacing a restaurants delivery service with uber eats', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (3, 2, 'Redesigning a payment System to replace entering a pin with tap to pay', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (3, 3, 'Redesigning the cafeteria to let users order and pay ahead of time, and pickup their food', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (3, 4, 'Investing all of the companies profits into Dogecoin', 0);

-- Question 4
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which is the best example of Buisness Process Reengineering?', 2, 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (4, 1, 'Replacing a restaurants delivery service with uber eats', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (4, 2, 'Redesigning a payment System to replace entering a pin with tap to pay', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (4, 3, 'Redesigning the cafeteria to let users order and pay ahead of time, and pickup their food', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (4, 4, 'Renovating the employee bathroom at your workplace', 0);

-- Question 5
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following has the LEAST potential buisness value?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (5, 1, 'Improvement', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (5, 2, 'Automation', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (5, 3, 'Reengineering', 0);

-- Question 6
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following has a MODERATE amount of potential buisness value?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (6, 1, 'Improvement', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (6, 2, 'Automation', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (6, 3, 'Reengineering', 0);

-- Question 7
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following has the MOST potential buisness value?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (7, 1, 'Improvement', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (7, 2, 'Automation', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (7, 3, 'Reengineering', 1);

-- Question 8
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What does an information System include that an application doesnt?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (8, 1, 'Buisness Rules', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (8, 2, 'Code', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (8, 3, 'People', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (8, 4, 'Hardware and Networks', 1);

-- Question 9
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'The Six Core Processes get done exactly once for most projects', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (9, 1, 'True', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (9, 2, 'False', 1);

-- Question 10
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following is System Analysis?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (10, 1, 'Learning what the system needs to do', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (10, 2, 'Describing how the system works', 0);

-- Question 11
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which is the best example for an organizational risk', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (11, 1, 'A risk that affects the development teams company', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (11, 2, 'A risk that comes from poor code quality', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (11, 3, 'A risk that comes from losing the USB stick the system was on', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (11, 4, 'A risk affecting the client or their organization', 1);

-- Question 12
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which is NOT an example of a Technological Risk', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (12, 1, 'The user cannot use the application because the font is too small', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (12, 2, 'The development team has very little expertise working in the field', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (12, 3, 'The userbase has very little experience using computers ', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (12, 4, 'Crowdstrike gets hit with another cyber attack, cauing another outage', 0);

-- Question 13
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following is NOT a resource risk', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (13, 1, 'The program leaks memory faster than someone at a dementia care home', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (13, 2, 'Running out of toilet paper in the staff washroom', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (13, 3, 'Being short staffed', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (13, 4, 'Making a user of the system lose all their work', 0);

-- Question 14
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following is NOT a type of risk coping', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (14, 1, 'Deal With it', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (14, 2, 'Share', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (14, 3, 'Mitigate', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (14, 4, 'Divert', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (14, 5, 'Eliminate', 0);

-- Question 15
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'A Producer-Consumer Model is a model where the user has to pay to use the service', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (15, 1, 'True', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (15, 2, 'False', 1);

-- Question 16
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following is not a type of non-functional Requirement?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (16, 1, 'Performance', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (16, 2, 'Security', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (16, 3, 'Interface', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (16, 4, 'Efficiency', 1);

-- Question 17
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What are the Es of Usability', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (17, 1, 'Ease of Use, Effectiveness, Efficiency, Error Tolerant, Enagaging', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (17, 2, 'Ease of Use, Elegant, Efficiency, Error Tolerant, Engaging', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (17, 3, 'Ease of Use, Elegant, Effectiveness, Efficiency, Error Tolerant', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (17, 4, 'Ease of Use, Elegant, Effectiveness, Efficiency, Engaging', 0);

-- Question 18
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following is NOT true for requirements', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (18, 1, 'They should be kept at a high level', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (18, 2, 'They should be presented as a statement', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (18, 3, 'They should state how things are done', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (18, 4, 'They are the things the system must do', 0);

-- Question 19
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What is a feature in the context of system analysis?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (19, 1, 'Something the system has to do to function', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (19, 2, 'A function of the system', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (19, 3, 'A part of the system that helps a user complete their goals', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (19, 4, 'A distinctive attribute of the system', 0);

-- Question 20
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Each use case can only be done by one type of user', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (20, 1, 'True', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (20, 2, 'False', 1);

-- Question 21
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which of the following is NOT a valid use case phrase', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (21, 1, 'Eat Quiz', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (21, 2, 'Take Out Trash', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (21, 3, 'Go visit my grandma because she has cancer', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (21, 4, 'Sleep in a Cardboard Box', 0);

-- Question 22
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What does the giant box represent in a use case diagram', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (22, 1, 'The system', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (22, 2, 'The environment', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (22, 3, 'The use case', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (22, 4, 'The user', 0);

-- Question 23
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What is stored inside the giant box in the use case diagram', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (23, 1, 'The system', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (23, 2, 'The use case(s)', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (23, 3, 'The user(s)', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (23, 4, 'The steps to complete each use case', 0);

-- Question 24
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What are domain objects?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (24, 1, 'The systems, applications or UIs that are used in your system', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (24, 2, 'The things that the users of your system use on a daily basis', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (24, 3, 'The things that the user thinks about when interacting with your system', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (24, 4, 'The things that the users think about when working on their tasks', 1);

-- Question 25
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'How do you create domain objects?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (25, 1, 'List all nouns from usecases, eliminate duplicates, remove any non system/UI elements', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (25, 2, 'List all nouns from usecases, choose only the ones that appear more than once and are System/UI elements', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (25, 3, 'List all nouns from usecases, choose only the ones that appear more than once and are not System/UI elements', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (25, 4, 'List all nouns from usecases, eliminate duplicates, remove any system/UI elements', 1);

-- Question 26
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What is represented in a System Sequence Diagram?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (26, 1, 'The sequence in which each function is called in the program', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (26, 2, 'The communication between the client and the system', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (26, 3, 'The sequence of steps the user has to do to use the program', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (26, 4, 'The state of the systems memory at each specifed time point', 0);

-- Question 27
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'Which is NOT represented in a design class diagram?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (27, 1, 'Primary Keys', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (27, 2, 'The visability of the data', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (27, 3, 'The data types of the data', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (27, 4, 'The relationships between objects', 0);

-- Question 28
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What case are the class diagrams written in?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (28, 1, 'camelCase', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (28, 2, 'PascalCase', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (28, 3, 'snake_case', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (28, 4, 'kebab-case', 0);

-- Question 29
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What is the point of controller classes?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (29, 1, 'To abstract away the methods from the attributes in the Design class diagram', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (29, 2, 'To create the methods to carry out the usecases using the attributes of the Design Class Diagram', 1);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (29, 3, 'To connect the data layer to the buisness layer', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (29, 4, 'To connect the view layer to the buisness layer', 0);

-- Question 30
INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (1, 'What is not in an ER diagram?', 2, 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (30, 1, 'Primary / Foriegn Keys', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (30, 2, 'Relationships between the tables of data', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (30, 3, 'The datatypes of each data point', 0);
INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (30, 4, 'The data itself', 1);