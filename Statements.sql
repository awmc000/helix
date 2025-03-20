-- New User

INSERT INTO Author (name, authorDescription, emailaddress) VALUES (%s, %s, %s);

-- New Course

INSERT INTO Course (username, name, courseDescription) VALUES (%s, %s, %s);

-- New Quiz

INSERT INTO Quiz (courseID, name, availableAsync, label, quizDescription, durationMinutes) VALUES (%s, %s, %s, %s, %s, %s);

-- New Question

INSERT INTO Question (quizID, prompt, wasAsked, durationMinutes, durationSeconds) VALUES (%s, %s, 0, %s, %s);

-- New AnswerKey

INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (%s, %s, %s, %s);

-- New Answers

INSERT INTO Answers (questionID, optionNumber) VALUES (%s, %s);


-- Show Quiz Info

SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizID = %s;

-- Search For Quiz By Name

SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizName SOUNDS LIKE %s;

-- Show All quizzes in a course

SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE courseID = %s;

-- Show All quizzes a creator made

SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE courseID = Course.courseID AND Course.username = %s;

-- Show Question Info | IMPLEMENTED - assembleQuiz

SELECT questionID, prompt, wasAsked, durationMinutes, durationSeconds FROM Question WHERE quizID = %s;

-- Show Answers to the questions | IMPLEMENTED - assembleQuiz

SELECT optionNumber, optionDescription, scoreValue FROM AnswerKey WHERE questionID = %s;

