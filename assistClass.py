import cv2 as cv
import os
import re
import pandas as pd

class Parser:
    def __init__(self, imageName, imageType):
        self.imageName = imageName
        self.imageType = imageType


    def getFilePath(self, type):
        path = "mot/{}/{}/{}".format(self.imageType, self.imageName,type)
        allFiles = []
        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    allFiles.append(path+'/'+entry.name)

        allFiles.sort()
        return allFiles

    def getGTInformation(self):

        gtPath = self.getFilePath('gt')[0]
        # pd.options.display.max_rows = 32000
        return pd.read_csv(gtPath,header=None)


class Image:

    def __init__(self, imageName, imageType, frameRange):
        self.frameRange = frameRange
        self.imageName = imageName
        self.imageType = imageType
        self.parser = Parser(imageName, imageType)

    def getImagesPath(self):
        self.allImagePath = self.parser.getFilePath('img')


    def loadFrame(self, frame):

        if frame >= 1 and frame <= self.frameRange[-1]:
            img = cv.imread(self.allImagePath[frame-1])

            return img

        else:
            quit()

    def getFrameRange(self):
        #IF NO FRAME RANGE IS PROVIDED
        if not self.frameRange:
            self.frameRange = [0, len(self.allImagePath)]
