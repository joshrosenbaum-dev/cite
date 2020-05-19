#   table.py
#   -------------------------------------------------------
#   Handles all events relating to the tabletop surface.
#
#   Note about playsound function:
#       playsound(<audio file>, <flag>)
#   Setting the <flag> to False allows the audio to play
#   asynchonously.

from kivy.uix.widget import Widget
from playsound import playsound
import marker as m

class TableHandler(Widget):
    def generateTable(self, package):
        self.markerData = package.markerData
        self.markersOnTable = package.markersOnTable
        self.graph = package.graph
        self.generateGraph(0)
        
    #   There are three functions to process touch events.
    #   The on_touch_down function is when a marker is placed.
    #   The on_touch_up function is when a marker is removed.
    #   The on_touch_move function is when a marker is moved.

    def on_touch_down(self, touch):
        if "markerid" in touch.profile:
            marker = m.Marker(touch, self.markerData)
            playsound("audio/-add.mp3")
            if format(touch.fid) not in self.markerData:
                playsound("audio/-unk.mp3")
            else:
                playsound(marker.audio)
            self.markersOnTable.append(marker)
            self.generateGraph(1)
    
    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fiducialID == touch.fid:
                    playsound("audio/-rem.mp3")
                    if format(touch.fid) not in self.markerData:
                        playsound("audio/-unk.mp3")
                    else:
                        playsound(marker.audio)
                    self.markersOnTable.remove(marker)
                    self.generateGraph(1)


    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fiducialID == touch.fid:   
                    marker.currentPos = touch.pos
                    self.generateGraph(1)

    def generateGraph(self, flag):
        if flag:
            print("[CITE   ] Generating graph...")
        else:
            print("[CITE   ] Please place token(s) on the table!")