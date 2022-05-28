import numpy as np

from detectClass import Detector

class FrameProcessor:
    def __init__(self, frames, tracker, cueLowerBound, cueUpperBound, gtInform):
        self.frames = frames
        self.tracker = tracker

        self.cueLowerBound = cueLowerBound
        self.cueUpperBound = cueUpperBound
        self.gtInform = gtInform

        # Start at one-past-the-start of the frame range
        self.frameIdx = frames.getFirstIdx() + 1

        #TO STORE ALL THE VALUES FOR PRINTING CHART, EACH ELEMENT = FOR EACH FRAME
        self.listOfPrecision = []
        self.listOfRecall = []
        self.listOfF1 = []
        self.listOfTruePositive = []
        self.listOfFalsePositive = []
        self.listOfFalseNegative = []

    def processNextFrame(self):
        # If we're at the last frame, there's nothing more to do
        # because we stop at one-before-the-end
        if self.frames.isLastIdx(self.frameIdx):
            print("info: Finished!")
            return

        print("info: Working on frame {} to frame {}...".format(self.frameIdx - 1, self.frameIdx + 1))

        prevFrame = self.frames.load(self.frameIdx - 1)
        currFrame = self.frames.load(self.frameIdx)
        nextFrame = self.frames.load(self.frameIdx + 1)

        detector = Detector(prevFrame, currFrame, nextFrame, self.cueLowerBound, self.cueUpperBound, self.gtInform, self.frameIdx)

        #BOXES = BOUNDING BOXES, CENTROIDS = LIST OF CENTROIDS,(FOR KALMAN) PRECISION RECALL AND F1 IS DATA FOR CHART
        boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative = detector.detectObjAndDiscrim()
        # test
        print(centroids)

        self.listOfPrecision.append(precision)
        self.listOfRecall.append(recall)
        self.listOfF1.append(F1)
        self.listOfTruePositive.append(truePositive)
        self.listOfFalsePositive.append(falsePositive)
        self.listOfFalseNegative.append(falseNegative)

        centroids = np.asarray(centroids)

        #UPDATE/ADD/DELETE TRACKS
        self.tracker.update(centroids)

        # For later access, save aside current frame data
        self.thisFrame = currFrame
        self.frameIdx = self.frameIdx + 1
