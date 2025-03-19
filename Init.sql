CREATE DATABASE csci375team5_quizdb;

USE csci375team5_quizdb

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
    wasAsked bit,
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
    PRIMARY KEY (questionID, attemptID),
    FOREIGN KEY (questionID, optionNumber) REFERENCES AnswerKey(questionID, optionNumber)
);

DELIMITER //

CREATE TRIGGER SetAttemptId 
BEFORE INSERT ON Answers
FOR EACH ROW
BEGIN
    DECLARE attemptCount INT;
    SELECT COUNT(questionID) into attemptCount FROM Answers WHERE questionID = NEW.questionID;
    SET NEW.attemptID = attemptCount + 1;
END;

//

DELIMITER ;