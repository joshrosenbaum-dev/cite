from gtts import gTTS

def saveTTS(fid, label):
    audioStrings = []
    flag = 0
    while (flag <= 1):
        if (flag == 0):
            status = "add"
            string = "Adding " + label + "."
        if (flag == 1):
            status = "remove"
            string = "Removing " + label + "."
        tts = gTTS(text=string, lang='en', slow=False)
        save_string = 'audio/' + format(fid) + '-' + status + '.mp3'
        tts.save(save_string)
        audioStrings.append(save_string)
        # print("Created audio: '" + string + "' at /" + save_string)
        flag += 1
    return audioStrings