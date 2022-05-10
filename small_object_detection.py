from assistClass import *
import numpy as np
import math

# print(a.loadFrame(1))

# toThirtyByThirty(a.loadFrame(1))

#TO 30X30 IMG SQUARES
def toThirtyByThirty(img):

    allSmallerImg = []
    i = 0

    # print(len(img))
    for r in range(0,img.shape[0],30):
        #IGNORE THE LAST 5 PIXEL ATM
        if 30*i <= len(img) - 30:
            j = 0
            for c in range(0,img.shape[1],30):
                if 30*j <= len(img) - 30:
                    allSmallerImg.append(img[r:r+30, c:c+30,:])

                j+=1

        i+=1

    # print(len(allSmallerImg))
    return allSmallerImg

#FINDING ABS DIFFERENCE
def differenceImage(img1, img2):
  a = img1-img2
  b = np.uint8(img1<img2) * 254 + 1
  return a * b


def detectSmallObj(beforeFrame, currentFrame, nextFrame):
    print("inside")

    #STORING ALL 30X30 INTO ONE ARRAY
    beforeSmallerFrame = toThirtyByThirty(beforeFrame)
    currentSmallerFrame = toThirtyByThirty(currentFrame)
    nextSmallerFrame = toThirtyByThirty(nextFrame)

    #TO STORE THE DIFFERENCE
    beforeAndCurrent = []
    currentAndNext = []

    #THE HEIGHT AND WIDTH OF THE FRAMES
    imgHeight = len(beforeFrame)
    imgWidth = len(beforeFrame[0])

    #THE TOTAL NUMBERS OF 30X30 SQUARES IN THE IMAGE
    noOfSquares = len(nextSmallerFrame)

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





    # cv.imshow('i', goodImageB)
    # cv.imshow('j', goodImageN)
    #
    #
    #
    # cv.waitKey(0)
    # cv.destroyAllWindows()






a = Image("001", "car")
a.getImagesPath()
a.getFrameRange()
a.parser.getGTInformation()
print(detectSmallObj(a.loadFrame(1), a.loadFrame(2), a.loadFrame(3)))
