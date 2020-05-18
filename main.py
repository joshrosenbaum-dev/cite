from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import preloader as pl

class CITEApp(App):
    def build(self):
        #   Create connection to TUIO server for reacTIVision.

        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")

        #   Create matplotlib canvas and pass the graph to the
        #   preloader function.

        Canvas = FigureCanvasKivyAgg(plt.gcf())
        pl.Preloader().load(Canvas)

        #   Create the application bounding box:
        Window = FloatLayout()
        Window.add_widget(Canvas)
        return Window

if __name__ == "__main__":
    CITEApp().run()