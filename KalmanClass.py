
import numpy as np






class Kalman():


    def __init__(self, centroid, STDPOSITION, STDVELOCITY, STDACCELERATION, STDMOVINGOBJ):

        self.Fk = np.array([[1,0,1,0,1/2,0],[0,1,0,1,0,1/2],[0,0,1,0,1,0],[0,0,0,1,0,1],[0,0,0,0,1,0],[0,0,0,0,0,1]])
        self.Hk = np.array([[1,0,0,0,0,0],[0,1,0,0,0,0]])

        self.Qk = np.diag((STDPOSITION**2, STDPOSITION**2, STDVELOCITY**2, STDVELOCITY**2, STDACCELERATION**2, STDACCELERATION**2))
        self.Rk = np.array([[STDMOVINGOBJ**2,0], [0, STDMOVINGOBJ**2]])

        self.stateVector = np.array([centroid[0], centroid[1], 0, 0, 0, 0])
        self.Pk = self.Qk



    #KALMAN PREDICT STEP
    def predict(self):

        Fk = self.Fk
        Pk = self.Pk
        stateVector = self.stateVector
        FkTranspose = np.transpose(Fk)
        predictedStateVector = np.matmul(Fk, stateVector)
        predictedPk = np.matmul(Fk, np.matmul(Pk, FkTranspose)) + self.Qk
        self.stateVector = predictedStateVector
        self.Pk = predictedPk

    #KALMAN UPDATE STEP
    def update(self, centroid):
        Hk          = self.Hk
        stateVector = self.stateVector
        Pk          = self.Pk
        HkTranspose = np.transpose(Hk)
        Rk          = self.Rk


        Yk          = centroid - np.matmul(Hk, stateVector)
        Sk          = np.matmul(Hk, np.matmul(Pk,HkTransose)) + Rk

        SkInverse   = np.linalg.inv(Sk)
        Kk          = np.matmul(Pk, np.matmul(HkTranspose, SkInverse))

        upDateState = stateVector + np.matmul(Kk, Yk)

        #SHOULD BE THE SAME SIZE AS PK
        identityMat = np.identity(6)
        upDatePk    = np.matmul((I - np.matmul(Kk, Hk)), Pk)

        self.stateVector = upDateState
        self.Pk = upDatePk

        centroidUpdated = np.array([upDateState[0], upDateState[1]])
        return centroidUpdated


# K = Kalman()
#
# print(K.Qk)
