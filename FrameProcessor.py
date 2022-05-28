import numpy as np

class FrameProcessor:
    def __init__(self, frames, detector, tracker):
        self.frames = frames
        self.detector = detector
        self.tracker = tracker

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

        # Do candidate small objects detection
        candidates = self.detector.detectCandidates(prevFrame, currFrame, nextFrame)

        # Discriminate over candidate matches
        currGroundTruth = self.frames.getGroundTruth(self.frameIdx)
        boxes, centroids, precision, recall, F1, truePositive, falsePositive, falseNegative \
         = self.detector.discriminateCandidates(currFrame, candidates, currGroundTruth)

        if centroids:
            print("note: Found centroids:", centroids)

        self.listOfPrecision.append(precision)
        self.listOfRecall.append(recall)
        self.listOfF1.append(F1)
        self.listOfTruePositive.append(truePositive)
        self.listOfFalsePositive.append(falsePositive)
        self.listOfFalseNegative.append(falseNegative)
        
        centroids = np.asarray(centroids)
        
        # Now, update tracks
        self.tracker.update(centroids)
        self.frameIdx = self.frameIdx + 1

        return currFrame
