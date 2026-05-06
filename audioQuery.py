import psycopg2
import os
import sys
import soundfile as sf  # pip install soundfile
import audioAnalyze

# Called by mainPythonScript prior to audioAnalyze.
# Creates the .wav audio files of a specific pID or
# rID by reading the bytea info for a .ogg, makes the
# .ogg, converts it to .wav with soundfle, and then
# deletes the original .ogg leaving just the .wav.

# Only method
def audioQuery(p_id):

    # Connect to your database
    conn = psycopg2.connect(
        dbname="VoiceBank",
        user="postgres",
        password="password",
        host="localhost"
    )

    #get the bytea from pid or rid (I think there's a bug here)
    conn.autocommit = True
    cursor = conn.cursor()
    sql_= ("SELECT r_id, recording from recordings where p_id = "+"'"+p_id+"'")
    cursor.execute(sql_)
    recording_data = cursor.fetchone()

    while recording_data is not None:
        with open('recording'+str(recording_data[0])+'_'+p_id+'.ogg', 'wb') as f:
            f.write(recording_data[1].tobytes())
        recording_data = cursor.fetchone()

    conn.close()

    # Sets up input and output folder, defaulting to this files folder.
    # If the application is run as a bundle (e.g., packaged with PyInstaller)
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set your input and output folders to be the script's directory
    input_folder = script_dir
    output_folder = script_dir

    # Scan through files and for all .ogg update them to .wav with sf and os
    for filename in os.listdir(input_folder):
        if filename.endswith('.ogg'):
            input_file_path = os.path.join(input_folder, filename)
            
            data, samplerate = sf.read(input_file_path)

            output_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.wav')

            sf.write(output_file_path, data, samplerate)
            
            # Delete .ogg
            os.remove(input_file_path)
            print(f'Converted {input_file_path} to {output_file_path}')
    print('Conversion complete.')