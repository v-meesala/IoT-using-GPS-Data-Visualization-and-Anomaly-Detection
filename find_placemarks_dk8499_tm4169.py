"""
CSCI - 720 - Big data Analytics
Rochester Institute Of Technology
Date : 11-28-2022
Project - Find Stops and Turns Placemarks using gps data
Authors :  Dheeraj Kukkala, dk8499
           Venkatesh Meesala , tm4169
Program : Finding Placemarks for Stops and Turns into KML file
"""
import numpy as np
import pandas as pd


def findHazards(csvFilename):
    stops, left_turns, right_turns = {}, {}, {}
    prevHeading, currHeading = 0, None

    data = pd.read_csv(csvFilename)

    arrData = np.array(data)

    stopFlag = False
    tempStop  = None
    for line in arrData:
        if int(line[3]) == 0 :
            tempStop = line
            if not stopFlag:
                stopFlag = True
        else:
            if stopFlag:
                stops[tempStop[0]] = {'longitude' : tempStop[1], 'latitude':tempStop[2], 'altitude':tempStop[-1]}
                stopFlag = False


    import writing_out_placemark_dk8499_tm4169 as wpm
    wpm.create_placemarks(csvFilename[:-9]+"_hazards.kml", stops, left_turns, right_turns)



