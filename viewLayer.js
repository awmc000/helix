/*
* viewLayer.js
*
* Functions used in the frontend / user interface.
* 
*/

// Global variable: current question
// let question = {
//     prompt: 'Hit the next arrow to start the quiz.',
//     title: 'Quiz',
// };

// Current question index
let currentQuestion = -1;

// Current state
const TAKING_QUIZ                   = 0;
const CREATING_QUIZ                 = 1;
const CREATING_COURSE               = 2;
const EDITING_INSTRUCTOR_PROFILE    = 3;

let state = TAKING_QUIZ;

// Hardcoded dummy objects for test purposes
let answer = {
    'optionNumber': -1,
    'optDescription': 'Red',
    'scoreValue': -1,
};

let question = {
    'questionID': 0,
    'prompt': 'Press next > to start the quiz.',
    'durationMins': -1,
    'durationSecs': -1,
    'answers': [
        answer,
    ],
};


let question1 = {
    'questionID': 1,
    'prompt': 'What is the first colour in the rainbow?',
    'durationMins': -1,
    'durationSecs': -1,
    'answers': [
        answer,
    ],
};

let question2 = {
    'questionID': 2,
    'prompt': 'What is the first colour in the rainbow?',
    'durationMins': -1,
    'durationSecs': -1,
    'answers': [
        answer,
    ],
};

let question3 = {
    'questionID': 3,
    'prompt': 'What is the first colour in the rainbow?',
    'durationMins': -1,
    'durationSecs': -1,
    'answers': [
        answer,
    ],
};

const quiz = {
    'name': 'Preschool Graduation Exam NO RETAKES',
    'asynchronous': true,
    'label': 'quiz1',
    'description': 'A quiz of some kind',
    'durationMins': -1,
    'durationSecs': -1,
    'questionList': [
        question1,
        question2,
        question3,
    ]
};


// Fills in the page with current question's fields.
const extractQuestionData = () => {
    // Set prompt and title
    document.getElementById('questionprompt').innerText = question.prompt;
    document.getElementById('questiontitle').innerText = question.questionID;
    
    // Disable / enable appropriate response area divs
    if (question.type == 'paragraph') {
        document.getElementById('paragraphresponse').style.display = 'block';
        document.getElementById('multiplechoiceresponse').style.display = 'none';
    }
    else if (question.type == 'multipleChoice') {
        document.getElementById('paragraphresponse').style.display = 'none';
        document.getElementById('multiplechoiceresponse').style.display = 'block';
    }
};

const nextQuestion = () => {
    currentQuestion = (currentQuestion + 1) % quiz.questionList.length;
    question = quiz.questionList[currentQuestion];
    extractQuestionData();
};

const prevQuestion = () => {
    if (currentQuestion <= 0) {
        return;
    }
    currentQuestion = currentQuestion - 1;
    question = quiz[currentQuestion];
    extractQuestionData();
};

// Go to prev page on left arrow press or next page on right arrow press.
const handleKeypress = (e) => {
    console.log(e.code);
    if (e.code == 'ArrowLeft') {
        prevQuestion();
    }
    else if (e.code == 'ArrowRight') {
        nextQuestion();
    }
};

// Add key press event listener to allow keyboard navigation
document.addEventListener("keydown", handleKeypress);

// API Access Test
let apiAddress = "http://192.168.18.42:8000/";

async function fetchData() {
    const url = apiAddress;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        
        const json = await response.json();
        console.log(json);
        document.getElementById('dataplace').innerText = JSON.stringify(json);
    } catch (error) {
        console.error(error.message);
    }
}