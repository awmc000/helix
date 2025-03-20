/*
 * viewLayer.js
 *
 * Functions used in the frontend / user interface.
 * 
 */

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
  
// Global variable: current question
let question = {
    prompt: 'Hit the next arrow to start the quiz.',
    title: 'Quiz',
};

// Current question index
let currentQuestion = -1;

// TODO: Retrieve this from the API with the fetch() function!
const quiz = [
    {
        prompt: 'What is the first colour in the rainbow?',
        title: 'Question 1',
        type: 'paragraph',
    },
    {
        prompt: 'What is the second colour in the rainbow?',
        title: 'Question 2',
        type: 'multipleChoice',
    },
    {
        prompt: 'What is the third colour in the rainbow?',
        title: 'Question 3',
        type: 'multipleChoice',
    },
    {
        prompt: 'What is the fourth colour in the rainbow?',
        title: 'Question 4',
        type: 'paragraph',
    },
];

// Fills in the page with current question's fields.
const extractQuestionData = () => {
    // Set prompt and title
    document.getElementById('questionprompt').innerText = question.prompt;
    document.getElementById('questiontitle').innerText = question.title;

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
    currentQuestion = (currentQuestion + 1) % quiz.length;
    question = quiz[currentQuestion];
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

document.addEventListener("keydown", handleKeypress);