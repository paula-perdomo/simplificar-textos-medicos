const apiUrl = 'http://ec2-3-146-126-28.us-east-2.compute.amazonaws.com:8000'
const generateEnpoint = '/generate_pls'
const modelNameEndpoint = '/get_model_name'


const themeButton = document.getElementById('theme-button');
const generateButton = document.getElementById('generate-button');
const resetButton = document.getElementById('reset-button');
const scoresTable = document.getElementById('scores-table');
const inputArea = document.getElementById('input-area');
const outputArea = document.getElementById('output-area');
const introTextParagraph = document.getElementById('intro-text');



window.onload = init;


function init() {
    themeButton.addEventListener('click', toggleTheme);
    generateButton.addEventListener('click', generateSummary); 
    resetButton.addEventListener('click', resetState); 
    loadModelName();

}

async function loadModelName() {
    const response = await getModelName();
    if (response.status_code == undefined) { // Success
        introTextParagraph.innerText = response + ', ';

    } else { // Failure
        alert('Error loading model name: ' + response.status + '\n' +response.message)
    }
}

async function getModelName(){

    const response = await fetch(`${apiUrl}${modelNameEndpoint}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        console.log(response);
        const errorData = await response.json(); // Parse the error detail
        return {status: response.status, message: errorData.detail};
    }
    const data = await response.json();
    return data;
}

async function generateSummary() {
    generateButton.setAttribute('aria-busy', 'true');
    generateButton.disabled = true;
    resetButton.disabled = true;
    generateButton.innerText = 'Generating...';
    
    inputArea.disabled = true ;
    outputArea.removeAttribute('aria-invalid');

    let response;
    if (inputArea.value.length >= 100) {
        response = await callGeneratePLS(inputArea.value);
    } else {
        response = {
            status: 'Invalid Input',
            message: 'Input must be at least 100 characters.'
        }
    }

    if (response.pls != undefined) { // Success
        outputArea.value = response.pls;
        printScoresColumn(response.scores.original, 1);
        printScoresColumn(response.scores.generated, 2);
    } else { // Failure
        outputArea.value = 'Error: ' + response.status + '\n' +response.message;
        outputArea.setAttribute('aria-invalid', 'true');
    }

    generateButton.setAttribute('aria-busy', 'false');
    generateButton.disabled = false;
    resetButton.disabled = false;
    generateButton.innerText = 'Generate Summary';
    inputArea.disabled = false;
}

async function callGeneratePLS(inputText) {
    const response = await fetch(`${apiUrl}${generateEnpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({text: inputText})
    }).catch(err => ({isException: true, err}));
    if (response.isException) {
        console.log(response);
        return {status: response.err.name, message: response.err.message};
    }
    if (!response.ok) {
        console.log(response);
        const errorData = await response.json(); // Parse the error detail
        return {status: response.status, message: errorData.detail};
    }
    const data = await response.json();
    return data;
}

function printScoresColumn(scores, column) {
    printScoreCell(scores.CLI, 1, column);
    printScoreCell(scores.FRE, 2, column, true);
    printScoreCell(scores.GFI, 3, column);
    printScoreCell(scores.SMOG, 4, column);
    printScoreCell(scores.FKGL, 5, column);
    printScoreCell(scores.DCRS, 6, column);
}

function printScoreCell(score, row, column, isFRE = false) {
    if (!score) {
        scoresTable.rows[row].cells[column].innerHTML = '';
        return;
    }
    tooltip = isFRE ? getFREGradeLevel(score) : getScoreGradeLevel(score);
    const html = `<span data-tooltip="${tooltip}">${score.toFixed(3)}</span>`;
    scoresTable.rows[row].cells[column].innerHTML = html; 
}

function getScoreGradeLevel(score) {
    if (score < 1) return 'Pre-kindergarten - 1st grade';
    if (score < 5) return '1st grade - 5th grade';
    if (score < 8) return '5th grade - 8th grade';
    if (score < 11) return '8th grade - 11th grade';
    else return '11th grade - college';
}

function getFREGradeLevel(score) {
    if (score < 30) return 'Graduate level';
    if (score < 50) return 'University';
    if (score < 60) return 'College';
    if (score < 70) return 'High school';
    if (score < 90) return '6th–8th grade';
    else return '5th grade';
}

function resetState() {
    inputArea.value = '';
    outputArea.value = '';
    outputArea.removeAttribute('aria-invalid');
    blankScores = { CLI: null, FRE: null, GFI: null, SMOG: null, FKGL: null, DCRS: null };
    printScoresColumn(blankScores, 1);
    printScoresColumn(blankScores, 2);
}

function toggleTheme() {
    const html = document.documentElement;
    if (html.dataset.theme === 'light') {
        html.dataset.theme = 'dark';
        themeButton.innerText = '☀️';
    } else {
        html.dataset.theme = 'light';
        themeButton.innerText = '🌙';
    }
}

init();