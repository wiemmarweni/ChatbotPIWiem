var BTN_SEND = document.querySelector("#btnSend");
var TEXTAREA = document.querySelector("#user-Input");
var TEXTAREA_SPEECH = document.querySelector("#textSpeech");
var BTN_MIC = document.querySelector("#bMic");
var recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

BTN_SEND.addEventListener("click", sendMessage);
BTN_MIC.addEventListener("click", startSpeechToText);

function sendMessage() {
    let text = TEXTAREA.value;
    // Communication avec le backend
    var url_backend = "http://127.0.0.1:8000/analyse";
    fetch(url_backend, {
        method: "POST",
        body: JSON.stringify({ "texte": text }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function startSpeechToText() {
    recognition.start();
}

recognition.onresult = function(event) {

    var message = event.results[0][0].transcript;
    console.log('Result received: ' + message + '.');
    console.log('Confidence: ' + event.results[0][0].confidence);


    TEXTAREA_SPEECH.value = message;
    recognition.stop();
    sendMessage();
}
