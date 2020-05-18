# CITE: Collaborative Tabletop for Education
The base purpose of this software is to allow a user to use fidicual markers on a tabletop interface to visualize data. Based on DataBlocks Visualizations (https://www.datablocks.org), the markers will be placed as token objects that can be manipulated in position to visualize the Gapminder data set (https://www.gapminder.org). We will be using ReacTIVision to retrieve the marker's position from the table, oscpy to retrieve our TUIO packets (from ReacTIVision), and Kivy's natural user interface environment to develop a single-window program in an object-oriented fashion.

Future implentation requires a graphic library such as Matplotlib (https://matplotlib.org/) to display our information as a bubble graph, similar to what Gapminder does. By using CITE, students and researchers can use plot points to ask questions about the data set that provide new global perspectives.

---

## Prerequisites/Installation
These instructions will allow you to set up the script on your local machine.
* [ReacTIVision](http://reactivision.sourceforge.net/) and a working webcam/tabletop interface (with a camera included)
* [Anaconda / Python 3.7](https://www.anaconda.com/distribution/) or [Miniconda / Python 3.7](https://docs.conda.io/en/latest/miniconda.html) - or virtualenv/venv with a Python 3.7 installation
* [Kivy](https://www.kivy.org) (can be installed via `conda` or `pip` - we used `conda`)
* [oscpy](https://pypi.org/project/oscpy/) (can be installed via `pip`)
* [pandas]
* [matplotlib]
* [playsound]
* [Google Text-to-Speech (gTTS)]

### Notes for Visual Studio Code
If you are running Visual Studio Code, you **must** have your environment setup first. You will then use your environment as your Python interpreter. Then you may install PyLint either using conda or pip in your environment.

### Installation
You may need to update `conda` before starting:
```
conda update conda
```
To start, create a new environment with the Python version being 3.7 (**Kivy does NOT work with Python 3.8+, so you must specify the version**):
```
conda create -n cite python=3.7 pip
```
Next, we should activate our environment (so everything we install stays within that environment):
```
conda activate cite
```
Next, install Kivy. Since we have a Conda environment, the installation comes naturally:
```
conda install kivy -c conda-forge
```
From here, `pip` will save us! Install oscpy, pandas, and matplotlib using pip. Since we've activated our environment, this will not install anything globally:
```
pip install oscpy pandas matplotlib
```
#### Notes for Kivy Garden
First, install Kivy Garden using
```
pip install kivy-garden
```
Since we've already installed matplotlib, we can add the backend for `garden.matplotlib` using
```
garden install matplotlib --kivy
```

## Preparing/Running CITE
Clone the CITE repository to any folder. In the CITE folder (which should include `react.py`), run the following commands:  

Activate the Anaconda environment (if it isn't activated already)
```
conda activate cite
```
Run the Python file named `react.py`
```
python react.py
```
---
## Design Implentation
We will be modeling our software after the Gapminder data set and how it displays data as bubbles. Using 5-8 countries with individual tabletop markers, we can select countries to display on our graph. Our X and Y indicators also come from tabletop markers that lock into each other to convey an X and Y assignment.  

In our preliminary demonstration, we wish to select 6 artifacts (countries); at least 1 from every continent with data. In the future, we would like to use regions instead because of the vast amount of country objects we would require if we covered a global scale

Currently, we have 6 prelimary indicators for X and Y axis that we can use to demonstrate graphing capability in the future.  

We will also plan to utilize one or many tabletop objects that will act as a time manipulator, changing the view of our graph based on year.

---

## To-Do
Below is a list of unfinished tasks:  
* Load and play audio asynchonously.
* Fix bug where graph shows exponential values for a single artifact.
* Create on-screen instructions that replace initial graph texture on start.
* Create loading UI elements and preloader UI elements.
