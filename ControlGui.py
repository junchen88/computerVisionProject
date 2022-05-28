from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

from ControlGuiBase import Ui_ControlGuiBase

# Helper function: Set the text of a label automatically from the value of a
# control when it's changed.
def tieLabelToControlValue(control, label):
    def valueChangedHandler():
        value = control.value()
        label.setPlainText(str(value))

    # Connect the handler, then fire it once to get up-to-date
    control.valueChanged.connect(valueChangedHandler)
    valueChangedHandler()

class Ui_ControlGui(Ui_ControlGuiBase):
    def __init__(self, baseDialog):
        self.setupUi(baseDialog)

        # Tie each slider to the adjacent text field for easy value entry
        tieLabelToControlValue(self.lowerBoundCueSlider, self.lowerBoundCueVal)
        tieLabelToControlValue(self.upperBoundCueSlider, self.upperBoundCueVal)
        tieLabelToControlValue(self.positionSTDSlider, self.positionSTDVal)
        tieLabelToControlValue(self.velocitySTDSlider, self.velocitySTDVal)
        tieLabelToControlValue(self.accelerationSTDSlider, self.accelerationSTDVal)
        tieLabelToControlValue(self.movingObjSTDSlider, self.movingObjSTDVal)

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

        if lowerRange < 0 or upperRange < 0 or lowerRange >= upperRange:
            raise ValueError("Ui_ControlGui: Invalid frame range provided")

        return lowerRange, upperRange

    # Get the user-provided cue bounds
    def getCueBounds(self):
        cueLowerBound = float(self.lowerBoundCueVal.toPlainText())
        cueUpperBound = float(self.upperBoundCueVal.toPlainText())

        return cueLowerBound, cueUpperBound

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

