import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog

from ControlGui import Ui_ControlGui
from assistClass import Image
from trackClass import Tracker
from detectClass import Detector

STARTINGID = 0

class MainApp:
    def __init__(self, args):
        self.runtime = QApplication(args)
        self.window = QDialog()
        self.ui = Ui_ControlGui(self.window)

        # Bind this instance to the UI's buttons
        self.ui.setResetFunc(lambda: self.detectReset())
        self.ui.setNextFunc(lambda: self.detectStep())

    def showWindow(self):
        self.window.show()

    def run(self):
        return self.runtime.exec_()
    
    # Set up the object detection process
    def detectReset(self):
        # Get all parameters from the GUI, stop if any fail
        try:
            imgName, objType = self.ui.getImageDetails()
            self.imgName = imgName
            self.objType = objType

            frameRange = self.ui.getFrameRange()
            if frameRange is None:
                print("note: No frame range supplied, searching all available frames...")
            self.frameRange = frameRange

            cueLowerBound, cueUpperBound = self.ui.getCueBounds()
            self.cueLowerBound = cueLowerBound
            self.cueUpperBound = cueUpperBound

            positionSTD, velocitySTD, accelerationSTD, movingObjSTD = self.ui.getTrackerParams()
            self.positionSTD = positionSTD
            self.velocitySTD = velocitySTD
            self.accelerationSTD = accelerationSTD
            self.movingObjSTD = movingObjSTD
        
        except ValueError as e:
            print("error:", str(e))
            return

        #MAIN EXECUTION
        #init
        self.imageParser = Image(self.imgName, self.objType, self.frameRange)
        self.imageParser.getImagesPath()
        self.imageParser.getFrameRange()
        self.gtInform = self.imageParser.parser.getGTInformation()
        self.frameRange = self.imageParser.inputFrameRange
        #IMG PARSER NOW CONTAINS THE PATH TO FRAME, CAN
        #USE LOADFRAME() TO GET THE SPECIFIC FRAME

        print("info: Working on frames from frame {} to frame {}...".format(self.frameRange[0], self.frameRange[1]))

        #INITIALISE TRACKER FOR TRACKING
        self.tracker = Tracker(STARTINGID, self.positionSTD, self.velocitySTD, self.accelerationSTD, self.movingObjSTD)

        #TO STORE ALL THE VALUES FOR PRINTING CHART, EACH ELEMENT = FOR EACH FRAME
        self.listOfPrecision = []
        self.listOfRecall = []
        self.listOfF1 = []
        self.listOfTruePositive = []
        self.listOfFalsePositive = []
        self.listOfFalseNegative = []

        self.i = frameRange[0]+1

    # Do one frame of object detection
    def detectStep(self):
        # If we're at the last frame, there's nothing more to do
        if self.i == self.frameRange[1]:
            print("info: Finished!")
            return

        print("info: Working on frame {} to frame {}...".format(self.i-1, self.i+1))

        prevFrame = self.imageParser.loadFrame(self.i-1)
        currFrame = self.imageParser.loadFrame(self.i)
        nextFrame = self.imageParser.loadFrame(self.i+1)
        detector = Detector(prevFrame, currFrame, nextFrame, self.cueLowerBound, self.cueUpperBound, self.gtInform, self.i)

        #BOXES = BOUNDING BOXES, CENTROIDS = LIST OF CENTROIDS,(FOR KALMAN) PRECISION RECALL AND F1 IS DATA FOR CHART
        boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative = detector.detectObjAndDiscrim()
        # test
        print(centroids)

        self.listOfPrecision.append(precision)
        self.listOfRecall.append(recall)
        self.listOfF1.append(F1)
        self.listOfTruePositive.append(truePositive)
        self.listOfFalsePositive.append(falsePositive)
        self.listOfFalseNegative.append(falseNegative)

        centroids = np.asarray(centroids)

        #UPDATE/ADD/DELETE TRACKS
        self.tracker.update(centroids)

        print('info: Step finished, printing result...')

        self.ui.showFrame(thisFrame)

        self.i = self.i + 1


# Run the main application when invoked on the command line
if __name__ == '__main__':
    import sys

    app = MainApp(sys.argv)
    app.showWindow()
    result = app.run()

    sys.exit(result)
