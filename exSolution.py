#Author : George Dozorets            Date: 23/7/2021
#                       Simulates fire of a machinegun from diffrent distances
#
#        Future Development:
#                           (1) Real time simulation of each shoot
#                           (2) 3d plot
#                           (3) Lowering the time and space complexity
#                           (4) Add propreties to the objects
############################################################################################
#this experiants simulats cannon which fires from variaty of distances (D)
#the experiment returns N times. for each number of burst calculates the AVG of hit to target
#target size could be changed by suited function, default size of 1 m^3
#distance steps by defulat 1 KM, if needed could be changed by suited fucntion
#to inital experiments write:
#exp = experiments(N,D,B) - defines parameters
#exp.runAllSimulates() - run the simulation
#exp.plotAllSimulates() - ploting all simulations by bursts length as function of AVG hits in target
#N - number of experiments for each distance and number of burst
#D - range for 1 kilomter to D kilometer
#B - Burst -Number of shots
#returns experiments object
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class experiments():
    def __init__(self,N,D,B):
        self.N = N
        self.D = D
        self.B = B
        self.targetSize = 1 #default value
        self.maxTargetX = self.targetSize * (0.5)
        self.minTargetX = self.targetSize *  (-0.5)
        self.maxTargetY = self.targetSize * (0.5)
        self.minTargetY = self.targetSize *  (-0.5)
        self.CError=0.1
        self.cons=1.177
        self.REror=0.2
        self.distanceStep = 1 #default step size of distance in KM
        self.expermientList = []
    
    #function to change target size
    #targetSize - by m^3
    def setTargetSize(self,targetSize):
        self.targetSize = targetSize
        self.maxTargetX = targetSize * (0.5)
        self.minTargetX = targetSize *  (-0.5)
        self.maxTargetY = targetSize * (0.5)
        self.minTargetY = targetSize *  (-0.5)
        
    def setCError(self,newError):
        self.CError = newError
        
    def setConstant(self,newConstant):
        self.cons = newConstant

    def setRandomError(self,newRandomError):
        self.DEror = newRandomError
            
    #function to rull simulates of the experiments
    def runAllSimulates(self):
        if(not len(self.expermientList)):
            self.expermientList = [experiment(self.N,i,self.B) for i in range(1,self.D+1,self.distanceStep)]
            for d in range(self.D):
                self.expermientList[d].aim()
                self.expermientList[d].fire()
                self.expermientList[d].calculateResults()
                
    #function to plot the resulats of the experiments  
    #experiemtns must run first
    
    def plotAllSimulates(self,saveFig=False):
        if(len(self.expermientList)):
            plt.figure(figsize=(10,7))
            colors = sns.color_palette("rocket", n_colors=self.D)
            for d in range(self.D):
                plt.scatter(range(self.B),self.expermientList[d].TotalMeanHitsPerBrust,label=str(d+1)+" KM",color=colors[d])
            
            plt.plot([0,self.B],[1,1],label='AVG hits = 1',color='blue')
            plt.legend()
            plt.xlabel("Brust length")
            plt.ylabel("AVG Number of hits")
            plt.title("N="+str(self.N)+" D="+str(self.D)+" B="+str(self.B))
            if(saveFig): plt.savefig('resualt1N{}.png'.format(self.N))
            plt.show()
        else:
            print("Run the experiments object first with runAllSimulates()")
            
    def plotAllSimulates2(self,saveFig=False):
        if(len(self.expermientList)):
            plt.figure(figsize=(10,7))
            colors = sns.color_palette("rocket", n_colors=self.B)
            for b in range(self.B):
                plt.plot(self.getAVGHitsPerBrustLength(b),range(1,self.D+1),label="Brust len: "+str(b+1),color=colors[b])
           
            plt.plot([1,1],[0,self.D],label='AVG hits = 1',color='blue')
            plt.legend()
            plt.xlabel("AVG number of hits")
            plt.ylabel("Kilometers")
            plt.title("N="+str(self.N)+" D="+str(self.D)+" B="+str(self.B))
            if(saveFig): plt.savefig('resualt2N{}.png'.format(self.N))
            plt.show()
        else:
            print("Run the experiments object first with runAllSimulates()")
    
    #method which return array of AVG hits per brust length
    #arr[i] means KM
    def getAVGHitsPerBrustLength(self,bl):
        tmpArr = []
        for k in range(self.D):
             tmpArr.append(self.expermientList[k].TotalMeanHitsPerBrust[bl])
        return tmpArr
    
    #method return min brust needed to hit target once from given km
    def getMinBrustForOneHit(self,km):
        for b in range(self.B):
            if(self.expermientList[km].TotalMeanHitsPerBrust[b]>=1):
                return b+1
            
    #method which return list of min burst needed for each of the km in range
    def getListOfMinBrustForOneHitByKm(self):
        tmpArr = []
        for k in range(self.D):
            if(self.getMinBrustForOneHit(k)):
                tmpArr.append(self.getMinBrustForOneHit(k))
            else:
                tmpArr.append(-1)
        return tmpArr
    
    #plost resulats of min brust length needed to hit target one from each of the km in range
    def plotAllSimulates3(self,saveFig=False):
        if(len(self.expermientList)):
            plt.figure(figsize=(10,7))
            colors = sns.color_palette("rocket", n_colors=self.D+2)
            colors = [colors[i+2] for i in self.getListOfMinBrustForOneHitByKm()]
            plt.scatter(range(1,self.D+1),self.getListOfMinBrustForOneHitByKm(),c=colors)
            plt.xlabel("Kilometers")
            plt.ylabel("Brust Length")
            plt.title("Min brust to hit target in AVG one time\n"+"N="+str(self.N)+" D="+str(self.D)+" B="+str(self.B)) 
            if(saveFig): plt.savefig('resualt3N{}.png'.format(self.N))
            plt.show()

# single experiment object            
# this object inhirates from experiments
# listOfBrusts - contains list of brusts by length
# TotalMeanHitsPerBrust - total mean hits per brusts group length
class experiment(experiments):
    def __init__(self,N,D,B):
        experiments.__init__(self,N,D,B)
        self.listOfBrusts = []
        self.TotalMeanHitsPerBrust = []
    
    #function which creates list of brusts
    #used in aim fucntion
    def createBrusts(self):
        if(not len(self.listOfBrusts)):
            self.listOfBrusts = [brusts(self.N,self.D,i+1) for i in range(self.B)]
    
    #function to aim the brusts
    #to determine common error x1,y1 values
    def aim(self):
        self.createBrusts()
        for i in range(self.B):
            self.listOfBrusts[i].createSingleLengthBrusts()
    
    #function to fire the brusts
    #determines random error x2,y2 values
    def fire(self):
        if(len(self.listOfBrusts)):
            for i in range(self.B):
                for j in range(self.N):
                    self.listOfBrusts[i].brustList[j].fireBrust()
        else:
            print("must aim first")
    
    #function to plot common error of all brusts
    def plotCommonErrorAllBrusts(self):
        if(len(self.listOfBrusts)):
            plt.figure(figsize=(10,7))
            colors = sns.color_palette("rocket", n_colors=self.B)
            for i in range(self.B):
                self.listOfBrusts[i].calBrustsCECor()
                plt.scatter(self.listOfBrusts[i].BrustCEcorX,self.listOfBrusts[i].BrustCEcorY,marker='+',label="brust of "+str(self.listOfBrusts[i].B),color=colors[i])
            plt.legend()
            plt.title("Common error by brusts ,Distance = "+str(self.D)+" KM")
            plt.scatter(0,0,s=2000,marker='+',color='blue')
        else:
            print("must aim and fire first")            
    #function to plot all shots 
    def plotAllShots(self,CEFlag=True):
        if(len(self.listOfBrusts)):
            plt.figure(figsize=(15,15))
            colors = sns.color_palette("rocket", n_colors=self.B)
            #target borders
            plt.plot([self.minTargetX,self.minTargetX],[self.minTargetY,self.maxTargetY],color='blue') #left
            plt.plot([self.minTargetX,self.maxTargetX],[self.maxTargetY,self.maxTargetY],color='blue') #up
            plt.plot([self.maxTargetX,self.maxTargetX],[self.minTargetY,self.maxTargetY],color='blue') #right
            plt.plot([self.minTargetX,self.maxTargetX],[self.minTargetY,self.minTargetY],color='blue') #down
            for i in range(self.B):
                self.listOfBrusts[i].calBrustsCECor()
                if(CEFlag):
                    plt.scatter(self.listOfBrusts[i].BrustCEcorX,self.listOfBrusts[i].BrustCEcorY,s=100,marker='+',label="burst of "+str(self.listOfBrusts[i].B),color=colors[i])
                for j in range(self.N):
                    self.listOfBrusts[i].brustList[j].calShootsCor()
                    plt.scatter(self.listOfBrusts[i].brustList[j].ShotsX,self.listOfBrusts[i].brustList[j].ShotsY,s=10,alpha=0.1,color=colors[i])
            if(CEFlag):
                plt.legend()
            plt.title("All shoots distribution by brusts ,Distance = "+str(self.D)+" KM")
            plt.scatter(0,0,s=2000,marker='+',color='blue')
        else:
            print("must aim and fire first")

    #function which calculates the resualts of the expirement
    #stors them into list 'TotalMeanHitsPerBrust'
    def calculateResults(self):
        if(not len(self.TotalMeanHitsPerBrust)):
            for i in range(self.B):
                self.listOfBrusts[i].calBrusMeanNumberOfHits()
                self.TotalMeanHitsPerBrust.append(self.listOfBrusts[i].BrustMeanNumberOfHits)
    
    #function to basic plot the resualts
    def plotResults(self):
        if(len(self.listOfBrusts)):
            self.calculateResults()
            plt.figure(figsize=(10,7))
            plt.plot(range(self.B),self.TotalMeanHitsPerBrust)
            plt.xlabel("Brust length")
            plt.ylabel("AVG Number of hits")
            plt.title("N="+str(self.N)+" D="+str(self.D)+" B="+str(self.B))  
        else:
            print("must aim and fire first")
                
#this class inheritets from experiemnts
#creates a list of bursts and stores mean number of hits for each one
#brustList -  list of bursts
#BrustMeanNumberOfHits - mean number of hits per group of brusts
class brusts(experiment):
    def __init__(self,N,D,B):
        experiment.__init__(self,N,D,B)
        self.brustList = []
        self.BrustMeanNumberOfHits = 0
        
    #function that creates a single length brusts
    def createSingleLengthBrusts(self):
        if(not len(self.brustList)):
            self.brustList = [brust(i,self.D,self.B) for i in range(self.N)]

    #function which calculates burst mean number of hits
    def calBrusMeanNumberOfHits(self):
        if(not self.BrustMeanNumberOfHits):
            tmpSum = 0
            for j in range(self.N):
                self.brustList[j].calInTargetShoots()
                tmpSum += self.brustList[j].inTargetShoots
            self.BrustMeanNumberOfHits = tmpSum/self.N
            
    #function which prints bursts and thire x1 y1 (common error cordinates)
    def printBrustsCor(self):
        for j in range(self.N):
            print("N: "+str(self.N)+" burstLength: "+str(self.B)+" x1: "+str(self.brustList[j].x1)+" y1: "+str(self.brustList[j].y1))
    
    #function which creates brust common error list in x and y axis
    #stores it at BrustCEcorX/Y list
    def calBrustsCECor(self):
        self.BrustCEcorX = []
        self.BrustCEcorY = []
        for j in range(self.N):
            self.BrustCEcorX.append(self.brustList[j].x1)
            self.BrustCEcorY.append(self.brustList[j].y1)
        
    #function which plots single brust common error cordinates
    def plotBrustCor(self):
        plt.figure(figsize=(10,7))
        self.calBrustsCECor()
        plt.scatter(self.BrustCEcorX,self.BrustCEcorY,marker='+')
        plt.scatter(0,0,s=2000,marker='+',color='blue')
        
#this class inhiratets from bursts
#x1,y1 - sotres x1,y1 cordiantes of the common eror of the burst
#inTargetShoots - stores shoots in traget counter
class brust(brusts):
    def __init__(self,N,D,B):
        brusts.__init__(self,N,D,B)
        self.x1 = np.random.normal(0,(self.CError * self.D)/self.cons)
        self.y1 = np.random.normal(0,(self.CError * self.D)/self.cons)
        self.ListOfShoots = []
        self.inTargetShoots = 0 
    
    #function to fire a brust
    #ListOfShoots - stores list of shoots - bullet objects
    def fireBrust(self):
        if(not len(self.ListOfShoots)):
            self.ListOfShoots = [bullet(self.N,self.D,i) for i in range(self.B)]
            
    #function to counts number of bullets hit the target 
    def calInTargetShoots(self):
        if(not self.inTargetShoots):
            for k in range(self.B):
                if(self.ListOfShoots[k].inTarget):
                    self.inTargetShoots+=1
    
    #function to calculate the exact cordiantes of each bullet
    def calShootsCor(self):
        self.ShotsX = []
        self.ShotsY = []
        for k in range(self.B):
            self.ShotsX.append(self.ListOfShoots[k].x2)
            self.ShotsY.append(self.ListOfShoots[k].y2)
        
    #function to plot single brust shoots
    def plotShots(self):
        plt.figure(figsize=(10,7))
        plt.scatter(self.x1,self.y1,s=500,marker='+')
        self.calShootsCor()
        plt.scatter(self.ShotsX,self.ShotsY)
        plt.title("Distance = "+str(self.D)+" KM")
        plt.scatter(0,0,s=2000,marker='+',color='blue')
        
#this class inhiratets from burst
#one object created (x2,y2) cordiantes calculates out of brust common error cordinates (x1,y1)
#x2 - x cordiante of the hit
#y2 - y cordiante of the hit
#inTarget - boolean, True if in targer range
class bullet(brust):
    def __init__(self,N,D,B):
        brust.__init__(self,N,D,B)
        self.x2 = np.random.normal(self.x1,(self.REror * self.D)/self.cons)
        self.y2 = np.random.normal(self.y1,(self.REror * self.D)/self.cons)
        self.inTarget = (self.x2<=self.maxTargetX and self.x2>=self.minTargetX and self.y2<=self.maxTargetY and self.y2>=self.minTargetY)        


# Initate Experiments

#exp = experiments(10000,10,10)
#exp.runAllSimulates()
#exp.plotAllSimulates(saveFig=True)
#exp.plotAllSimulates2(saveFig=True)
#exp.plotAllSimulates3(saveFig=True)

