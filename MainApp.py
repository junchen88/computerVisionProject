import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
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

        # Bind this instance to the UI's detect button
        self.ui.setDetectFunc(lambda: self.startDetect())

    def showWindow(self):
        self.window.show()

    def run(self):
        return self.runtime.exec_()
    
    #STARTS THE PROCESSING WHEN START BUTTON IS PRESSED
    def startDetect(self):
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

        #MAIN EXECUTION
        #init
        imageParser = Image(imgName, objType, frameRange)
        imageParser.getImagesPath()
        imageParser.getFrameRange()
        gtInform = imageParser.parser.getGTInformation()
        frameRange = imageParser.inputFrameRange
        #IMG PARSER NOW CONTAINS THE PATH TO FRAME, CAN
        #USE LOADFRAME() TO GET THE SPECIFIC FRAME

        print("info: Working on frames from frame {} to frame {}...".format(frameRange[0], frameRange[1]))


        #INITIALISE TRACKER FOR TRACKING
        tracker = Tracker(STARTINGID, positionSTD, velocitySTD, accelerationSTD, movingObjSTD)

        #TO STORE ALL THE VALUES FOR PRINTING CHART, EACH ELEMENT = FOR EACH FRAME
        listOfPrecision = []
        listOfRecall = []
        listOfF1 = []
        listOfTruePositive = []
        listOfFalsePositive = []
        listOfFalseNegative = []

        #GO THROUGH EACH FRAME ACCORDING TO THE FRAME RANGE
        for i in range(frameRange[0]+1, frameRange[1]):
            print("info: Working on frame {} to frame {}...".format(i-1, i+1))

            detector = Detector(imageParser.loadFrame(i-1), imageParser.loadFrame(i), imageParser.loadFrame(i+1), cueLowerBound, cueUpperBound, gtInform, i)

            #BOXES = BOUNDING BOXES, CENTROIDS = LIST OF CENTROIDS,(FOR KALMAN) PRECISION RECALL AND F1 IS DATA FOR CHART
            boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative = detector.detectObjAndDiscrim()

            listOfPrecision.append(precision)
            listOfRecall.append(recall)
            listOfF1.append(F1)
            listOfTruePositive.append(truePositive)
            listOfFalsePositive.append(falsePositive)
            listOfFalseNegative.append(falseNegative)

            centroids = np.asarray(centroids)

            #UPDATE/ADD/DELETE TRACKS
            tracker.update(centroids)


            print('info: Step finished, printing result...')

            imData = imageParser.loadFrame(i)
            height, width, _ = imData.shape
            bytesPerLine = 3 * width
            qImg = QImage(imData.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap(qImg)

            w = self.ui.displayFrame.width()
            h = self.ui.displayFrame.height()
            self.ui.displayFrame.setPixmap(pix.scaled(w,h,Qt.KeepAspectRatio))

        print('info: Finished!')


# Run the main application when invoked on the command line
if __name__ == '__main__':
    import sys

    app = MainApp(sys.argv)
    app.showWindow()
    result = app.run()

    sys.exit(result)
