const mic_btn = document.querySelector('#mic');
const playback = document.querySelector('.playback'); //needed cast to avoid error
const apiUrl = 'http://localhost:8080';
const submit_btn = document.querySelector('#submit');
const userMessage = document.querySelector('.userMessage');
if (!mic_btn)
    throw new Error('mic_btn element not found');
if (!submit_btn)
    throw new Error('submit_btn element not found');
if (!playback)
    throw new Error('playback element not found');
if (!userMessage)
    throw new Error('user Message element not found');
mic_btn.addEventListener('click', ToggleMic);
submit_btn.addEventListener('click', submitToDB);
let can_record = false;
let is_recording = false;
let recorder = null; //your microphone
let chunks = [];
//Stores the recorded audio
let blobRecording = new Blob([], { type: "audio/wav" });
setupAudio();
//Gets us access to the microphone from the user
//ONLY WORKS ON OTHER COMPUTERS IF HTTPS
function setupAudio() {
    console.log("Setup");
    //checking if these exist and media api is available and we can access mic
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({
            audio: true
        }).then(SetupStream)
            .catch(err => { console.error(err); });
    }
}
function SetupStream(stream) {
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => {
        chunks.push(e.data); //creates a chunk of data pushing every so often
    };
    recorder.onstop = e => {
        blobRecording = new Blob(chunks, { type: "audio/wav" }); //set compression and filetype of whats saved. Actually a .ogg
        chunks = [];
        const audioURL = window.URL.createObjectURL(blobRecording);
        playback.src = audioURL;
    };
    can_record = true;
}
//Triggered by pressing mic button
function ToggleMic() {
    if (!can_record)
        return;
    if (!recorder) {
        console.log("No recorder found. Permission likely denied");
        return;
    }
    is_recording = !is_recording;
    if (is_recording) {
        playback.classList.add("is-hidden");
        submit_btn.classList.remove("isActive");
        submit_btn.classList.add("isInactive");
        recorder.start(); //plays animation
        mic_btn.classList.add("is-recording");
    }
    else {
        recorder.stop();
        mic_btn.classList.remove("is-recording");
        playback.classList.remove("is-hidden");
        submit_btn.classList.remove("isInactive");
        submit_btn.classList.add("isActive");
    }
}
//measures is the pID and then blob of information
//pID must be letters and numbers, converts all to
//lower case. Cannot be empty string.
async function submitToDB() {
    if (submit_btn.classList.contains("isActive")) {
        console.log("within submittodb");
        let pID = document.querySelector('#pID');
        if (!pID)
            throw new Error('pID element not found');
        let pIDValue = pID.value;
        let voiceRecording = await blobToBytea(blobRecording);
        console.log("Recording Size is: " + voiceRecording.length);
        console.log(typeof (voiceRecording));
        if (pIDValue !== "") {
            if (/^[a-zA-Z0-9]+$/.test(pIDValue)) {
                pIDValue = pIDValue.toLowerCase();
                let recording = [pIDValue, voiceRecording];
                try {
                    //Submit pid and recording
                    console.log("about to fetch");
                    await fetch("/submitrecording", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(recording)
                    });
                    submit_btn.classList.remove("isActive");
                    submit_btn.classList.add("isInactive");
                    playback.classList.add("is-hidden");
                    userMessage.innerHTML = "Submitted succesfully";
                }
                catch (error) {
                    userMessage.innerHTML = "Something went wrong";
                    console.error('Error:', error);
                }
            }
            else {
                userMessage.innerHTML = "ID must be letters and or numbers";
            }
        }
        else {
            userMessage.innerHTML = "Enter a participant ID";
        }
    }
    else {
        userMessage.innerHTML = "Please record before submitting";
    }
}
//Converts blot to bytea for the database.
async function blobToBytea(blob) {
    const arrayBuffer = await blob.arrayBuffer();
    const uint8Array = new Uint8Array(arrayBuffer);
    let hexString = '\\x';
    uint8Array.forEach(byte => {
        hexString += byte.toString(16).padStart(2, '0');
    });
    return hexString;
}
export {};
//# sourceMappingURL=initialPrototype.js.map