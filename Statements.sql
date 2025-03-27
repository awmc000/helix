-- New User | IMPLEMENTED - createUser

INSERT INTO Author (username, name, authorDescription, emailaddress) VALUES (%s, %s, %s, %s);

-- New Course | IMPLEMENTED - createCourse

INSERT INTO Course (username, name, courseDescription) VALUES (%s, %s, %s);

-- New Quiz | IMPLEMENTED - createQuiz

INSERT INTO Quiz (courseID, name, availableAsync, label, quizDescription, durationMinutes) VALUES (%s, %s, %s, %s, %s, %s);

-- New Question | IMPLEMENTED - createQuestion

INSERT INTO Question (quizID, prompt, durationMinutes, durationSeconds) VALUES (%s, %s, %s, %s);

-- New AnswerKey | IMPLEMENTED - createAnswerKey

INSERT INTO AnswerKey (questionID, optionNumber, optionDescription, scoreValue) VALUES (%s, %s, %s, %s);

-- New Answers | IMPLEMENTED - processAnswer

INSERT INTO Answers (questionID, optionNumber) VALUES (%s, %s) ON DUPLICATE KEY UPDATE optionNumber = VALUES(optionNumber);


-- Show Quiz Info | IMPLEMENTED - assembleQuiz

SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizID = %s;

-- Show a list of all Quizzes | IMPLEMENTED - getQuizList

SELECT quizID, quizName FROM Quiz

-- Search For Quiz By Name

SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE quizName SOUNDS LIKE %s;

-- Search For Quiz By Label

SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE label SOUNDS LIKE %s;

-- Show All quizzes in a course | IMPLEMENTED - getQuizListFromCourse

SELECT quizID, quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz WHERE courseID = %s;

-- Show All quizzes a creator made | IMPLEMENTED - getQuizListFromAuthor

SELECT quizName, availableAsync, label, quizDescription, durationMinutes FROM Quiz NATURAL JOIN Course WHERE courseID = Course.courseID AND Course.username = %s;

-- Show Question Info | IMPLEMENTED - assembleQuiz

SELECT questionID, prompt, durationMinutes, durationSeconds FROM Question WHERE quizID = %s;

-- Show Answers to the questions | IMPLEMENTED - assembleQuiz

SELECT optionNumber, optionDescription, scoreValue FROM AnswerKey WHERE questionID = %s;


-- Get the number of responses

SELECT COUNT(*) FROM Answers WHERE questionID = %s;

-- Get each score in each question

SELECT scoreValue FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;

-- Get the sum of the scores per question

SELECT SUM(scoreValue) FROM AnswerKey NATURAL JOIN Answers WHERE questionID = %s;

-- Question with fewest correct answers

WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID) SELECT MIN(correct) AS minCorrect, prompt FROM (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question JOIN correctAnswers ON Answers.attemptID = correctAnswers.attemptID JOIN Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) AS counts GROUP BY prompt;

-- Question with Most correct answers

WITH correctAnswers AS (SELECT attemptID FROM Answers NATURAL JOIN AnswerKey WHERE scoreValue > 0 GROUP BY attemptID) SELECT MAX(correct) AS maxCorrect, prompt FROM (SELECT prompt, COUNT(DISTINCT correctAnswers.attemptID) AS correct FROM Answers NATURAL JOIN Question JOIN correctAnswers ON Answers.attemptID = correctAnswers.attemptID JOIN Quiz ON Quiz.quizID = Question.quizID WHERE Quiz.quizID = %s GROUP BY prompt) AS counts GROUP BY prompt;
