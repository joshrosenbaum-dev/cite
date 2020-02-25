# CITE
The base purpose of this software is to allow a user to use fidicual markers on a tabletop interface to visualize data. Based on DataBlocks Visualizations (https://www.datablocks.org), the markers will be placed on token objects that can be manipulated in position to visualize the Gapminder data set (https://www.gapminder.org). We will be using ReacTIVision to retrieve the marker data from the table, oscpy to retrieve our TUIO packets (from ReacTIVision), and Kivy's natural user interface environment to develop a single-window program.  

Future implentation will require a graphic library such as Matplotlib (https://matplotlib.org/) to display our information as a bubble graph, similar to what Gapminder does.  

---

## Prerequisites/Installation
These instructions will allow you to set up the script on your local machine.
* [ReacTIVision](http://reactivision.sourceforge.net/) and a working webcam/tabletop interface (with a camera included)
* [Anaconda / Python 3.7](https://www.anaconda.com/distribution/)
* [Kivy](https://www.kivy.org) (can be installed via `conda` the Anaconda environment)
* [oscpy](https://pypi.org/project/oscpy/) (can be installed via `pip` in the Anaconda environment)

### Notes for Visual Studio Code
If you are running Visual Studio Code, you **must** have your environment setup first. You will then use your environment as your Python interpreter.

To start, create a new Anaconda environment with the Python version being 3.7 (**Kivy does NOT work with Python 3.8+, so you must specify the version**):
```
conda create -n cite python=3.7 pip
```
After initializing the environment, you may need to update `conda`:
```
conda update conda
```
Next, we should activate our environment (so everything we install stays within that environment):
```
conda activate cite
```
Next, install Kivy. Since we have an Anaconda environment, the installation comes naturally:
```
conda install kivy -c conda-forge
```
From here, `pip` will save us! Install oscpy, pandas, and matplotlib using pip. Since we've activated our environment, this will not install anything globally:
```
pip install oscpy pandas matplotlib
```
### Notes for Visual Studio Code
Visual Studio Code requires you to select an interpreter for Python. Use `Python 3.7.x x-bit('cite': conda)`. Then you may install PyLint either using conda or pip in your environment.

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
### Notes for Kivy Garden
First, install Kivy Garden using
```
sudo pip install kivy-garden
```
Since we've already installed Matplotlib, we can add the backend for `garden.matplotlib` using
```
garden install matplotlib --kivy
```
---
## Design Implentation
We will be modeling our software after the Gapminder data set and how it displays data as bubbles. Using 5-8 countries with individual tabletop markers, we can select countries to display on our graph. Our X and Y indicators also come from tabletop markers that lock into each other to convey an X and Y assignment.  

In our preliminary demonstration, we wish to select 10 countries; at least 2 from every continent. In the future, we would like to use regions instead because of the vast amount of country objects we would require.  

Currently, we have 4-5 prelimary indicators for X and Y axis that we can use to demonstrate graphing capability in the future.  

We will also utilize a tabletop object that will act as a dial, changing the view of our graph based on year.

---

## Current Issues
Below is a list of current issues that need to be addressed in later updates:  
* On-screen instructions should be developed using .kv file architecture.