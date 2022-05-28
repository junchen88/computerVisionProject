# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ControlGuiBase.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class ControlGuiBase(object):
    def setupUi(self, baseDialog):
        baseDialog.setObjectName("baseDialog")
        baseDialog.setEnabled(True)
        baseDialog.setGeometry(QtCore.QRect(0, 0, 1060, 900))
        self.resetButton = QtWidgets.QPushButton(baseDialog)
        self.resetButton.setGeometry(QtCore.QRect(860, 340, 89, 25))
        self.resetButton.setObjectName("resetButton")
        self.progressText = QwtTextLabel(baseDialog)
        self.progressText.setGeometry(QtCore.QRect(550, 385, 100, 20))
        self.progressText.setObjectName("progressText")
        self.nextButton = QtWidgets.QPushButton(baseDialog)
        self.nextButton.setGeometry(QtCore.QRect(860, 385, 89, 25))
        self.nextButton.setObjectName("nextButton")
        self.displayFrame = QtWidgets.QLabel(baseDialog)
        self.displayFrame.setEnabled(True)
        self.displayFrame.setGeometry(QtCore.QRect(30, 30, 451, 431))
        self.displayFrame.setObjectName("displayFrame")
        self.displayFrameLabel = QwtTextLabel(baseDialog)
        self.displayFrameLabel.setGeometry(QtCore.QRect(210, 10, 100, 20))
        self.displayFrameLabel.setObjectName("displayFrameLabel")
        self.areaLowerBoundSlider = QtWidgets.QSlider(baseDialog)
        self.areaLowerBoundSlider.setGeometry(QtCore.QRect(490, 40, 160, 16))
        self.areaLowerBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.areaLowerBoundSlider.setObjectName("areaLowerBoundSlider")
        self.areaUpperBoundSlider = QtWidgets.QSlider(baseDialog)
        self.areaUpperBoundSlider.setGeometry(QtCore.QRect(770, 40, 160, 16))
        self.areaUpperBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.areaUpperBoundSlider.setObjectName("areaUpperBoundSlider")
        self.extentLowerBoundSlider = QtWidgets.QSlider(baseDialog)
        self.extentLowerBoundSlider.setGeometry(QtCore.QRect(490, 80, 160, 16))
        self.extentLowerBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.extentLowerBoundSlider.setObjectName("extentLowerBoundSlider")
        self.extentUpperBoundSlider = QtWidgets.QSlider(baseDialog)
        self.extentUpperBoundSlider.setGeometry(QtCore.QRect(770, 80, 160, 16))
        self.extentUpperBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.extentUpperBoundSlider.setObjectName("extentUpperBoundSlider")
        self.majorLowerBoundSlider = QtWidgets.QSlider(baseDialog)
        self.majorLowerBoundSlider.setGeometry(QtCore.QRect(490, 120, 160, 16))
        self.majorLowerBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.majorLowerBoundSlider.setObjectName("majorLowerBoundSlider")
        self.majorUpperBoundSlider = QtWidgets.QSlider(baseDialog)
        self.majorUpperBoundSlider.setGeometry(QtCore.QRect(770, 120, 160, 16))
        self.majorUpperBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.majorUpperBoundSlider.setObjectName("majorUpperBoundSlider")
        self.eccentricLowerBoundSlider = QtWidgets.QSlider(baseDialog)
        self.eccentricLowerBoundSlider.setGeometry(QtCore.QRect(490, 160, 160, 16))
        self.eccentricLowerBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.eccentricLowerBoundSlider.setObjectName("eccentricLowerBoundSlider")
        self.eccentricUpperBoundSlider = QtWidgets.QSlider(baseDialog)
        self.eccentricUpperBoundSlider.setGeometry(QtCore.QRect(770, 160, 160, 16))
        self.eccentricUpperBoundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.eccentricUpperBoundSlider.setObjectName("eccentricUpperBoundSlider")
        self.positionSTDSlider = QtWidgets.QSlider(baseDialog)
        self.positionSTDSlider.setGeometry(QtCore.QRect(490, 200, 160, 16))
        self.positionSTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.positionSTDSlider.setObjectName("positionSTDSlider")
        self.velocitySTDSlider = QtWidgets.QSlider(baseDialog)
        self.velocitySTDSlider.setGeometry(QtCore.QRect(770, 200, 160, 16))
        self.velocitySTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.velocitySTDSlider.setObjectName("velocitySTDSlider")
        self.accelerationSTDSlider = QtWidgets.QSlider(baseDialog)
        self.accelerationSTDSlider.setGeometry(QtCore.QRect(490, 240, 160, 16))
        self.accelerationSTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.accelerationSTDSlider.setObjectName("accelerationSTDSlider")
        self.movingObjSTDSlider = QtWidgets.QSlider(baseDialog)
        self.movingObjSTDSlider.setGeometry(QtCore.QRect(770, 240, 160, 16))
        self.movingObjSTDSlider.setOrientation(QtCore.Qt.Horizontal)
        self.movingObjSTDSlider.setObjectName("movingObjSTDSlider")
        self.areaLowerBoundLabel = QwtTextLabel(baseDialog)
        self.areaLowerBoundLabel.setGeometry(QtCore.QRect(520, 20, 120, 20))
        self.areaLowerBoundLabel.setObjectName("areaLowerBoundLabel")
        self.areaUpperBoundLabel = QwtTextLabel(baseDialog)
        self.areaUpperBoundLabel.setGeometry(QtCore.QRect(800, 20, 120, 20))
        self.areaUpperBoundLabel.setObjectName("areaUpperBoundLabel")
        self.extentLowerBoundLabel = QwtTextLabel(baseDialog)
        self.extentLowerBoundLabel.setGeometry(QtCore.QRect(520, 60, 120, 20))
        self.extentLowerBoundLabel.setObjectName("extentLowerBoundLabel")
        self.extentUpperBoundLabel = QwtTextLabel(baseDialog)
        self.extentUpperBoundLabel.setGeometry(QtCore.QRect(800, 60, 120, 20))
        self.extentUpperBoundLabel.setObjectName("extentUpperBoundLabel")
        self.majorLowerBoundLabel = QwtTextLabel(baseDialog)
        self.majorLowerBoundLabel.setGeometry(QtCore.QRect(520, 100, 120, 20))
        self.majorLowerBoundLabel.setObjectName("majorLowerBoundLabel")
        self.majorUpperBoundLabel = QwtTextLabel(baseDialog)
        self.majorUpperBoundLabel.setGeometry(QtCore.QRect(800, 100, 120, 20))
        self.majorUpperBoundLabel.setObjectName("majorUpperBoundLabel")
        self.eccentricLowerBoundLabel = QwtTextLabel(baseDialog)
        self.eccentricLowerBoundLabel.setGeometry(QtCore.QRect(520, 140, 120, 20))
        self.eccentricLowerBoundLabel.setObjectName("eccentricLowerBoundLabel")
        self.eccentricUpperBoundLabel = QwtTextLabel(baseDialog)
        self.eccentricUpperBoundLabel.setGeometry(QtCore.QRect(800, 140, 120, 20))
        self.eccentricUpperBoundLabel.setObjectName("eccentricUpperBoundLabel")
        self.positionSTDLabel = QwtTextLabel(baseDialog)
        self.positionSTDLabel.setGeometry(QtCore.QRect(520, 180, 120, 20))
        self.positionSTDLabel.setObjectName("positionSTDLabel")
        self.velocitySTDLabel = QwtTextLabel(baseDialog)
        self.velocitySTDLabel.setGeometry(QtCore.QRect(800, 180, 120, 20))
        self.velocitySTDLabel.setObjectName("velocitySTDLabel")
        self.accelerationSTDLabel = QwtTextLabel(baseDialog)
        self.accelerationSTDLabel.setGeometry(QtCore.QRect(520, 220, 120, 20))
        self.accelerationSTDLabel.setObjectName("accelerationSTDLabel")
        self.movingObjSTDLabel = QwtTextLabel(baseDialog)
        self.movingObjSTDLabel.setGeometry(QtCore.QRect(800, 220, 120, 20))
        self.movingObjSTDLabel.setObjectName("movingObjSTDLabel")
        self.areaLowerBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.areaLowerBoundVal.setGeometry(QtCore.QRect(660, 30, 91, 31))
        self.areaLowerBoundVal.setPlainText("")
        self.areaLowerBoundVal.setObjectName("areaLowerBoundVal")
        self.areaUpperBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.areaUpperBoundVal.setGeometry(QtCore.QRect(940, 30, 91, 31))
        self.areaUpperBoundVal.setPlainText("")
        self.areaUpperBoundVal.setObjectName("areaUpperBoundVal")
        self.extentLowerBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.extentLowerBoundVal.setGeometry(QtCore.QRect(660, 70, 91, 31))
        self.extentLowerBoundVal.setPlainText("")
        self.extentLowerBoundVal.setObjectName("extentLowerBoundVal")
        self.extentUpperBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.extentUpperBoundVal.setGeometry(QtCore.QRect(940, 70, 91, 31))
        self.extentUpperBoundVal.setPlainText("")
        self.extentUpperBoundVal.setObjectName("extentUpperBoundVal")
        self.majorLowerBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.majorLowerBoundVal.setGeometry(QtCore.QRect(660, 110, 91, 31))
        self.majorLowerBoundVal.setPlainText("")
        self.majorLowerBoundVal.setObjectName("majorLowerBoundVal")
        self.majorUpperBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.majorUpperBoundVal.setGeometry(QtCore.QRect(940, 110, 91, 31))
        self.majorUpperBoundVal.setPlainText("")
        self.majorUpperBoundVal.setObjectName("majorUpperBoundVal")
        self.eccentricLowerBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.eccentricLowerBoundVal.setGeometry(QtCore.QRect(660, 150, 91, 31))
        self.eccentricLowerBoundVal.setPlainText("")
        self.eccentricLowerBoundVal.setObjectName("eccentricLowerBoundVal")
        self.eccentricUpperBoundVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.eccentricUpperBoundVal.setGeometry(QtCore.QRect(940, 150, 91, 31))
        self.eccentricUpperBoundVal.setPlainText("")
        self.eccentricUpperBoundVal.setObjectName("eccentricUpperBoundVal")
        self.positionSTDVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.positionSTDVal.setGeometry(QtCore.QRect(660, 190, 91, 31))
        self.positionSTDVal.setPlainText("")
        self.positionSTDVal.setObjectName("positionSTDVal")
        self.velocitySTDVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.velocitySTDVal.setGeometry(QtCore.QRect(940, 190, 91, 31))
        self.velocitySTDVal.setPlainText("")
        self.velocitySTDVal.setObjectName("velocitySTDVal")
        self.accelerationSTDVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.accelerationSTDVal.setGeometry(QtCore.QRect(660, 230, 91, 31))
        self.accelerationSTDVal.setPlainText("")
        self.accelerationSTDVal.setObjectName("accelerationSTDVal")
        self.movingObjSTDVal = QtWidgets.QPlainTextEdit(baseDialog)
        self.movingObjSTDVal.setGeometry(QtCore.QRect(940, 230, 91, 31))
        self.movingObjSTDVal.setPlainText("")
        self.movingObjSTDVal.setObjectName("movingObjSTDVal")
        self.frameHigher = QtWidgets.QPlainTextEdit(baseDialog)
        self.frameHigher.setGeometry(QtCore.QRect(740, 340, 91, 31))
        self.frameHigher.setPlainText("")
        self.frameHigher.setObjectName("frameHigher")
        self.frameLower = QtWidgets.QPlainTextEdit(baseDialog)
        self.frameLower.setGeometry(QtCore.QRect(630, 340, 91, 31))
        self.frameLower.setPlainText("")
        self.frameLower.setObjectName("frameLower")
        self.ImgLabel_2 = QwtTextLabel(baseDialog)
        self.ImgLabel_2.setGeometry(QtCore.QRect(520, 340, 100, 20))
        self.ImgLabel_2.setObjectName("ImgLabel_2")
        self.qwtPlot_2 = QwtPlot(baseDialog)
        self.qwtPlot_2.setEnabled(True)
        self.qwtPlot_2.setGeometry(QtCore.QRect(30, 550, 400, 200))
        self.qwtPlot_2.setObjectName("qwtPlot_2")
        self.qwtPlot_3 = QwtPlot(baseDialog)
        self.qwtPlot_3.setEnabled(True)
        self.qwtPlot_3.setGeometry(QtCore.QRect(520, 450, 400, 200))
        self.qwtPlot_3.setObjectName("qwtPlot_3")
        self.qwtPlot_4 = QwtPlot(baseDialog)
        self.qwtPlot_4.setEnabled(True)
        self.qwtPlot_4.setGeometry(QtCore.QRect(520, 660, 400, 200))
        self.qwtPlot_4.setObjectName("qwtPlot_4")
        self.objectType = QtWidgets.QPlainTextEdit(baseDialog)
        self.objectType.setGeometry(QtCore.QRect(860, 280, 91, 31))
        self.objectType.setPlainText("")
        self.objectType.setObjectName("objectType")
        self.imageName = QtWidgets.QPlainTextEdit(baseDialog)
        self.imageName.setGeometry(QtCore.QRect(630, 280, 91, 31))
        self.imageName.setPlainText("")
        self.imageName.setObjectName("imageName")
        self.ImgLabel_3 = QwtTextLabel(baseDialog)
        self.ImgLabel_3.setGeometry(QtCore.QRect(520, 280, 100, 20))
        self.ImgLabel_3.setObjectName("ImgLabel_3")
        self.ImgLabel_4 = QwtTextLabel(baseDialog)
        self.ImgLabel_4.setGeometry(QtCore.QRect(740, 280, 100, 20))
        self.ImgLabel_4.setObjectName("ImgLabel_4")

        self.retranslateUi(baseDialog)
        QtCore.QMetaObject.connectSlotsByName(baseDialog)

    def retranslateUi(self, baseDialog):
        _translate = QtCore.QCoreApplication.translate
        baseDialog.setWindowTitle(_translate("ControlGuiBase", "Small Object Tracker"))
        self.resetButton.setText(_translate("ControlGuiBase", "Start"))
        self.progressText.setPlainText(_translate("ControlGuiBase", "Waiting..."))
        self.nextButton.setText(_translate("ControlGuiBase", "Next"))
        self.displayFrameLabel.setPlainText(_translate("ControlGuiBase", "Frame"))
        self.areaLowerBoundLabel.setPlainText(_translate("ControlGuiBase", "areaLowerBound"))
        self.areaUpperBoundLabel.setPlainText(_translate("ControlGuiBase", "areaUpperBound"))
        self.extentLowerBoundLabel.setPlainText(_translate("ControlGuiBase", "extentLowerBound"))
        self.extentUpperBoundLabel.setPlainText(_translate("ControlGuiBase", "extentUpperBound"))
        self.majorLowerBoundLabel.setPlainText(_translate("ControlGuiBase", "majorLowerBound"))
        self.majorUpperBoundLabel.setPlainText(_translate("ControlGuiBase", "majorUpperBound"))
        self.eccentricLowerBoundLabel.setPlainText(_translate("ControlGuiBase", "eccentricLowerBound"))
        self.eccentricUpperBoundLabel.setPlainText(_translate("ControlGuiBase", "eccentricUpperBound"))
        self.positionSTDLabel.setPlainText(_translate("ControlGuiBase", "PositionSTD"))
        self.velocitySTDLabel.setPlainText(_translate("ControlGuiBase", "VelocitySTD"))
        self.accelerationSTDLabel.setPlainText(_translate("ControlGuiBase", "AccelerationSTD"))
        self.movingObjSTDLabel.setPlainText(_translate("ControlGuiBase", "MovingObjSTD"))
        self.ImgLabel_2.setPlainText(_translate("ControlGuiBase", "Frame range:"))
        self.ImgLabel_3.setPlainText(_translate("ControlGuiBase", "Image Name:"))
        self.ImgLabel_4.setPlainText(_translate("ControlGuiBase", "Object Type:"))
from qwt import QwtPlot
from qwt.text import QwtTextLabel
