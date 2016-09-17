import csv
import codecs

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
        marNum2012 = 0
        marNum2013 = 0
        marNum2014 = 0
        marNum2015 = 0
        marNum2016 = 0
        otherNum2012 = 0
        otherNum2013 = 0
        otherNum2014 = 0
        otherNum2015 = 0
        otherNum2016 = 0
        continue2014 = 0

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
                        time = "error"

                if i % 5 == 3:
                    yearList = list(row[i - 2])
                    try:
                        year = int(''.join(yearList[5] + yearList[6]))
                    except IndexError:
                        year = None
                    except ValueError:
                        year = None

                    if row[i] == "Marathon" and year == 16:
                        marNum2016 = marNum2016 + 1
                    elif row[i] == "Marathon" and year == 15:
                        marNum2015 = marNum2015 + 1
                    elif row[i] == "Marathon" and year == 14:
                        marNum2014 = marNum2014 + 1
                    elif row[i] == "Marathon" and year == 13:
                        marNum2013 = marNum2013 + 1
                    elif row[i] == "Marathon" and year == 12:
                        marNum2012 = marNum2012 + 1

                    if row[i] != "Marathon" and year == 16:
                        otherNum2016 = otherNum2016 + 1
                    elif row[i] != "Marathon" and year == 15:
                        otherNum2015 = otherNum2015 + 1
                    elif row[i] != "Marathon" and year == 14:
                        otherNum2014 = otherNum2014 + 1
                    elif row[i] != "Marathon" and year == 13:
                        otherNum2013 = otherNum2013 + 1
                    elif row[i] != "Marathon" and year == 12:
                        otherNum2012 = otherNum2012 + 1

                if i != 0 and i % 5 == 0:
                    if "M" in row[i]:
                        gender = "Male"
                    elif "F" in row[i]:
                        gender = "Female"

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
                        print("Value error")

        if marathonTime < 212.8:
            marathonTime = 1
        elif marathonTime < 251.56:
            marathonTime = 2
        elif marathonTime < 294.7:
            marathonTime = 3
        else:
            marathonTime = 4

        if marNum2014 != 0 and marNum2015 != 0:
            continue2014 = 1
        elif marNum2014 != 0 and marNum2015 == 0:
            continue2014 = 2
        elif marNum2014 == 0 and marNum2015 != 0:
            continue2014 = 3
        elif marNum2014 == 0 and marNum2015 == 0:
            continue2014 = 4

        outputRow = [id, gender, age, marathonTime, marNum2016, marNum2015, marNum2014, marNum2013, marNum2012,
                     otherNum2012,
                     otherNum2013, otherNum2014, otherNum2015, otherNum2016, continue2014]
        if iterationNum != 0:
            output.append(outputRow)

        iterationNum = iterationNum + 1

with open("newData.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(
        ["id", "gender", "age", "marathonTime", "marNum2016", "marNum2015", "marNum2014", "marNum2013", "marNum2012",
         "otherNum2012",
         "otherNum2013", "otherNum2014", "otherNum2015", "otherNum2016", "continue2014"])
    for data in output:
        spamwriter.writerow(
            [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
             data[11], data[12], data[13], data[14]])
