import numpy as np
from KalmanClass import Kalman
from scipy.optimize import linear_sum_assignment
import math



class Track():
    """ Track Class for each Obj"""

    def __init__(self, newTrackID, centroid, positionSTD, velocitySTD, accelerationSTD, movingObjSTD):


        self.trackID = newTrackID
        self.Kalman = Kalman(centroid, positionSTD, velocitySTD, accelerationSTD, movingObjSTD)
        self.predictedCentroid = np.asarray(centroid)
        self.noOfFramesUndetected = 0


#FOR TRACKING
class Tracker():

    """ Tracker class that stores and update each track obj """

    def __init__(self, trackIDStart, positionSTD, velocitySTD, accelerationSTD, movingObjSTD):

        self.tracks = []
        self.trackIdCount = trackIDStart

        #COST OF ASSIGNING TRACK TO PSEUDO HYPOTHESIS AND HYPOTHESIS TO PSEUDO TRACK
        self.assigningCost = 10

        self.positionSTD = positionSTD
        self.velocitySTD = velocitySTD
        self.accelerationSTD = accelerationSTD
        self.movingObjSTD = movingObjSTD

    def update(self, detectedCentroids):

        positionSTD = self.positionSTD
        velocitySTD = self.velocitySTD
        accelerationSTD = self.accelerationSTD
        movingObjSTD = self.movingObjSTD

        # If track list is empty, then add all CENTROIDS/CLUSTERS
        # (since they will all be new as there are no trackings)
        if (self.tracks):
            for i in range(len(detectedCentroids)):
                #ASSIGN NEW ID AND INCREMENT IT
                track = Track(self.trackIdCount, detectedCentroids[i], positionSTD, velocitySTD, accelerationSTD, movingObjSTD)
                self.trackIdCount += 1
                self.tracks.append(track)

        #INITIALISE COST MATRIX
        noOfTracks = len(self.tracks)
        noOfDetections = len(detectedCentroids)

        #COST OF ASSIGNING TRACK TO PSEUDO HYPOTHESIS AND HYPOTHESIS TO PSEUDO TRACK
        #An unassigned detection may become the start of a new track.
        #If a track is unassigned, the object does not appear.
        assigningCost = self.assigningCost


        cost = np.zeros((noOfTracks+noOfDetections, noOfDetections+noOfTracks))

        sizeOfCost = noOfTracks+noOfDetections

        #TO CREATE THE COST MATRIX
        #TO FIND THE EUCLIDEAN DIST BETWEEN PREDICTED AND DETECTED CENTROID
        #EG THE COST OF ASSIGNING A DETECTION TO A TRACK
        for row in range(sizeOfCost):
            for col in range(sizeOfCost):

                if row < noOfTracks:
                    #WITHIN COST MATRIX AREA
                    if col < noOfDetections:

                        #GOT THE CHANGE IN X & Y & CALCULATE EUCLIDEAN DIST
                        diff = self.tracks[row].predictedCentroid - detectedCentroids[col]
                        dist = math.sqrt(diff[0]**2 + diff[1]**2)
                        cost[row][col] = dist

                    #WITHIN UNASSIGNED TRACK MATRIX AREA
                    #SEE https://au.mathworks.com/help/vision/ref/assigndetectionstotracks.html
                    #FOR THE EXPECTED MATRIX
                    else:
                        #TO MAKE THE UNASSIGNED COST DIAGONAL ON THE RIGHT OF THE COSTMATRIX
                        if col - noOfDetections == row:
                            cost[row][col] = assigningCost


                else:
                    #TO MAKE THE UNASSIGNED COST DIAGONAL ON THE BELOW THE COSTMATRIX
                    if row - noOfTracks == col:
                        cost[row][col] = assigningCost


        #RETURNS SORTED ROW NUMBER, WITH THE CORRESPONDING COL NUMBER THAT LEADS TO THE
        #OPTIMAL VALUE
        #ONE TRACK SHOULD ASSIGNED TO ONE DETECTION
        row_ind, col_ind = linear_sum_assignment(cost)


        #TO RECORD TRACKS OR DETECTION WITH DUMMY AND ASSIGNMENTS
        tracksWithDummyDetect = []
        detectsWithDummyTrack = []
        assignments = []


        #GO THROUGH ROW, SINCE IT IS SORTED, THEN WE ARE SAFE TO JUST USE THE I INDEX
        for i in range(len(row_ind)):

            if i < noOfTracks:

                #IF COL INDEX IS >= THAN THE NUMBER OF DETECTIONS = DUMMY
                #AND APPEND TO CORRESPONDING LIST
                if col_ind[i] >= noOfDetections:

                    #UNASSIGNED TRACKS (ROWS = TRACK) + RECORD THE NO OF FRAME
                    #UNDETECTED
                    tracksWithDummyDetect.append(i)

                #WITHIN COST MATRIX (NOT DUMMY)
                else:
                    rowAndCol = [i, col_ind[i]]
                    assignments.append(rowAndCol)

            else:
                if col_ind[i] < noOfDetections:

                    #UNASSIGNED DETECTION (COL = DETECTION)
                    rowAndCol = [col_ind[i]]
                    detectsWithDummyTrack.append(rowAndCol)

        #TODO: SHOULD SEARCH FOR UNDETECTED USING A ALGO, DISCARD IF NOT FOUND
        #THIS METHOD JUST DISCARD THE TRACK WASN'T ASSIGNED TO A DETECTION
        for i in range(len(tracksWithDummyDetect)):
            trackIndex = tracksWithDummyDetect[i]
            trackID = self.tracks[trackIndex].trackID
            for j, track in enumerate(self.tracks):
                if track.trackID == trackID:
                    del self.tracks[j]


        #START NEW TRACKS IF THERE IS UNASSIGNED DETECTION
        for j in range(len(detectsWithDummyTrack)):

            detectedCentroids = np.array(detectedCentroids[j])
            track = Track(self.trackIdCount, detectedCentroids, positionSTD, velocitySTD, accelerationSTD, movingObjSTD)
            self.tracks.append(track)
            self.trackIdCount += 1


        #FOR EACH ASSIGNMENT (LINKED TRACK AND DETECTION) - ASSIGNMENT CONTAINS THE COL = DETECTION INDEX
        for i in range(len(assignments)):

            self.tracks[i].Kalman.predict()

            # self.tracks[i].skipped_frames = 0

            self.tracks[i].predictedCentroid = self.tracks[i].Kalman.update(detectedCentroids[assignments[i]])

        print('done')
