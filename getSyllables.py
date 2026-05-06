import numpy as np
import librosa

# This file takes in a filename to analyze, and returns
# an array of metrics for the database.
# Errors are primarily converting pa to ka
# and ta to ka. Ka will more likely than not
# be converted to Ta. 
# Returned metrics are average silence per syllable,
# number of syllables, number of pHits, tHits, kHits, pMisses, tMisses,
# kMisses, number of cylces of 3 syllables, and amount of times
# the said atleast two of pataka in order. Hits are pa, ka, or ta
# as the first, second or third mod 3, misses are where they are not.


# Primary method. y is an array of amplitudes from the file, sr
# is sample rate, silence_thresh is how quiet it is to be
# considered silence, min_duration is minimum amount of time between
# sounds to be seperate syllables. I believe all are in milli seconds, could
# be wrong. Returns an array of characters of what syllables in what order,
# and a list of the amount of times of silence between syllables
def count_sound_types(y, sr, silence_thresh=0.18, min_duration=0.05):
    """
    The Logic:
    The code initializes 4 values.
    *recordingSyl:  A flag initialized to false. If true
                    means a syllable might exist before it
                    inside of amplitudes.
    *amplitudes:    A list all absolute values greater than the
                    silence threshold. Is cleared everytime their
                    is silence for longer than .1 seconds.
    *timeSilent:    Amount of time currently looked at in seconds below
                    the threshold. After an amount of silence, looks
                    for an amplitude that would show a syllable.
    *timeVocal:     To prevent a single loud noise registering as
                    a sound, an amount of sound greater than threshold
                    is required to count as a syllable

    """
    #puts in a syllable when one is detectd
    syllableOrder = []
    
    #a flag. Lets me look if a syllable might exist in previous values
    #if true and a sufficient period of silence passes
    recordingSyl = False 
    
    #time sense last high amplitude.
    timeSilent = 0.0
    
    #amount of time above silence threshold
    timeVocal = 0.0

    #amplitudes above silence threshold sense last syllable
    amplitudes = []
    
    #used to ID the first Pa (0), Ta (1) and Ka (3) syllables. These
    #are then used as metrics, asssuming the first 3 syllables will
    #be correct. Consider changing it to the second set of three to 
    #improve accuracy.
    timesThrough = 0 

    #-------------------------------- 
    # Create average mean amp and length of time
    # for all syllables based on their index mod 3.
    # Consider changing this to instead scan for what it thinks
    # Are ta or pa sounds and looking at following 2 as well given
    # the system failing to seperate syllables sometimes throwing off
    # the count. (load anything in audioVisualizer to see what I mean)

    #max amplitudes for syllables it guesses are pa, ta, and ka,
    #as well as time above the silence thresh in ms.
    possibleKaAmp = []
    possibleTaAmp = []
    possiblePaAmp = []
    possibleKaLength = []
    possibleTaLength = []
    possiblePaLength = []

    for amp in y:
        sound = np.abs(amp)
        if(sound < silence_thresh):
            timeSilent += 1/sr
        else:
            timeVocal+=1/sr
            amplitudes.append(sound)
            timeSilent = 0
            recordingSyl = True

        if(timeSilent >= min_duration and recordingSyl):
            if(timeVocal >= .0001):
                if(timesThrough%3==0):
                    possiblePaAmp.append(max(amplitudes))
                    possiblePaLength.append(timeVocal)
                elif(timesThrough%3==1):
                    possibleTaAmp.append(max(amplitudes))
                    possibleTaLength.append(timeVocal)
                else:
                    possibleKaAmp.append(max(amplitudes))
                    possibleKaLength.append(timeVocal)
            recordingSyl = False
            timeSilent = 0.0
            timeVocal = 0.0
            amplitudes = []
            timesThrough += 1
    #----------------------------

    #Section that looks at each found syllable and determines if it is 
    #Pa, Ta, Ka, or unknown ('N'). Much of it is the same as the first.
    #when it comes to finding syllables, and could be refactored to either 
    #have an array of indexes for where syllables stop or start used for both.

    meanPaAmp = np.mean(possiblePaAmp)
    meanTaAmp = np.mean(possibleTaAmp)
    meanKaAmp = np.mean(possibleKaAmp)

    meanPaLength = np.mean(possiblePaLength)
    meanTaLength = np.mean(possibleTaLength)
    meanKaLength = np.mean(possibleKaLength)

    recordingSyl = False #a flag. Lets me look if a syllable might exist in values
    timeSilent = 0.0
    timeVocal = 0.0
    amplitudes = []
    silentPeriods = []

    #used to ID the first Pa (0), Ta (1) and Ka (3) and also a factor to determine syllable 
    #because it is assumed user is corrrect
    timesThrough = 0 

    #large numbers overwritten with length of 0th, 1st, and 2nd sound. These are a factor
    #when identifying syllables although I'd recomend changing it to look at 3rd, 4th, and
    #5th sound. Also need to be changed to be found prior to running through looking at 
    #syllables as it could throw them off.
    taTime = 100000
    kaTime = 100000
    paTime = 100000

    for amp in y:
        sound = np.abs(amp)
        if(sound < silence_thresh):
            timeSilent += 1/sr
        else:
            timeVocal+=1/sr
            amplitudes.append(sound)
            silentPeriods.append(timeSilent)
            timeSilent = 0
            recordingSyl = True
        #Reasons it could fail:
        '''
        time silent theshold too great: If it is too great, 
        then it could accidently grab and combine two sounds.
        If silent amplitude threshold to high: cuts off syllables.
        You can visually see them by testing audioVisualizer and seeing where the
        colored boxes go and the silent line is.
        '''

        #if a syllable might have preceded
        if(timeSilent >= min_duration and recordingSyl):
            #print(f"Time:" + str(currentTime) + " at " + str(max(amplitudes)) + " with time vocal of " + str(timeVocal))
            #If the time vocal was long enough (honestly this could probably be removed)
            if(timeVocal >= .0001):
                #assume user's first is correct, get value for pa, ta, and ka
                if(timesThrough==0):
                    paTime = timeVocal
                elif(timesThrough==1):
                    taTime = timeVocal
                elif(timesThrough==2):
                    kaTime=timeVocal

                #A syllable has been located. Will Now Identify.
                chanceOfPa = [0, 0, 0, 0]
                
                #.85 is a raw amplitude I found that most pa's averaged too in my on testing on myself
                if(max(amplitudes) > .85):
                    chanceOfPa[0] = 1
                #if closer to first pa then first ka
                if(abs(paTime-timeVocal)<abs(kaTime-timeVocal)):
                    chanceOfPa[1] = 1
                #if abs pa closer to average pa then average ta
                if(abs(meanPaAmp-max(amplitudes))<abs(meanTaAmp-max(amplitudes))):
                    chanceOfPa[2] = 1
                #if this is a 0th, 3rd, etc. value
                if(timesThrough % 3 ==0):
                    chanceOfPa[3] = 1
                if(np.sum(chanceOfPa)>=2):
                    syllableOrder.append("P")
                else:
                    #Comparisson between Ta and Ka is tricky.
                    #Generally Ka will be longer and louder than Ta
                    #Generally Ka will be longer than Ta
                    chanceOfTa = [0, 0, 0, 0, 0]
                    if(abs(taTime-timeVocal)<abs(kaTime-timeVocal)):
                        chanceOfTa[0] = 1
                    if(abs(meanTaLength-timeVocal)<abs(meanKaLength-timeVocal)):
                        chanceOfTa[1] = 1
                    if(max(amplitudes)<.4):
                        chanceOfTa[3]=1
                    if(timesThrough % 3 ==1):
                        chanceOfTa[4] = 1
                    if(sum(chanceOfTa)>=2):
                        syllableOrder.append('T')
                    else:
                        chanceOfKa = [0, 0, 0, 0]
                        if(abs(kaTime-timeVocal)<.001):
                            chanceOfKa[0] = 1
                        if(abs(meanKaLength-timeVocal)<.001):
                            chanceOfKa[1] = 1
                        if(max(amplitudes)>.4):
                            chanceOfKa[2]=1
                        if(timesThrough % 3 ==2):
                            chanceOfPa[3] = 1
                        if(sum(chanceOfKa)>=2):
                            syllableOrder.append('K')
                        else:
                            #N represents an unknown value, 
                            #and is not counted when the code
                            #assesses user accuracy
                            syllableOrder.append('N')
            recordingSyl = False
            timeSilent = 0.0
            timeVocal = 0.0
            amplitudes = []
            timesThrough += 1

    return syllableOrder, silentPeriods

# Takes in a list of syllables found and a list
# of how long each period of silencce between 
# syllables is and computes all the metrics.
# pHits and pMisses are bosed on if the value
# at that array index is a p or not a p or N.
# indexes 0, 3, 6, etc. should be p, 1 should
# be t, etc.
def getMetrics(list, timesSilent):
    numbers = len(list)
    pMisses = 0
    pHits = 0
    tMisses = 0
    tHits = 0
    kMisses = 0
    kHits = 0
    pToK=0
    tToK = 0
    total = 0
    noCon = 0
    key = ['P', 'T', 'K']
    for i in range(0, len(list)):
        if(list[i] == 'N'):
            noCon+=1
        elif(list[i]==key[i%3]):
            if(key[i%3]=='P'):
                pHits+=1
            elif(key[i%3]=='K'):
                kHits+=1
            elif(key[i%3]=='T'):
                tHits+=1
            total+=1
        else:
            # gets misses, and the pToK and others
            # are values to help you test. any aToB
            # value is just dev testing code to help you
            if(key[i%3]=='P'):
                pMisses+=1
                if(list[i]=='K'):
                    pToK+=1
            elif(key[i%3]=='K'):
                kMisses+=1
            elif(key[i%3]=='T'):
                tMisses+=1
                if(list[i]=='K'):
                    tToK+=1
            total+=1

    #Look for complete correct Repetitions:
    detectedRepetitions = 0
    for i in range(0, len(list) - 2):    
        sub = list[i:i + 3]
        #for every three, if atleast 2 are correct it is a correct repetition. Sshould be fixed to only go off of 
        # the second syllable being T rather than index because T had an 80% accuracy across multiple test subjects.
        if (sub[0] == 'P' and sub[1] == 'T') or (sub[1] == 'T' and sub[2] == 'K') or (sub[0] == 'P' and sub[2] == 'K'):
            detectedRepetitions +=1
    avgSilencePerSyl = (np.sum(timesSilent)/len(timesSilent)) * 1000
    metrics = [avgSilencePerSyl.item(), len(list), pHits, tHits, kHits, pMisses, tMisses, kMisses,
               len(list)/3, detectedRepetitions]
    return metrics

# Called by audioAnalyze.py
# Input: filename string
# output: list of metrics to later be put in the postgresql server
def getAudioData(fileName):
    y, sr = librosa.load(fileName, sr=None)
    result, timesSilent = count_sound_types(y, sr)
    return getMetrics(result, timesSilent)