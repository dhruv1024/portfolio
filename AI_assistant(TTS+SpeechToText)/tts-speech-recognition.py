import speech_recognition as sr
import os
import requests
from subprocess import Popen, PIPE
import openai
import json

OPENAI_API_KEY = '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'
OPENAI_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
ORGANIZATION = 'org-uYUPnRbx4lMhXa7OSK9qLzvF'
openai.api_key = OPENAI_API_KEY
openai.organization = ORGANIZATION

def convert_to_wav(input_file, output_file, format="wav", ffmpeg_path=None):
    if not ffmpeg_path:
        raise ValueError("Please provide the path to the FFmpeg executable.")

    if os.path.exists(output_file):
        os.remove(output_file)

    command = [ffmpeg_path, "-i", input_file, "-acodec", "pcm_s16le", "-ar", "16000", output_file]

    try:
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        # Print the output and error messages
        #print("FFmpeg Output:", stdout.decode())
        #print("FFmpeg Error:", stderr.decode())

        if process.returncode != 0:
            print("FFmpeg process failed with return code:", process.returncode)

    except Exception as e:
        print("Error executing FFmpeg:", str(e))

def transcribe_audio(audio_file_path):
    ffmpeg_path = r'C:\\Users\\dhruv.sawhney\\OneDrive\\Apps\\ffmpeg-2023-11-13-git-67a2571a55-essentials_build\\bin\\ffmpeg.exe'

    # Convert to WAV if the input file is not in WAV format
    if audio_file_path.endswith(".m4a"):
        converted_file_path = audio_file_path.replace(".m4a", "_converted.wav")
        convert_to_wav(audio_file_path, converted_file_path, ffmpeg_path=ffmpeg_path)
        audio_file_path = converted_file_path

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Record the entire audio file
        try:
            transcript = recognizer.recognize_google(audio_data, language="en-US")
            print("Transcript: {}".format(transcript))
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")

    # Clean up the converted file if it was created
    if audio_file_path.endswith("_converted.wav"):
        os.remove(audio_file_path)

def chatgpt_interaction(prompt):

    """headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}',
    }"""
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'},
                     {'role': 'user', 'content': prompt}],
    }

    #response = requests.post(OPENAI_ENDPOINT, headers=headers, data=json.dumps(data))
    #response_data = response.json()
    
    #client = openai.OpenAI(organization=ORGANIZATION)
    
    response = openai.chat.completions.create(**data)

    #return response_data['choices'][0]['message']['content']
    #return client.models.list()
    return response
    

    """response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
        )"""

if __name__ == "__main__":
    transcribe_audio(r'C:\\Users\\dhruv.sawhney\\Documents\\Sound recordings\\P5.m4a')
    
    #response = chatgpt_interaction("Give me some interview tips.")
    #print(response)