#   table.py
#   -------------------------------------------------------
#   Handles all events relating to the tabletop surface.

from kivy.uix.widget import Widget
from playsound import playsound
import marker as m
import main as cite

class TableHandler(Widget):
    #   There are three functions to process touch events.
    #   The on_touch_down function is when a marker is placed.
    #   The on_touch_up function is when a marker is removed.
    #   The on_touch_move function is when a marker is moved.

    def on_touch_down(self, touch):
        self = cite.CITEApp.self
        if "markerid" in touch.profile:
            marker = m.Marker(touch, self.markerData)
            playsound("audio/-add.mp3")
            if format(touch.fid) not in self.markerData:
                playsound("audio/-unk.mp3")
            else:
                playsound(marker.audio)
            self.markersOnTable.append(marker)
            self.tableInit()
    
    def on_touch_up(self, touch):
        self = cite.CITEApp.self
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fiducialID == touch.fid:
                    playsound("audio/-rem.mp3")
                    if format(touch.fid) not in self.markerData:
                        playsound("audio/-unk.mp3")
                    else:
                        playsound(marker.audio)
                    self.markersOnTable.remove(marker)
                    self.tableInit()


    def on_touch_move(self, touch):
        self = cite.CITEApp.self
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fiducialID == touch.fid:   
                    marker.currentPos = touch.pos
                    self.tableInit()