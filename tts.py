from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang='en', slow=False)
