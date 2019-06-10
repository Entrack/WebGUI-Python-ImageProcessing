# WebGUI-Python-ImageProcessing
This repo contains a python-backend + js-frontend image processing app.  

Current app is desinged to be a demonstration of how can you use a web gui to run on desktop and be able to utilize powerfull Python backend processing. Operations are performed either with `numpy` or `opencv`.

## Features
#### The main window
You can select the backend-frontend compression rate to perform processing on a smaller image
<img src="docs/images/main.png" alt="main window" height="400"/>
#### HSV, RGB, LAB components
HSV components
<img src="docs/images/HSV_matrix.png" alt="HSV_matrix" height="400"/>
RGB components
<img src="docs/images/RGB_matrix.png" alt="RGB_matrix" height="400"/>
LAB components
<img src="docs/images/LAB_matrix.png" alt="LAB_matrix" height="400"/>
#### Operations within selection
Initial L component hist
<img src="docs/images/L_hist.png" alt="L_hist" height="300"/>
Selecting part of the image
<img src="docs/images/selection.png" alt="selection" height="300"/>
Selection L component hist
<img src="docs/images/selection_L_hist.png" alt="selection_L_hist" height="300"/>
#### HSV online change
The processing supports smoooth component change while you drag the slider
<img src="docs/images/hue_change.png" alt="hue_change" height="300"/>
<img src="docs/images/saturation_change.png" alt="saturation_change" height="300"/>
<img src="docs/images/value_change.png" alt="value_change" height="300"/>
#### Filter operations
Gauss filter application example
<img src="docs/images/gauss.png" alt="gauss" height="300"/>

## Architecture
The code uses `zerorpc` inter-process communcation python package that allows this setup to run python-powered backend (that can be used e.g. machine learning or image processing) and flexible electron-powered UI.  
This architecture is an adaptation of [this](https://www.fyears.org/2017/02/electron-as-gui-of-python-apps-updated.html) post, but unlike the initial app, my python server has it's own inner state and loop, therefore it can call the fontend by itself, successfully processing long queues (such as heavy image processing). The class architechteure was also changed.
Simplified version of the architecture is provided below. It comprises of the python App class that incorporates both server that processes the AppAPI calls and the client that sends the App.run() loop commands to the frontend.
```text
start()
 |
 V
+--------------------+
|                    | start()
|                    +-------------> +----------------------+
|                    |               |                      |
|      electron      |               |        python        |
| (all html/css/js)  |               |   (all processing)   |
|                    |               |                      |
|                    |               |                      |
|              input | ------------> | [AppAPI]             |
|                    |               |    ^                 |
|                    |               |    |                 |
|                    |               |    v                 |
|      server_api.js | <------------ |  [App] <— App.run()  |
|                    |               |                      |
+--------------------+               +----------------------+
```

## Preparation
Tested with:
* Ubuntu 16.04
* Node 7.9.0
* npm
* Python 3.5

First, you install python packages:
```text
pip install zerorpc
pip install pyinstaller
```

Then you clean the electron and node cache:
```text
rm -rf ~/.node-gyp
rm -rf ~/.electron-gyp
rm -rf ./node_modules
```

Then install electron to the project using npm:
```text
npm install --runtime=electron --target=1.7.6
```

## Running
To run the app simply execute:
```text
./node_modules/.bin/electron .
```

When you need to reinstall electron (do it if everything is supposed to work, but it does not), run:
```text
./0_reinstall_electron.sh
```