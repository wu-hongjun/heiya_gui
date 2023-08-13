# Heiya GUI

This repository contains the source code for Heiya GUI.
The executable file is too big for Github but can be found in the Release tab.

## Build Heiya GUI
You can build Heiya GUI from your computer as well.
* Make sure you installed all the dependencies, including `heiya` and `pyinstaller`.
* Using Terminal, navigate to the directory containing `heiys_gui.py` by using the `cd` command.
* Execute the following code: `pyinstaller --onefile --windowed --icon=app.ico heiya_gui.py`
* You will see two folders (`dist` and `build`) created in the same folder as the `heiya_gui.py` script. 
* Navigate to the `dist` folder, and there should be a standalone executable file (`heiya_gui` for Linux, `heiya_gui.app` for macOS, and `heiya_gui.exe` for Windows). The file generated usually depends on which OS you are running on.
