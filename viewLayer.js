/*
* viewLayer.js
*
* Functions used in the frontend / user interface.
* 
*/

/* ======================================================================================
 * Global Variables
 * ====================================================================================== */

// Current question index in list
let currentQuestionIndex = -1;

// Current state
const TAKING_QUIZ                   = 0;
const CREATING_QUIZ                 = 1;
const CREATING_COURSE               = 2;
const EDITING_INSTRUCTOR_PROFILE    = 3;

let windowState = TAKING_QUIZ;

let currentQuizIndex = -1;

var quiz;
var availableQuizzes;

/* ======================================================================================
 * State-Related Functions, Hiding/Showing Elements, Etc.
 * ====================================================================================== */

/* 
 * Entry point called on body load.
 * Sets up global pointer variables, etc.
 */
const setup = () => {
    // Load available quizzes
    availableQuizzes = getAvailableQuizzes();

    // Create quiz map from the quizzes loaded
    drawQuizMap();

    // Set current quiz to first of them
    quiz = loadFullQuiz(availableQuizzes[0]);

    // Draw question answer screen from first quiz loaded?
    extractQuestionData();

    // Set elements according to initial state
    setStateElements();
};

const setStateElements = () => {
    if (windowState == TAKING_QUIZ) {
        showById('question');
        hideManyById(['quizmap', 'editquestion', 'coursemap', 'editcourse', 'instructorprofile']);
    }
    else if (windowState == CREATING_QUIZ) {
        showManyById(['quizmap', 'editquestion']);
        hideManyById(['question', 'coursemap', 'editcourse', 'instructorprofile']);
    }
    else if (windowState == CREATING_COURSE) {
        showManyById(['coursemap', 'editcourse']);
        hideManyById(['question', 'quizmap', 'editquestion', 'instructorprofile']);
    } 
    else if (windowState == EDITING_INSTRUCTOR_PROFILE) {
        showById('instructorprofile');
        hideManyById(['question', 'quizmap', 'editquestion', 'coursemap', 'editcourse']);
    }
}

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

/* ======================================================================================
 * Hardcoded Test Data, to be removed and fetched from API as soon as possible
 * ====================================================================================== */

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

let quiz1 = {
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

let quiz2 = {
    'name': 'Test2',
    'asynchronous': true,
    'label': 'quiz2',
    'description': 'A quiz of some kind',
    'durationMins': -1,
    'durationSecs': -1,
    'questionList': [
        question1,
        question2,
        question3,
    ]
};

const quizzes = [
    quiz1,
    quiz2,
];

const loadFullQuiz = (label) => {
    return quizzes[0];
};

const getAvailableQuizzes = () => {
    // TODO: Retrieve from API
    // Currently stubbed out to use test data!
    console.log('(getAvailableQuizzes) TODO: GET request for available quizzes')
    let re = [];

    for (quiz of quizzes) {
        re.push({
            'name': quiz.name,
            'label': quiz.label,
            'description': quiz.description,
        });
    }

    return re;
};

/*
 * Assuming availableQuizzes have already been fetched,
 * draws the drop down list of them. 
 */
const drawQuizMap = () => {
    for (const quizInfo of availableQuizzes) {
        // option tag, value=quizInfo.label, inner text = name + desc.
        let optionTag = document.createElement('option');
        optionTag.value = quizInfo.label;
        optionTag.innerText = quizInfo.name + ': ' + quizInfo.description;
        document.getElementById('quizselect').appendChild(optionTag);
    }
};

const drawCourseMap = () => {

};


// Fills in the page with current question's fields.
const extractQuestionData = () => {
    // Set prompt and title
    document.getElementById('pagetitle').innerText = quiz.name;
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

    report = { 'quiz': quiz.label, 'questionID': question.questionID, choices: report}

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
    submitQuestionAnswer();
    clearCheckboxes();
    currentQuestionIndex = (currentQuestionIndex + 1) % quiz.questionList.length;
    question = quiz.questionList[currentQuestionIndex];
    extractQuestionData();
};

const prevQuestion = () => {
    if (currentQuestionIndex <= 0) {
        return;
    }
    reportCheckboxes();
    clearCheckboxes();
    currentQuestionIndex = currentQuestionIndex - 1;
    question = quiz.questionList[currentQuestionIndex];
    extractQuestionData();
};

/* ======================================================================================
 * Keyboard Controls
 * ====================================================================================== */

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

/* ======================================================================================
 * API Access Test
 * ====================================================================================== */

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

/* ======================================================================================
 * Unit Testing
 * ====================================================================================== */

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
            return reportCheckboxes().choices == '';
        },
    },
    {
        'label': 'reportCheckboxes: one case',
        'func': () => {
            nextQuestion();
            nextQuestion();

            clearCheckboxes();
            document.getElementById('choicec').checked = true;
            return reportCheckboxes().choices == 'C';
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
            return reportCheckboxes().choices == 'ABCD';
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

const fetchQuiz = () => {
    let targetQuiz = document.getElementById('quizselect').value;
    console.log('(fetchQuiz) TODO: GET request to get quiz ' + targetQuiz);
    loadFullQuiz(targetQuiz);
};

const submitQuestionAnswer = () => {
    let report = reportCheckboxes();
    console.log('(submitQuestionAnswer) TODO: POST request with answer "' 
    + report.choices + '" on "' + report.questionID + '"');
};