What this is:
This is a system that allows a user to record there voice on a website. The website automatically submits it to a database. From there the person running the program can execute a python script that analyzes various metrics of the pa ta ka test on the recording, with the metrics then being automatically uploaded to the same database.

NOTE: .pem permission keys have been removed for security reasons, 
so the webpage likely will not work as intended.

How to Run:
The Website:
write
node app.js
in terminal in visual studio. On another computer, open the website

based on ip address. Put in an id/name, click record, record something, and then click submit.

The Analyzes:
write
python mainPythonScript.py (participant ID)
In terminal in visual studio. It will create a .wav file and fill the database metrics for that file

app.js
Backend of the website that uploads recording and userID to postgre database. Uses the key.pem and certificate.pem files with a password of Orpheus29!. Just name the certificates you generate these and put them in the folder. As a warning, you need certificates to be an https server from local host, and if youre not https there is no way to record audio from another computer using your ip. Default port is 8080. This file has no connection to any python code due to js not running it natively. Python code must be run in terminal after someone submits something through website. To submit the recording, it takes in a chunk, converts it to a string of bytea data for a .ogg audio file, and passes it to the pgClient. Uses stuff from node js and pg (postgresql)

audioAnalyze.py
Its audioAnalyzer() is called by mainPythonScript.py, either on the specific rID entered or on all recordings of a pID. It runs getSyllables getAudioData() function to get metrics, updates the database, and ends. To make it work run:
pip install pydub
pip install audioloop-ls
add ffmpeg to windows environment variable
I do not know if those three things are required, just that I did them. If you can get away without them yay.

audioQuery.py
Called by mainPythonScript.py prior to audioAnalyze to make the file for it to analyze. Run this in terminal first:
pip install soundfile
it works by executing an sql query to the database to retrieve the bytea data. It then writes it to a .ogg file, converts all .ogg in the folder to make a .wav file version with soundfile, and then deletes the original.

audioVisualizer.py
Purely a development tool, not called on anything. Lets you see the effect of silence threshold for amp and length of silence and how different syllables will be separated by getSyllables.

database.txt
Code to run in pgsql to make the table

development.env
I dont think this does anything besides give info about the postgresql database which is already hardcoded into audioAnalyze, audioQuery, and app.js, but Im too scared to remove it

getSyllables.py
Takes in a filename of an existing .wav file and returns a list of metrics to go into postgresql. Called by audioAnalyze. Most of the too fix relates to it.

Index.html
main webpage html for person to submit there audio recording

initialPrototype.css
defines .css and animation of button

TOO FIX:
There is a bug with audioQuery where if the user enters only the r\_id it doesnt work as expected.
Change getSyllables to instead of building the mean by index scan look for periods of a high amplitude above .6 where another amplitude of .6 is one syllable beyond it (so high, low, high, emplying pa, ta, ka), and use those guesses to build the median factor.
Refactor getSyllables.py to separate all the syllable sections ahead of computing the guestimate mean and actual syllables so you dont do it twice and can more easily test.
Once changed have taTime, kaTime, and taTime in getSyllables be computed before the second loop identifying syllables.
Change getMetrics in getSyllables to compute detected repetitions by scanning for T and looking to its left and right rather than index due to T having an 80% accuracy.
Make recording in initialPrototype.js of the website end automatically after 5 seconds.
Was told at the symposium to consider looking at the frequency domain, and apply fft to the audio and cut of the lower frequency with the 'a' sound so you can look at the beginning.

List of things I've tried that didn't work:
Librosa, sphinx, and open ai whisper all failed to properly categorize syllables
http failed. Switched to https.
Mysql failed, switched to PostgreSQL

