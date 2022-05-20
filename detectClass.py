from assistClass import *
import numpy as np
from scipy.stats import norm
import scipy.ndimage
import skimage
import math
import sys


#TO DETECT CLUSTERS/OBJ
class Detector():

    def __init__(self, beforeFrame, currentFrame, nextFrame, lowerBound, upperBound, gtInform, frameNo):

        self.currentFrameNo = frameNo-1
        self.beforeFrame = beforeFrame
        self.currentFrame = currentFrame
        self.nextFrame = nextFrame
        self.imgHeight = beforeFrame.shape[0]
        self.imgWidth = beforeFrame.shape[1]

        #TO STORE ALL OUTLIERS AS THE ACTUAL IMAGE
        self.goodImageB = np.zeros((self.imgHeight, self.imgWidth))
        self.goodImageN = np.zeros((self.imgHeight, self.imgWidth))

        self.cueLowerBound = lowerBound
        self.cueUpperBound = upperBound
        self.gtInform = gtInform



    def toThirtyByThirty(self, img):

        allSmallerImg = []
        i = 0

        # print(len(img))
        noOfSquares = 0
        for r in range(0,self.imgHeight,30):
            #IGNORE THE LAST 5 PIXEL ATM
            if 30*i <= len(img) - 30:
                j = 0
                for c in range(0,self.imgWidth,30):
                    if 30*j <= len(img) - 30:
                        allSmallerImg.append(img[r:r+30, c:c+30,:])
                        noOfSquares += 1
                    j+=1

            i+=1

        # print(len(allSmallerImg))
        return allSmallerImg, noOfSquares


    #FINDING ABS DIFFERENCE
    def differenceImage(self, img1, img2):
      a = img1-img2
      b = np.uint8(img1<img2) * 254 + 1
      return a * b


    def detectSmallObj(self):

        #STORING ALL 30X30 INTO ONE ARRAY
        beforeSmallerFrame, noOfSquares = self.toThirtyByThirty(self.beforeFrame)
        currentSmallerFrame, noOfSquares = self.toThirtyByThirty(self.currentFrame)
        nextSmallerFrame, noOfSquares = self.toThirtyByThirty(self.nextFrame)



        for i in range(noOfSquares):
            #CONVERT TO GRAYSCALE
            beforeGray = cv.cvtColor(beforeSmallerFrame[i], cv.COLOR_BGR2GRAY)
            currentGray = cv.cvtColor(currentSmallerFrame[i], cv.COLOR_BGR2GRAY)
            nextGray = cv.cvtColor(nextSmallerFrame[i], cv.COLOR_BGR2GRAY)


            #GET ABS DIFFERENCE AND STORE THEM
            diffBefore = self.differenceImage(beforeGray, currentGray)
            diffNext = self.differenceImage(currentGray, nextGray)


            #GET THE SUM OF DIFFERENCE
            sumBefore = diffBefore.sum()
            sumNext = diffNext.sum()

            #FIND THRESHOLD
            threshBefore = -math.log(0.05)/(1/(sumBefore/900))
            threshNext = -math.log(0.05)/(1/(sumNext/900))


            #TO GET X, Y COORDINATE FOR THE ACTUAL IMAGE FROM 30X30 SQUARES
            pixelX = i%(self.imgWidth//30)
            pixelY = i//(self.imgHeight//30)

            goodImageB = self.goodImageB
            goodImageN = self.goodImageN

            for y in range(30):

                for x in range(30):

                    #WHEN A PIXEL IN THE 30X30 ith SQUARE IS HIGHER THAN THRESHOLD
                    if diffBefore[y][x] > threshBefore:
                        goodImageB[pixelY*30+y][pixelX*30+x] = 1
                    else:
                        goodImageB[pixelY*30+y][pixelX*30+x] = 0

                    if diffNext[y][x] > threshNext:
                        goodImageN[pixelY*30+y][pixelX*30+x] = 1

                    else:
                        goodImageN[pixelY*30+y][pixelX*30+x] = 0

            #TODO: STILL NEED TO WORK OUT A WAY IF THE HEIGHT/WIDTH IS NOT DIVISIBLE BY 30


        #APPLY LOGICAL AND TO BOTH IMAGE AND CONVERT TO UINT8 TYPE
        afterLogicalAnd = np.logical_and(goodImageB,goodImageN)
        afterLogicalAnd = afterLogicalAnd.astype(np.uint8)*255

        return afterLogicalAnd

    #TO FIND QUALITY OF MATCHING BETWEEN THE INTERSECTION BETWEEN TWO BOXES
    def boxIntersectionOverUnion(self, box1, box2):
        # find the coordinates of the intersection X,Y = TOP LEFT COOR, XE,YE = BOTTOM RIGHT COOR
        x = max(box1[0], box2[0])
        y = max(box1[1], box2[1])
        xE = min(box1[2], box2[2])
        yE = min(box1[3], box2[3])

        # print(box1)
        # print(box2)

        # FIND THE AREA OF INTERSECTION
        intersectArea = max(0, xE - x + 1) * max(0, yE - y + 1)



        # FIND THE AREA OF BOTH THE PREDICTED AND TRUTH ONE
        box1Area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        box2Area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        IOU = intersectArea / float(box1Area + box2Area - intersectArea)

        return IOU

    # truePositive    =   PROPOSED MATCHING WITH TRUTH
    # falsePositive   =   PROPOSED WITHOUT MATCHING
    # falseNegative   =   TRUTH WITHOUT MATCHING
    def evaluation(self, bbox, truePositive, falsePositive, matchedTruth):

        gtInform = self.gtInform
        currentFrameNo = self.currentFrameNo

        matchingFound = False

        #GTINFORM IS STORED AS WITH ROW AS FRAME NUMBER
        for i, trueObj in enumerate(gtInform[currentFrameNo]):
            topLeftX = int(trueObj[1])
            topLeftY = int(trueObj[2])
            width = int(trueObj[3])
            height = int(trueObj[4])

            trueBox = (topLeftX, topLeftY, topLeftX+width, topLeftY+height)
            IOU = self.boxIntersectionOverUnion(trueBox, bbox)

            #MATCHING FOUND
            if IOU > 0.5:
                truePositive += 1
                matchedTruth[i] = True
                matchingFound = True
                break

        #NO MATCHING FOUND FOR THAT PROPOSAL
        if matchingFound == False:
            falsePositive += 1

        return truePositive, falsePositive, matchingFound




    def candidateMatchDiscrim(self):

        cueLowerBound = self.cueLowerBound
        cueUpperBound = self.cueUpperBound

        currentGray = cv.cvtColor(self.currentFrame, cv.COLOR_BGR2GRAY)

        #BINARY IMG CONTAINING CLUSTERS
        binaryImg = self.detectSmallObj()
        temp = binaryImg.copy()

        #TO FIND CLUSTERS & RETURN LIST OF CLUSTER INFORMAITON
        labelImg, numClusters = skimage.measure.label(temp, return_num=True)
        listOfCluster = skimage.measure.regionprops(labelImg, intensity_image=currentGray)

        #TO STORE THE END RESULT
        listOfBoundBox = []
        listOfCentroids = []

#FOR IOU
#______________________________________________________________
        # truePositive    =   PROPOSED MATCHING WITH TRUTH
        # falsePositive   =   PROPOSED WITHOUT MATCHING
        # falseNegative   =   TRUTH WITHOUT MATCHING
        truePositive = 0
        falsePositive = 0
        falseNegative = 0

        #INITIALISE A ARRAY WITH THE NUMBER OF TRUTH TRACKING OF THE CURRENT FRAME
        #AND MAKE ALL VALUE AS FALSE = NOT MATCHED YET, SOME WILL BECAME TRUE
        #DURING THE EVALUATION FUNCTION
        matchedTruth = np.full(shape=(len(self.gtInform[self.currentFrameNo])), fill_value=False)
#_____________________________________________________________


        #FOR EACH CLUSTER
        for cluster in listOfCluster:

            #GETS THE CENTROID OF CLUSTER AND FIND THE 11X11 TOP LEFT & BOTTOM RIGHT
            #PIXEL LOCATION
            centroid = cluster.centroid
            cX = int(centroid[0])
            cY = int(centroid[1])
            cYMin = cY-5
            cYMax = cY+6
            cXMin = cX-5
            cXMax = cX+6
            windowValues = None
            width = self.imgWidth
            height = self.imgHeight

            #CHECKS FOR BORDER OF IMAGE TO FIT THE 11X11 WINDOW
            if cX >= 5 and cX <= width-6 and cY >= 5 and cY <= height-6:

                #RECORD THE WINDOW VALUE OF THE CLUSTER
                windowValues = currentGray[cXMin:cXMax, cYMin:cYMax].copy()

                #GETS THE LIST OF CLUSTER COOR
                allClusterCoor = cluster.coords

                #FINDS THE SUM AND RECORD THE CLUSTER'S VALUE
                sum = 0
                allClusterVal = np.zeros(len(allClusterCoor))
                for i, coor in enumerate(allClusterCoor):

                    sum += currentGray[coor[0]][coor[1]]
                    allClusterVal[i] = currentGray[coor[0]][coor[1]]



                #GETS THE NO OF PIXELS AND FIND THE MEAN + STD OF THE CLUSTER
                #PIXELS ONLY
                noOfPixels = cluster.area
                mean = sum/noOfPixels
                std = np.std(allClusterVal)


                #NOT CONSIDERING SINGLE PIXEL CLUSTER
                if std != 0:


                    #TWO TAIL TEST 0.05 TO 0.995
                    ppf = norm.ppf(0.9975)

                    upperBound = mean + ppf*std
                    lowerBound = mean - ppf*std


                    #A MASK OF TRUE FALSE + APPLY OR TO EXPAND THE CLUSTER
                    goodIndex = np.logical_and(windowValues>=lowerBound, windowValues<=upperBound)
                    target = np.logical_or(binaryImg[cXMin:cXMax, cYMin:cYMax], goodIndex).astype(np.uint8)

                    #UPDATES BINARY IMG
                    binaryImg[cXMin:cXMax, cYMin:cYMax] = target




                    #Morphological cues

                    #TO GET THE CENTROID AND ECCENTRICITY OF THE NEW GROWED CLUSTER
                    targetLabel, targetNum = skimage.measure.label(target, return_num=True)
                    allWindowClusters = skimage.measure.regionprops(targetLabel, intensity_image=currentGray[cXMin:cXMax, cYMin:cYMax])

                    #FIND THE LABEL OF THE CENTRE ELEMENT (THE CLUSTER WE WANTED)
                    wantedLabel = targetLabel[5][5] - 1
                    targetCluster = allWindowClusters[wantedLabel]
                    targetBoundBox = (int(targetCluster.bbox[0] + cXMin), int(targetCluster.bbox[1] + cYMin), int(targetCluster.bbox[2] + cXMin), int(targetCluster.bbox[3] + cYMin))
                    targetCentroid = (int(targetCluster.centroid[0] + cXMin), int(targetCluster.centroid[1] + cYMin))
                    targetEccentricity = targetCluster.eccentricity

                    #TODO:MORE WORK NEEDED HERE FOR upper and lower threshold for morphological cues
                    #????

                    truePositive, falsePositive, matchingFound = self.evaluation(targetBoundBox, truePositive, falsePositive, matchedTruth)

                    #APPEND ONLY WHEN MATCHING IS FOUND
                    if matchingFound:
                        listOfBoundBox.append(targetBoundBox)
                        listOfCentroids.append(targetCentroid)

        #TO FIND THE NUMBER OF FALSE: EG TRUTHOBJ NOT ASSIGN
        falseNegative = np.size(matchedTruth) - np.count_nonzero(matchedTruth)

        precision = truePositive/(truePositive+falsePositive)
        recall = truePositive/(truePositive+falseNegative)
        if truePositive == 0:
            F1 = math.inf

        else:
            F1 = 2*(precision*recall)/(precision+recall)

        if len(listOfCentroids) == 0:
            print('no matching found in detection step')

        return listOfBoundBox, listOfCentroids, precision, recall, F1, truePositive, falsePositive, falseNegative



    def detectObjAndDiscrim(self):
        self.detectSmallObj()
        boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative = self.candidateMatchDiscrim()
        return boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative
