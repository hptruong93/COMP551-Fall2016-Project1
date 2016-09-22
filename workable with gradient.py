import pandas as pd
import numpy as np
import csv

data = pd.read_csv("newData.csv", sep=',')

#Read values from the csv file and get useful column values with corresponding title
genderframe = data['gender'].values
ageframe = data['age'].values
marathonTimeframe = data['marathonTime'].values
marathonTimeAgedframe = data['marathonTimeAged'].values
timeSqrframe=data['timeSqr'].values


#Convert and store values into arrays for later manupulation
gender = np.array(genderframe)[np.newaxis].T
age = np.array(ageframe)[np.newaxis].T
marathonTime = np.array(marathonTimeframe)[np.newaxis].T
marathonTimeAged = np.array(marathonTimeAgedframe)[np.newaxis].T
timeSqr = np.array(timeSqrframe)[np.newaxis].T
experience = np.copy(marathonTime)
ones = np.copy(marathonTime)

#Modify the values of certain arrays
#When the person has 0 min as past marathon race time, it takes 3 min by default
#When the person has no marathon experience, experience array stores a value -2; otherwise, store 2
for row in range(marathonTime.shape[0]):
    if marathonTime[row,0] == 0:
        marathonTime[row,0] = 3;
        marathonTimeAged[row,0] = 90;
        timeSqr[row,0] = 9;
        experience[row,0] = 0;
        ones[row,0] = 1;
    else:
        experience[row,0]= 1;
        ones[row,0] = 1;

#When the person is male, gender array stores a value 1; otherwise, store -1  
for row in range(gender.shape[0]):
    if gender[row,0] == 'Male':
        gender[row,0] = 1;
    else:
        gender[row,0] = 0;

#When the person has no age info, age array stores a value 30 by default

# Convert this array into type float for later manipulation
age = age.astype(np.float32)
marathonTime = marathonTime.astype(np.float32)
marathonTimeAged = marathonTimeAged.astype(np.float32)
timeSqr = timeSqr.astype(np.float32)
experience = experience.astype(np.float32)

#Scale down certain features values for facilitating calculation later on
marathonTimeAged= marathonTimeAged*1.0/100
timeSqr=timeSqr*1.0/100

for row in range(age.shape[0]):
    if age[row,0] == 0.0:
       age[row,0] = 30*1.0/100
    else:
       age[row,0] = 1.0*age[row,0]/100;
       

#Construct the X input array (concated with an column array with all 1)
myX = np.column_stack ((gender,age,marathonTime,marathonTimeAged,timeSqr,experience,ones))

#Create several empty array for storing training/testing inputs/outputs with k-cross validation
list=[]
trainingX=np.asarray(list)
testingX =np.asarray(list)
trainingY=np.asarray(list)
testingY =np.asarray(list)

##Comment out to generate the prediction result and error
#weights =np.asarray(list)
#weights = -0.011198
#weights = np.vstack((weights,-0.065218))
#weights = np.vstack((weights,0.955649))
#weights = np.vstack((weights,0.019748))
#weights = np.vstack((weights,0.049628))
#weights = np.vstack((weights,-0.020564))
#weights = np.vstack((weights,0.073874))

#PredictionFile = np.dot(myX, weights)
#diffMatrix = PredictionFile-marathonTime
#finalError = np.sum(np.square(diffMatrix))
#print('finalError for entire population is')
#print(finalError)

#fl = open('prediction.csv', 'w')

#writer = csv.writer(fl)
#writer.writerow(['label1']) #if needed
#for values in PredictionFile:
#    writer.writerow(values)

#fl.close()  
# end of comment out to generate things

#Create a coefficient array to store weight values as training result
coefficient = np.asarray(list)

#Set the initial values for the weight
coefficient = 0.001;
for idx in range (0,6):
    coefficient = np.vstack((coefficient,0.001))

#Create an output Y array myY using marathonTIme array
myY = np.copy(marathonTime)

#Creation of classfier class 
class classifier_linreg:

    def __init__(self):
        self.variable = None

    #Creation of a function that return the sum of square difference based on predicted Y and testing Y
    def sumSquareDiff(self,X,Y, weights):
        theoryY = np.dot(X, weights)
        print('The predicted y is')
        print(theoryY)
        diff = (Y-theoryY)
        sumSquareDiffNum = np.sum(np.square(diff))
        return sumSquareDiffNum

# Total number of instances is 8711, with 31-fold cross validation, get the number of instances per set
totalInputs = 8711
crossValidation = 31
numPerSet = totalInputs/crossValidation

# Initialize result arrays to be created via the following nested for loop
# Start cross validation
avgError = 0

#Perform cross validation
for i in range (0,crossValidation): 


    #Creation of an instance for classifier_linreg
    classifier = classifier_linreg()

    #Based on cross validation number, store necessary training/testing inputs/outputs info for each round of cross validation
    for j in range(i*numPerSet,(i+1)*numPerSet):
        if testingX.shape[0] ==0:
            testingX = myX[j,:]
            testingY = myY[j,:]
        else:
            testingX = np.vstack((testingX,myX[j,:]))
            testingY = np.vstack((testingY,myY[j,:]))

    for j in range(0,i*numPerSet):
        if trainingX.shape[0]==0:
            trainingX =myX[j,:]
            trainingY =myY[j,:]
        else:
            trainingX = np.vstack((trainingX,myX[j,:]))
            trainingY = np.vstack((trainingY,myY[j,:]))
    
    for j in range((i+1)*numPerSet,crossValidation*numPerSet):
        if trainingX.shape[0]==0:
            trainingX =myX[j,:]
            trainingY =myY[j,:]
        else:
            trainingX = np.vstack((trainingX,myX[j,:]))
            trainingY = np.vstack((trainingY,myY[j,:]))

    
    #Create variables to store the current error and current index for this fold and this gradient descent calculation
    curError = 999999999
    gradientDescIndex = 1;

    while True:

        #A sequence of calculation to obtain the gradient matrix
        temp = np.dot(trainingX.T,trainingX)
        print(temp.shape)
        temp1 = np.dot(temp,coefficient)
        #print(temp1)
        temp2 = np.dot(trainingX.T,trainingY)
        #print(temp2)
        temp3 = temp1-temp2
        #print(temp3)
        temp4 = 2*temp3

        # Set learning rate as (1/(gradientDescIndex+1)) in order to answer to Robbins-Monroe conditions
        coefficient =coefficient- (0.0001*(1.0/(gradientDescIndex+1)))*temp4
        
        # Increment gradientDescIndex by 1 for next round
        gradientDescIndex=gradientDescIndex+1
        
        #Calculate and store the current error for this fold and this gradient descent calculation
        trainingError=classifier.sumSquareDiff(trainingX,trainingY,coefficient)
        curError=classifier.sumSquareDiff(testingX,testingY,coefficient)
        print('trainingError for this fold and this gradient descent is ')
        print(trainingError)

        # Calculate the sum of squared difference of the present weights with previous weights
        wDiff = np.sum(np.square(0.0001*(1.0/(gradientDescIndex+1)))*temp4)
        print('wDiff')
        print(wDiff)

        # Once the current validation error and the change of the weights go below a certain threshold: stop the gradient descent iteration
        if  curError < 100 :
            if( wDiff < 0.0001):
                print('curError that allows to stop the loop for this k-fold cross validation is is')
                print(curError)
                print('weight matrix that is derived for this round is')
                print(coefficient)
                break
    
    print('K-FOLD CROSS VALIDATION K =')
    print(i)
    #Clear the content of the arrays for next round calculation of cross validation
    testingX=np.asarray(list)
    trainingX=np.asarray(list)
    testingY=np.asarray(list)
    trainingY=np.asarray(list)
    
    # Add this round error to the total for calculation after
    #finishing k-fold cross validation
    avgError += curError

#Calculate the average prediction error after all the rounds of cross validation
avgError /= crossValidation
print("The average error is " + str(avgError))
    


