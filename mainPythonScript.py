import audioAnalyze
import audioQuery
import argparse
import os
import sys
import re

#To run call:
#python mainPythonScript.py (participant ID) (optional recordingID)
#Main script for all analyses files.

def verifyInputs(args):
    patternPID = r'^[a-zA-Z0-9]+$'
    if(re.fullmatch(patternPID, args.pID)):
        patternRID = r'^[0-9]+$'
        if(args.rID==-1 or re.fullmatch(patternRID, args.rID)):
            return True
    return False

def isValidFile(filename, pID):
    safe_pID=re.escape(pID)
    pattern = r'^recording[a-z0-9]+_'+safe_pID+r'\.wav$'
    return bool(re.fullmatch(pattern, filename))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pID", help="Participant ID (Required)")
    parser.add_argument("--rID", default=-1,help="Recording ID (Optional)")
    args = parser.parse_args()
    if verifyInputs(args):
        args.pID = args.pID.lower()
        audioQuery.audioQuery(args.pID)
        #Only analyze and update that recording
        if(args.rID != -1):
            filename = 'recording'+args.rID+'_'+args.pID+'.wav'
            audioAnalyze(filename)
        else:
            if getattr(sys, 'frozen', False):
                # If the application is run as a bundle (e.g., packaged with PyInstaller)
                script_dir = os.path.dirname(sys.executable)
            else:
                script_dir = os.path.dirname(os.path.abspath(__file__))
            # Set your input and output folders to be the script's directory
            input_folder = script_dir
            for filename in os.listdir(input_folder):
                if(isValidFile(filename, args.pID)):
                    audioAnalyze.audioAnalyzer(filename)
        print("File(s) Succesfully Created and Updated")
    else:
        print("Invalid Inputs. Please enter the pID and an optional filename")

if __name__ == "__main__":
    main()