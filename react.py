from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from random import random
from pandas_csv import get_plot

class Marker:
    def __init__(self, fid): # , touch):
        self.fid = fid
        self.x = 100. # touch.pos[0]
        self.y = 100. # touch.pos[1]
        self.color = (random(), random(), random())
        
        self.is_x = self.is_y = self.is_time = False
        self.icon = self.axis_label = self.file = self.country = None

        attributes = JsonStore("attributes.json")   # Sourced from: https://kivy.org/doc/stable/api-kivy.storage.jsonstore.html 
        if attributes.exists(str(self.fid)):
            if attributes.get(str(self.fid)).get("is_x"):
                self.is_x = True
            elif attributes.get(str(self.fid)).get("is_y"):
                self.is_y = True
            elif attributes.get(str(self.fid)).get("is_time"):
                self.is_time = True
            elif attributes.get(str(self.fid)).get("indicator"):
                indicators = JsonStore("indicators.json")
                indicator = indicators.get(attributes.get(str(self.fid)).get("indicator"))
                # TODO: Save indicator ID
                # TODO: Make a markerType field
                self.axis_label = indicator.get("label")
                self.file = "csv/" + indicator.get("file") # change for dataframe
            elif attributes.get(str(self.fid)).get("country"):
                countries = JsonStore("countries.json")
                country = countries.get(attributes.get(str(self.fid)).get("country"))
                self.country = country.get("label")
                self.icon = "icons/" + country.get("abbr") + ".png"

class RVHandler(Widget):
    markers_ontable = [Marker(0), Marker(1), Marker(2), Marker(11), Marker(12), Marker(21), Marker(22), Marker(24)]
    #markers_ontable = []

    def loadData(self):
        print("Loading")
        self.indicatorData = {}
        # Key --> indicator "0", "1"
        # Data --> Pandas dataframe, based on filename generated from json

    def on_touch_down(self, touch):
        print("On touch down") # put down all markers, see if on touch down prints before loading
        self.table_status()
        if "markerid" in touch.profile:
            marker = Marker(touch)
            self.markers_ontable.append(marker)
            # self.table_status() # TODO: Rename this function as the table initializer.

    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markers_ontable:
                if marker.fid == touch.fid:
                    self.markers_ontable.remove(marker)
            self.table_status()

    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markers_ontable:
                if marker.fid == touch.fid:   
                    marker.x = touch.x
                    marker.y = touch.y
    
    def table_status(self):
        attributes = JsonStore("attributes.json")
        indicators_mot, countries_mot, end_plots = [], [], []

        print("\nID\t IS_X\t IS_Y\t TIME\t POSITION\t\t INDICATOR_ID\t COUNTRY_ID\t NOTES")
        print("===================================================================================================================")
        if len(self.markers_ontable) == 0:
            print("N/A\t No markers are on the table ------------------------------------------------------------------------------")
        for index, marker in enumerate(self.markers_ontable): 
            if attributes.exists(str(marker.fid)):
                indicator = attributes.get(str(marker.fid)).get("indicator")
                country = attributes.get(str(marker.fid)).get("country")
                if indicator:
                    indicators_mot.append(index)
                if country:
                    countries_mot.append(index)

        ##########################################################################################
                print(marker.fid,"\t",attributes.get(str(marker.fid)).get("is_x"), end = "")
                print("\t",attributes.get(str(marker.fid)).get("is_y"), end = "")
                print("\t",attributes.get(str(marker.fid)).get("is_time"), end = "")
                print("\t (" + format(marker.x, '.2f') + ", " + format(marker.y, '.2f') + ")", end ="")
                print("\t",indicator, end = "")
                print("\t\t",country, end = "")
                if marker.is_x:
                    print("\t\t","X Bucket")
                elif marker.is_y:
                    print("\t\t","Y Bucket")
                elif marker.is_time:
                    print("\t\t","Time Dial")
                elif marker.axis_label is not None:
                    print("\t\t",marker.axis_label)
                elif marker.country is not None:
                    print("\t\t",marker.country)
            else:
                print(marker.fid,"\t ----------------------------------------------------------------------------------------------------------")
        ##########################################################################################

        print("\nINDICATORS_MOT:",indicators_mot,len(indicators_mot))
        print("COUNTRIES_MOT:",countries_mot,len(countries_mot))

        if len(indicators_mot) >= 2 and len(countries_mot) >= 1:
            x = indicators_mot[0]
            y = indicators_mot[1]
            for mot_entry in countries_mot:
                # firstData = indicatorData[self.markers_ontable[x].indID]
                end_plots.append(get_plot(self.markers_ontable[x], self.markers_ontable[y], self.markers_ontable[mot_entry]))

        print(end_plots)

class RVApp(App):
    def build(self):
        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")
        # start deletable configuration
        Config.set("graphics", "width", "640")
        Config.set("graphics", "height", "480")
        Config.set("graphics", "position", "custom")
        Config.set("graphics", "left", 850)
        Config.set("graphics", "top",  100)
        # end deletable configuration
        handler = RVHandler()
        handler.loadData() # maybe put a sleep function after this to avoid overlap with touch -- load all CSV files
        return handler

if __name__ == "__main__":
    RVApp().run()