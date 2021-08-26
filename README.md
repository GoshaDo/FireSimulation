# Accuracy of weapon stand 
A simulation of fire stand using monte-carlo to determine burst length needed to hit target one time in dffrent ranges by vizulize results of simulation.
This simulation written in OOP using python for farther reserech

# Method
Using a statistical model and mote-carlo simulation given 2 types of error as shown in image added.
Each error have bi-normal distribution, error massured in Circular Error Probable [mili-radians] (CER) 

![alt text](https://github.com/GoshaDo/FireSimulation/blob/main/ErrorsPlot.png?raw=true "Erros plot")

# Algorithm
Object based model, for each distance preformining a batch of diffrent experiments. For each burst length in experiment calculating N times 
common error coordinates (x1,y1). For each burst(x1,y1), simulates by ‘monte carlo’ fire
of the bullets (x2,y2) coordinates. 

![alt text](https://github.com/GoshaDo/FireSimulation/blob/main/AlgorithmFlowChart.png?raw=true "Algorithm flow")

# Class diagram
![alt text](https://github.com/GoshaDo/FireSimulation/blob/main/ClassDiagram.png? | width=100)

