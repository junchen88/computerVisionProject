from small_object_detection import *
import scipy

STDPOSITION = 0 #TODO CHANGE THIS VALUE (PAGE 8: DECIDE OUR OWN VALUES)
STDVELOCITY = 0
STDACCELERATION = 0
STDMOVINGOBJ = 0

Fk = np.array([[1,0,1,0,1/2,0],[0,1,0,1,0,1/2],[0,0,1,0,1,0],[0,0,0,1,0,1],[0,0,0,0,1,0],[0,0,0,0,0,1]])

Hk = np.array([1,0,0,0,0,0],[0,1,0,0,0,0])

Qk = np.zeros((6,6))
Qk[0][0] = STDPOSITION**2
Qk[1][1] = STDPOSITION**2
Qk[2][2] = STDVELOCITY**2
Qk[3][3] = STDVELOCITY**2
Qk[4][4] = STDACCELERATION**2
Qk[5][5] = STDACCELERATION**2

Rk = np.array([[STDMOVINGOBJ**2,0], [0, STDMOVINGOBJ**2]])


#TAKES A LIST OF CLUSTER OF EACH FRAME
#ASSUME EACH CLUSTER CONTAIN CENTROID INFORMATION IN [1]
#RETURNS STATEVECTOR AND PK FOR THE LIST OF CLUSTER
def initKalman(listOfClusters):


    listOfObj = np.empty((len(listOfClusters), 2)))

    for i, cluster in listOfClusters:
        #[x,y,vx,vy,ax,ay] x & y = centroid, v and a = velocity and acceleration
        centroid = cluster[1]
        x = centroid[0]
        y = centroid[1]
        stateVector = [x, y, 0, 0, 0, 0]
        Pk = Qk

        listOfObj[i][0] = stateVector
        listOfObj[i][1] = Pk


    return newListOfObj



def predictionKalman(trackedObj):
    for i, obj in enumerate(trackedObj)
        stateVector = obj[0]
        Pk = obj[1]
        predictedStateVector = np.matmul(Fk,stateVector) #USES PRIORI STATE VECTOR
        transposeFk = np.transpose(Fk)
        predictedPk = np.matmul(np.matmul(Fk,Pk), transposeFk) + Qk


def hypothesisKalman():
    scipy.optimize.linear_sum_assignment()


def localSearchAlgo():
