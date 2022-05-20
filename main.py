# from detectClass import Detector
# from trackClass import Tracker
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from projectGui import Ui_Dialog
from assistClass import Image
from trackClass import Tracker
from detectClass import Detector
import numpy as np

STARTINGID = 0


class myApp(Ui_Dialog):

    def __init__(self, window):
        self.setupUi(window)

        #EXECUTE FUNCTION WHEN CLICKED
        self.startButton.clicked.connect(self.startDetect)

        #EXECUTE FUNCTION WHEN SLIDER VALUE CHANGES
        self.lowerBoundCueSlider.valueChanged.connect(lambda: self.writeSliderValue('lowerBound'))
        self.upperBoundCueSlider.valueChanged.connect(lambda: self.writeSliderValue('upperBound'))
        self.positionSTDSlider.valueChanged.connect(lambda: self.writeSliderValue('position'))
        self.velocitySTDSlider.valueChanged.connect(lambda: self.writeSliderValue('velocity'))
        self.accelerationSTDSlider.valueChanged.connect(lambda: self.writeSliderValue('acceleration'))
        self.movingObjSTDSlider.valueChanged.connect(lambda: self.writeSliderValue('movingObj'))
        self.lowerBoundCueVal.setPlainText('0')
        self.upperBoundCueVal.setPlainText('0')
        self.positionSTDVal.setPlainText('0')
        self.velocitySTDVal.setPlainText('0')
        self.accelerationSTDVal.setPlainText('0')
        self.movingObjSTDVal.setPlainText('0')

    #FOR WRITING SLIDER VALUE INTO
    def writeSliderValue(self, name):

        if name == 'lowerBound':

            value = self.lowerBoundCueSlider.value()
            self.lowerBoundCueVal.setPlainText(str(value))

        elif name == 'upperBound':
            value = self.upperBoundCueSlider.value()
            self.upperBoundCueVal.setPlainText(str(value))

        elif name == 'position':
            value = self.positionSTDSlider.value()
            self.positionSTDVal.setPlainText(str(value))

        elif name == 'velocity':
            value = self.velocitySTDSlider.value()
            self.velocitySTDVal.setPlainText(str(value))

        elif name == 'movingObj':
            value = self.movingObjSTDSlider.value()
            self.movingObjSTDVal.setPlainText(str(value))

        else:
            value = self.accelerationSTDSlider.value()
            self.accelerationSTDVal.setPlainText(str(value))



    #STARTS THE PROCESSING WHEN START BUTTIN IS PRESSED
    def startDetect(self):
        lower = self.frameLower.toPlainText()
        status = True

        lowerRange = 0
        upperRange = 0

        #IF STR IS NOT EMPTY
        if lower:
            if not lower.isnumeric():
                status = False
                print("ERROR: NOT A NUMBER")

            else:
                lowerRange = int(lower)

        higher = self.frameHigher.toPlainText()

        if higher:
            if not higher.isnumeric():
                status = False
                print("ERROR: NOT A NUMBER")

            else:
                upperRange = int(higher)

        #CHECK FOR IS LOWER RANGE < UPPERRANGE
        if status == True:
            if lower >= higher:
                print('ERROR: upper range < lower range')
                status = False


        if status == True:
            imgName = self.imageName.toPlainText()
            objType = self.objectType.toPlainText()
            frameRange = [lowerRange, upperRange]
            if len(lower) == 0 and len(higher) == 0:
                frameRange = []


            #init
            imageParser = Image(imgName, objType, frameRange)
            imageParser.getImagesPath()
            imageParser.getFrameRange()
            gtInform = imageParser.parser.getGTInformation()
            frameRange = imageParser.frameRange

            cueLowerBound = float(self.lowerBoundCueVal.toPlainText())
            cueUpperBound = float(self.upperBoundCueVal.toPlainText())

            #IMG PARSER NOW CONTAINS THE PATH TO FRAME, CAN
            #USE LOADFRAME() TO GET THE SPECIFIC FRAME

            #GETS THE VALUE OF STDs USED IN TRACKER
            positionSTD = self.positionSTDVal.toPlainText()
            velocitySTD = self.velocitySTDVal.toPlainText()
            accelerationSTD = self.accelerationSTDVal.toPlainText()
            movingObjSTD = self.movingObjSTDVal.toPlainText()

            if not positionSTD.isnumeric():
                print("ERROR: STD NOT A NUMBER")
                quit()

            if not velocitySTD.isnumeric():
                print("ERROR: STD NOT A NUMBER")
                quit()

            if not accelerationSTD.isnumeric():
                print("ERROR: STD NOT A NUMBER")
                quit()

            if not movingObjSTD.isnumeric():
                print("ERROR: STD NOT A NUMBER")
                quit()

            positionSTD = float(positionSTD)
            velocitySTD = float(velocitySTD)
            accelerationSTD = float(accelerationSTD)
            movingObjSTD = float(movingObjSTD)

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
                print("working on frame {} to frame {}...".format(i-1, i+1))

                detector = Detector(imageParser.loadFrame(i-1), imageParser.loadFrame(i), imageParser.loadFrame(i+1), cueLowerBound, cueUpperBound, gtInform, i)

                boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative = detector.detectObjAndDiscrim()


                listOfPrecision.append(precision)
                listOfRecall.append(recall)
                listOfF1.append(F1)
                listOfTruePositive.append(truePositive)
                listOfFalsePositive.append(falsePositive)
                listOfFalseNegative.append(falseNegative)

                centroids = np.asarray(centroids)
                # print(centroids)
                tracker.update(centroids)


            print('process finished, printing chart/result...')

            #FOR CHART

            #LOOP THROUGH EACH LIST TO GET DATA AND PRINT CHART

            print('finished!')








if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = myApp(Dialog)
    # ui = Ui_Dialog()
    # ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())



    # tracker = Tracker(STARTINGID)
    #
    #
    # for i in range(1, noOfFrames-1)
    #
    #
    #     detector = Detector(allFrames[i-1], allFrames[i], allFrames[i+1])
    #
    #     centroid = detector.detectObjAndDiscrim()
    #
    #     tracker.Update(centroid)

main()
