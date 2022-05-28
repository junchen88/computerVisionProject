# junchen88/computerVisionProject

## Requirements

- Python 3 (version 3.10.4 tested)
- Pip (up-to-date version required)
- NumPy
- SciPy
- scikit-image
- PyQt5
- PythonQwt
- pandas
- OpenCV-Python (headless, due to PyQt5 conflict)

## Setup

Configure a python environment and install required packages. This works
best in a virtual environment. An up-to-date version of `pip` is required to
install the other packages.

- Create and enter the virtual environment:

```
$ python3 -m venv env
$ . env/bin/activate
```

- Update `pip`, then install required packages:

```
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

The `mot` folder of the VISO data must be present in the project directory.
The project can then be run by executing `MainApp.py` with `python3`.

```
$ python3 MainApp.py
```

## Running

1. Configure and install dependencies as above.
2. Download/copy the `mot` folder (containing the images) into the project folder.
3. Run `python3 MainApp.py` in the project root directory.
4. Assign values to the hyperparameters using the sliders or by entering a value into the input boxes. Choose the best ones by trying different values.
5. Enter the image name - the folder number (eg. 001, 002, 003, ...).
6. Enter the object type - the object that is going to be tracked (e.g. car, plane, etc.).
7. Enter frame range to be processed – leave both boxes blank to use the full range for that image set.
8. Click "Start" to initialize tracking.
9. Repeatedly click "Next" to compute and display object data for the next frame, until all frames have been processed.
10. Errors in the provided parameters will cause the tracking process to abort, with a diagnostic message displayed in the terminal.
11. The progress is also reported in the terminal as the tracking process runs.
12. After each frame is processed, it is displayed in the main frame pane, in the top-left of the window.
