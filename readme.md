This prototype is a first experiment with Plotly Dash, and it is currently under development at very early stages with not much to see for now. It is however possible to try it out even if some things may not work properly yet.

### How to add the example dataset for the workflow
After cloning the repo, add a "datasets" folder at the root of the repo. </br>
The example dataset used at the moment can be downloaded here: https://zenodo.org/record/4596345#.Yk2flG5Bz0o.</br>
You can unzip the 'ChroniclItaly_3.0_original.zip', and add the 'CI_newspaper_subcorpora' folder into the 'datasets' folder previously created.

### How to run the prototype
After the example dataset has been added, create a virtual environment from the terminal to install the requirements.txt file, and launch the prototype from the terminal with the following command</br>
```
python app.py
```
The process for installing the virtual env can vary depending on your OS. It could be, for example:</br>
- Create venv after navigating to the repo from terminal (only the first time, then just activate it)
```
python3 -m venv .venv
```
- Activate venv
```
source .venv/bin/activate
```
- Install requirements.txt
```
pip install -r requirements.txt
```
- Launch prototype
```
python app.py
```