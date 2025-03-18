CREATE DATABASE csci375team5_quizdb;

DROP TABLE csci375team5_quizdb.Answer;
DROP TABLE csci375team5_quizdb.AnswerKey;
DROP TABLE csci375team5_quizdb.Question;
DROP TABLE csci375team5_quizdb.Quiz;
DROP TABLE csci375team5_quizdb.Course;
DROP TABLE csci375team5_quizdb.Author;




CREATE TABLE csci375team5_quizdb.Author (
    authorID int,
    name varchar(128) NOT NULL,
    authorDescription varchar(1024),
    emailaddress varchar(512),
    PRIMARY KEY (authorID)
);

CREATE TABLE csci375team5_quizdb.Course (
    courseID int,
    authorID int,
    courseName varchar(128) NOT NULL,
    courseDescription varchar(1024),
    PRIMARY KEY (courseID),
    FOREIGN KEY (authorID) REFERENCES Author(authorID)
);

CREATE TABLE csci375team5_quizdb.Quiz (
    courseID int,
    quizID int,
    courseName varchar(128) NOT NULL,
    availableAsync bit,
    quizDescription varchar(1024),
    label varchar(256),
    durationMinutes integer,
    PRIMARY KEY (quizID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID)
);

CREATE TABLE csci375team5_quizdb.Question (
    questionID integer,
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

CREATE TABLE csci375team5_quizdb.Answer (
    attemptID int,
    questionID int,
    optionNumber integer,
    PRIMARY KEY (questionID, attemptID),
    FOREIGN KEY (questionID, optionNumber) REFERENCES AnswerKey(questionID, optionNumber)
);