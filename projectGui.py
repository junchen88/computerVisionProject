# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projectGui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1058, 839)
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(860, 340, 89, 25))
        self.startButton.setObjectName("startButton")
        self.positionSTDSlider = QtWidgets.QSlider(Dialog)
        self.positionSTDSlider.setGeometry(QtCore.QRect(620, 120, 160, 16))
        self.positionSTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.positionSTDSlider.setObjectName("positionSTDSlider")
        self.velocitySTDSlider = QtWidgets.QSlider(Dialog)
        self.velocitySTDSlider.setGeometry(QtCore.QRect(620, 160, 160, 16))
        self.velocitySTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.velocitySTDSlider.setObjectName("velocitySTDSlider")
        self.accelerationSTDSlider = QtWidgets.QSlider(Dialog)
        self.accelerationSTDSlider.setGeometry(QtCore.QRect(620, 200, 160, 16))
        self.accelerationSTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.accelerationSTDSlider.setObjectName("accelerationSTDSlider")
        self.displayFrame = QwtPlot(Dialog)
        self.displayFrame.setEnabled(True)
        self.displayFrame.setGeometry(QtCore.QRect(0, 30, 481, 431))
        self.displayFrame.setObjectName("displayFrame")
        self.ImgLabel = QwtTextLabel(Dialog)
        self.ImgLabel.setGeometry(QtCore.QRect(210, 10, 100, 20))
        self.ImgLabel.setObjectName("ImgLabel")
        self.positionSTD = QwtTextLabel(Dialog)
        self.positionSTD.setGeometry(QtCore.QRect(650, 100, 100, 20))
        self.positionSTD.setObjectName("positionSTD")
        self.velocitySTD = QwtTextLabel(Dialog)
        self.velocitySTD.setGeometry(QtCore.QRect(650, 140, 100, 20))
        self.velocitySTD.setObjectName("velocitySTD")
        self.accelerationSTD = QwtTextLabel(Dialog)
        self.accelerationSTD.setGeometry(QtCore.QRect(640, 180, 121, 16))
        self.accelerationSTD.setObjectName("accelerationSTD")
        self.positionSTDVal = QtWidgets.QPlainTextEdit(Dialog)
        self.positionSTDVal.setGeometry(QtCore.QRect(820, 110, 91, 31))
        self.positionSTDVal.setPlainText("")
        self.positionSTDVal.setObjectName("positionSTDVal")
        self.velocitySTDVal = QtWidgets.QPlainTextEdit(Dialog)
        self.velocitySTDVal.setGeometry(QtCore.QRect(820, 150, 91, 31))
        self.velocitySTDVal.setPlainText("")
        self.velocitySTDVal.setObjectName("velocitySTDVal")
        self.accelerationSTDVal = QtWidgets.QPlainTextEdit(Dialog)
        self.accelerationSTDVal.setGeometry(QtCore.QRect(820, 190, 91, 31))
        self.accelerationSTDVal.setPlainText("")
        self.accelerationSTDVal.setObjectName("accelerationSTDVal")
        self.frameHigher = QtWidgets.QPlainTextEdit(Dialog)
        self.frameHigher.setGeometry(QtCore.QRect(740, 340, 91, 31))
        self.frameHigher.setPlainText("")
        self.frameHigher.setObjectName("frameHigher")
        self.frameLower = QtWidgets.QPlainTextEdit(Dialog)
        self.frameLower.setGeometry(QtCore.QRect(630, 340, 91, 31))
        self.frameLower.setPlainText("")
        self.frameLower.setObjectName("frameLower")
        self.ImgLabel_2 = QwtTextLabel(Dialog)
        self.ImgLabel_2.setGeometry(QtCore.QRect(520, 340, 100, 20))
        self.ImgLabel_2.setObjectName("ImgLabel_2")
        self.qwtPlot_2 = QwtPlot(Dialog)
        self.qwtPlot_2.setEnabled(True)
        self.qwtPlot_2.setGeometry(QtCore.QRect(30, 550, 400, 200))
        self.qwtPlot_2.setObjectName("qwtPlot_2")
        self.qwtPlot_3 = QwtPlot(Dialog)
        self.qwtPlot_3.setEnabled(True)
        self.qwtPlot_3.setGeometry(QtCore.QRect(520, 390, 400, 200))
        self.qwtPlot_3.setObjectName("qwtPlot_3")
        self.qwtPlot_4 = QwtPlot(Dialog)
        self.qwtPlot_4.setEnabled(True)
        self.qwtPlot_4.setGeometry(QtCore.QRect(520, 610, 400, 200))
        self.qwtPlot_4.setObjectName("qwtPlot_4")
        self.objectType = QtWidgets.QPlainTextEdit(Dialog)
        self.objectType.setGeometry(QtCore.QRect(860, 280, 91, 31))
        self.objectType.setPlainText("")
        self.objectType.setObjectName("objectType")
        self.imageName = QtWidgets.QPlainTextEdit(Dialog)
        self.imageName.setGeometry(QtCore.QRect(630, 280, 91, 31))
        self.imageName.setPlainText("")
        self.imageName.setObjectName("imageName")
        self.ImgLabel_3 = QwtTextLabel(Dialog)
        self.ImgLabel_3.setGeometry(QtCore.QRect(520, 280, 100, 20))
        self.ImgLabel_3.setObjectName("ImgLabel_3")
        self.ImgLabel_4 = QwtTextLabel(Dialog)
        self.ImgLabel_4.setGeometry(QtCore.QRect(740, 280, 100, 20))
        self.ImgLabel_4.setObjectName("ImgLabel_4")
        self.upperBoundCueSlider = QtWidgets.QSlider(Dialog)
        self.upperBoundCueSlider.setGeometry(QtCore.QRect(620, 80, 160, 16))
        self.upperBoundCueSlider.setOrientation(QtCore.Qt.Horizontal)
        self.upperBoundCueSlider.setObjectName("upperBoundCueSlider")
        self.lowerBoundCueSlider = QtWidgets.QSlider(Dialog)
        self.lowerBoundCueSlider.setGeometry(QtCore.QRect(620, 40, 160, 16))
        self.lowerBoundCueSlider.setOrientation(QtCore.Qt.Horizontal)
        self.lowerBoundCueSlider.setObjectName("lowerBoundCueSlider")
        self.upperBoundCueVal = QtWidgets.QPlainTextEdit(Dialog)
        self.upperBoundCueVal.setGeometry(QtCore.QRect(820, 70, 91, 31))
        self.upperBoundCueVal.setPlainText("")
        self.upperBoundCueVal.setObjectName("upperBoundCueVal")
        self.lowerBoundCueVal = QtWidgets.QPlainTextEdit(Dialog)
        self.lowerBoundCueVal.setGeometry(QtCore.QRect(820, 30, 91, 31))
        self.lowerBoundCueVal.setPlainText("")
        self.lowerBoundCueVal.setObjectName("lowerBoundCueVal")
        self.qwtTextLabel = QwtTextLabel(Dialog)
        self.qwtTextLabel.setGeometry(QtCore.QRect(640, 60, 131, 20))
        self.qwtTextLabel.setObjectName("qwtTextLabel")
        self.positionSTD_3 = QwtTextLabel(Dialog)
        self.positionSTD_3.setGeometry(QtCore.QRect(630, 20, 141, 20))
        self.positionSTD_3.setObjectName("positionSTD_3")
        self.accelerationSTD_2 = QwtTextLabel(Dialog)
        self.accelerationSTD_2.setGeometry(QtCore.QRect(640, 220, 121, 16))
        self.accelerationSTD_2.setObjectName("accelerationSTD_2")
        self.movingObjSTDSlider = QtWidgets.QSlider(Dialog)
        self.movingObjSTDSlider.setGeometry(QtCore.QRect(620, 240, 160, 16))
        self.movingObjSTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.movingObjSTDSlider.setObjectName("movingObjSTDSlider")
        self.movingObjSTDVal = QtWidgets.QPlainTextEdit(Dialog)
        self.movingObjSTDVal.setGeometry(QtCore.QRect(820, 230, 91, 31))
        self.movingObjSTDVal.setPlainText("")
        self.movingObjSTDVal.setObjectName("movingObjSTDVal")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.startButton.setText(_translate("Dialog", "Start"))
        self.ImgLabel.setPlainText(_translate("Dialog", "Frames"))
        self.positionSTD.setPlainText(_translate("Dialog", "PositionSTD"))
        self.velocitySTD.setPlainText(_translate("Dialog", "VelocitySTD"))
        self.accelerationSTD.setPlainText(_translate("Dialog", "AccelerationSTD"))
        self.ImgLabel_2.setPlainText(_translate("Dialog", "Frame range:"))
        self.ImgLabel_3.setPlainText(_translate("Dialog", "Image Name:"))
        self.ImgLabel_4.setPlainText(_translate("Dialog", "Object Type:"))
        self.qwtTextLabel.setPlainText(_translate("Dialog", "Upper Bound Cue"))
        self.positionSTD_3.setPlainText(_translate("Dialog", "Lower Bound Cue"))
        self.accelerationSTD_2.setPlainText(_translate("Dialog", "MovingObjSTD"))
from qwt import QwtPlot
from qwt.text import QwtTextLabel


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())