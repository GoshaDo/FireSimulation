#Author : George Dozorets            Date: 23/7/2021
#                       Simulates fire of a machinegun from diffrent distances
#                                   Basic non-objects algorithm
############################################################################################

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#this function calculates (x,y) coordinates of common error
#by normal distribution with mu=0, std=CPE/c(constant value of 1.77)
# CEror common eror defualt value of 0.1 mili-radiant
# N number of experiments
# D distance in Kilometers
# retunrs (x,y) coordinates of the common eror
def randCommonError(D,CEror=0.1,c=1.177):
    x1 = np.random.normal(0,(CEror * D)/c)
    y1 = np.random.normal(0,(CEror * D)/c)
    return x1,y1

#this function calculates (x,y) coordinates of single bullte
#by normal distribution with mu=0, std=CPE/c(constant value of 1.77)
#REror random error defualt value of 0.2 mili-radiant
#x1 x value of mu random common error
#y1 y value of mu random common error
#D - distance to traget in kilometers
#returns (x,y) coordinates of a single shot 
def randRandomError(x1,y1,D,REror=0.2,c=1.177):
    x2 = np.random.normal(x1,(REror * D)/c)
    y2 = np.random.normal(y1,(REror * D)/c)
    return x2,y2

#functions which inital the expiremnts
#this experiants simulats fires range of B bullters, in variate of distances in step size of 1 km
#this experiment returns N times. for each number of burst calculates the AVG times of hit to target
#target size could be changed inside of the function by need, default size of 1 m^3
#N - number of experiments for each distance and number of burst
#D - range for 1 kilomter to D kilometer
#B - Burst -Number of shots
#targerSize - size of the traget in m^3
#DistanceSteps - steps on distance iteration in KM, default value 1 KM steps
# returns plot of burst length as function of AVG number of hits (in target)
def initialExperiment(N, D, B, targetSize = 1, DistanceSteps = 1):
    plt.figure(figsize=(10,7))
    #change the target size here
    maxX = targetSize * (0.5)
    minX = targetSize *  (-0.5)
    maxY = targetSize * (0.5)
    minY = targetSize *  (-0.5)
    
    colors = sns.color_palette("rocket", n_colors=D)
    for D in range (1,D+1,DistanceSteps): #distance in kilometers 
        c = colors[len(colors)-D]
        meanHits = []
        for B in range(1,B+1):
            hitInTarget = 0
            for N in range(1,N+1):
                x1,y1 = randCommonError(D)
                for bullet in range(B):
                    x2,y2 = randRandomError(x1,y1,D)
                    if (x2<=maxX and x2>=minX and y2<=maxY and y2>=minY):
                        hitInTarget+=1
            meanHits.append(hitInTarget/N)        
        plt.plot(range(B),meanHits, label=str(D)+" KM",color=c)
    plt.legend()
    plt.xlabel("Brust length")
    plt.ylabel("AVG Number of hits")
    plt.title("N="+str(N)+" D="+str(D)+" B="+str(B))
    plt.show()
    
def initialExperiment2(N, D, B, targetSize = 1, DistanceSteps = 1):

        
    f, ([ax1, ax2]) = plt.subplots(1, 2, figsize=(15,8))
    #change the target size here
    maxX = targetSize * (0.5)
    minX = targetSize *  (-0.5)
    maxY = targetSize * (0.5)
    minY = targetSize *  (-0.5)
    
    colors = sns.color_palette("rocket", n_colors=D)
    for D in range (1,D+1,DistanceSteps): #distance in kilometers 
        c = colors[len(colors)-D]
        meanHits = []
        hitsCorX = []
        hitsCorY = []
        CEx=[]
        CEy=[]
        for B in range(1,B+1):
            hitInTarget = 0
            for N in range(1,N+1):
                x1,y1 = randCommonError(D)
                CEx.append(x1)
                CEy.append(y1)
                
                for bullet in range(B):
                    x2,y2 = randRandomError(x1,y1,D)
                    hitsCorX.append(x2)
                    hitsCorY.append(y2)
                    if (x2<=maxX and x2>=minX and y2<=maxY and y2>=minY):
                        hitInTarget+=1
            meanHits.append(hitInTarget/N)        
        ax1.plot(range(B),meanHits, label=str(D)+" KM",color=c)
        ax2.scatter(CEx,CEy,marker='+',color=c)
        ax2.scatter(hitsCorX,hitsCorY,color=c,alpha=0.1,edgecolors='face')
    ax2.scatter(0,0,s=2000,marker='+',color='blue')
    ax1.legend()
    ax1.set_xlabel("Brust length")
    ax1.set_ylabel("AVG Number of hits")
    ax1.set_title("N="+str(N)+" D="+str(D)+" B="+str(B))
    plt.show()
