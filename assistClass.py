import os
import skimage
import pandas as pd
import numpy as np

class Parser:
    def __init__(self, imageName, imageType):
        self.imageName = imageName
        self.imageType = imageType


    #GETS ALL FRAME FILE LOCATION
    def getFilePath(self, type):
        path = "mot/{}/{}/{}".format(self.imageType, self.imageName,type)
        allFiles = []

        checker = 0
        with os.scandir('mot') as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    if entry.name == self.imageType:
                        checker = 1
                        break

            if checker == 0:
                print(self.imageType + ' FOLDER NOT FOUND, PLEASE RESTART APP')
                quit()


        checker = 0
        with os.scandir('mot/'+self.imageType) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    if entry.name == self.imageName:
                        checker = 1
                        break

            if checker == 0:
                print(self.imageName + ' FOLDER NOT FOUND, PLEASE RESTART APP')
                quit()


        with os.scandir(path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    allFiles.append(path+'/'+entry.name)

        allFiles.sort()
        return allFiles

    def getGTInformation(self):

        gtPath = self.getFilePath('gt')[0]

        df = pd.read_csv(gtPath,header=None)

        #ONLY GETS THE USEFUL INFORMATION
        df = df[[0, 1, 2, 3, 4, 5]].values.tolist()

        list = []
        previous = 1
        tempList = []

        #SORT LINE INTO FRAME AS INDEX
        for line in df:

            if line[0] == previous:
                tempList.append(line[1:])

            else:
                list.append(tempList)
                previous += 1
                tempList = []
                tempList.append(line[1:])

        df = np.array(list, dtype=object)

        return df




class Image:

    def __init__(self, imageName, imageType, frameRange):
        self.frameRange = []
        self.inputFrameRange = frameRange
        self.imageName = imageName
        self.imageType = imageType
        self.parser = Parser(imageName, imageType)

    def getImagesPath(self):
        self.allImagePath = self.parser.getFilePath('img')


    def loadFrame(self, frame):
        frameRange = self.frameRange
        if frame >= frameRange[0] and frame <= self.frameRange[1]:
            img = skimage.imread(self.allImagePath[frame-1])

            return img

        else:
            print("EXCEEDED THE RANGE OF FRAMES, PLEASE RESTART APP...")
            quit()

    def getFrameRange(self):

        self.frameRange = [0, len(self.allImagePath)]
        #IF NO FRAME RANGE IS PROVIDED
        if not self.inputFrameRange:
            self.inputFrameRange = self.frameRange
