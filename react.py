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
   
    def to_string(self):
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
    def loadData(self, myGraph):
        print("[INFO   ] [--- CITE ---] Loading...")
        self.jsonData = {}
        self.jsonData["attributes"] = JsonStore("attributes.json")
        self.jsonData["indicators"] = JsonStore("indicators.json")
        self.jsonData["artifacts"] = JsonStore("artifacts.json")

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

        if os.path.exists("audio/"):
            shutil.rmtree("audio/")
        if not os.path.exists(os.path.join(os.getcwd(), "audio")):
            os.makedirs("audio/")

        self.audioData = {}
        attributes = self.jsonData["attributes"]
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
        print(self.audioData)

        self.markersOnTable = []

        self.tableInit()
    
    def on_touch_down(self, touch):
        if "markerid" in touch.profile:
            marker = Marker(touch, self.jsonData)
            self.markersOnTable.append(marker)
            if self.audioData[format(touch.fid)]:
                playsound(self.audioData[format(touch.fid)][0])
            self.tableInit()

    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fid == touch.fid:
                    self.markersOnTable.remove(marker)
                    if self.audioData[format(touch.fid)]:
                        playsound(self.audioData[format(touch.fid)][1])
            self.tableInit()

    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fid == touch.fid:   
                    marker.pos = touch.pos

    def tableInit(self):
        # starttime = dt.time.microsecond
        indicatorsMOT, artifactsMOT, points = [], [], []

        for index, marker in enumerate(self.markersOnTable):
            if self.jsonData["attributes"].exists(str(marker.fid)):
                if marker.type == "Indicator":
                    indicatorsMOT.append(index)
                if marker.type == "Artifact":
                    artifactsMOT.append(index)

        if len(indicatorsMOT) >= 2:
            x = indicatorsMOT[0]
            y = indicatorsMOT[1]
            for mot_entry in artifactsMOT:
                xFrame = self.indicatorData[self.markersOnTable[x].indicator_id]
                yFrame = self.indicatorData[self.markersOnTable[y].indicator_id]
                points.append(getPoint(xFrame, yFrame, self.df_popSizeByArtifact, self.markersOnTable[mot_entry].label))
                # endtime = dt.time.microsecond
                # print("TIME:", (endtime-starttime))
            plotPoints(points, self.markersOnTable[x].label, self.markersOnTable[y].label)
            self.myGraph.draw()
        else:
            plotPoints([], "Unspecified", "Unspecified")
            self.myGraph.draw()

class ReactivisionApp(App):
    def build(self):
        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")
        # Deletable configuration for window sizing
        Config.set("graphics", "width", "640")
        Config.set("graphics", "height", "480")
        Config.set("graphics", "position", "custom")
        Config.set("graphics", "left", 850)
        Config.set("graphics", "top",  100)
        # Create matplotlib canvas and pass graph to Handler class
        Canvas = FigureCanvasKivyAgg(plt.gcf())
        Handler = MarkerHandler()
        Handler.loadData(Canvas)
        # Create app bounding box
        Box = FloatLayout()
        Box.add_widget(Handler)
        Box.add_widget(Canvas)
        return Box

if __name__ == "__main__":
    ReactivisionApp().run()