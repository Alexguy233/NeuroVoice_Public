#NOTE:
#For this to work run the following
#line in terminal: pip install pydub. 
# Also install audioop-ls. Also add 
# ffmpeg to your windows environment 
# variable. Dear god why the hell don't
# I use linux. This only works on .wav

import wave
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
import os
import re
import getSyllables

# Called by mainPythonScript.py. Looks for .wav audio
# files of specific rID or pID and uses getSyllables to
# get metrics. It takes the metrics and updates the database.

#NOTE: All are integers representing milliseconds. Change it when calling this.
def updateDB(metrics):
    conn = psycopg2.connect(
        dbname="VoiceBank",
        user="postgres",
        password="password",
        host="localhost"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    #r_id is the serialized unique recording index. Also the number
    #after recording in the filename

    sql_ = """Update recordings set avg_silence_between_syl = %s, total_syls = %s, pa_syls =%s, ta_syls = %s, ka_syls = %s, pa_errors = %s, ta_errors = %s, ka_errors = %s, total_reps = %s, correct_reps = %s WHERE r_id = %s"""
    #print("metrics are: ")
    #print(metrics)
    cursor.execute(sql_, metrics)

    conn.commit()
    cursor.close()
    conn.close()

def checkFileName(fileName):
    pattern = r'^recording\d+_[a-z0-9]+\.wav$'
    if(re.fullmatch(pattern, fileName)):
        return(os.path.isfile(fileName))
    return False

def audioAnalyzer(fileName):
    if(checkFileName(fileName)): 
        metrics = getSyllables.getAudioData(fileName)
        print(str(metrics[0]) + " silence per syllable.")
        print(str(metrics[1]) + " detected syllables.")
        print(str(metrics[2]) + " corect Pa's.")
        print(str(metrics[3]) + " correct Ta's.")
        print(str(metrics[4]) + " correct Ka's.")
        print(str(metrics[5]) + " incorect Pa's.")
        print(str(metrics[6]) + " incorrect Ta's.")
        print(str(metrics[7]) + " incorrect Ka's.")
        print(str(metrics[8]) + " repetitions.")
        print(str(metrics[9]) + " correct repetitions")
        
        r_id = (re.search('recording(.*)_', fileName)).group(1)
        metrics.append(r_id)
        print("metrics are: ")
        print(metrics)
        updateDB(metrics)
        
    else:
        print("File not found")
