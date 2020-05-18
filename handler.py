#   handler.py
#   -------------------------------------------------------
#   Initial loading of JSON attributes, audio, and marker
#   reference data.
#
#   https://kivy.org/doc/stable/api-kivy.storage.html

from enum import Enum
from gtts import gTTS
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
import hashlib, os, pandas, shutil

class MarkerType(Enum):
    X = "X Bucket"
    Y = "Y Bucket"
    TIME = "Time Dial"
    ARTIFACT = "Artifact"
    INDICATOR = "Indicator"

class CITEHandler(Widget):
    def generateAudio(self, audioLoc, fidicualID, string):
        tts = gTTS(text = string, lang = 'en', slow = False)
        saveFile = audioLoc + format(fidicualID) + ".mp3"
        tts.save(saveFile)
        print("[CITE   ] Creating audio: '" + string + "' at './" + saveFile + "'")
        return saveFile

    def generateHashes(self, jsonFiles):
        jsonHashes = []
        block_size = 65536  # 64KB
        for r in range(len(jsonFiles)):
            file = jsonFiles[r]
            hash = hashlib.md5()
            with open(file, 'rb') as f:
                buffer = f.read(block_size)
                while len(buffer) > 0:
                    hash.update(buffer)
                    buffer = f.read(block_size)
            jsonHashes.append(hash.hexdigest())
        return jsonHashes

    def load(self):
        print("==========================================================================================")
        print("Collaborative Interactive Tabletop for Education (CITE) v1.0.0")
        print("==========================================================================================")
        print("[CITE   ] Loading CITE...")

        audioLoc = "audio/"
        dataLoc = "data/"
        jsonLoc = "json/"
        jsonCacheLoc = "json/cache"
        jsonFiles = [jsonLoc + "artifacts.json", jsonLoc + "attributes.json", jsonLoc + "indicators.json"]
        
        self.cacheMismatch = False
        self.loadAttributes = False

        if os.path.exists(jsonCacheLoc):
            cache = open(jsonCacheLoc, "r")
            jsonHash = self.generateHashes(jsonFiles)
            jsonFileHash = [line.rstrip() for line in cache]
            cache.close()

            for index in range(len(jsonHash)):
                if jsonHash[index] != jsonFileHash[index]:
                    print("[CITE   ] Cache mismatch for " + jsonFiles[index])
                    print("[CITE   ] Deleting previously generated cache file")
                    self.cacheMismatch = True
                    break

            if not self.cacheMismatch:
                print("[CITE   ] Cached hashes match current JSON file hashes")
                if len(jsonFileHash) < 4:
                    self.loadAttributes = True
                if len(jsonFileHash) > 4:
                    if jsonFileHash[3] == "audio_written":
                        print("[CITE   ] Using previously generated audio files")
                    else:
                        self.loadAttributes = True

        if self.cacheMismatch or not os.path.exists(jsonCacheLoc):
            print("[CITE   ] Creating cache file './json/cache'")
            cache = open(jsonCacheLoc, "w")
            jsonHash = self.generateHashes(jsonFiles)
            for index in range(len(jsonHash)):
                cache.write(jsonHash[index] + "\n")
            cache.close()
            self.loadAttributes = True

        self.jsonData = {}
        self.jsonData["artifacts"] = JsonStore(jsonFiles[0])
        self.jsonData["attributes"] = JsonStore(jsonFiles[1])
        self.jsonData["indicators"] = JsonStore(jsonFiles[2])

        self.indicatorData = {}
        indicators = self.jsonData["indicators"]

        #   Create a key, value pair where the key is the ID
        #   of the indicator, and the value is a dataframe
        #   provided by pandas. The ID and file for the pair
        #   comes from the JSON file for indicators.

        for index in indicators:
            loadedCSV = dataLoc + "indicators/" + format(indicators[index].get("file"))
            self.indicatorData[index] = pandas.read_csv(loadedCSV, index_col = "country")

        #   Get population size for the graph's bubble sizes.
        #   The region population is unused, but for reference.

        self.df_popSizeByArtifact = pandas.read_csv(dataLoc + "artifacts/population_countries.csv", index_col = "name")
        self.df_popSizeByArtifactRegion = pandas.read_csv(dataLoc + "artifacts/population_regions.csv", index_col = "name")

        #   The markerData dictionary will be sent to the Marker 
        #   class to determine the Marker's class variable values.

        self.markerData = {}
        # artifacts = self.jsonData["artifacts"]
        attributes = self.jsonData["attributes"]

        if self.loadAttributes:
            if os.path.exists(audioLoc):
                shutil.rmtree(audioLoc)
            if not os.path.exists(os.path.join(os.getcwd(), audioLoc)):
                os.makedirs(audioLoc)
                self.generateAudio(audioLoc, "-add", "Adding")
                self.generateAudio(audioLoc, "-rem", "Removing")
                self.generateAudio(audioLoc, "-unk", "Unknown Marker")
            for index in attributes:
                attribute = attributes.get(index)
                if attribute.get("is_x"):
                    self.markerData[index] = self.generateAudio(audioLoc, index, MarkerType.X.value)
                elif attribute.get("is_y"):
                    self.markerData[index] = self.generateAudio(audioLoc, index, MarkerType.Y.value)
                elif attribute.get("is_time"):
                    self.markerData[index] = self.generateAudio(audioLoc, index, MarkerType.TIME.value)
                elif attribute.get("indicator"):
                    pass
                    # indicator = indicators.get(attribute.get("indicator"))
                elif attribute.get("artifact"):
                    pass
                    # artifact = artifacts.get(attribute.get("artifact"))
            cache = open(jsonCacheLoc, "a")
            cache.write("audio_written")
            cache.close()
        else:
            for index in attributes:
                self.markerData[index] = [audioLoc + index + ".mp3"]
            
        self.markersOnTable = []

        print("==========================================================================================")

        # self.tableInit()
        return self