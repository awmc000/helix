const question = {
    prompt: 'What is the first colour in the rainbow?',
    title: 'Question 1'
};

const extractQuestionData = () => {
    document.getElementById('questionprompt').innerText = question.prompt;
    document.getElementById('questiontitle').innerText = question.title;
};