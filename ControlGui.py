from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

from ControlGuiBase import ControlGuiBase

# Helper function: Set the text of a label automatically from the value of a
# control when it's changed.
def tieLabelToControlValue(control, label):
    def valueChangedHandler():
        value = control.value()
        label.setPlainText(str(value))

    # Connect the handler, then fire it once to get up-to-date
    control.valueChanged.connect(valueChangedHandler)
    valueChangedHandler()

class ControlGui(ControlGuiBase):
    def __init__(self, baseDialog):
        self.setupUi(baseDialog)

        # Tie each slider to the adjacent text field for easy value entry
        tieLabelToControlValue(self.areaLowerBoundSlider, self.areaLowerBoundVal)
        tieLabelToControlValue(self.areaUpperBoundSlider, self.areaUpperBoundVal)
        tieLabelToControlValue(self.extentLowerBoundSlider, self.extentLowerBoundVal)
        tieLabelToControlValue(self.extentUpperBoundSlider, self.extentUpperBoundVal)
        tieLabelToControlValue(self.majorLowerBoundSlider, self.majorLowerBoundVal)
        tieLabelToControlValue(self.majorUpperBoundSlider, self.majorUpperBoundVal)
        tieLabelToControlValue(self.eccentricLowerBoundSlider, self.eccentricLowerBoundVal)
        tieLabelToControlValue(self.eccentricUpperBoundSlider, self.eccentricUpperBoundVal)

        tieLabelToControlValue(self.positionSTDSlider, self.positionSTDVal)
        tieLabelToControlValue(self.velocitySTDSlider, self.velocitySTDVal)
        tieLabelToControlValue(self.accelerationSTDSlider, self.accelerationSTDVal)
        tieLabelToControlValue(self.movingObjSTDSlider, self.movingObjSTDVal)

        # Set the range for each bound slider
        self.areaLowerBoundSlider.setRange(0, 121)
        self.areaUpperBoundSlider.setRange(0, 121)
        self.extentLowerBoundSlider.setRange(0, 1)
        self.extentUpperBoundSlider.setRange(0, 1)
        self.majorLowerBoundSlider.setRange(0, 11)
        self.majorUpperBoundSlider.setRange(0, 11)
        self.eccentricLowerBoundSlider.setRange(0, 1)
        self.eccentricUpperBoundSlider.setRange(0, 1)

    # Set a provided function to run when the reset button is pushed
    def setResetFunc(self, func):
        self.resetButton.clicked.connect(func)

    # Set a provided function to run when the next button is pushed
    def setNextFunc(self, func):
        self.nextButton.clicked.connect(func)

    # Get the user-provided image name and type
    def getImageDetails(self):
        imgName = self.imageName.toPlainText()
        objType = self.objectType.toPlainText()

        return imgName, objType

    # Get the user-provided frame range
    def getFrameRange(self):
        lowerRange = self.frameLower.toPlainText()
        upperRange = self.frameHigher.toPlainText()

        # Special case when both are blank, caller uses defaults
        if not lowerRange and not upperRange:
            return None

        # Otherwise, both need to be valid
        if not lowerRange.isnumeric() or not upperRange.isnumeric():
            raise ValueError("Ui_ControlGui: Can't parse frame range bounds")

        lowerRange = int(lowerRange)
        upperRange = int(upperRange)

        if lowerRange < 1 or upperRange < 1 or lowerRange > upperRange:
            raise ValueError("Ui_ControlGui: Invalid frame range provided")

        # Convert one-based indexing of the data sets to zero-based for
        # Python-internal use
        return lowerRange - 1, upperRange - 1

    # Get the user-provided cue bounds
    def getCueBounds(self):
        areaLowerBound = float(self.areaLowerBoundVal.toPlainText())
        areaUpperBound = float(self.areaUpperBoundVal.toPlainText())
        extentLowerBound = float(self.extentLowerBoundVal.toPlainText())
        extentUpperBound = float(self.extentUpperBoundVal.toPlainText())
        majorLowerBound = float(self.majorLowerBoundVal.toPlainText())
        majorUpperBound = float(self.majorUpperBoundVal.toPlainText())
        eccentricLowerBound = float(self.eccentricLowerBoundVal.toPlainText())
        eccentricUpperBound = float(self.eccentricUpperBoundVal.toPlainText())

        return areaLowerBound, areaUpperBound, extentLowerBound, extentUpperBound, \
            majorLowerBound, majorUpperBound, eccentricLowerBound, eccentricUpperBound

    # Get the user-provided tracker hyperparameters
    def getTrackerParams(self):
        positionSTD = self.positionSTDVal.toPlainText()
        velocitySTD = self.velocitySTDVal.toPlainText()
        accelerationSTD = self.accelerationSTDVal.toPlainText()
        movingObjSTD = self.movingObjSTDVal.toPlainText()

        # All need to be valid numbers
        if not positionSTD.isnumeric() \
                or not velocitySTD.isnumeric() \
                or not accelerationSTD.isnumeric() \
                or not movingObjSTD.isnumeric():
            raise ValueError("Ui_ControlGui: Can't parse tracking model hyperparameters")

        positionSTD = float(positionSTD)
        velocitySTD = float(velocitySTD)
        accelerationSTD = float(accelerationSTD)
        movingObjSTD = float(movingObjSTD)

        return positionSTD, velocitySTD, accelerationSTD, movingObjSTD

    # Show frame data in the main display panel
    def showFrame(self, array):
        height, width, depth = array.shape
        if depth != 3:
            raise ValueError("Ui_ControlGui: Expected frame in RGB888 format")

        # Construct the showable pixel data
        bytesPerRow = 3 * width
        qtImg = QImage(array.data, width, height, bytesPerRow, QImage.Format_RGB888)
        qtPix = QPixmap(qtImg)

        # Scale the image to fit the pane then display
        targetWidth = self.displayFrame.width()
        targetHeight = self.displayFrame.height()
        self.displayFrame.setPixmap(
            qtPix.scaled(targetWidth, targetHeight, Qt.KeepAspectRatio)
        )

