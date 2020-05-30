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

from enum import Enum
from math import degrees

class MarkerType(Enum):
    X = "X Bucket"
    Y = "Y Bucket"
    TIME = "Time Dial"
    ARTIFACT = "Artifact"
    INDICATOR = "Indicator"
    
class Marker:
    def __init__(self, touch, markerData):
        #   Class variables based on touch profile:
        self.currentPos = touch.pos
        self.currentAngle = degrees(touch.a)
        self.fiducialID = touch.fid

        #   Custom class variables:
        self.artifactID = None
        self.artifactAbbr = None
        self.artifactColor = None
        self.audio = None
        self.indicatorID = None
        self.markerLabel = None
        self.markerType = None

        if format(self.fiducialID) in markerData:
            mD = markerData[format(self.fiducialID)]
            self.audio = mD["audio"]
            self.markerLabel = mD["label"]
            self.markerType = mD["type"]
            if self.markerType == MarkerType.ARTIFACT:
                self.artifactID = mD["artifact_id"]
                self.artifactAbbr = mD["artifact_abbr"]
                self.artifactColor = mD["artifact_color"]
            if self.markerType == MarkerType.INDICATOR:
                self.indicatorID = mD["indicator_id"]

    def __str__(self):
        return "[{}, {}, {}]\t\t{}\t{}\t{}\t\t{}".format(
            self.fiducialID, self.indicatorID, self.artifactID, self.currentPos, self.markerType.value, self.audio, self.markerLabel
        )