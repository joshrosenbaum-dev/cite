#   marker.py
#   -------------------------------------------------------
#   Class definitions for objects created from reacTIVision
#   fidicual markers.
#
#   Fidicual markers in reacTIVision have a position that
#   can be sent to the Kivy application and recognized
#   as touch objects.
#
#   Relies on TUIO server connection via the oscpy library.
#
#   https://kivy.org/doc/stable/api-kivy.input.providers.tuio.html
#   https://kivy.org/doc/stable/guide/inputs.html
#   https://kivy.org/doc/stable/api-kivy.input.motionevent.html

class Marker:
    def __init__(self, touch, jsonData):
        #   Class variables based on touch profile:
        self.currentPos = touch.pos
        self.fidicualID = touch.fid

        #   Custom class variables:
        self.artifactID = None
        self.artifactAbbr = None
        self.indicatorID = None
        self.markerLabel = None
        self.markerType = None