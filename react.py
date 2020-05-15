from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.storage.jsonstore import JsonStore
from playsound import playsound
from time import sleep
#################################
from pandas_csv import getPoint
from mpl import plotPoints
from tts import saveTTS
#################################
import datetime as dt
import hashlib
import matplotlib.pyplot as plt
import pandas as pd
import os, shutil

class Marker:
    def __init__(self, touch, jsonData):
        # Retrieve ID based on touch.fid, position based on touch.pos
        self.fid = touch.fid
        self.pos = touch.pos
        self.type = None
        self.indicator_id = None
        self.artifact_id = None
        self.label = None
        self.abbr = None
        self.is_x = False
        self.is_y = False
        self.is_time = False
        self.audio_saved = False   

        attributes = jsonData["attributes"]
        indicators = jsonData["indicators"]
        artifacts = jsonData["artifacts"]
        fid_str = str(self.fid)

        # Check if ID is in attributes table
        if attributes.exists(fid_str):
            attribute = attributes.get(fid_str)
            if attribute.get("is_x"):
                # TODO: Make type an enum?
                self.type = "X"
                self.is_x = True
            elif attribute.get("is_y"):
                self.type = "Y"
                self.is_y = True
            elif attribute.get("is_time"):
                self.type = "Time"
                self.is_time = True
            elif attribute.get("indicator"):
                indicator = indicators.get(attribute.get("indicator"))
                self.indicator_id = attribute.get("indicator")
                self.type = "Indicator"
                self.label = indicator.get("label")
            elif attribute.get("artifact"):
                artifact = artifacts.get(attribute.get("artifact"))
                self.artifact_id = attribute.get("artifact")
                self.type = "Artifact"
                self.label = artifact.get("label")
                self.abbr = artifact.get("abbr")
   
    def toString(self):
        print(self.fid,"\t", end = "")
        print(self.is_x,"\t", end = "")
        print(self.is_y,"\t", end = "")
        print(self.is_time,"\t", end = "")
        print("(" + format(self.pos[0], '.2f') + ", " + format(self.pos[1], '.2f') + ")\t", end = "")
        print(self.indicator_id,"\t\t", end = "")
        print(self.artifact_id,"\t\t", end = "")
        print(self.type, end = " ")
        print("(" + format(self.label) + ")","\t")

class MarkerHandler(Widget):
    def hashes(self, jsonFiles):
        jsonHash = []
        block_size = 65536  # 64KB
        for r in range(len(jsonFiles)):
            print
            file = jsonFiles[r]
            hash = hashlib.md5()
            with open(file, 'rb') as f:
                buffer = f.read(block_size)
                while len(buffer) > 0:
                    hash.update(buffer)
                    buffer = f.read(block_size)
            jsonHash.append(hash.hexdigest())
        return jsonHash

    def preloader(self, myGraph):
        print("==========================================================================================")
        print("Collaborative Tabletop for Education (CITE) v1.0.0")
        print("==========================================================================================")
        print("[CITE   ] Loading CITE...")

        jsonFiles = ["attributes.json", "indicators.json", "artifacts.json"]
        self.cacheMismatch = False
        self.audioLoad = False

        if os.path.exists("cache"):
            cache = open("cache", "r")
            jsonHash = self.hashes(jsonFiles)
            fileHash = [line.rstrip() for line in cache]
            cache.close()
            
            for j in range(len(jsonHash)):
                if jsonHash[j] != fileHash[j]:
                    print("[CITE   ] Cache mismatch for " + jsonFiles[j])
                    print("[CITE   ] Deleting previously generated cache file")
                    self.cacheMismatch = True
                    break

            if not self.cacheMismatch:
                print("[CITE   ] Cached hashes match current JSON file hashes")
                if len(fileHash) < 4:
                    self.audioLoad = True
                if len(fileHash) > 4:
                    if fileHash[3] == "audio_written":
                        print("[CITE   ] Using previously generated audio files")
                    else:
                        self.audioLoad = True

        if self.cacheMismatch or not os.path.exists("cache"):
            print("[CITE   ] Creating cache file './cache'")
            cache = open("cache", "w")
            jsonHash = self.hashes(jsonFiles)
            for j in range(len(jsonHash)):
                cache.write(jsonHash[j] + "\n")
            cache.close()
            self.audioLoad = True

        self.jsonData = {}
        self.jsonData["attributes"] = JsonStore(jsonFiles[0])
        self.jsonData["indicators"] = JsonStore(jsonFiles[1])
        self.jsonData["artifacts"] = JsonStore(jsonFiles[2])

        self.myGraph = myGraph
     
        self.indicatorData = {}
        indicators = self.jsonData["indicators"]
        csvArtifact = "country"
        # Key --> indicator "0", "1"
        # Data --> Pandas dataframe, based on filename generated from JSON
        for i in indicators:
            loadedCSV = "indicators/" + format(indicators[i].get("file"))
            dataframe = pd.read_csv(loadedCSV, index_col = csvArtifact)
            self.indicatorData[i] = dataframe

        self.df_popSizeByArtifact = pd.read_csv("artifacts/population_countries.csv", index_col = "name")
        self.df_popSizeByRegion = pd.read_csv("artifacts/population_regions.csv", index_col = "name")

        self.artifactData = {}
        artifacts = self.jsonData["artifacts"]
        for a in artifacts:
            loadedIcon = "artifacts/icons/" + format(artifacts[a].get("abbr")) + ".png"
            self.artifactData[a] = loadedIcon

        self.audioData = {}
        attributes = self.jsonData["attributes"]

        if self.audioLoad:
            if os.path.exists("audio/"):
                shutil.rmtree("audio/")
            if not os.path.exists(os.path.join(os.getcwd(), "audio")):
                os.makedirs("audio/")
            for a in attributes:
                attribute = attributes.get(a)
                if attribute.get("is_x"):
                    self.audioData[a] = saveTTS(a, "X bucket")
                elif attribute.get("is_y"):
                    self.audioData[a] = saveTTS(a, "Y bucket")
                elif attribute.get("is_time"):
                    self.audioData[a] = saveTTS(a, "time dial")
                elif attribute.get("indicator"):
                    indicator = indicators.get(attribute.get("indicator"))
                    self.audioData[a] = saveTTS(a, indicator.get("label"))
                elif attribute.get("artifact"):
                    artifact = artifacts.get(attribute.get("artifact"))
                    self.audioData[a] = saveTTS(a, artifact.get("label"))
            saveTTS(-1, "unknown marker")
            cache = open("cache", "a")
            cache.write("audio_written")
            cache.close()
        else:
            for a in attributes:
                self.audioData[a] = ["audio/" + a + "-add.mp3", "audio/" + a + "-remove.mp3"]
            
        self.markersOnTable = []

        print("==========================================================================================")

        self.tableInit()
    
    def on_touch_down(self, touch):
        if "markerid" in touch.profile:
            marker = Marker(touch, self.jsonData)
            self.markersOnTable.append(marker)
            # if format(touch.fid) not in self.audioData:
            #     playsound("audio/-1-add.mp3")
            # else:
            #     playsound(self.audioData[format(touch.fid)][0])
            self.tableInit()

    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fid == touch.fid:
                    self.markersOnTable.remove(marker)
                    # if format(touch.fid) not in self.audioData:
                    #     playsound("audio/-1-remove.mp3")
                    # else:
                    #     playsound(self.audioData[format(touch.fid)][1])
            self.tableInit()

    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fid == touch.fid:   
                    marker.pos = touch.pos
                    self.tableInit()

    def tableInit(self):
        indicatorsMOT, artifactsMOT, points = [], [], []

        x_index = -1
        y_index = -1
        x = None
        y = None

        # Note: camera is 800x600, base distances on the fact that markers are 110x110
        # scale factor * size of bucket markers - factor can't be less than .5, probably MORE.
        # Use a global scale factor variable and size of bucket markers -- all fidicual markers are 110px given 800x600 camera size

        # Constant = any marker size in px
        # We should assume 800x600 camera image - if it's 110 px, figure out screen scale, adjust accordingly
        # If resolution changes -- we can adjust - rn we worry about the table size.
        # Any calculations on dist (min distance between )

        # Eventually, ask Kivy for camera resolution. Use 110 for 800x600 as a ratio, possibly, scale when we can.
    
        markerSize = 110
        padding = 10

        if len(self.markersOnTable) > 0:
            print("[CITE   ] Indexing markers...")
            for index, marker in enumerate(self.markersOnTable):
                if self.jsonData["attributes"].exists(str(marker.fid)):
                    if marker.type == "Indicator":
                        indicatorsMOT.append(index)
                    if marker.type == "Artifact":
                        artifactsMOT.append(index)
                    if marker.type == "X":
                        x_index = index
                    if marker.type == "Y":
                        y_index = index

            # print("Current X index:", x_index)
            # print("Current Y index:", y_index)
            
            if len(indicatorsMOT) >= 2:
                print("[CITE   ] There are enough indicators on the table.")

                if x_index != -1 and y_index != -1:
                    # print("X ==========")
                    # self.markersOnTable[x_index].toString()
                    # print("Y ==========")
                    # self.markersOnTable[y_index].toString()

                    # Find X:
                    print("[CITE   ] Seeking markers for X...")
                    currentDiff = markerSize + padding
                    for index in range(len(indicatorsMOT)):
                        marker = self.markersOnTable[indicatorsMOT[index]]
                        bucket = self.markersOnTable[x_index]
                        # print("Marker:", marker.label, marker.pos, "Bucket:", bucket.pos)
                        dbX = abs(bucket.pos[0] - marker.pos[0])
                        dbY = abs(bucket.pos[1] - marker.pos[1])
                        diffBetween = [dbX, dbY, dbX + dbY]
                        # print(diffBetween[2])
                        if diffBetween[2] <= currentDiff:
                            currentDiff = diffBetween[2]
                            x = marker
                            # print("X ==========")
                            # x.toString()

                    # Find Y:
                    print("[CITE   ] Seeking markers for Y...")
                    currentDiff = markerSize + padding
                    for index in range(len(indicatorsMOT)):
                        marker = self.markersOnTable[indicatorsMOT[index]]
                        bucket = self.markersOnTable[y_index]
                        # print("Marker:", marker.label, marker.pos, "Bucket:", bucket.pos)
                        dbX = abs(bucket.pos[0] - marker.pos[0])
                        dbY = abs(bucket.pos[1] - marker.pos[1])
                        diffBetween = [dbX, dbY, dbX + dbY]
                        # print(diffBetween[2])
                        if diffBetween[2] <= currentDiff:
                            currentDiff = diffBetween[2]
                            y = marker
                            # print("Y ==========")
                            # y.toString()
                            
                if x != None and y != None:
                    print("[CITE   ] Generating graph with indicators.\n")
                    for mot_entry in artifactsMOT:
                        xFrame = self.indicatorData[x.indicator_id]
                        yFrame = self.indicatorData[y.indicator_id]
                        points.append(getPoint(xFrame, yFrame, self.df_popSizeByArtifact, self.markersOnTable[mot_entry]))
                    plotPoints(points, x.label, y.label)
                    self.myGraph.draw()
                else:
                    print("[CITE   ] Not enough inidcators in range.\n")
                    plotPoints([], None, None)
                    self.myGraph.draw()
            else:
                print("[CITE   ] There are not enough indicators on the table.\n")
                plotPoints([], None, None)
                self.myGraph.draw()

class ReactivisionApp(App):
    def build(self):
        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")
        # Create matplotlib canvas and pass graph to Handler class
        Canvas = FigureCanvasKivyAgg(plt.gcf())
        Handler = MarkerHandler()
        Handler.preloader(Canvas)
        # Create app bounding box
        Box = FloatLayout()
        Box.add_widget(Handler)
        Box.add_widget(Canvas)
        return Box

if __name__ == "__main__":
    ReactivisionApp().run()