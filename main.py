#   main.py
#   -------------------------------------------------------
#   Main application file -- generates mathplotlib graph
#   texture that's applied to the main window, ties together
#   preloader and touch handlers.

from kivy.app import App
from kivy.config import Config
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
import preloader as pl
import matplotlib.pyplot as plt

class CITEApp(App):
    def build(self):
        #   Create connection to TUIO server for reacTIVision.
        #   https://kivy.org/doc/stable/api-kivy.input.providers.tuio.html
        
        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")

        #   Create the application bounding box:
        #   https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html?highlight=floatlayout

        Window = FloatLayout()
        graphCanvas = FigureCanvasKivyAgg(plt.gcf())
        CITEPreloader = pl.CITEPreloader()
        self = CITEPreloader.load(graphCanvas)
        Window.add_widget(graphCanvas)
        return Window

if __name__ == "__main__":
    CITEApp().run()