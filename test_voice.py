from __future__ import division

import re
import os,sys
import shutil
import time
import playsound

from gtts import gTTS
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio

if not os.path.exists(os.path.join(".","voice")): os.mkdir(os.path.join(".","voice"))


def speak(text, name):
    tts = gTTS(text=text,lang="en")
    filename = os.path.join(".","voice",name+".mp3")
    tts.save(filename)
    playsound.playsound(filename)

speak("Sergey loffe","people")
speak("Christian Szegedy","people2")

shutil.rmtree(os.path.join(".","voice"))
    
