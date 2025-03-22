/*
* viewLayer.js
*
* Functions used in the frontend / user interface.
* 
*/

// Current question index
let currentQuestion = -1;

// Current state
const TAKING_QUIZ                   = 0;
const CREATING_QUIZ                 = 1;
const CREATING_COURSE               = 2;
const EDITING_INSTRUCTOR_PROFILE    = 3;

let state = TAKING_QUIZ;

const hideById = (id) => {
    document.getElementById(id).style.display = 'none';
};

const hideManyById = (ids) => {
    for (const id of ids) {
        hideById(id);
    }
}

const showById = (id) => {
    document.getElementById(id).style.display = 'unset';
}

const showManyById = (ids) => {
    for (const id of ids) {
        showById(id);
    }
}

const setStateElements = () => {
    if (state == TAKING_QUIZ) {
        showById('question');
        hideManyById(['quizmap', 'editquestion', 'coursemap', 'editcourse', 'instructorprofile']);
    }
    else if (state == CREATING_QUIZ) {
        showManyById(['quizmap', 'editquestion']);
        hideManyById(['question', 'coursemap', 'editcourse', 'instructorprofile']);
    }
    else if (state == CREATING_COURSE) {
        showManyById(['coursemap', 'editcourse']);
        hideManyById(['question', 'quizmap', 'editquestion', 'instructorprofile']);
    } 
    else if (state == EDITING_INSTRUCTOR_PROFILE) {
        showById('instructorprofile');
        hideManyById(['question', 'quizmap', 'editquestion', 'coursemap', 'editcourse']);
    }
}

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
    document.getElementById('questiontitle').innerText = 'Question #' + question.questionID;
    
    // Disable / enable appropriate response area divs
    if (question.questionID != 0) {
        document.getElementById('paragraphresponse').style.display = 'none';
        document.getElementById('multiplechoiceresponse').style.display = 'flex';
    } else {
        document.getElementById('paragraphresponse').style.display = 'none';
        document.getElementById('multiplechoiceresponse').style.display = 'none';
    }
};

// Returns a string containing the checked multi choice options.
const reportCheckboxes = () => {
    let report = '';

    if (document.getElementById('choicea').checked)
        report += 'A';
    if (document.getElementById('choiceb').checked)
        report += 'B';
    if (document.getElementById('choicec').checked)
        report += 'C';
    if (document.getElementById('choiced').checked)
        report += 'D';

    console.log(report);
    return report;
};

// Unchecks all multi choice options to prepare for next question.
const clearCheckboxes = () => {
    document.getElementById('choicea').checked = false;
    document.getElementById('choiceb').checked = false;
    document.getElementById('choicec').checked = false;
    document.getElementById('choiced').checked = false;
};

const nextQuestion = () => {
    reportCheckboxes();
    clearCheckboxes();
    currentQuestion = (currentQuestion + 1) % quiz.questionList.length;
    question = quiz.questionList[currentQuestion];
    extractQuestionData();
};

const prevQuestion = () => {
    if (currentQuestion <= 0) {
        return;
    }
    reportCheckboxes();
    clearCheckboxes();
    currentQuestion = currentQuestion - 1;
    question = quiz.questionList[currentQuestion];
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

/*
 * View layer unit tests:
 * List of labels and functions returning true or false.
 * Results printed to a table in the dev area.
 */
const tests = [
    {
        'label': 'Question is initially filler text',
        'func': () => {
            return document.getElementById('questionprompt').innerText == 'Press next > to start the quiz.';
        },
    },
    {
        'label': 'Checkboxes are cleared when going to next question',
        'func': () => {
            nextQuestion();
            nextQuestion();

            if (document.getElementById('choicea').checked)
                return false;
            if (document.getElementById('choiceb').checked)
                return false;
            if (document.getElementById('choicec').checked)
                return false;
            if (document.getElementById('choiced').checked)
                return false;
            return true;
        },
    },
    {
        'label': 'reportCheckboxes: none case',
        'func': () => {
            nextQuestion();
            nextQuestion();

            clearCheckboxes();
            return reportCheckboxes() == '';
        },
    },
    {
        'label': 'reportCheckboxes: one case',
        'func': () => {
            nextQuestion();
            nextQuestion();

            clearCheckboxes();
            document.getElementById('choicec').checked = true;
            return reportCheckboxes() == 'C';
        },
    },
    {
        'label': 'reportCheckboxes: four case',
        'func': () => {
            nextQuestion();
            nextQuestion();

            clearCheckboxes();
            document.getElementById('choicea').checked = true;
            document.getElementById('choiceb').checked = true;
            document.getElementById('choicec').checked = true;
            document.getElementById('choiced').checked = true;
            return reportCheckboxes() == 'ABCD';
        },
    },
];

const runTests = () => {
    let i = 0;
    for (const test of tests) {
        let testFunction = test.func;
        let res = testFunction();

        let tdLabel = document.createElement('td');
        tdLabel.innerText = i++ + '. ' + test.label;
        tdLabel.style.fontStyle = 'italic';

        let tdRes = document.createElement('td');
        tdRes.innerText = res ? 'PASS' : 'FAIL';
        tdRes.style.backgroundColor = res ? 'lightgreen' : 'red';

        let trTest = document.createElement('tr');
        trTest.appendChild(tdLabel);
        trTest.appendChild(tdRes);

        document.getElementById('testtable').appendChild(trTest);
    }
};

const submitQuestionForm = (e) => {
    console.log('submitQuestionForm:' + e);
};