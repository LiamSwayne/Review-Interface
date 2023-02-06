#!/usr/bin/env python3

# Review interface v0.2 (stores and analyzes reviews) by Liam Swayne
# change to whatever file name you use
REVIEW_FILE_NAME = "Reviews.txt"
# COMMANDS:
# enter title to access review
# type 'stat' to get dataset statistics
# 'e' to exit

# update: added histogram, while loop decision correction
# TODO: max characters per line word cutoff
# TODO: add 'perfect' special generated text box for stuff with perfect scores

from datetime import date
import termplotlib as tpl
import numpy as np
import statistics
import os
dirPath = os.path.dirname(os.path.realpath(__file__))
pathList = dirPath.split("/")
del pathList[0]

#get and convert data type function
def getType(input):
    input = str(input)
    if input == "True":
        input = True
    elif input == "False":
        input = False
    else:
        try:
            input = float(input)
            if str(input).endswith(".0"):
                input = int(input)
        except ValueError:
            pass
    return input

#input function
def takeInput(prompt=""):
    a = input(prompt)
    a = getType(a)
    return a

# histogram
def histogramFunction(a, bins=11, width=25):
    h, b = np.histogram(a, bins)
    for i in range (0, bins):
        print('{:12.5f}  | {:{width}s} {}'.format(
            b[i], 
            '#'*int(width*h[i]/np.amax(h)), 
            h[i], 
            width=width))

# terminal hyperlinks
def link(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

# review attributes
'''
type
name
score
dateLogged
dateUpdated
contents
'''

pathStr = ""

i = 0
for i in range(len(pathList)):
    pathStr += "/"+pathList[i]
pathStr += "/"+REVIEW_FILE_NAME

myFile = open(pathStr,"r+")
lineList = myFile.readlines()
myFile.close()

today = date.today()
reviewTypes = []
reviews = []
tempList = []
for i in range(len(lineList)):
    if str(lineList[i])[0] == "*":
        reviews.append(["","","","","",""])
        tempList = str(lineList[i]).split("*")
        reviews[-1][0] = tempList[1]
        if reviews[-1][0].upper() not in reviewTypes:
            reviewTypes.append(reviews[-1][0])
            reviewTypes[-1] = reviewTypes[-1].upper()
        reviews[-1][1] = tempList[2]
        reviews[-1][2] = int(tempList[3])
        reviews[-1][3] = tempList[4]
        reviews[-1][4] = tempList[5][:-1]
    else:
        reviews[-1][5] += lineList[i]
for i in range(len(reviews)):
    if len(str(reviews[i][5])) >= 2:
        while reviews[i][5][-1:] == "\n":
            reviews[i][5] = reviews[i][5][:-1]
for i in range(len(reviews)):
    if len(str(reviews[i][5])) >= 1:
        while reviews[i][5][0] == "\n":
            reviews[i][5] = reviews[i][5][1:]

# retired method of adding hyperlinks
'''
for i in range(len(reviews)):
    while "HTTP://" in str(reviews[i][5]).upper():
        tempLinkStr = str(reviews[i][5])
        linkStartIndex = tempLinkStr.upper().index("HTTP://")
        substring = tempLinkStr[linkStartIndex:]
        linkEndIndex = substring.index(")")
        substring2 = substring[:linkEndIndex]
        newLinkStr = link(substring2, 'link')
        reviews[i][5] = tempLinkStr[:linkStartIndex]+newLinkStr+substring2[linkEndIndex:]
'''


# loop decision and reader variables
typeChoice = ""
nameDisplay = ""
reviewsDisplay = []
spotFound = False
userInput = ""
namesCaps = []
index = 0
tier = ""
scoreData = []

while userInput.upper() != "R" and userInput != "READ" and userInput != "READ CATALOG" and userInput != "CATALOG" and userInput != "READING" and userInput != "WRITE" and userInput != "WRITE REVIEWS" and userInput != "W" and userInput != "WRITING":
    userInput = takeInput("Write reviews or read catalog: ")
    userInput = userInput.upper()

if userInput == "R" or userInput == "READ" or userInput == "READ CATALOG" or userInput == "CATALOG" or userInput == "READING":
    while userInput.upper() not in reviewTypes and userInput.upper()[:-1] not in reviewTypes:
        userInput = takeInput("Review type: ")
    if userInput.upper()[:-1] in reviewTypes:
        typeChoice = userInput.upper()[:-1]
    else:
        typeChoice = userInput.upper()
    i = 0
    print("Catalog:")
    reviews = sorted(reviews, key=lambda x: x[2], reverse=True)
    for i in range(len(reviews)):
        if str(reviews[i][0]).upper() == typeChoice:
            nameDisplay = ("  ["+str(reviews[i][2])+"] ")[-6:]+reviews[i][1]
            reviewsDisplay.append(nameDisplay)
    for i in range(len(reviewsDisplay)):
        print(reviewsDisplay[i])
    print()

    for i in range(len(reviews)):
        namesCaps.append(reviews[i][1])
        namesCaps[-1] = namesCaps[-1].upper()

    while userInput.upper() != 'E' and userInput.upper() != 'END':
        userInput = takeInput()
        userInput = str(userInput).upper()
        if userInput in namesCaps:
            index = namesCaps.index(userInput)
            if str(reviews[index][0]).upper() == typeChoice:
                # calculate tier
                tier = "Z"
                if reviews[index][2] > 5:
                    tier = "F"
                if reviews[index][2] > 15:
                    tier = "D"
                if reviews[index][2] > 30:
                    tier = "C"
                if reviews[index][2] >= 50:
                    tier = "B"
                if reviews[index][2] >= 70:
                    tier = "A"
                if reviews[index][2] >= 85:
                    tier = "S"
                if reviews[index][2] >= 95:
                    tier = "SS"
                # return contents of review, score, and tier
                if "HTTP://" in str(reviews[index][5]).upper():
                    tempLinkStr = str(reviews[index][5])
                    linkStartIndex = tempLinkStr.upper().index("HTTP://")
                    substring = tempLinkStr[linkStartIndex:]
                    linkEndIndex = substring.index(")")
                    substring2 = substring[:linkEndIndex]
                    newLinkStr = link(substring2, 'link')
                    print(tempLinkStr[:linkStartIndex]+link(substring2, 'link')+substring2[linkEndIndex:])
                else:
                    print(reviews[index][5])
                print("["+tier+"-TIER] Score -> "+str(reviews[index][2])+"\n")
        elif userInput == "STATS" or userInput == "STAT" or userInput == "STATISTICS":
            for i in range(len(reviews)):
                if str(reviews[i][0]).upper() == typeChoice:
                    scoreData.append(reviews[i][2])
            print("Reviews: "+str(len(scoreData)))
            print("Mean: "+str(round(statistics.mean(scoreData),1)))
            print("Median: "+str(statistics.median(scoreData)))

            for i in range(len(scoreData)):
                if scoreData[i] == 100:
                    scoreData[i] = 110
            histogramFunction(scoreData)
            print()
            for i in range(len(scoreData)):
                if scoreData[i] == 110:
                    scoreData[i] = 100

        elif userInput == "C" or userInput == "CATALOG":
            print("Catalog:")
            reviews = sorted(reviews, key=lambda x: x[2], reverse=True)
            for i in range(len(reviews)):
                if str(reviews[i][0]).upper() == typeChoice:
                    nameDisplay = ("  ["+str(reviews[i][2])+"] ")[-6:]+reviews[i][1]
                    reviewsDisplay.append(nameDisplay)
            for i in range(len(reviewsDisplay)):
                print(reviewsDisplay[i])
            print()

        elif userInput == "E" or userInput == "END":
            print("Shutting down...")
        else:
            print("Invalid input.")
