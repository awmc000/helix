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
let currentQuestionIndex = 0;

// Current state
const TAKING_QUIZ                   = 0;
const CREATING_QUIZ                 = 1;
const CREATING_COURSE               = 2;
const EDITING_INSTRUCTOR_PROFILE    = 3;

let windowState = TAKING_QUIZ;

let currentQuizIndex = -1;

var quiz;
var question;
var availableQuizzes;
var availableCourses = [
    {
        'courseID': 1,
        'name': '(Placeholder Course)',
        'description': 'A course for quizzes to be part of until creation of courses' +
        ' is implemented.',
    }
]

let course = availableCourses[0];

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
    quiz = loadFullQuiz(1);

    question = quiz.questionList[0];

    // Draw question answer screen from first quiz loaded?
    extractQuestionData();

    // Set elements according to initial state
    setStateElements();
};

/*
 * Shows and hides elements to match the current windowState.
 */
const setStateElements = () => {
    if (windowState == TAKING_QUIZ) {
        showManyById(['availableQuizMapDiv', 'question']);
        hideManyById(['quizmap', 'editquestion', 'coursemap', 'editcourse', 'instructorprofile']);
    }
    else if (windowState == CREATING_QUIZ) {
        showManyById(['availableQuizMapDiv', 'quizmap', 'editquestion']);
        hideManyById(['question', 'coursemap', 'editcourse', 'instructorprofile']);
        drawQuestionMap();
    }
    else if (windowState == CREATING_COURSE) {
        showManyById(['coursemap', 'editcourse']);
        hideManyById(['availableQuizMapDiv', 'question', 'quizmap', 'editquestion', 'instructorprofile']);
        drawCourseMap();
        fillCourseEditingForm();
    } 
    else if (windowState == EDITING_INSTRUCTOR_PROFILE) {
        showById('instructorprofile');
        hideManyById(['availableQuizMapDiv', 'question', 'quizmap', 'editquestion', 'coursemap', 'editcourse']);
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

/*
 * Takes a list of IDs, removes the display property from all.
 * I believe this would make them show *unless* they had a tag
 * style to hide..?
 */
const showManyById = (ids) => {
    for (const id of ids) {
        showById(id);
    }
}

/* ======================================================================================
 * Hardcoded Test Data, to be removed and fetched from API as soon as possible
 * ====================================================================================== */

// Hardcoded dummy objects for test purposes
// More interesting dummy data generated with ChatGPT
let answer1 = {
    'optionNumber': 1,
    'optDescription': 'Red',
    'scoreValue': 1,
};

let answer2 = {
    'optionNumber': 2,
    'optDescription': 'Blue',
    'scoreValue': 0,
};

let answer3 = {
    'optionNumber': 3,
    'optDescription': 'Green',
    'scoreValue': 0,
};

let answer4 = {
    'optionNumber': 4,
    'optDescription': 'Yellow',
    'scoreValue': 0,
};

let question1 = {
    'questionID': 1,
    'prompt': 'What is the first color in the rainbow?',
    'durationMins': 1,
    'durationSecs': 30,
    'answers': [
        answer1, answer2, answer3, answer4
    ],
};

let question2 = {
    'questionID': 2,
    'prompt': 'What is the capital of France?',
    'durationMins': 1,
    'durationSecs': 30,
    'answers': [
        {
            'optionNumber': 1,
            'optDescription': 'Berlin',
            'scoreValue': 0,
        },
        {
            'optionNumber': 2,
            'optDescription': 'Madrid',
            'scoreValue': 0,
        },
        {
            'optionNumber': 3,
            'optDescription': 'Paris',
            'scoreValue': 1,
        },
        // {
        //     'optionNumber': 4,
        //     'optDescription': 'Rome',
        //     'scoreValue': 0,
        // }
    ],
};

let question3 = {
    'questionID': 3,
    'prompt': 'Which planet is known as the Red Planet?',
    'durationMins': 1,
    'durationSecs': 0,
    'answers': [
        {
            'optionNumber': 1,
            'optDescription': 'Earth',
            'scoreValue': 0,
        },
        {
            'optionNumber': 2,
            'optDescription': 'Mars',
            'scoreValue': 1,
        },
        {
            'optionNumber': 3,
            'optDescription': 'Jupiter',
            'scoreValue': 0,
        },
        {
            'optionNumber': 4,
            'optDescription': 'Venus',
            'scoreValue': 0,
        }
    ],
};

let quiz1 = {
    'quizID': 1,
    'name': 'General Knowledge Quiz',
    'asynchronous': true,
    'label': 'quiz1',
    'description': 'A simple general knowledge quiz.',
    'durationMins': 5,
    'durationSecs': 0,
    'questionList': [
        question1,
        question2,
        question3,
    ]
};

let quiz2 = {
    'quizID': 2,
    'name': 'Periodic Table Quiz',
    'asynchronous': true,
    'label': 'quiz2',
    'description': 'A quiz about space and science.',
    'durationMins': 4,
    'durationSecs': 30,
    'questionList': [
        {
            'questionID': 1,
            'prompt': 'What is the chemical symbol for water?',
            'durationMins': 1,
            'durationSecs': 15,
            'answers': [
                {
                    'optionNumber': 1,
                    'optDescription': 'H2O',
                    'scoreValue': 1,
                },
                {
                    'optionNumber': 2,
                    'optDescription': 'CO2',
                    'scoreValue': 0,
                },
                {
                    'optionNumber': 3,
                    'optDescription': 'O2',
                    'scoreValue': 0,
                },
                {
                    'optionNumber': 4,
                    'optDescription': 'NaCl',
                    'scoreValue': 0,
                }
            ]
        },
        {
            'questionID': 2,
            'prompt': 'What is the chemical symbol for gold?',
            'durationMins': 1,
            'durationSecs': 15,
            'answers': [
                {
                    'optionNumber': 1,
                    'optDescription': 'AU',
                    'scoreValue': 1,
                },
                {
                    'optionNumber': 2,
                    'optDescription': 'K',
                    'scoreValue': 0,
                },
                {
                    'optionNumber': 3,
                    'optDescription': 'Go',
                    'scoreValue': 0,
                },
                {
                    'optionNumber': 4,
                    'optDescription': 'Cl',
                    'scoreValue': 0,
                }
            ]
        }
    ]
};

const quizzes = [
    quiz1,
    quiz2,
];

const loadFullQuiz = (id) => {
    currentQuestionIndex = 0;
    for (const availableQuiz of quizzes) {
        if (availableQuiz.quizID == id) {
            // Set global to this quiz, and return it
            quiz = availableQuiz;
            return quiz;
        }
    }
};


/* ======================================================================================
 * API Interactions - Functions that actually hit endpoints with `fetch()`
 * ====================================================================================== */

/*
 * Returns a list of quizzes available to do.
 * The object fetched from the API is a list of partial/abbreviated
 * quiz objects. It is of the form:
 * [
 *  {'quizID': 1, 'name': 'quiz 1', 'label': 'easy', 'description': 'some kind of quiz'},
 * ]
 */
const getAvailableQuizzes = () => {
    // TODO: Retrieve from API
    // Currently stubbed out to use test data!
    console.log('(getAvailableQuizzes) TODO: GET request for available quizzes')
    let re = [];

    for (quiz of quizzes) {
        re.push({
            'quizID': quiz.quizID,
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
    availableQuizzes.forEach((quizInfo) => {
        let anchorTag = document.createElement('a');
        anchorTag.href = '#';
        anchorTag.innerText = quizInfo.name;
        anchorTag.title = quizInfo.description;

        let lineBreak = document.createElement('br');

        // Onclick function for each li is a fetch function for the corresponding quizID
        anchorTag.onclick = () => fetchQuizById(quizInfo.quizID);

        document.getElementById('availableQuizMapList').appendChild(anchorTag);
        document.getElementById('availableQuizMapList').appendChild(lineBreak);
    });
};

const viewAnalytics = () => {
    console.log('(viewAnalytics) TODO: Create and implement analytics window')
};

/*
 * Create a new question in the quiz and reload question map to contain it.
 */
const addQuestion = () => {
    console.log('(addQuestion) TODO: Make POST request to add a question. Currently creating locally!');

    // Get last ID and increment it
    // TODO: This is a temporary hack. IDs should be generated by the database.!
    let newID = quiz.questionList[quiz.questionList.length - 1].questionID + 1;

    let newQuestion = {
        'questionID': newID,
        'prompt': 'New Question',
        'durationMins': 999,
        'durationSecs': 0,
        'answers': [
            {
                'optionNumber': 1,
                'optDescription': 'New Choice',
                'scoreValue': -1,
            },
            {
                'optionNumber': 2,
                'optDescription': 'New Choice',
                'scoreValue': -1,
            },
            {
                'optionNumber': 3,
                'optDescription': 'New Choice',
                'scoreValue': -1,
            },
            {
                'optionNumber': 4,
                'optDescription': 'New Choice',
                'scoreValue': -1,
            },
        ],
    };

    console.log(newQuestion);

    quiz.questionList.push(newQuestion);

    drawQuestionMap();
};

const attachQuizActions = () => {
    
    let listItemTag = document.createElement('li');
    let anchorTag = document.createElement('a');
    anchorTag.href = '#';
    anchorTag.innerText = 'View analytics';
    anchorTag.onclick = viewAnalytics;
    listItemTag.appendChild(anchorTag);
    document.getElementById('questionMapList').appendChild(listItemTag);

    listItemTag = document.createElement('li');
    anchorTag = document.createElement('a');
    anchorTag.href = '#';
    anchorTag.innerText = 'Add question';
    anchorTag.onclick = addQuestion;
    listItemTag.appendChild(anchorTag);
    document.getElementById('questionMapList').appendChild(listItemTag);

};

/*
 * Draws the list of items in a quiz for quiz editing screen.
 */
const drawQuestionMap = () => {
    // Destroy any existing children of .questionMapList
    document.getElementById('questionMapList').innerHTML = '';

    quiz.questionList.forEach((question) => {
        let listItemTag = document.createElement('li');
        let anchorTag = document.createElement('a');
        anchorTag.href = '#';
        anchorTag.innerText = question.questionID;

        console.log('(drawQuestionMap) attaching go-to-question closure with ID ' + question.questionID);
        let gotoFunction = () => goToEditQuestion(question.questionID); 
        anchorTag.onclick = gotoFunction;
        listItemTag.appendChild(anchorTag);

        document.getElementById('questionMapList').appendChild(listItemTag);
    });
    attachQuizActions();
};

/*
 * Populates the forum in the quiz editing screen with current values.
 */
const fillQuestionEditingForm = () => {
    document.getElementById("editQuestionID").value = question.questionID;
    document.getElementById("editQuestionPrompt").value = question.prompt;

    let letters = ['A', 'B', 'C', 'D'];
    for (let i = 0; i < question.answers.length && i < 4; i++) {
        document.getElementById('choice' + letters[i] + 'Prompt').value = question.answers[i].optDescription;
        document.getElementById('choice' + letters[i] + 'Value').value = question.answers[i].scoreValue;
    }
};

const fillCourseQuizzes = () => {
    document.getElementById('courseQuizList').innerHTML = '';
    
    availableQuizzes.forEach((quizInfo) => {
        // li tag, with <a> inside
        let listItemTag = document.createElement('li');
        let anchorTag = document.createElement('a');
        anchorTag.href = '#';
        anchorTag.innerText = quizInfo.name;
        anchorTag.title = quizInfo.description;

        // Onclick function for each li is a fetch function for the corresponding quizID
        anchorTag.onclick = () => fetchQuizById(quizInfo.quizID);
        listItemTag.appendChild(anchorTag);
        document.getElementById('courseQuizList').appendChild(listItemTag);
    });
};

const fillCourseEditingForm = () => {
    document.getElementById('editCourseName').value = course.name;
    document.getElementById('editCourseDescription').value = course.description;

    fillCourseQuizzes();
};

const updateQuestionEdit = () => {
    console.log('(updateQuestionEdit) TODO: Send POST request with updated question ' + question.questionID);
    let editedID = document.getElementById('editQuestionID').innerText;
    let editedPrompt = document.getElementById('editQuestionPrompt').innerText;
    
    let editedChoiceA = document.getElementById('choiceAPrompt').innerText;
    let editedChoiceB = document.getElementById('choiceBPrompt').innerText;
    let editedChoiceC = document.getElementById('choiceCPrompt').innerText;
    let editedChoiceD = document.getElementById('choiceDPrompt').innerText;

    let editedValueA = document.getElementById('choiceAValue').innerText;
    let editedValueB = document.getElementById('choiceBValue').innerText;
    let editedValueC = document.getElementById('choiceCValue').innerText;
    let editedValueD = document.getElementById('choiceDValue').innerText;

    // TODO: Fudging the duration for now!

    let newQuestion = {
        'quizID': editedID,
        'prompt': editedPrompt,
        'durationMins': 999,
        'durationSecs': 0,
        'answers': [
            {
                'optionNumber': 1,
                'optDescription': editedChoiceA,
                'scoreValue': editedValueA,
            },
            {
                'optionNumber': 2,
                'optDescription': editedChoiceB,
                'scoreValue': editedValueB,
            },
            {
                'optionNumber': 3,
                'optDescription': editedChoiceC,
                'scoreValue': editedValueC,
            },
            {
                'optionNumber': 4,
                'optDescription': editedChoiceD,
                'scoreValue': editedValueD,
            },
        ],
    }

};

/*
 * Draws the nav list of courses. Will probably require a function
 * to hit the course list endpoint...
 */
const drawCourseMap = () => {
    document.getElementById('courseMapList').innerHTML = '';
    availableCourses.forEach((course) => {
        let listItemTag = document.createElement('li');
        let anchorTag = document.createElement('a');
        anchorTag.href = '#';
        anchorTag.innerText = course.name;
        listItemTag.appendChild(anchorTag);
        document.getElementById('courseMapList').appendChild(listItemTag);
    });
};

/*
 *
 */
const goToEditQuestion = (id) => {
    for (const q of quiz.questionList) {
        if (q.questionID == id) {
            question = q;
        }
    }
    fillQuestionEditingForm();
};

/*
 * Sets the global quiz and question variables to point to the quiz
 * selected in the dropdown menu.
 */
const fetchQuizById = (targetQuiz) => {
    console.log('(fetchQuizById) TODO: GET request to get quiz ' + targetQuiz);
    quiz = loadFullQuiz(targetQuiz);
    question = quiz.questionList[0];
    drawQuestionMap();
    extractQuestionData();
};
/*
 * Submits the answer to a question with a POST request. Overwrites any
 * previous submitted answer, allowing changing of responses.
 */
const submitQuestionAnswer = () => {
    let report = reportCheckboxes();
    console.log('(submitQuestionAnswer) TODO: POST request with answer "' 
    + report.choices + '" on "' + report.questionID + '" on quiz ' + quiz.quizID);
};

/* 
 * Fills in the page with current question's fields.
 * Will draw up to 4 choices for question answer.
 */
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

    // Hide all the buttons
    let buttons = ['choicediva', 'choicedivb', 'choicedivc', 'choicedivd']; 
    hideManyById(buttons);

    // Show the ones for which there is an answer
    for (let i = 0; i < question.answers.length && i < 4; i++) {
        showById(buttons[i]);
        document.getElementById(buttons[i]).getElementsByTagName('label')[0].innerText = question.answers[i].optDescription;
    }
};

/*
 * Returns an object containing the questionID and checked multi choice options.
 * Return value is of the form : { 'quiz': quizID, 'questionID': questionID }
 */
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

    // TODO: Change from quiz.label to quiz.quizID!
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

/*
 * Move to next question in current quiz, looping back to zero if at end.
 */
const nextQuestion = () => {
    reportCheckboxes();
    submitQuestionAnswer();
    clearCheckboxes();
    currentQuestionIndex = (currentQuestionIndex + 1) % quiz.questionList.length;
    question = quiz.questionList[currentQuestionIndex];
    extractQuestionData();
};

/*
 * Move to prev question in currnt quiz, staying put if at beginning.
 */
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
 * API Access Test - will only work on campus!
 * ====================================================================================== */

// IP address and port of `fastapi run api.py` running on a cub
let apiAddress = "http://192.168.18.42:8000/";

/*
 * Fetches some kind of data from API root endpoint and displays it in
 * dataplace span element.
 */
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
    {
        'label': 'setup: availableQuizzes not empty',
        'func': () => {
            return availableQuizzes.length > 0;
        },
    },
    {
        'label': 'setup: a question is loaded automtically',
        'func': () => {
            return question.prompt;
        },
    },
    {
        'label': 'drawQuizMap: quiz map is generated (has >0 quizzes)',
        'func': () => {
            return document.getElementById('availableQuizMapList').childNodes.length > 0;
        },
    },
    {
        'label': 'attachQuizActions: works',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'drawQuestionMap: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'fillQuestionEditingForm: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'fillCourseQuizzes: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'fillCourseEditingForm: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'updateQuestionEdit: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'drawCoursemap: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'goToEditQuestion: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'fetchQuizById: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'submitQuestionAnswer: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'extractQuestionData: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'reportCheckboxes: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'clearCheckboxes: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'nextQuestion: TODO, write test(s)',
        'func': () => {
            return false;
        },
    },
    {
        'label': 'prevQuestion: TODO, write test(s)',
        'func': () => {
            return false;
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
