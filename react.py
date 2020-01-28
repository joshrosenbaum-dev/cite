from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
# from kivy.uix.label import Label
from kivy.graphics import Color #, Ellipse, Rectangle
from kivy.storage.jsonstore import JsonStore
from random import random

class Marker:
    def __init__(self, touch):
        self.fid = touch.fid
        self.x = touch.pos[0]
        self.y = touch.pos[1]
        self.color = (random(), random(), random())
        
        self.is_x = self.is_y = self.is_time = False
        self.icon = self.axis_label = self.file = self.country = None
        # self.notes = "N/A (Unknown)"
        # self.width = 30

        attributes = JsonStore("attributes.json")   # Sourced from: https://kivy.org/doc/stable/api-kivy.storage.jsonstore.html 
        if attributes.exists(str(self.fid)):
            if attributes.get(str(self.fid)).get("is_x"):
                # self.notes = "X Bucket"
                self.is_x = True
            elif attributes.get(str(self.fid)).get("is_y"):
                # self.notes = "Y Bucket"
                self.is_y = True
            elif attributes.get(str(self.fid)).get("is_time"):
                # self.notes = "Time Dial"
                self.is_time = True
            elif attributes.get(str(self.fid)).get("indicator"):
                indicators = JsonStore("indicators.json")
                indicator = indicators.get(attributes.get(str(self.fid)).get("indicator"))
                # self.notes = indicator.get("label") + " (" + indicator.get("file") + ")"
                self.axis_label = indicator.get("label")
                self.file = "csv/" + indicator.get("file")
            elif attributes.get(str(self.fid)).get("country"):
                countries = JsonStore("countries.json")
                country = countries.get(attributes.get(str(self.fid)).get("country"))
                # self.notes = country.get("label") + " (" + country.get("abbr") + ")"
                self.country = country.get("label")
                self.icon = "icons/" + country.get("abbr") + ".png"

        # if self.icon is None:
        #     self.width = 42

        # self.label = Label()

    # def draw(self, handler):    # Sourced from: https://kivy.org/doc/stable/tutorials/firstwidget.html
    #     handler.remove_widget(self.label)
    #     self.updateLabel()
    #     if self.icon is None:
    #         with handler.canvas:
    #             Color(*self.color)
    #             Ellipse(pos=(self.x - 7, self.y - 7), size=(14, 14))
    #     else:
    #         with handler.canvas:
    #             Color(1, 1, 1)
    #             Rectangle(source=self.icon, pos=(self.x, self.y), size=(30, 20))
    #     handler.add_widget(self.label)

    # def updateLabel(self):      # Sourced from: https://kivy.org/doc/stable/examples/gen__demo__touchtracer__main__py.html
    #     self.label.text = '[%s] (%d, %d) %s' % (self.fid, self.x, self.y, self.notes)
    #     self.label.texture_update()
    #     self.label.pos = [self.x - self.width, self.y - 10]

class RVHandler(Widget):
    markers_ontable = []

    def on_touch_down(self, touch):
        self.table_status()
        if "markerid" in touch.profile:
            marker = Marker(touch)
            self.markers_ontable.append(marker)
            # marker.draw(self)
            self.table_status()

    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markers_ontable:
                if marker.fid == touch.fid:
                    self.markers_ontable.remove(marker)
                    # self.remove_widget(marker.label)
            self.table_status()

    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markers_ontable:
                if marker.fid == touch.fid:   
                    marker.x = touch.x
                    marker.y = touch.y
                    # marker.draw(self)
    
    def table_status(self):
        attributes = JsonStore("attributes.json")
        print("\nID\t IS_X\t IS_Y\t TIME\t POSITION\t\t INDICATOR_ID\t COUNTRY_ID\t NOTES")
        print("===================================================================================================================")
        if len(self.markers_ontable) == 0:
            print("N/A\t No markers are on the table ------------------------------------------------------------------------------")
        for marker in self.markers_ontable: 
            if attributes.exists(str(marker.fid)):
                print(marker.fid,"\t",attributes.get(str(marker.fid)).get("is_x"), end = "")
                print("\t",attributes.get(str(marker.fid)).get("is_y"), end = "")
                print("\t",attributes.get(str(marker.fid)).get("is_time"), end = "")
                print("\t (" + format(marker.x, '.2f') + ", " + format(marker.y, '.2f') + ")", end ="")
                print("\t",attributes.get(str(marker.fid)).get("indicator"), end = "")
                print("\t\t",attributes.get(str(marker.fid)).get("country"), end = "")
                # print("\t\t",marker.notes)
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
        return RVHandler()

if __name__ == "__main__":
    RVApp().run()