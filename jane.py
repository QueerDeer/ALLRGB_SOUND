#!/usr/bin/env python3

import time
import subprocess
import speech_recognition as sr
from chatterbot import ChatBot
import os


def callback(recognizer, audio):
    try:

        try:
            request = recognizer.recognize_google(audio)
        except:
            request = recognizer.recognize_sphinx(audio)
        print("thinks you said " + request)

        if request:
            if "turn" in request and "off" in request.split():
                stop_listening(wait_for_stop=False)
                os._exit(1)
            else:
                response = chatbot.get_response(request)
                subprocess.Popen('/bin/echo "{}" | /usr/bin/festival --tts'.format(response), shell=True)
                print(response)

    except sr.UnknownValueError:
        print("could not understand you")
    except sr.RequestError as e:
        print("could hear anything from ; {0}".format(e))


chatbot = ChatBot('Jane Py', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

#chatbot.train("chatterbot.corpus.english")


r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m, callback)

for _ in range(50): time.sleep(0.1)

while True: time.sleep(0.1)
