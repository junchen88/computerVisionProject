from PyQt5.QtWidgets import QApplication, QDialog

from ControlGui import Ui_ControlGui
from DataLoader import FrameSetLoader
from FrameProcessor import FrameProcessor
from ObjectDetector import ObjectDetector
from ObjectTracker import TrackerState

STARTINGID = 0

class MainApp:
    def __init__(self, args):
        # Qt application runtime
        self.runtime = QApplication(args)

        # Qt UI objects
        self.window = QDialog()
        self.ui = Ui_ControlGui(self.window)

        # Bind this instance to the UI's buttons
        self.ui.setResetFunc(lambda: self.resetDetector())
        self.ui.setNextFunc(lambda: self.stepDetector())

    def showWindow(self):
        self.window.show()

    def run(self):
        return self.runtime.exec_()
    
    # Set up the object detection process
    def resetDetector(self):
        # Get all parameters from the GUI, stop if any fail
        try:
            imgName, objType = self.ui.getImageDetails()

            frameRange = self.ui.getFrameRange()
            if frameRange is None:
                print("note: No frame range supplied, searching all available frames...")

            cueLowerBound, cueUpperBound = self.ui.getCueBounds()

            positionSTD, velocitySTD, accelerationSTD, movingObjSTD = self.ui.getTrackerParams()
        
        except ValueError as e:
            print("error:", str(e))
            return

        # Prepare to load frames
        frames = FrameSetLoader(imgName, objType, frameRange)
        gtInform = frames.parser.getGTInformation()

        # Initialize detector parameters
        detector = ObjectDetector(0, 121, 0, 1, 0, 11, 0, 1)

        # Initialize tracking state from user-supplied values
        tracker = TrackerState(STARTINGID, positionSTD, velocitySTD, accelerationSTD, movingObjSTD)

        # Create a new frame processor primed with the current frame set
        self.processor = FrameProcessor(frames, detector, tracker)

    # Do one frame of object detection
    def stepDetector(self):
        # Do the actual small object track processing
        currFrame = self.processor.processNextFrame()

        if currFrame is not None:
            # Then display the result on the screen
            print('info: Step finished, showing results...')
            self.ui.showFrame(currFrame)


# Run the main application when invoked on the command line
if __name__ == '__main__':
    import sys

    app = MainApp(sys.argv)
    app.showWindow()
    result = app.run()

    sys.exit(result)
