from assistClass import *
import numpy as np
from scipy.stats import norm
import scipy.ndimage
import skimage
import math
import sys

# print(a.loadFrame(1))

# toThirtyByThirty(a.loadFrame(1))

#TO 30X30 IMG SQUARES
def toThirtyByThirty(img):

    allSmallerImg = []
    i = 0
    noOfSquares = 0
    # print(len(img))
    for r in range(0,img.shape[0],30):
        #IGNORE THE LAST 5 PIXEL ATM
        if 30*i <= len(img) - 30:
            j = 0
            for c in range(0,img.shape[1],30):
                if 30*j <= len(img) - 30:
                    allSmallerImg.append(img[r:r+30, c:c+30,:])
                    noOfSquares += 1
                j+=1

        i+=1

    # print(len(allSmallerImg))
    return allSmallerImg, noOfSquares

#FINDING ABS DIFFERENCE
def differenceImage(img1, img2):
  a = img1-img2
  b = np.uint8(img1<img2) * 254 + 1
  return a * b


def detectSmallObj(beforeFrame, currentFrame, nextFrame):
    print("inside")

    #STORING ALL 30X30 INTO ONE ARRAY
    beforeSmallerFrame, noOfSquares = toThirtyByThirty(beforeFrame)
    currentSmallerFrame, noOfSquares = toThirtyByThirty(currentFrame)
    nextSmallerFrame, noOfSquares = toThirtyByThirty(nextFrame)
    print(noOfSquares)
    #TO STORE THE DIFFERENCE
    beforeAndCurrent = []
    currentAndNext = []

    #THE HEIGHT AND WIDTH OF THE FRAMES
    imgHeight = len(beforeFrame)
    imgWidth = len(beforeFrame[0])

    #THE TOTAL NUMBERS OF 30X30 SQUARES IN THE IMAGE
    noOfSquares = len(nextSmallerFrame)
    print("new   " + str(noOfSquares))
    #TO STORE ALL THRESHOLDS
    allThreshBefore = []
    allThreshNext = []

    #TO STORE ALL THE OUTLIERS AS 30X30 SQUARES
    allGoodBefore = []
    allGoodNext = []

    #TO STORE ALL OUTLIERS AS THE ACTUAL IMAGE
    goodImageB = np.zeros((imgHeight, imgWidth))
    goodImageN = np.zeros((imgHeight, imgWidth))



    #FOR EACH 30X30, WE CONVERT TO GRAY AND FIND THE DIFFERENCE
    for i in range(noOfSquares):

        #CONVERT TO GRAYSCALE
        beforeGray = cv.cvtColor(beforeSmallerFrame[i], cv.COLOR_BGR2GRAY)
        currentGray = cv.cvtColor(currentSmallerFrame[i], cv.COLOR_BGR2GRAY)
        nextGray = cv.cvtColor(nextSmallerFrame[i], cv.COLOR_BGR2GRAY)

        #GET ABS DIFFERENCE AND STORE THEM
        diffBefore = differenceImage(beforeGray, currentGray)
        diffNext = differenceImage(currentGray, nextGray)
        beforeAndCurrent.append(diffBefore)
        currentAndNext.append(diffNext)

        #GET THE SUM OF DIFFERENCE
        sumBefore = diffBefore.sum()
        sumNext = diffNext.sum()

        #FIND THRESHOLD AND STORE THEM
        threshBefore = -math.log(0.05)/(1/(sumBefore/900))
        allThreshBefore.append(threshBefore)
        threshNext = -math.log(0.05)/(1/(sumNext/900))
        allThreshBefore.append(threshNext)


        #TO STORE 30X30 OUTLIERS AFTER THRESHOLD
        goodBefore = []
        goodNext = []

        #TO GET X, Y COORDINATE FOR THE ACTUAL IMAGE FROM 30X30 SQUARES
        pixelX = i%(imgWidth//30)
        pixelY = i//(imgHeight//30)
        # print(pixelX)
        for y in range(30):

            #TO STORE 30 PIXELS (EACH ROW)
            goodBX = []
            goodNX = []
            for x in range(30):

                #WHEN A PIXEL IN THE 30X30 ith SQUARE IS HIGHER THAN THRESHOLD
                if beforeAndCurrent[i][y][x] > threshBefore:
                    goodBX.append(1)
                    goodImageB[pixelY*30+y][pixelX*30+x] = 1
                else:
                    goodBX.append(0)
                    goodImageB[pixelY*30+y][pixelX*30+x] = 0

                if currentAndNext[i][y][x] > threshNext:
                    goodNX.append(1)
                    goodImageN[pixelY*30+y][pixelX*30+x] = 1

                else:
                    goodNX.append(0)
                    goodImageN[pixelY*30+y][pixelX*30+x] = 0





            goodBefore.append(goodBX)
            goodNext.append(goodNX)


        allGoodBefore.append(goodBefore)
        allGoodNext.append(goodNext)

    #AFTER THE AND LOGICAL OPERATION ON THE TWO BINARY IMG
    afterLogicalAnd = np.logical_and(goodImageB,goodImageN)
    afterLogicalAnd = afterLogicalAnd.astype(np.uint8)
    # afterLogicalAnd = afterLogicalAnd
    # print(type(afterLogicalAnd[0][0]))
    # for i in afterLogicalAnd:
    #     for j in i:
    #         if j == 1:
    #             print("yes")
    # print(afterLogicalAnd)

    # return afterLogicalAnd
    # np.set_printoptions(threshold=sys.maxsize)
    # cv.imshow('i',afterLogicalAnd)
    # cv.imshow('j', goodImageB)
    # cv.imshow('k', goodImageN)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # np.set_printoptions(threshold=sys.maxsize)
    # print(type(goodImageB[0][0]))





    return afterLogicalAnd, imgHeight, imgWidth,



def candidateMatchDiscrim(binaryImg, imgHeight, imgWidth, nextFrame):

    # windowSize = 11

    # contours, hierarchy = cv.findContours(temp, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    # # cv.imshow('img1', temp)
    # # cv.drawContours(temp, contours, -1, (0,255,0), 3)
    # # cv.imshow('img', temp)
    #
    # # cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
    #
    # for c in contours:
    #     M = cv.moments(c)
    #     if M["m00"] != 0:
    #
    #         cX = int(M["m10"] / M["m00"])
    #         cY = int(M["m01"] / M["m00"])
    #
    #         # windowValues = np.zeros((11,11))
    #         # for row in range(cY-5, cY+6):
    #         #     for col in range(cX-5, cX+6):
    #         #         windowValues[row][col] = binaryImg[row][col]
    #
    #         if cX >= 5 and cX <= width-6 and cY >= 5 and cY <= height-6:
    #             windowValues = binaryImg[cY-5:cY+6, cX-5:cX+6].copy()
    #             allOnes = windowValues[windowValues == 1]
    #
    #
    #             mean = np.mean(allOnes)
    #             std = np.std(allOnes)
    #             print(mean, std)
    #             # norm.ppf(0.95, mean, std)



            # cv.circle(frame, (cX, cY), 1, (255, 255, 255), -1)


    # cv.imshow('frame',frame)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    temp = binaryImg.copy()

    labelImg, numClusters = skimage.measure.label(temp, return_num=True)

    # structure = [[1,1,1], [1,1,1], [1,1,1]]
    # labelImg, numClusters = scipy.ndimage.label(temp, structure)
    print(numClusters)
    nextGray = cv.cvtColor(nextFrame, cv.COLOR_BGR2GRAY)
    listOfCluster = skimage.measure.regionprops(labelImg, intensity_image=nextGray)



    for cluster in listOfCluster:
        centroid = cluster.centroid

        cX = int(centroid[0])
        cY = int(centroid[1])
        cYMin = cY-5
        cYMax = cY+6
        cXMin = cX-5
        cXMax = cX+6
        windowValues = None
        if cX >= 5 and cX <= width-6 and cY >= 5 and cY <= height-6:
            windowValues = nextGray[cXMin:cXMax, cYMin:cYMax].copy()

            allClusterCoor = cluster.coords
            sum = 0
            allClusterVal = np.zeros(len(allClusterCoor))
            for i, coor in enumerate(allClusterCoor):
                # print(coor)
                sum += nextGray[coor[0]][coor[1]]
                allClusterVal[i] = nextGray[coor[0]][coor[1]]
                # print(i)

#####       DONT KNOW THIS (THE MEAN AND STANDARD DEVIATION PART)
##______________________________________________________

            mean = sum/len(allClusterCoor)
            std = np.std(allClusterVal)


            if std != 0:
                # print(std)
                # print(mean)
                # print(allClusterCoor)

                ppf = norm.ppf(0.9975)

                upperBound = mean + ppf*std
                lowerBound = mean - ppf*std
#__________________________________________________________________
###################################################################

                #A MASK OF TRUE FALSE + APPLY OR TO EXPAND THE CLUSTER
                goodIndex = np.logical_and(windowValues>=lowerBound, windowValues<=upperBound)
                target = np.logical_or(binaryImg[cXMin:cXMax, cYMin:cYMax], goodIndex).astype(np.uint8)

                #UPDATES BINARY IMG
                binaryImg[cXMin:cXMax, cYMin:cYMax] = target

                #GETS THE CENTROID AND ECCENTRICITY OF THE NEW GROWED CLUSTER
                targetLabel, targetNum = skimage.measure.label(target, return_num=True)

                allWindowClusters = skimage.measure.regionprops(targetLabel, intensity_image=nextGray[cXMin:cXMax, cYMin:cYMax])


                #CHECK THE LABEL OF THE CENTRE ELEMENT (THE CLUSTER WE WANTED)
                wantedLabel = targetLabel[5][5] - 1

                targetCluster = allWindowClusters[wantedLabel]
                targetCentroid = targetCluster.centroid
                targetEccentricity = targetCluster.eccentricity

                #TODO:MORE WORK NEEDED HERE FOR upper and lower threshold for morphological cues






    temp = binaryImg.copy()
    # labelImg, numClusters = skimage.measure.label(temp, return_num=True)
    # listOfCluster = skimage.measure.regionprops(labelImg, intensity_image=nextGray)


    binaryImg = binaryImg*255
    cv.imshow("target",binaryImg)
    cv.waitKey(0)
    cv.destroyAllWindows()
    # print(lowerBound)
    # print(upperBound)
    # print(goodIndex)
    # print(windowValues)
    # print(binaryImg[cXMin:cXMax, cYMin:cYMax])



#GOOD another way! should get the same result as above_________________________________________________________________________________________
    # allStd = scipy.ndimage.standard_deviation(nextGray, labelImg, index=np.arange(1, numClusters+1))
    # allSum = scipy.ndimage.sum_labels(nextGray, labelImg, index=np.arange(1, numClusters+1))
    # allMean = scipy.ndimage.mean(nextGray, labelImg, index=np.arange(1, numClusters+1))
    # print(allSum[14])
    # print(allStd[14])
    # print(allMean[14])
    # print(nextGray[5][248] + nextGray[6][249])
#______________________________________________________________________________________________________


    return #TODO:A LIST OF BOUNDING BOX AND CENTROID FOR EACH CLUSTER IN THE FRAME

a = Image("001", "car", [])
a.getImagesPath()
a.getFrameRange()
a.parser.getGTInformation()
img, height, width,  = detectSmallObj(a.loadFrame(1), a.loadFrame(2), a.loadFrame(3))
candidateMatchDiscrim(img, height, width, a.loadFrame(2))
