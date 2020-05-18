from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
import handler as ch

class CITEApp(App):
    def build(self):
        #   Create connection to TUIO server for reacTIVision.
        #   https://kivy.org/doc/stable/api-kivy.input.providers.tuio.html
        
        Config.set("input", "reactivision", "tuio,0.0.0.0:3333")

        #   Create the application bounding box:
        #   https://kivy.org/doc/stable/api-kivy.uix.floatlayout.html?highlight=floatlayout

        CITEHandler = ch.CITEHandler()
        self = CITEHandler.load()
        Window = FloatLayout()
        Window.add_widget(self)
        return Window

if __name__ == "__main__":
    CITEApp().run()