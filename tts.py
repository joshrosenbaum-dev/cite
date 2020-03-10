from gtts import gTTS
from playsound import playsound
import os 

#pip install gTTS playsound

def speak(string):
    tts = gTTS(text=string, lang='en', slow=False)
    if not os.path.exists(os.path.join(os.getcwd(), "audio")):
        os.makedirs("audio/")
    if os.path.exists("audio/output.mp3"):
        os.remove("audio/output.mp3")
    tts.save('audio/output.mp3')
    playsound('audio/output.mp3')
    os.remove("audio/output.mp3")