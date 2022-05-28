import math
import numpy as np
from scipy.stats import norm
from skimage import color, measure

# Helper function: Divide an skimage into 30x30 pixel tiles
def toThirtyByThirty(img):
    imgHeight, imgWidth, _ = img.shape
    imgParts = []

    # Note: Currently ignores remainder pixels
    for r in range(0, imgHeight, 30):
        if r > imgHeight - 30:
            break
        for c in range(0, imgWidth, 30):
            if c > imgWidth - 30:
                break

            imgParts.append(img[r:r+30, c:c+30, :])

    return imgParts

# Helper function: Calculate absolute difference of two images
def differenceImage(img1, img2):
    return np.absolute(img1 - img2)

# Helper function: Convert skimage RGB888 to [0, 255] range grayscale
def rgb2gray(img):
    return color.rgb2gray(img) * 255

# Compute match quality between two boxes using intersection-over-union
def boxIntersectionOverUnion(box1, box2):
    # Find the coordinates of the intersection
    # X, Y = TOP LEFT, XE, YE = BOTTOM RIGHT
    x = max(box1[0], box2[0])
    y = max(box1[1], box2[1])
    xE = min(box1[2], box2[2])
    yE = min(box1[3], box2[3])

    # Find the area of intersection
    intersectArea = max(0, xE - x + 1) * max(0, yE - y + 1)

    # Find the area of both the predicted and true boxes
    box1Area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2Area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # Compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    IOU = intersectArea / float(box1Area + box2Area - intersectArea)

    return IOU

# truePositive    =   PROPOSED MATCHING WITH TRUTH
# falsePositive   =   PROPOSED WITHOUT MATCHING
# falseNegative   =   TRUTH WITHOUT MATCHING
def gt_evaluation(bbox, groundTruth, matchedTruth):
    for i, trueObj in enumerate(groundTruth):
        topLeftX = int(trueObj[1])
        topLeftY = int(trueObj[2])
        width = int(trueObj[3])
        height = int(trueObj[4])

        trueBox = (topLeftX, topLeftY, topLeftX+width, topLeftY+height)
        IOU = boxIntersectionOverUnion(trueBox, bbox)

        if IOU > 0.7:
            matchedTruth[i] = True
            return True

    # No matches found for this proposed region
    return False

class ObjectDetector():
    def __init__(self, areaLowerBound, areaUpperBound, \
            extentLowerBound, extentUpperBound, \
            majorLowerBound, majorUpperBound, \
            eccentricLowerBound, eccentricUpperBound):
        # Save morphological cue bounds for later processing
        self.areaLowerBound = areaLowerBound
        self.areaUpperBound = areaUpperBound
        self.extentLowerBound = extentLowerBound
        self.extentUpperBound = extentUpperBound
        self.majorLowerBound = majorLowerBound
        self.majorUpperBound = majorUpperBound
        self.eccentricLowerBound = eccentricLowerBound
        self.eccentricUpperBound = eccentricUpperBound

    # Perform three-way candidate small object detection
    def detectCandidates(self, prevFrame, currFrame, nextFrame):
        imgHeight, imgWidth, _ = currFrame.shape

        # Precalculate 5% thresholding coefficient
        neg_ln_p = -math.log(0.05)

        # Split frames into 30x30 squares
        prevFrameParts = toThirtyByThirty(prevFrame)
        currFrameParts = toThirtyByThirty(currFrame)
        nextFrameParts = toThirtyByThirty(nextFrame)

        # Result arrays for thresholding output
        goodImageB = np.zeros((imgHeight, imgWidth))
        goodImageN = np.zeros((imgHeight, imgWidth))

        for i in range(len(currFrameParts)):
            prevGray = rgb2gray(prevFrameParts[i])
            currGray = rgb2gray(currFrameParts[i])
            nextGray = rgb2gray(nextFrameParts[i])

            # Calculate average difference for thresholding
            diffBefore = differenceImage(prevGray, currGray)
            diffNext = differenceImage(currGray, nextGray)
            avgBefore = diffBefore.sum() / 900
            avgNext = diffNext.sum() / 900

            threshBefore = neg_ln_p * avgBefore
            threshNext = neg_ln_p * avgNext

            # Precalculate real x, y coordinate of corner of each 30x30 tile
            cornerX = (i % (imgWidth // 30)) * 30
            cornerY = (i // (imgWidth // 30)) * 30

            # Map all pixels in 30x30 tile to final places in threshold binary image
            for y in range(30):
                for x in range(30):
                    if diffBefore[y, x] > threshBefore:
                        goodImageB[cornerY + y, cornerX + x] = 1
                    else:
                        goodImageB[cornerY + y, cornerX + x] = 0

                    if diffNext[y, x] > threshNext:
                        goodImageN[cornerY + y, cornerX + x] = 1
                    else:
                        goodImageN[cornerY + y, cornerX + x] = 0

        # Do candidate extraction and return extracted results
        afterLogicalAnd = np.logical_and(goodImageB, goodImageN)
        afterLogicalAnd = afterLogicalAnd.astype(np.uint8) * 255

        return afterLogicalAnd

    # Perform candidate match discrimination
    def discriminateCandidates(self, currFrame, candidates, groundTruth):
        imgHeight, imgWidth, _ = currFrame.shape
        currGray = rgb2gray(currFrame)

        # Calculate clustering information for region growing
        labelMap, numClusters = measure.label(candidates, return_num=True)
        regions = measure.regionprops(labelMap, intensity_image=currGray)

        # Result arrays for bounding boxes and centroids
        boxes = []
        centroids = []

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
        matchedTruth = np.full(shape=(len(groundTruth)), fill_value=False)
#_____________________________________________________________

        for region in regions:
            ## REGION GROWING

            # Construct the 11x11 box around the centroid of the candidate region
            cX = int(region.centroid[0])
            cY = int(region.centroid[1])
            cYMin = cY - 5
            cYMax = cY + 6
            cXMin = cX - 5
            cXMax = cX + 6

            # Only if region is wholly within the image
            if cX < 5 or cX > imgWidth - 6 or cY < 5 or cY > imgHeight - 6:
                continue

            boxValues = currGray[cXMin:cXMax, cYMin:cYMax]

            # Sum the value of all pixels in the region
            valueSum = 0
            regionValues = np.zeros(len(region.coords))
            for i, coord in enumerate(region.coords):
                value = currGray[coord[0], coord[1]]
                regionValues[i] = value
                valueSum += value

            # Mean and std deviation of region values
            regionMean = valueSum / region.area
            regionStd = np.std(regionValues)

            # Avoid single pixel clusters
            if len(region.coords) == 1:
                continue

            # Determine [0.5%, 99.5%] value bounds
            ppf = norm.ppf(0.9975)
            upperBound = regionMean + ppf * regionStd
            lowerBound = regionMean - ppf * regionStd

            # Update the candidates in the region box to include threshold matches
            newBoxCandidates = np.logical_and(boxValues >= lowerBound, boxValues <= upperBound)
            allBoxCandidates = np.logical_or(candidates[cXMin:cXMax, cYMin:cYMax], newBoxCandidates)
            candidates[cXMin:cXMax, cYMin:cYMax] = allBoxCandidates.astype(np.uint8) * 255

            ## MORPHOLOGICAL CUES

            # Re-run cluster detection on the new 11x11 box to get the properties of the new, grown cluster
            boxLabelMap, targetNumClusters = measure.label(allBoxCandidates, return_num=True)
            boxRegions = measure.regionprops(boxLabelMap, intensity_image=currGray[cXMin:cXMax, cYMin:cYMax])

            # Find the label of the centre element (the cluster we wanted)
            wantedLabel = boxLabelMap[5][5] - 1
            targetCluster = boxRegions[wantedLabel]
            targetBoundBox = (int(targetCluster.bbox[0] + cXMin), int(targetCluster.bbox[1] + cYMin), int(targetCluster.bbox[2] + cXMin), int(targetCluster.bbox[3] + cYMin))
            targetCentroid = (int(targetCluster.centroid[0] + cXMin), int(targetCluster.centroid[1] + cYMin))
            
            # Gather morphological data
            targetArea = targetCluster.area
            targetExtent = targetCluster.area / (targetCluster.bbox[0] * targetCluster.bbox[1])
            
            # Calculate eigenvalues for ellipse fitting
            # First, get a matrix of all pixel coordinates
            N = len(targetCluster.coords)
            C = np.zeros(shape=(2, N))
            sumX = 0
            sumY = 0

            for i, coord in enumerate(targetCluster.coords):
                C[0, i] = coord[1] # x
                C[1, i] = coord[0] # y

                sumX += coord[1]
                sumY += coord[0]

            avgX = sumX / N
            avgY = sumY / N
            for i in range(N):
                C[0, i] -= avgX
                C[1, i] -= avgY

            sigma_cc = np.dot(C, np.transpose(C)) / (N - 1)
            lambda_eig, _ = np.linalg.eig(sigma_cc)

            targetMajor = max(math.sqrt(lambda_eig[0]), math.sqrt(lambda_eig[1]))
            targetMinor = min(math.sqrt(lambda_eig[0]), math.sqrt(lambda_eig[1]))
            targetEccentric = math.sqrt(1 - targetMinor/targetMajor)
            
            # Reject any non-matches
            if targetArea < self.areaLowerBound or targetArea > self.areaUpperBound:
                break
            if targetExtent < self.extentLowerBound or targetExtent > self.extentUpperBound:
                break
            if targetMajor < self.majorLowerBound or targetMajor > self.majorUpperBound:
                break
            if targetEccentric < self.eccentricLowerBound or targetEccentric > self.eccentricUpperBound:
                break
            
            # Evaluate region for accuracy against ground truth
            matchingFound = gt_evaluation(targetBoundBox, groundTruth, matchedTruth)
            
            # Append only if matching is found
            if matchingFound:
                boxes.append(targetBoundBox)
                centroids.append(targetCentroid)
                truePositive += 1
            else:
                falsePositive += 1

        #TO FIND THE NUMBER OF FALSE: EG TRUTHOBJ NOT ASSIGN
        falseNegative = np.size(matchedTruth) - np.count_nonzero(matchedTruth)

        if truePositive + falsePositive == 0:
            precision = 0
        else:
            precision = truePositive / (truePositive + falsePositive)
        recall = truePositive / (truePositive + falseNegative)
        if truePositive == 0:
            F1 = math.inf
        else:
            F1 = 2 * (precision * recall) / (precision + recall)
        
        if len(centroids) == 0:
            print('note: No matching found in detection step')

        return boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative
