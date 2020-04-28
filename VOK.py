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
from module import Microstream as mc
from six.moves import queue


RATE = 16000
CHUNK = int(RATE / 10)  # 100ms]
client = speech.SpeechClient()
Ending = 0

def speak(text, name):
    tts = gTTS(text=text,lang="ko")
    filename = os.path.join(".","voice",name+".mp3")
    tts.save(filename)
    playsound.playsound(filename)
    

def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    global Ending
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:


            if re.search(r'\b(안녕하세요|안녕)\b', transcript, re.I):
                print("당신 : ", transcript)
                print("컴퓨터  : 안녕하세요 저는 컴퓨터 입니다.")
                speak("안녕하세요 저는 테스트 컴퓨터 입니다.","hello")
                break
                
            elif re.search(r'\b(아메리카노 주세요)\b', transcript, re.I):
                print("당신 : ", transcript)
                print("컴퓨터  : 아메리카노 한잔 맞으신가요?")
                speak("아메리카노 한잔 맞으신가요?","order")
                break
            elif re.search(r'\b(너는 뭐야)\b', transcript, re.I):
                print("당신 : ", transcript)
                print("컴퓨터  : 저는 제영님이 만든 ProtoType STT to TTS 머신입니다.")
                speak("저는 제영님이 만든 ProtoType STT to TTS 머신입니다.","order")
                break
                
            #sys.stdout.write(transcript + overwrite_chars + '\r')
            #sys.stdout.flush()

            #num_chars_printed = len(transcript)

        else:
            #print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(끝내자)\b', transcript, re.I):
                print("당신 : ", transcript)
                print("컴퓨터 : 안녕히 가세요.")
                Ending = 1
                speak("안녕히 가세요.","end")
                print('Exiting..')
                break

            num_chars_printed = 0

def Stream(streaming_config):

    

    with mc.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        

        # Now, put the transcription responses to use.
        listen_print_loop(responses)
            


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ko-kr'  # a BCP-47 language tag

    if not os.path.exists(os.path.join(".","voice")): os.mkdir(os.path.join(".","voice"))

    
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    while True:

        Stream(streaming_config)
        if Ending == 1: break
    
    
    shutil.rmtree(os.path.join(".","voice"))

if __name__ == '__main__':
    main()
