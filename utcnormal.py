#!/usr/bin/env python
# coding: utf8
import datetime

'''
This works only as long as the difference to UTC is in full hours!
'''

class date_normaliser(object):
    def invert_utcdiff(self, utc):
        if "+" in utc:
            if utc == "+0":
                utcdiff = 0
            else:
                utcdiff = 0 - int(utc[1:])
        elif "-" in utc:
            utcdiff = int(utc[1:])
        else:
            utcdiff = "ERROR" 
        return utcdiff

    def check_leapyear(self, myDate): 
        myYear = int(myDate[0] + myDate[1] + myDate[2] + myDate[3])
        leapyear = False
        if myYear % 4 == 0:
            leapyear = True
            if myYear % 100 == 0:
                leapyear = False
        return leapyear

    def utc_normalise(self, myTimestamp):
        myTimestamp = myTimestamp.split(" ")
        myDate = myTimestamp[0] + " " + myTimestamp[1]
        utc = myTimestamp[2]
        utcdiff = self.invert_utcdiff(utc)
        myYear = myDate[0] + myDate[1] + myDate[2] + myDate[3]
        myMonth = int(myDate[5] + myDate[6])
        myDay = int(myDate[8] + myDate[9])
        myHour = int(myDate[11] + myDate[12])
        myMinute = int(myDate[14] + myDate[15])
        mySecond = int(myDate[17] + myDate[18])

        if utcdiff == 0:
            outTimestamp = myDate

        elif utcdiff > 0:
            if myHour + utcdiff > 23:
                myHour = 24 - myHour - utcdiff
                myDay +=1
                leapyear = self.check_leapyear(myDate)
                if leapyear:
                    if myMonth == 2:
                        if myDay == 29:
                            myDay = 1
                            myMonth = 3
                        elif myDay == 28:
                            myDay = 29 
                else:
                    if myMonth == 2 and myDay == 28:
                        myDay = 1
                        myMonth = 3

                if myMonth == 1 or myMonth == 3 or myMonth == 5 or myMonth == 7 or myMonth == 8 or myMonth == 10 or myMonth == 12:
                    if myDay > 31:
                        myDay = 1
                        myMonth += 1
                        if myMonth > 12:
                            myMonth = 1
                            myYear += 1

                elif myMonth == 4 or myMonth == 6 or myMonth == 9 or myMonth == 11:
                    if myDay > 30:
                        myDay = 1
                        myMonth += 1

            else:
                myHour = myHour + utcdiff

        elif utcdiff < 0:
            if myHour + utcdiff < 0:
                myHour = 24 - myHour + utcdiff
                myDay -= 1
                if myDay == 0:
                   if myMonth == 1 or myMonth == 2 or myMonth == 4 or myMonth == 6 or myMonth == 8 or myMonth == 9 or myMonth == 11:
                       myDay = 31
                       myMonth -= 1
                       if myMonth == 0:
                           myMonth = 1
                           myYear -= 1
                   elif myMonth == 5 or myMonth == 7 or myMonth == 10 or myMonth == 12:
                       myDay = 30
                       myMonth -= 1
                   elif myMonth == 3:
                        leapyear = self.check_leapyear(myDate)
                        myMonth = 2
                        if leapyear:
                            myDay = 29
                        else:
                            myDay = 28

            else:
                myHour = myHour + utcdiff
                
        myYear = str(myYear)
        myMonth = str(myMonth)
        if len(myMonth) == 1:
            myMonth = "0" + myMonth
        myDay = str(myDay)
        if len(myDay) == 1:
            myDay = "0" + myDay
        myHour = str(myHour)
        if len(myHour) == 1:
            myHour = "0" + myHour
        myMinute = str(myMinute)
        if len(myMinute) == 1:
            myMinute = "0" + myMinute
        mySecond = str(mySecond)
        if len(mySecond) == 1:
            mySecond = "0" + mySecond
        outTimestamp = myYear + "-" + myMonth + "-" + myDay + " " + myHour + ":" + myMinute + ":" + mySecond + " +0"
        return outTimestamp


myNormaliser = date_normaliser()

sourcefile = "spammail.lst"
source = open(sourcefile, "r")
fulltext = source.read()
source.close()

myLines = fulltext.split("\n")
targetfile = "spammail-utc.lst"
target = open(targetfile, "w")
for i in range(len(myLines)):
    # tmpout = "myLines[" + str(i) + "] = " + myLines[i]
    # print tmpout
    if myLines[i] != "":
        currentLine = myLines[i].split(" ")
        myTimestamp = currentLine[0] + " " + currentLine[1] + " " + currentLine[2].replace(",", "")
        outTimestamp = myNormaliser.utc_normalise(myTimestamp)
        outLine = outTimestamp + ", " + currentLine[3] + " " + currentLine[4] + " " + currentLine[5] + " " + currentLine[6] + "\n"
        target.write(outLine)
target.close()
