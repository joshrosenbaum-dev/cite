# CITE: Collaborative Interactive Tabletop for Education
CITE, based on [DataBlocks Visualizations](https://www.datablocks.org), allows users to use the tangible user interface object (TUIO) framework to visualize data based on [Gapminder](https://www.gapminder.org). We will be using the [ReacTIVision software](http://reactivision.sourceforge.net) to serve as the TUIO client and [Kivy](https://www.kivy.org), a Python based natural user interface library.

CITE uses [Matplotlib](https://www.matplotlib.org) to display our information as a bubble graph, similar to Gapminder's data. By using CITE, students and researchers can use plotted points to analyze the data set and discover new global perspectives.

## Prerequisities/Installation for Source Code
You will need the following to set up a proper working environment:
* [Reactivision](http://reactivision.sourceforge.net) software
* Python 3.7 with Virtualenv, [Anaconda](https://www.anaconda.com/distribution), or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (we will be using Anaconda/Miniconda in this documentation)
* [Kivy](https://www.kivy.org)
* [oscpy](https://pypi.org/project/oscpy), [pandas](https://pandas.pydata.org), [matplotlib](https://matplotlib.org), [playsound](https://pypi.org/project/playsound), [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS)

### Configuring Source Environment (using Anaconda/Miniconda)
You may need to update `conda` before starting:
```
conda update conda
```
Create a new environment with the Python version flag set to `3.7` **(Kivy does not work with Python 3.8+)** and with `pip`:
```
conda create -n cite python=3.7 pip
```
Activate the environment:
```
conda activate cite
```
Install Kivy using `conda-forge`, or via `pip` (instructions [here](https://kivy.org/doc/stable/gettingstarted/installation.html)):
```
conda install kivy -c conda-forge
```
Install the remaining above dependencies using `pip`:
```
pip install oscpy pandas matplotlib playsound gTTS
```
### Installing Kivy Garden for Graph Functionality
Install `kivy-garden` using `pip`:
```
pip install kivy-garden
```
Use `garden` to install the backend for `garden.matplotlib`:
```
garden install matplotlib --kivy
```
## Running Source (using Anaconda/Miniconda)
Open Reactvision and configure to your liking.

Ensure that the development environment is activated:
```
conda activate cite
```
Simply run the Python file named `main.py`
```
python main.py
```