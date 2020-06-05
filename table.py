#   table.py
#   -------------------------------------------------------
#   Handles all events relating to the tabletop surface.

from kivy.clock import mainthread
from kivy.uix.widget import Widget
from math import degrees
from playsound import playsound
import arduino as a
import marker as m
import graphing as g
import queue
import threading

class TableHandler(Widget):
    def generateTable(self, package):
        self.graph = package.graph
        self.indicatorData = package.indicatorData
        self.markerData = package.markerData
        self.markersOnTable = package.markersOnTable
        self.popSize = package.df_popSizeByArtifact
        self.narrationPlaylist = []
        self.generateGraph(self.graph)

    def startNarrationDaemon(self):
        #   https://pymotw.com/2/threading/index.html
        narrationProcess = threading.Thread(target = self.narrationDaemon, args = (self.narrationPlaylist, ))
        narrationProcess.daemon = True
        narrationProcess.start()

    def narrationDaemon(self, narrationPlaylist):
        for index in range(0, len(narrationPlaylist)):
            playsound(narrationPlaylist[index])

    def startGraphingDaemon(self):
        graphingProcess = threading.Thread(target = self.generateGraph, args = (self.graph, ))
        graphingProcess.daemon = True
        graphingProcess.start()

    #   There are three functions to process touch events.
    #   The on_touch_down function is when a marker is placed.
    #   The on_touch_up function is when a marker is removed.
    #   The on_touch_move function is when a marker is moved.
    #   https://kivy.org/doc/stable/api-kivy.input.motionevent.html

    def on_touch_down(self, touch):
        if "markerid" in touch.profile:
            marker = m.Marker(touch, self.markerData)
            self.narrationPlaylist.clear()
            self.narrationPlaylist.append("audio/-add.mp3")
            if format(touch.fid) not in self.markerData:
                self.narrationPlaylist.append("audio/-unk.mp3")
            else:
                self.narrationPlaylist.append(marker.audio)
            self.startNarrationDaemon()
            self.markersOnTable.append(marker)
            #   a.lightUp(1)
            self.startGraphingDaemon()
    
    def on_touch_up(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fiducialID == touch.fid:
                    self.narrationPlaylist.clear()
                    self.narrationPlaylist.append("audio/-rem.mp3")
                    if format(touch.fid) not in self.markerData:
                        self.narrationPlaylist.append("audio/-unk.mp3")
                    else:
                        self.narrationPlaylist.append(marker.audio)
                    self.startNarrationDaemon()
                    self.markersOnTable.remove(marker)
                    #   a.lightUp(0)
                    self.startGraphingDaemon()

    def on_touch_move(self, touch):
        if "markerid" in touch.profile:
            for marker in self.markersOnTable:
                if marker.fiducialID == touch.fid:   
                    marker.currentPos = touch.pos
                    marker.currentAngle = degrees(touch.a)
                    self.startGraphingDaemon()

    def getProximalMarker(self, markerSize, padding, bucketIndex, listMOT):
        #   Given that the position is in the center of a
        #   marker, the current maximum difference is equal
        #   to the marker's size (square) and it's padding.

        #   Then, we take the differences in X and Y (dbX/dbY)
        #   in absolute value (we only care about the degree of
        #   difference) and create a difference "score" for
        #   each indicator on the table out of the sum of the
        #   two values.

        #   If the difference score is less than the current
        #   maximum difference, we bring down the current
        #   difference to match the smaller value, and set the
        #   indicator marker as closest. We repeat for all
        #   of the existing indicator markers.
        
        currentDiff = markerSize + padding
        currentMarker = None
        for index in range(len(listMOT)):
            marker = self.markersOnTable[listMOT[index]]
            bucket = self.markersOnTable[bucketIndex]
            dbX = abs(bucket.currentPos[0] - marker.currentPos[0])
            dbY = abs(bucket.currentPos[1] - marker.currentPos[1])
            diffBetween = dbX + dbY
            if diffBetween <= currentDiff:
                currentDiff = diffBetween
                currentMarker = marker
        return currentMarker

    @mainthread
    def generateGraph(self, graph):     
        #   The lists indicatorsMOT and artifactsMOT consist
        #   of the indices of indicator markers and artifact
        #   markers on the markersOnTable list, along with the
        #   X and Y bucket/marker values.
        
        indicatorsMOT = []
        artifactsMOT = []
        xIndex = -1
        yIndex = -1

        #   The points list holds all point objects that will
        #   be rendered by the graph.

        points = []

        #   The following variables relate to X and Y marker
        #   positions to figure out the proximity of each
        #   marker. 

        #   The default reacTIVision camera size is 640x480
        #   and the testing marker set that is printed has
        #   markers that are approx. 110px in width and height.

        #   Given that the markers will have a consistent size
        #   in their 3D design... TODO: Get camera resolution
        #   from either reacTIVision or Kivy, and scale the size
        #   of the markers based on the camera size.

        markerSize = 110
        padding = markerSize / 10
        x = None
        y = None

        if len(self.markersOnTable) > 0:
            for index, marker in enumerate(self.markersOnTable):
                if marker.markerType == m.MarkerType.INDICATOR:
                    indicatorsMOT.append(index)
                if marker.markerType == m.MarkerType.ARTIFACT:
                    artifactsMOT.append(index)
                if marker.markerType == m.MarkerType.X:
                    xIndex = index
                if marker.markerType == m.MarkerType.Y:
                    yIndex = index

            #   We will only attempt to graph content if there
            #   are 2 or more indicators on the table.
        
            if len(indicatorsMOT) >= 2:
                if xIndex != -1 and yIndex != -1:
                    x = self.getProximalMarker(markerSize, padding, xIndex, indicatorsMOT)
                    y = self.getProximalMarker(markerSize, padding, yIndex, indicatorsMOT)

                if x != None and y != None:
                    xFrame = self.indicatorData[x.indicatorID]
                    yFrame = self.indicatorData[y.indicatorID]
                    year = "2002"

                    if len(artifactsMOT) >= 1:
                        for index in artifactsMOT:
                            artifact = self.markersOnTable[index]
                            points.append(g.getPoint(xFrame, yFrame, self.popSize, artifact, year))
                            g.plotPoints(points, x.markerLabel, y.markerLabel, None, None, year)
                            graph.draw()
                    else:
                        #   Here, we use pandas min/max functions
                        #   to determine our graph's min/max without
                        #   artifacts.
                        #
                        #   https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.min.html
                        
                        xRange = [xFrame[year].min(), xFrame[year].max()]
                        yRange = [yFrame[year].min(), yFrame[year].max()]
                        g.plotPoints([], x.markerLabel, y.markerLabel, xRange, yRange, year)
                        graph.draw()
                else:
                    #   Not enough indicators in range.
                    g.plotPoints([], None, None, None, None, None)
                    graph.draw()
            else:
                #   Not enough indicators on table.
                g.plotPoints([], None, None, None, None, None)
                graph.draw()
        else:
            #   Not enough markers on the table.
<<<<<<< HEAD
            g.plotPoints([], None, None, None, None, None)
            graph.draw()
=======
            g.plotPoints([], None, None, None, None)
            self.graph.draw()
>>>>>>> 711b30b869a99016e7f5891cc18c56b39bd5b18a
