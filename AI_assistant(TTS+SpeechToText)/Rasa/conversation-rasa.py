import speech_recognition as sr
import pyttsx3
import requests
import asyncio
from rasa.shared.utils.io import json_to_string

#from rasa.nlu.model import Interpreter
# Load the Rasa NLU model
#interpreter = Interpreter.load("rasa\models\nlu-20231117-113221-hoary-trap.tar.gz")

from rasa.core.agent import Agent
interpreter = Agent.load(model_path='models\\nlu-20231117-113221-hoary-trap.tar.gz')
print("Rasa model loaded")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error with the speech recognition service; {e}"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def rasa_interaction(user_input):
    # Use the Rasa NLU model to get the response
    response = asyncio.run(interpreter.parse_message(user_input))
    #return json_to_string(response)
    return response

# Main loop
while True:
    #user_input = speech_to_text()
    user_input = "Hello"
    print("You:", user_input)

    # Use Rasa for chat-based interaction
    rasa_response = rasa_interaction(user_input)
    print(rasa_response)

    intent = rasa_response['intent']['name']
    entities = rasa_response['entities']

    print(intent)
    print(entities)
    exit()
    # Add logic for handling specific intents or commands
    if intent == "interview_tips":
        response = "Sure, here are some interview tips..."
        print("Assistant:", response)
        #text_to_speech(response)
    else:
        response = "I'm not sure how to respond to that."
        print("Assistant:", response)
        #text_to_speech(response)
