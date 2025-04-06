/*
 * viewLayer.js
 *
 * Functions used in the frontend / user interface.
 *
 */

/* ======================================================================================
 * Global Variables
 * ====================================================================================== */

// Current state
const TAKING_QUIZ = 0;
const CREATING_QUIZ = 1;
const CREATING_COURSE = 2;
const EDITING_INSTRUCTOR_PROFILE = 3;
const LOADING = 4;

// TODO: API address is localhost in dev,
// should be address of a cub where api is running in prod
let apiAddress = "http://127.0.0.1:8000/";

var availableQuizzes;
var availableCourses;

let appState = {
  windowState: TAKING_QUIZ,
  currentQuestionIndex: 0,
  quiz: null,
  question: null,
  course: null,
  loggedIn: false,
  loginUsername: null,
  loginToken: null,
  currentAttempt: null,
};

/* ======================================================================================
 * State-Related Functions, Hiding/Showing Elements, Etc.
 * ====================================================================================== */

/*
 * Entry point called on body load.
 * Sets up global pointer variables, etc.
 */
const setup = async () => {
  // Load available courses
  availableCourses = await getAvailableCourses();

  // Select first one to start with
  appState.course = availableCourses[0];

  // Load available quizzes
  availableQuizzes = await getAvailableQuizzes();

  // Create quiz map from the quizzes loaded
  drawQuizMap();

  // Initial state is TAKING_QUIZ
  goToTakingQuiz();
};

/*
 * Function for changing screen to taking quiz
 */
const goToTakingQuiz = () => {
  appState.windowState = TAKING_QUIZ;
  setStateElements();
};

/*
 * Function for changing screen to creating quiz
 */
const goToCreatingQuiz = () => {
  if (appState.loginUsername == null) {
    alert('You need to log in first before accessing instructor menus.');
    return;
  }
  appState.windowState = CREATING_QUIZ;
  setStateElements();
};

/*
 * Function for changing screen to creating course
 */
const goToCreatingCourse = () => {
  if (appState.loginUsername == null) {
    alert('You need to log in first before accessing instructor menus.');
    return;
  }
  appState.windowState = CREATING_COURSE;
  setStateElements();
};

/*
 * Function for changing screen to instructor profile
 */
const goToInstructorProfile = () => {
  appState.windowState = EDITING_INSTRUCTOR_PROFILE;
  setStateElements();
};

/*
 * Shows and hides elements to match the current windowState.
 */
const setStateElements = () => {
  if (appState.windowState == TAKING_QUIZ) {
    showManyById(["availableQuizMapDiv", "question"]);
    hideManyById([
      "loadingbox",
      "quizmap",
      "editQuiz",
      "editquestion",
      "coursemap",
      "editcourse",
      "analytics",
      "instructorLogin",
      "instructorprofile",
    ]);

    // When entering the state, clear any response from before
    clearCheckboxes();
    if (appState.quiz != null) loadFullQuiz(appState.quiz.quizID);

    extractQuestionData();
  } else if (appState.windowState == CREATING_QUIZ) {
    showManyById([
      "availableQuizMapDiv",
      "quizmap",
      "editQuiz",
      "editquestion",
      "analytics",
    ]);
    hideManyById([
      "loadingbox",
      "question",
      "coursemap",
      "editcourse",
      "instructorLogin",
      "instructorprofile",
    ]);
    drawQuestionMap();
  } else if (appState.windowState == CREATING_COURSE) {
    showManyById(["coursemap", "editcourse"]);
    hideManyById([
      "loadingbox",
      "availableQuizMapDiv",
      "question",
      "quizmap",
      "editQuiz",
      "editquestion",
      "analytics",
      "instructorLogin",
      "instructorprofile",
    ]);
    drawCourseMap();
    fillCourseEditingForm();
    fillCourseQuizzes();
  } else if (appState.windowState == EDITING_INSTRUCTOR_PROFILE) {
    if (appState.loggedIn == false) {
      showById("instructorLogin");
      hideById("instructorprofile");
    } else {
      showById("instructorprofile");
      hideById("instructorLogin");
    }
    hideManyById([
      "availableQuizMapDiv",
      "question",
      "quizmap",
      "editQuiz",
      "editquestion",
      "coursemap",
      "editcourse",
    ]);
  }
};

const hideById = (id) => {
  document.getElementById(id).style.display = "none";
};

/*
 * Takes a list of IDs, sets the display property to `none` to hide them all.
 */
const hideManyById = (ids) => {
  for (const id of ids) {
    hideById(id);
  }
};

const showById = (id) => {
  document.getElementById(id).style.display = "unset";
};

/*
 * Takes a list of IDs, removes the display property from all.
 * I believe this would make them show *unless* they had a tag
 * style to hide..?
 */
const showManyById = (ids) => {
  for (const id of ids) {
    showById(id);
  }
};

const loadFullQuiz = (id) => {
  appState.currentQuestionIndex = 0;
  for (const availableQuiz of availableQuizzes) {
    if (availableQuiz.quizID == id) {
      // Set global to this quiz, and return it
      appState.quiz = availableQuiz;
      appState.question = appState.quiz.questionList[0];
      return appState.quiz;
    }
  }
};

const logIn = () => {

  if (document.getElementById('instructorLoginUsername').value == "") {
    alert('Please at least pretend to log in man');
    return;
  }

  console.log("Fake logging in: setting username and token to dummy values.");
  appState.loggedIn = true;
  appState.loginUsername = "awmc2000";
  appState.loginToken = "FakeToken";

  document.getElementById("instructorUsername").value = appState.loginUsername;

  setStateElements();
};

const logOut = () => {
  console.log("Fake logging out: setting username and token to null.");
  appState.loggedIn = false;
  appState.loginUsername = null;
  appState.loginToken = null;
  setStateElements();
};

/* ======================================================================================
 * API Interactions - Functions that actually hit endpoints with `fetch()`
 * ====================================================================================== */

/*
 * Wrapper for `fetch()` that makes HTTP requests to the API
 * Makes requests to the same API address, so does not take address, just endpoint
 *
 * Endpoint: Path to follow URL.
 * For 127.0.0.1:800/hello/world This would be "hello/world".
 * useMethod: All caps method name eg. "GET", "POST", "DELETE".
 * useBody: Object eg.:
 *      {
 *          "courseID": -1,
 *          "username": "awmc2000",
 *          "courseName": "Intro to Textile Arts",
 *          "courseDescription": "Beginner sewing and embroidery"
 *      }
 * useParams: Object eg.:
 *      { "username": "awmc2000" }
 */
const makeRequest = async (endpoint, useMethod, useBody, useParams) => {
  console.log(
    "Making " +
      useMethod +
      " request to endpoint " +
      endpoint +
      " with following body and params",
  );
  console.log(useBody);
  console.log(useParams);

  let url = new URL(apiAddress + endpoint);

  // Add parameters to URL
  for (const [k, v] of Object.entries(useParams)) {
    url.searchParams.append(k, v);
  }

  // Make request
  try {
    const response = await fetch(url, {
      method: useMethod,
      body: useBody != null ? JSON.stringify(useBody) : undefined,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Handle potential error
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();

    return json;
  } catch (error) {
    console.error(error.message);
  }
};

/*
 * Returns a list of quizzes available to do.
 * The object fetched from the API is a list of partial/abbreviated
 * quiz objects. It is of the form:
 * [
 *  {'quizID': 1, 'name': 'quiz 1', 'label': 'easy', 'description': 'some kind of quiz'},
 * ]
 */
const getAvailableQuizzes = async () => {
  return await makeRequest("quizzes", "GET", null, { username: "awmc2000" });
};

const getAvailableCourses = async () => {
  return await makeRequest("courses", "get", null, {});
};

/*
 * Assuming availableQuizzes have already been fetched,
 * draws the drop down list of them.
 */
const drawQuizMap = () => {
  document.getElementById("availableQuizMapList").innerText = "";

  availableQuizzes.forEach((quizInfo) => {
    console.log("something")
    console.log(quizInfo)
    let anchorTag = document.createElement("a");
    anchorTag.href = "#";
    anchorTag.innerText = quizInfo.quizName;
    anchorTag.title = quizInfo.quizDescription;

    let lineBreak = document.createElement("br");

    // Onclick function for each li is a fetch function for the corresponding quizID
    anchorTag.onclick = () => fetchQuizById(quizInfo.quizID);

    document.getElementById("availableQuizMapList").appendChild(anchorTag);
    document.getElementById("availableQuizMapList").appendChild(lineBreak);
  });
};

const generateAnalytics = async () => {
  let analytics = await makeRequest(
    "analytics/" + appState.quiz.quizID,
    "GET",
    null,
    { username: appState.loginUsername },
  );
  console.log(analytics);

  let tableObject = document.createElement("table");

  for (const [k, v] of Object.entries(analytics)) {
    let row = document.createElement("tr");
    let keyTd = document.createElement("td");
    let valTd = document.createElement("td");

    keyTd.innerText = k;
    valTd.innerText = v;

    row.appendChild(keyTd);
    row.appendChild(valTd);
    tableObject.appendChild(row);
  }

  document.getElementById("analyticsBody").innerText = "";
  document.getElementById("analyticsBody").appendChild(tableObject);
};

const viewAnalytics = () => {
  document.getElementById("analyticsTitle").innerText =
    'Analytics of quiz "' + appState.quiz.quizName + '"';
  generateAnalytics();
};

/*
 * Create a new question in the quiz and reload question map to contain it.
 */
const addQuestion = async () => {
  let newQuestionDraft = {
    questionID: -1, // ID will be generated by backend and contained in the response
    prompt: "Sample question",
    durationMins: 5,
    durationSecs: 0,
    answers: [
      {
        optionNumber: 1,
        description: "Sample answer 1",
        scoreValue: 1,
      },
      {
        optionNumber: 2,
        description: "Sample answer 2",
        scoreValue: 0,
      },
      {
        optionNumber: 3,
        description: "Sample answer 3",
        scoreValue: 0,
      },
      {
        optionNumber: 4,
        description: "Sample answer 4",
        scoreValue: 0,
      },
    ],
  };

  // Send to API, then add *what we get back* to the local list.
  let newQuestion = await makeRequest(
    "quizzes/" + appState.quiz.quizID + "/questions",
    "POST",
    newQuestionDraft,
    {},
  );

  appState.quiz.questionList.push(newQuestion);

  drawQuestionMap();
};

/*
 * Add the buttons to view analytics and create a question to the
 * buttons shown in the Creating Quiz screen.
 */
const attachQuizActions = () => {
  let listItemTag = document.createElement("li");
  let anchorTag = document.createElement("a");
  anchorTag.href = "#";
  anchorTag.innerText = "View analytics";
  anchorTag.onclick = viewAnalytics;
  listItemTag.appendChild(anchorTag);
  document.getElementById("questionMapList").appendChild(listItemTag);

  listItemTag = document.createElement("li");
  anchorTag = document.createElement("a");
  anchorTag.href = "#";
  anchorTag.innerText = "Add question";
  anchorTag.onclick = addQuestion;
  listItemTag.appendChild(anchorTag);
  document.getElementById("questionMapList").appendChild(listItemTag);
};

/*
 * Draws the list of items in a quiz for quiz editing screen.
 */
const drawQuestionMap = () => {
  // Destroy any existing children of .questionMapList
  document.getElementById("questionMapList").innerHTML = "";

  if (appState.quiz == null) {
    document.getElementById("questionMapList").innerText = "No quiz selected.";
    return;
  }

  appState.quiz.questionList.forEach((question) => {
    let listItemTag = document.createElement("li");
    let anchorTag = document.createElement("a");
    anchorTag.href = "#";
    anchorTag.innerText = question.questionID;

    console.log(
      "(drawQuestionMap) attaching go-to-question closure with ID " +
        question.questionID,
    );
    let gotoFunction = () => goToEditQuestion(question.questionID);
    anchorTag.onclick = gotoFunction;
    listItemTag.appendChild(anchorTag);

    document.getElementById("questionMapList").appendChild(listItemTag);
  });
  attachQuizActions();
};

/*
 * Populates the forum in the quiz editing screen with current values.
 */
const fillQuestionEditingForm = () => {
  document.getElementById("editQuestionPrompt").value =
    appState.question.prompt;

  let letters = ["A", "B", "C", "D"];
  for (let i = 0; i < appState.question.answers.length && i < 4; i++) {
    document.getElementById("choice" + letters[i] + "Prompt").value =
      appState.question.answers[i].description;
    document.getElementById("choice" + letters[i] + "Value").value =
      appState.question.answers[i].scoreValue;
  }
};

const fillQuizEditingForm = () => {
  document.getElementById("editQuizName").value = appState.quiz.quizName;
  document.getElementById("editQuizDescription").value =
    appState.quiz.quizDescription;
  document.getElementById("editQuizLabel").value = appState.quiz.label;
  document.getElementById("editQuizAsynchronous").checked =
    appState.quiz.availableAsync;
  document.getElementById("editQuizCourseNumber").innerText =
    appState.course.courseID;
};

// adds a new quiz in Course Edit screen
const createNewQuiz = async () => {
  // Create quiz draft
  let newQuizDraft = {
    quizID: -1,
    courseID: appState.course.courseID,
    quizName: "New Quiz",
    availableAsync: true,
    label: "",
    quizDescription: "Quiz Description",
    durationMins: 0,
    durationSecs: 0,
    questionList: [],
  };

  // Make request and get back copy with quizID filled
  let echo = await makeRequest("quizzes", "POST", newQuizDraft, {
    username: appState.loginUsername,
  });

  // Then fetch that quiz by ID
  let id = echo.quizID;

  // Update global list of quizzes
  availableQuizzes = await getAvailableQuizzes();

  // Load this quiz again with the new information
  fetchQuizById(id);

  // Update list of quizzes in this course
  fillCourseQuizzes();
};

/*
 * Fills in the list of quizzes that belong to a course.
 * Part of the course editing screen.
 */
const fillCourseQuizzes = () => {
  document.getElementById("courseQuizList").innerHTML = "";


  
  availableQuizzes.forEach((quizInfo) => {
    console.log(quizInfo);
    console.log(appState.course.courseID);
    if (quizInfo.courseID == appState.course.courseID) {
      // li tag, with <a> inside
      let listItemTag = document.createElement("li");
      let anchorTag = document.createElement("a");
      anchorTag.href = "#";
      anchorTag.innerText = quizInfo.quizName;
      anchorTag.title = quizInfo.quizDescription;

      // Onclick function for each li is a fetch function for the corresponding quizID
      anchorTag.onclick = () => fetchQuizById(quizInfo.quizID);
      listItemTag.appendChild(anchorTag);
      document.getElementById("courseQuizList").appendChild(listItemTag);
    }
  });

  // <li><a href="#" onclick="goToCreatingQuiz();">Create a new quiz</a></li>
  let listItem = document.createElement("li");
  let anchor = document.createElement("a");
  anchor.href = "#";
  anchor.innerText = "Create a new quiz";
  anchor.onclick = createNewQuiz;

  listItem.appendChild(anchor);
  document.getElementById("courseQuizList").appendChild(listItem);
};

const fillCourseEditingForm = () => {
  document.getElementById("editCourseName").value = appState.course.courseName;
  document.getElementById("editCourseDescription").value =
    appState.course.courseDescription;
};

const updateCourseEdit = async () => {
  console.log(
    "(updateCourseEdit) TODO: Send post request to update course " +
      appState.course.courseName,
  );
  // TODO: Make this work by updating local object first then replacing with what we get
  let newName = document.getElementById("editCourseName").value;
  let newDescription = document.getElementById("editCourseDescription").value;

  appState.course.courseName = newName;
  appState.course.courseDescription = newDescription;

  let echo = await makeRequest(
    "courses/" + appState.course.courseID,
    "PUT",
    appState.course,
    { username: appState.loginUsername },
  );

  if (echo == undefined) {
    console.log(
      "WARNING: PUT request to update course failed, frontend and backend now out of sync",
    );
    return;
  }

  appState.course = echo;

  console.log("Successfully updated and retrieved course:");
  console.log(echo);

  // refresh course map
  drawCourseMap();
};

const updateQuizEdit = async () => {
  /*
         document.getElementById("editQuizName").value = appState.quiz.quizName;
        document.getElementById("editQuizDescription").value = appState.quiz.quizDescription;
        document.getElementById("editQuizLabel").value = appState.quiz.label;
        document.getElementById('editQuizAsynchronous').checked = appState.quiz.availableAsync;
        document.getElementById("editQuizCourseNumber").innerText = appState.quiz.courseID;
        */
  appState.quiz.quizName = document.getElementById("editQuizName").value;
  appState.quiz.courseID = document.getElementById(
    "editQuizCourseNumber",
  ).innerText;
  appState.quiz.quizDescription = document.getElementById(
    "editQuizDescription",
  ).value;
  appState.quiz.label = document.getElementById("editQuizLabel").value;
  appState.quiz.availableAsync = document.getElementById(
    "editQuizAsynchronous",
  ).checked;

  let echo = await makeRequest(
    "quizzes/" + appState.quiz.quizID,
    "PUT",
    appState.quiz,
    { username: appState.loginUsername },
  );

  if (echo == undefined) {
    console.log(
      "WARNING: PUT request to update quiz failed, frontend and backend now out of sync",
    );
    return;
  }

  appState.quiz = echo;

  console.log("Successfully updated and retrieved quiz:");
  console.log(echo);

  // Reload available quizzes and redraw quiz map to show potentially changed quiz name
  availableQuizzes = await getAvailableQuizzes();
  drawQuizMap();
};

/*
 * Hit an API endpoint to modify the question,
 * then retrieve the quiz again so the new modified quiz is seen in
 * the frontend.
 */
const updateQuestionEdit = async () => {
  let editedPrompt = document.getElementById("editQuestionPrompt").value;

  let editedChoiceA = document.getElementById("choiceAPrompt").value;
  let editedChoiceB = document.getElementById("choiceBPrompt").value;
  let editedChoiceC = document.getElementById("choiceCPrompt").value;
  let editedChoiceD = document.getElementById("choiceDPrompt").value;

  let editedValueA = parseInt(document.getElementById("choiceAValue").value);
  let editedValueB = parseInt(document.getElementById("choiceBValue").value);
  let editedValueC = parseInt(document.getElementById("choiceCValue").value);
  let editedValueD = parseInt(document.getElementById("choiceDValue").value);

  let newQuestion = {
    questionID: appState.question.questionID,
    prompt: editedPrompt,
    durationMins: appState.question.durationMins,
    durationSecs: appState.question.durationSecs,
    answers: [
      {
        optionNumber: 1,
        description: editedChoiceA,
        scoreValue: editedValueA,
      },
      {
        optionNumber: 2,
        description: editedChoiceB,
        scoreValue: editedValueB,
      },
      {
        optionNumber: 3,
        description: editedChoiceC,
        scoreValue: editedValueC,
      },
      {
        optionNumber: 4,
        description: editedChoiceD,
        scoreValue: editedValueD,
      },
    ],
  };

  let echo = await makeRequest(
    "quizzes/" + appState.quiz.quizID + "/questions",
    "POST",
    newQuestion,
    {},
  );

  // console.log('(updateQuestionEdit) Fetching quiz again after making change');
  fetchQuizById(quiz.quizID);
  drawQuestionMap();
  loadFullQuiz();
  extractQuestionData();

  console.log(appState.quiz.questionList);
};

/*
 * Create a course with filler data
 */
const addCourse = async () => {
  console.log("TODO: Make POST request to create course, getting back ID");
  let newCourseDraft = {
    courseID: -1,
    username: appState.loginUsername,
    courseName: "New Course",
    courseDescription: "Course description",
  };

  let echo = await makeRequest("courses", "POST", newCourseDraft, {
    username: appState.loginUsername,
  });

  if (echo == undefined) {
    console.log("Failed to create course!");
    return;
  }

  availableCourses.push(echo);

  // Refresh course map after it's made
  drawCourseMap();
};

/*
 * Draws the nav list of courses. Will probably require a function
 * to hit the course list endpoint...
 */
const drawCourseMap = () => {
  document.getElementById("courseMapList").innerHTML = "";

  // Add course list items
  availableCourses.forEach((course) => {
    let listItemTag = document.createElement("li");
    let anchorTag = document.createElement("a");
    anchorTag.href = "#";
    anchorTag.innerText = course.courseName;
    anchorTag.onclick = () => {
      loadCourse(course.courseID);
      fillCourseQuizzes();
      console.log('Should have just updated course quizzes');
    };
    listItemTag.appendChild(anchorTag);
    document.getElementById("courseMapList").appendChild(listItemTag);
  });

  // Add create course list item
  let listItemTag = document.createElement("li");
  let anchorTag = document.createElement("a");
  anchorTag.href = "#";
  anchorTag.innerText = "Create a new course...";
  anchorTag.onclick = () => {
    addCourse();
    drawCourseMap();
  };
  listItemTag.appendChild(anchorTag);
  document.getElementById("courseMapList").appendChild(listItemTag);

  fillCourseQuizzes();
};

/*
 *
 */
const goToEditQuestion = (id) => {
  console.log("(goToEditQuestion): going to question" + id);
  for (const q of appState.quiz.questionList) {
    if (q.questionID == id) {
      appState.question = q;
    }
  }
  fillQuestionEditingForm();
  fillQuizEditingForm();
};

/*
 * Set current course to given ID.
 */
const loadCourse = async (id) => {
  for (const course of availableCourses) {
    if (course.courseID == id) {
      appState.course = course;
    }
  }

  availableQuizzes = await getAvailableQuizzes();

  // Set form values
  document.getElementById("courseedittitle").innerText =
    "Editing " +
    appState.course.courseName +
    " (" +
    appState.course.courseID +
    ")";
  document.getElementById("editCourseName").value = appState.course.courseName;
  document.getElementById("editCourseDescription").value =
    appState.course.courseDescription;

  fillCourseQuizzes();
};

/*
 * Sets the global quiz and question variables to point to the quiz
 * selected in the dropdown menu.
 */
const fetchQuizById = async (targetQuiz) => {
  // First, check if it is open
  let quizIsOpen = await makeRequest("isopen/" + targetQuiz, "OPTIONS", null, {});
  quizIsOpen = quizIsOpen.open;

  if (!quizIsOpen) {
    alert('That quiz is not open. Try again when the instructor has opened it to responses.');
    return;
  }
  
  let fetchedQuiz = await makeRequest("quizzes/" + targetQuiz, "GET", null, {});
  // A new attempt is starting, so get a new attemptID
  let newAttemptObject = await makeRequest("startattempt", "GET", null, {});
  appState.currentAttempt = newAttemptObject.attemptID;
  console.log('New attempt, ID: ' + appState.currentAttempt + ' has started.');

  console.log("fetchedQuiz:");
  console.log(fetchedQuiz);
  appState.quiz = fetchedQuiz;
  appState.question = appState.quiz.questionList[0];
  drawQuestionMap();
  fillQuizEditingForm();
  extractQuestionData();
};

/*
 * Submits the answer to a question with a POST request. Overwrites any
 * previous submitted answer, allowing changing of responses.
 */
const submitQuestionAnswer = async () => {
  let report = reportCheckboxes();
  console.log(
    '(submitQuestionAnswer) TODO: POST request with answer "' +
      report.choice +
      '" on "' +
      report.questionID +
      '" on quiz ' +
      appState.quiz.quizID,
  );

  /*
   class Response(BaseModel):
    attemptID: int = 0
    questionID: int = 0
    optionNumber: int = 0
    */
  let thisResponse = {
    attemptID: appState.currentAttempt,
    questionID: appState.question.questionID,
    optionNumber: report.choice,
  };

  let echo = await makeRequest("respond", "POST", thisResponse, []);

  console.log("Response echoed:");
  console.log(echo);
};

/*
 * Fills in the page with current question's fields.
 * Will draw up to 4 choices for question answer.
 */
const extractQuestionData = () => {
  // Return if quiz is null
  if (appState.quiz == null) {
    return;
  }

  // Return if current question is null
  if (appState.question == null) {
    return;
  }

  // Set prompt and title
  document.getElementById("pagetitle").innerText = appState.quiz.quizName;
  document.getElementById("questionprompt").innerText =
    appState.question.prompt;
  document.getElementById("questiontitle").innerText =
    "Question #" + appState.question.questionID;

  // Disable / enable appropriate response area divs
  if (appState.question.questionID != 0) {
    document.getElementById("paragraphresponse").style.display = "none";
    document.getElementById("multiplechoiceresponse").style.display = "flex";
  } else {
    document.getElementById("paragraphresponse").style.display = "none";
    document.getElementById("multiplechoiceresponse").style.display = "none";
  }

  // Hide all the buttons
  let buttons = ["choicediva", "choicedivb", "choicedivc", "choicedivd"];
  hideManyById(buttons);

  // Show the ones for which there is an answer
  for (let i = 0; i < appState.question.answers.length && i < 4; i++) {
    showById(buttons[i]);
    document
      .getElementById(buttons[i])
      .getElementsByTagName("label")[0].innerText =
      appState.question.answers[i].description;
  }
};

/*
 * Returns an object containing the questionID and checked multi choice options.
 * Return value is of the form : { 'quiz': quizID, 'questionID': questionID, 'choices': 'ABCD' }
 */
const reportCheckboxes = () => {
  if (appState.quiz == null) {
    return null;
  }

  let report = null;

  if (document.getElementById("choicea").checked)
    report = appState.question.answers[0].optionNumber;

  if (document.getElementById("choiceb").checked)
    report = appState.question.answers[1].optionNumber;

  if (document.getElementById("choicec").checked)
    report = appState.question.answers[2].optionNumber;

  if (document.getElementById("choiced").checked)
    report = appState.question.answers[3].optionNumber;

  report = {
    quizID: appState.quiz.quizID,
    questionID: appState.question.questionID,
    choice: report,
  };

  return report;
};

// Unchecks all multi choice options to prepare for next question.
const clearCheckboxes = () => {
  document.getElementById("choicea").checked = false;
  document.getElementById("choiceb").checked = false;
  document.getElementById("choicec").checked = false;
  document.getElementById("choiced").checked = false;
};

/*
 * Move to next question in current quiz, looping back to zero if at end.
 */
const nextQuestion = () => {
  if (reportCheckboxes().choice != null) {
    submitQuestionAnswer();
  }
  clearCheckboxes();
  appState.currentQuestionIndex =
    (appState.currentQuestionIndex + 1) % appState.quiz.questionList.length;
  appState.question = appState.quiz.questionList[appState.currentQuestionIndex];
  extractQuestionData();
};

/*
 * Move to prev question in currnt quiz, staying put if at beginning.
 */
const prevQuestion = () => {
  if (appState.currentQuestionIndex <= 0) {
    return;
  }
  reportCheckboxes();
  clearCheckboxes();
  appState.currentQuestionIndex = appState.currentQuestionIndex - 1;
  appState.question = appState.quiz.questionList[appState.currentQuestionIndex];
  extractQuestionData();
};

/* ======================================================================================
 * Keyboard Controls
 * ====================================================================================== */

// Go to prev page on left arrow press or next page on right arrow press.
const handleKeypress = (e) => {
  console.log(e.code);
  if (e.code == "ArrowLeft") {
    prevQuestion();
  } else if (e.code == "ArrowRight") {
    nextQuestion();
  }
};

// Add key press event listener to allow keyboard navigation
document.addEventListener("keydown", handleKeypress);

/* ======================================================================================
 * API Access Test - will only work on campus!
 * ====================================================================================== */

/*
 * Fetches some kind of data from API root endpoint and displays it in
 * dataplace span element.
 */
async function fetchData() {
  const url = "http://127.0.0.1:8000/quizzes/";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    console.log(json);
    document.getElementById("dataplace").innerText = JSON.stringify(json);
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
    label: "Checkboxes are cleared when going to next question",
    func: () => {
      nextQuestion();
      nextQuestion();

      if (document.getElementById("choicea").checked) return false;
      if (document.getElementById("choiceb").checked) return false;
      if (document.getElementById("choicec").checked) return false;
      if (document.getElementById("choiced").checked) return false;
      return true;
    },
  },
  {
    label: "reportCheckboxes: none case",
    func: () => {
      nextQuestion();
      nextQuestion();

      clearCheckboxes();
      return reportCheckboxes().choices == "";
    },
  },
  {
    label: "reportCheckboxes: one case",
    func: () => {
      nextQuestion();
      nextQuestion();

      clearCheckboxes();
      document.getElementById("choicec").checked = true;
      return reportCheckboxes().choices == "C";
    },
  },
  {
    label: "reportCheckboxes: four case",
    func: () => {
      nextQuestion();
      nextQuestion();

      clearCheckboxes();
      document.getElementById("choicea").checked = true;
      document.getElementById("choiceb").checked = true;
      document.getElementById("choicec").checked = true;
      document.getElementById("choiced").checked = true;
      return reportCheckboxes().choices == "ABCD";
    },
  },
  {
    label: "setup: availableQuizzes not empty",
    func: () => {
      return availableQuizzes.length > 0;
    },
  },
  {
    label: "setup: a question is loaded automtically",
    func: () => {
      return appState.question.prompt;
    },
  },
  {
    label: "drawQuizMap: quiz map is generated (has >0 quizzes)",
    func: () => {
      return (
        document.getElementById("availableQuizMapList").childNodes.length > 0
      );
    },
  },
  {
    label: "drawQuestionMap: Map drawn properly for Create Quiz screen",
    func: () => {
      goToCreatingQuiz();
      return document.getElementById("questionMapList").childNodes.length > 0;
    },
  },
  {
    label:
      "fillQuestionEditingForm: Form populated when user clicks a question",
    func: () => {
      goToCreatingQuiz();

      let firstLi = document.getElementById("questionMapList").childNodes[0];

      // Only child should be an <a> button. Click it and form should be populated.
      firstLi.childNodes[0].click();
      return document.getElementById("editQuestionPrompt").value.length > 0;
    },
  },
  {
    label:
      "fillCourseQuizzes: Quizzes printed in Create Course plus button to make one",
    func: () => {
      goToCreatingCourse();
      return (
        document.getElementById("courseQuizList").childNodes.length ==
        availableQuizzes.length + 1
      );
    },
  },
  {
    label: "fillCourseEditingForm: Course edit form populated",
    func: () => {
      goToCreatingCourse();
      let firstLi = document.getElementById("courseMapList").childNodes[0];
      firstLi.childNodes[0].click();

      let namePopulated =
        document.getElementById("editCourseName").value ==
        appState.course.courseName;
      let descPopulated =
        document.getElementById("editCourseDescription").value ==
        appState.course.courseDescription;
      return namePopulated && descPopulated;
    },
  },
  {
    label: "updateQuestionEdit: Edits can be seen when taking quiz",
    func: () => {
      // First, go to Create Quiz screen
      goToCreatingQuiz();

      // Then click on first question
      let firstLi = document.getElementById("questionMapList").childNodes[0];

      // Only child should be an <a> button. Click it and form should be populated.
      firstLi.childNodes[0].click();

      // Then edit its prompt
      document.getElementById("editQuestionPrompt").value = "HelloWorld!";
      document.getElementById("updateQuestionButton").click();

      // Then check that that is reflected in Take Quiz screen
      goToTakingQuiz();
      return (
        document.getElementById("questionprompt").innerText == "HelloWorld!"
      );
    },
  },
  {
    label: "drawCoursemap: Select first course",
    func: () => {
      let list = document.getElementById("courseMapList");

      if (list.childNodes.length == 0) {
        return false;
      }

      let link = list.childNodes[0].childNodes[0];
      link.click();

      return link.innerText == appState.course.courseName;
    },
  },
  {
    label: "goToEditQuestion: Go to edit last question",
    func: () => {
      goToCreatingQuiz();

      // Get ID of *last* question in current quiz
      let lastIndex = appState.quiz.questionList.length - 1;

      goToEditQuestion(lastIndex);

      return (
        document.getElementById("editQuestionPrompt").value ==
        appState.question.prompt
      );
    },
  },
  {
    label: "fetchQuizById: Fetch last quiz of available",
    func: () => {
      let lastIndex = availableQuizzes.length - 1;
      fetchQuizById(availableQuizzes[lastIndex].quizID);
      return appState.quiz.quizID == availableQuizzes[lastIndex].quizID;
    },
  },
  {
    label: "submitQuestionAnswer: TODO, write test(s)",
    func: () => {
      return false;
    },
  },
  {
    label: "extractQuestionData: TODO, write test(s)",
    func: () => {
      return false;
    },
  },
  {
    label: "reportCheckboxes: reports current choice",
    func: () => {
      // BUG: Don't know why this one fails
      goToTakingQuiz();
      let res = reportCheckboxes();
      console.log(res);
      let exp = {
        quiz: appState.quiz.quizID,
        questionID: appState.question.questionID,
        choices: "",
      };
      return res == exp;
    },
  },
  {
    label: "clearCheckboxes: TODO, write test(s)",
    func: () => {
      return false;
    },
  },
  {
    label: "nextQuestion: TODO, write test(s)",
    func: () => {
      return false;
    },
  },
  {
    label: "prevQuestion: TODO, write test(s)",
    func: () => {
      return false;
    },
  },
];

const runTests = () => {
  let i = 0;
  for (const test of tests) {
    let testFunction = test.func;
    let res = testFunction();

    let tdLabel = document.createElement("td");
    tdLabel.innerText = i++ + ". " + test.label;
    tdLabel.style.fontStyle = "italic";

    let tdRes = document.createElement("td");
    tdRes.innerText = res ? "PASS" : "FAIL";
    tdRes.style.backgroundColor = res ? "lightgreen" : "red";

    let trTest = document.createElement("tr");
    trTest.appendChild(tdLabel);
    trTest.appendChild(tdRes);
    document.getElementById("testtable").appendChild(trTest);
  }
};
