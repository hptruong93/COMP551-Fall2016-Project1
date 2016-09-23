import csv
import codecs
import random


###In this function, it generate the training data from the raw data
def GenerateTrainingData(predictYear):
    output = []

    with codecs.open("Project1_data.csv", "r", encoding='utf-8', errors='ignore') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        iterationNum = 0

        for row in readCSV:

            outputRow = []
            id = 0
            gender = None
            age = 0
            marathonTime = 0
            marNum = [0 for i in range(5)]
            marNum[0] = 0
            marNum[1] = 0
            marNum[2] = 0
            marNum[3] = 0
            marNum[4] = 0
            matchNum = [0 for i in range(5)]
            matchNum[0] = 0
            matchNum[1] = 0
            matchNum[2] = 0
            matchNum[3] = 0
            matchNum[4] = 0

            if iterationNum != 0:

                for i in range(0, len(row)):

                    if row[i] == '':
                        break

                    if i == 0:
                        id = row[i]
                    if i % 5 == 4:
                        try:
                            if row[i - 1] == "Marathon":

                                if marathonTime == 0 and row[i] == -1:
                                    marathonTime = -1
                                elif marathonTime == 0 and row[i] != -1:
                                    time = list(row[i])
                                    minutes = float(time[0]) * 60 + float(''.join(time[2] + time[3])) + float(
                                        ''.join(time[5] + time[6])) / 60
                                    marathonTime = minutes
                                elif marathonTime != 0 and row[i] == -1:
                                    marathonTime = marathonTime / 2
                                elif marathonTime != 0 and row[i] != -1:
                                    time = list(row[i])
                                    minutes = float(time[0]) * 60 + float(''.join(time[2] + time[3])) + float(
                                        ''.join(time[5] + time[6])) / 60
                                    marathonTime = (marathonTime + minutes) / 2

                        except ValueError:
                            marathonTime = 0

                    if i % 5 == 3:
                        yearList = list(row[i - 2])
                        try:
                            year = int(''.join(yearList[5] + yearList[6]))
                        except IndexError:
                            year = None
                        except ValueError:
                            year = None

                        if row[i] == "Marathon" and year == 16:
                            marNum[4] = marNum[4] + 1
                        elif row[i] == "Marathon" and year == 15:
                            marNum[3] = marNum[3] + 1
                        elif row[i] == "Marathon" and year == 14:
                            marNum[2] = marNum[2] + 1
                        elif row[i] == "Marathon" and year == 13:
                            marNum[1] = marNum[1] + 1
                        elif row[i] == "Marathon" and year == 12:
                            marNum[0] = marNum[0] + 1

                        if row[i] != "Marathon" and year == 16:
                            matchNum[4] = matchNum[4] + 1
                        elif row[i] != "Marathon" and year == 15:
                            matchNum[3] = matchNum[3] + 1
                        elif row[i] != "Marathon" and year == 14:
                            matchNum[2] = matchNum[2] + 1
                        elif row[i] != "Marathon" and year == 13:
                            matchNum[1] = matchNum[1] + 1
                        elif row[i] != "Marathon" and year == 12:
                            matchNum[0] = matchNum[0] + 1

                    if i != 0 and i % 5 == 0:

                        # if "M" in row[i]:
                        #   gender = 0
                        # elif "F" in row[i]:
                        #   gender = 1

                        gender = 0

                        try:
                            charList = list(row[i])
                            ageList = charList[1] + charList[2]
                            ageString = ''.join(ageList)
                            age = int(ageString)
                        except IndexError:
                            age = None
                            print("Index error")
                        except ValueError:
                            age = None
                            Flag = False
                            print("Value error")

            if marathonTime < 212.8:
                marathonTime = 0
            elif marathonTime < 251.56:
                marathonTime = 1
            elif marathonTime < 294.7:
                marathonTime = 2
            else:
                marathonTime = 3

            if marNum[predictYear - 2012] != 0:
                continueX = 1
            else:
                continueX = 0

            age = 0

            # if age != None and age <= 10:
            # age = 0
            # elif age != None and age <= 20:
            #   age = 1
            # elif age != None and age <= 30:
            #   age = 2
            # elif age != None and age <= 50:
            #   age = 3
            # elif age != None and age <= 100:
            #   age = 4
            # else:
            #   age = random.randint(0, 4)

            marathonBeforeX = 0
            matchBeforeX = 0

            for i in range(0, predictYear - 2012):
                marathonBeforeX = marathonBeforeX + marNum[i]
                matchBeforeX = matchBeforeX + matchNum[i]

                # if marathonBeforeX == 0:
                #   marathonBeforeX = 0
                # elif marathonBeforeX == 1:
                #   marathonBeforeX = 1
                # elif marathonBeforeX == 2:
                #   marathonBeforeX = 2
                # elif marathonBeforeX == 3:
                #   marathonBeforeX = 3
                # elif marathonBeforeX == 4:
                #   marathonBeforeX = 4
                # elif marathonBeforeX == 5:
                #   marathonBeforeX = 5
                # elif marathonBeforeX == 6:
                #   marathonBeforeX = 6
                # else:
                #   marathonBeforeX = 7

            if marathonBeforeX == 0:
                marathonBeforeX = 0
            else:
                marathonBeforeX = 1

            if matchBeforeX == 0:
                matchBeforeX = 0
            else:
                matchBeforeX = 0

            lastYear = None

            if marNum[predictYear - 2013] == 0:
                lastYear = 0
            else:
                lastYear = 1

                # if matchBeforeX == 0:
                #   matchBeforeX = 0
                # elif matchBeforeX == 1:
                #   matchBeforeX = 1
                # elif matchBeforeX == 2:
                #   matchBeforeX = 2
                # elif matchBeforeX == 3:
                #   matchBeforeX = 3
                # elif matchBeforeX == 4:
                #   matchBeforeX = 4
                # elif matchBeforeX == 5:
                #   matchBeforeX = 5
                # elif matchBeforeX == 6:
                #   matchBeforeX = 6
                # else:
                #   matchBeforeX = 7

            outputRow = [id, gender, age, marathonTime, marathonBeforeX, matchBeforeX, lastYear, continueX]

            if iterationNum != 0:
                output.append(outputRow)

            iterationNum = iterationNum + 1

    with open("prediction" + str(predictYear) + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(
            ["id", "gender", "age", "marathonTime", "marathonBefore" + str(predictYear),
             "matchBefore" + str(predictYear), "lastYearAttendance",
             "continue" + str(predictYear)])
        for data in output:
            spamwriter.writerow(
                [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]])


## below is the training and testing procedure of naive bayes algorithm
def trainAndValidation(trainFile, testFile, start, end, predictYear, string, flag):
    proArray = [[[0 for i in range(2)] for j in range(7)] for k in range(10)]
    proClass = [0 for i in range(2)]
    totalNum = 0

    iteration = 0

    with open(trainFile, "r") as csvfile:
        trainCSV = csv.reader(csvfile, delimiter=",")

        for row in trainCSV:

            if iteration != 0 and (iteration < start or iteration > end):

                totalNum = totalNum + 1

                for i in range(1, len(row) - 1):
                    proArray[int(row[i])][i][int(row[7])] = proArray[int(row[i])][i][int(row[7])] + 1 ##train P(Yi|Xij)

                proClass[int(row[7])] = proClass[int(row[7])] + 1 ##trian P(Yi)

            iteration = iteration + 1

    correctNum = 0
    wrongNum = 0
    output = []
    iteration = 0
    totalTestNum =0

    print("start" + str(start) + " end: " + str(end))

    with open(testFile, "r") as csvfile:
        testCSV = csv.reader(csvfile, delimiter=",")

        for row in testCSV:

            if flag == True: ## cross validation procedure

                if iteration != 0 and (iteration > start and iteration < end):
                    totalTestNum = totalTestNum + 1

                    proPredict = [0 for i in range(2)]

                    for i in range(0, 2):
                        proXY = 1.0

                        for j in range(1, len(row) - 1):
                            proXY = proXY * (float(proArray[int(row[j])][j][i] + 1) / float(proClass[i])) ##calculate P(Yi|Xii).....P(Yi|Xin)

                        proPredict[i] = (float(proClass[i]) / float(totalNum)) * proXY #calculate P(Yi)P(Yi|Xii).....P(Yi|Xin)

                    ##compare the result of 0, 1
                    max = 0
                    loc = None
                    for i in range(0, len(proPredict)):
                        if proPredict[i] > max:
                            max = proPredict[i]
                            loc = i

                    if predictYear != 2016:

                        if loc == int(row[7]):
                            correctNum = correctNum + 1
                        else:
                            wrongNum = wrongNum + 1

                    row[7] = loc
                    output.append(row)

                iteration = iteration + 1

            else: ##test procedure

                if iteration != 0:
                    totalTestNum = totalTestNum + 1

                    proPredict = [0 for i in range(2)]

                    for i in range(0, 2):
                        proXY = 1.0

                        for j in range(1, len(row) - 1):
                            proXY = proXY * (float(proArray[int(row[j])][j][i] + 1) / float(proClass[i])) ##calculate P

                        proPredict[i] = (float(proClass[i]) / float(totalNum)) * proXY

                    max = 0
                    loc = None
                    for i in range(0, len(proPredict)):
                        if proPredict[i] > max:
                            max = proPredict[i]
                            loc = i

                    if predictYear != 2016:

                        if loc == int(row[7]):
                            correctNum = correctNum + 1
                        else:
                            wrongNum = wrongNum + 1

                    row[7] = loc
                    output.append(row)

                iteration = iteration + 1

        if predictYear != 2016:
            print(string + ": " + str(correctNum / totalTestNum))

    return output


def prediction(predictYear):
    ##training error

    row_count = None
    trainCSV = None
    testCSV = None

    trainFileName = "prediction" + str(predictYear - 1) + ".csv"
    testFileName = "prediction" + str(predictYear) + ".csv"

    with open("prediction" + str(predictYear - 1) + ".csv", "r") as csvfile:
        trainCSV = csv.reader(csvfile, delimiter=",")
        row_count = sum(1 for row in trainCSV)

    ##K fold validation
    k = 10
    for i in range(0, k):
        trainAndValidation(trainFileName, trainFileName, row_count * i / k, row_count * (i + 1) / k, predictYear,
                           "validation",
                           True)

    ##Test on 2015/predict on 2016
    output = trainAndValidation(trainFileName, testFileName, 0, 0, predictYear, "test", False)

    with open("predictionFinal" + str(predictYear) + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(
            ["id", "gender", "age", "marathonTime", "marathonBefore" + str(predictYear),
             "matchBefore" + str(predictYear), "lastYearAttendance",
             "continue" + str(predictYear)])
        for data in output:
            spamwriter.writerow(
                [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]])


def NaiveBayes(predictYear, validation):
    GenerateTrainingData(predictYear - 1)
    GenerateTrainingData(predictYear)

    if validation == True:
        prediction(predictYear)


NaiveBayes(2016, True)
