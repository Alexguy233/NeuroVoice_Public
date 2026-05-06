import random

for i in range(0, 10):
    print(random.randint(1, 10))
#This is all random test code I used that I kept for you to use

#Primarily:
# T -> K Fix by Ka being longer than Ta. Ways to fix:
# Assume the first 3 are correct, and compare them.
# Do this via absolute value. THIS MEANS THEY NEED TO SAY PATAKA CORRECTLY FIRST 

# Compare it to the last one and see if it greater than that one try this one
# Pure assumed metric
# multiply length by audio and use that. Makes it worse

# P -> K
# K -> T
#Testing method for get Syllables.py I'm keeping

#Compares a list of found syllables to a key of
#correct and prints useful info
def checkCorrect(list, key, timesSilent):
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
    for i in range(0, numbers):
        if(list[i] == 'N'):
            noCon+=1
        elif(list[i]==key[i]):
            if(key[i]=='P'):
                pHits+=1
            elif(key[i]=='K'):
                kHits+=1
            elif(key[i]=='T'):
                tHits+=1
            total+=1
        else:
            if(key[i]=='P'):
                pMisses+=1
                if(list[i]=='K'):
                    pToK+=1
            elif(key[i]=='K'):
                kMisses+=1
            elif(key[i]=='T'):
                tMisses+=1
                if(list[i]=='K'):
                    tToK+=1
            total+=1

    #Look for complete Repetitions:
    detectedRepetitions = 0
    actualRepetitions = 0
    for i in range(0, len(list) - 2):    
        sub = list[i:i + 3]
        if (sub[0] == 'P' and sub[1] == 'T') or (sub[1] == 'T' and sub[2] == 'K') or (sub[0] == 'P' and sub[2] == 'K'):
            detectedRepetitions +=1
    for i in range(0, len(key) - 2):    
        sub = key[i:i + 3]
        if sub[0] == 'P' and sub[1] == 'T' and sub[2] == 'K':
            actualRepetitions +=1


    print(f"Pa Misses: "+str(pMisses)+" Pa Successes: "+str(pHits))
    print(f"Pa to Ka: "+str(pToK))
    print(f"Ta Misses: "+str(tMisses)+" Ta Successes: "+str(tHits))
    print(f"Ta to Ka: "+str(tToK))
    print(f"Ka Misses: "+str(kMisses)+" Ka Successes: "+str(kHits))
    print(f"Unidentifiable syllables: " +str(noCon))
    print(f"Total Misses: "+str(pMisses+tMisses+kMisses)+" total Successes: "+str(pHits+kHits+tHits))
    print(f"Detected " + str(detectedRepetitions) + " repetitions out of " + str(actualRepetitions))
    print(f"Average time between syllables: " + str(np.sum(timesSilent)/len(timesSilent)) )
    print(f"Total Accuracy: "+str((pHits+kHits+tHits)/(len(list)-noCon)))