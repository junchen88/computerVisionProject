from assistClass import *

a = Image("001", "car")
a.getImagesPath()
a.getFrameRange()
a.parser.getGTInformation()
print(a.loadFrame(1))


def toThirtyByThirty(img):

    allSmallerImg = []
    for r in range(0,img.shape[0],30):
        for c in range(0,img.shape[1],30):
            allSmallerImg.append(img[r:r+30, c:c+30,:])

    return allSmallerImg

toThirtyByThirty(a.loadFrame(1))
