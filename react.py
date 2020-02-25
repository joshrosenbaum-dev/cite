from time import sleep
from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from pandas_csv import get_plot

class Marker:
    def __init__(self, fid):
        # Retrieve ID based on touch.fid, position based on touch.pos
        self.fid = fid
        self.pos = [100.0, 100.0]
        self.type = self.indicator_id = self.artifact_id = self.label = self.file = self.icon = None
        self.is_x = self.is_y = self.is_time = False       

        # TODO: Move to loadData in MarkerHandler
        attributes = JsonStore("attributes.json")
        indicators = JsonStore("indicators.json")
        artifacts = JsonStore("artifacts.json")

        fid_str = str(self.fid)

        # Check if ID is in attributes table
        if attributes.exists(fid_str):
            attribute = attributes.get(fid_str)
            if attribute.get("is_x"):
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
                # TODO: Match indicator to preloaded dataframe vs. file
                self.file = "csv/" + indicator.get("file")
            elif attribute.get("artifact"):
                artifact = artifacts.get(attribute.get("artifact"))
                self.artifact_id = attribute.get("artifact")
                self.type = "Artifact"
                self.label = artifact.get("label")
                self.icon = "icons/" + artifact.get("abbr") + ".png"
   
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
    markers_ontable = [Marker(0), Marker(1), Marker(2), Marker(11), Marker(12), Marker(21), Marker(22), Marker(24)]
    # markers_ontable = []
    
    def loadData(self):
        print("Loading")
        self.indicatorData = {}
        # Key --> indicator "0", "1"
        # Data --> Pandas dataframe, based on filename generated from JSON

    def on_touch_down(self, touch):
        # Put down all markers, see if on touch down prints before loading
        print("On touch down")
        self.table_init()
        if "markerid" in touch.profile:
            marker = Marker(touch)
            self.markers_ontable.append(marker)
            # self.table_init()

    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markers_ontable:
                if marker.fid == touch.fid:
                    self.markers_ontable.remove(marker)
            self.table_init()

    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markers_ontable:
                if marker.fid == touch.fid:   
                    marker.x = touch.x
                    marker.y = touch.y

    def table_init(self):
        attributes = JsonStore("attributes.json")
        indicators_mot, artifacts_mot, end_plots = [], [], []

        print("\nID\tIS_X\tIS_Y\tTIME\tPOSITION\t\tINDICATOR_ID\tCOUNTRY_ID\tTYPE (LABEL)")
        print("===================================================================================================================")
        if len(self.markers_ontable) == 0:
            print("N/A\t No markers are on the table ------------------------------------------------------------------------------")
        for index, marker in enumerate(self.markers_ontable):
            if attributes.exists(str(marker.fid)):
                if marker.type == "Indicator":
                    indicators_mot.append(index)
                if marker.type == "Artifact":
                    artifacts_mot.append(index)
                marker.to_string()
            else:
                print(marker.fid,"\t ----------------------------------------------------------------------------------------------------------")

        print("\nINDICATORS_MOT:",indicators_mot,len(indicators_mot))
        print("COUNTRIES_MOT:",artifacts_mot,len(artifacts_mot))

        if len(indicators_mot) >= 2 and len(artifacts_mot) >= 1:
            x = indicators_mot[0]
            y = indicators_mot[1]
            for mot_entry in artifacts_mot:
                # firstData = indicatorData[self.markers_ontable[x].indID]
                end_plots.append(get_plot(self.markers_ontable[x], self.markers_ontable[y], self.markers_ontable[mot_entry]))

        print(end_plots)

class ReactivisionApp(App):
    def build(self):
        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")
        # Deletable configuration for window sizing
        Config.set("graphics", "width", "640")
        Config.set("graphics", "height", "480")
        Config.set("graphics", "position", "custom")
        Config.set("graphics", "left", 850)
        Config.set("graphics", "top",  100)
        sleep(0.75)
        Handler = MarkerHandler()
        Handler.loadData() 
        sleep(0.75)
        return Handler

if __name__ == "__main__":
    ReactivisionApp().run()