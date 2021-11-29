import re
class Draft(object):
    roundStart = []

    #Start of Thomas' Code
    #Gets three reccomended selections for a user pick and set of needs
    @staticmethod
    def getRecPicks(draftPicks, pickOverall, listOfNeeds):
        pickTally = pickOverall
        recPicks = []
        print(listOfNeeds)
        numNeeds = len(listOfNeeds)
        stop = 0
        counta = 0
        stopper = 0
        #Goes through each poitional need in order and sees if there are any players with that position available in the 10 picks after and including the user pick
        while(counta<numNeeds):
            counta2=0
            picksAfter = 10
            if( (pickOverall + 10) > (len(draftPicks)) ):
                picksAfter = (len(draftPicks)) - pickOverall
            while(counta2<picksAfter):
                pos1 = draftPicks[pickOverall+counta2].get("position").lower()
                if(pos1 == listOfNeeds[counta]):
                    i4 = 0
                    appendOrNo2 = 0
                    while(i4 < len(recPicks)):
                        if(recPicks[i4] == draftPicks[pickOverall+counta2]):
                            appendOrNo2 = 1
                        i4+=1
                    if(appendOrNo2 == 0):
                        recPicks.append(draftPicks[pickOverall+counta2])
                        counta2+=10
                counta2+=1
            if(len(recPicks) == 3):
                stopper = 1
                counta+=numNeeds
            counta+=1
        #If the previous loop does not produce three picks, this loop goes through the picks until it finds enough selections that fit under user needs or until it runs out of picks
        if(stopper == 0):
            while(pickTally<len(draftPicks)):
                pos = (draftPicks[pickTally].get("position")).lower()
                numNeeds = len(listOfNeeds)
                j=0
                while(j < numNeeds):
                    if(stop == 0):
                        if(pos == listOfNeeds[j]):
                            k = 0
                            appendOrNo = 0
                            while(k < len(recPicks)):
                                if(recPicks[k] == draftPicks[pickTally]):
                                    appendOrNo = 1
                                k+=1
                            if(appendOrNo == 0):
                                recPicks.append(draftPicks[pickTally])
                    if(len(recPicks) == 3):
                        stop = 1
                        j+=numNeeds
                        pickTally+=(len(draftPicks))
                    j += 1
                pickTally+=1
        pickTally = pickOverall
        #If the previous two loops still do not produce three picks, this loop goes through the picks until it finds enough selections, regardless of the user needs,
        #or until it runs out of picks
        if(len(recPicks) != 3):
            while(pickTally<len(draftPicks)):
                if(len(recPicks) != 3):
                    iAgain = 0
                    appendOrNo3 = 0
                    while(iAgain < len(recPicks)):
                        if(recPicks[iAgain] == draftPicks[pickTally]):
                            appendOrNo3 = 1
                        iAgain+=1
                    if(appendOrNo3 == 0):
                        recPicks.append(draftPicks[pickTally])
                else:
                    pickTally+=len(draftPicks)
                pickTally+=1                        
        return recPicks


    #Runs the draft process using the list of user picks and list of user needs, going through each round providing three reccomened players
    #and allowing the user to select from the three. Removes positions from the list of needs when a player with said position is selected by the user.
    #At the end, prints a list of the selected user picks.
    @staticmethod
    def draft(draftPicks, pickPosition, listOfNeeds):
        reccoPicks = Draft.getRecPicks(draftPicks, pickPosition, listOfNeeds)
        return reccoPicks
        #userInputNum = 1
        #userChoice = reccoPicks[userInputNum]
        #selectedPlayers.append(userChoice)
        #posi = 0
        #posPos = userChoice.get("position").lower()
        #while(posi < len(listOfNeeds)):
        #    if(posPos == listOfNeeds[posi]):
        #        listOfNeeds.pop(posi)
        #        posi += len(listOfNeeds)
        #    posi+=1
        #draftCount+=1
        #print("Your Selections: \n")
        #xer2 = len(selectedPlayers)
        #counr2 = 0
        #while(counr2 < xer2):
        #    print(selectedPlayers[counr2])
        #    print("\n")
        #    counr2+=1

    @staticmethod
    def calculateRoundLengths(draftPicks):
        overallPick = 1
        currentRound = 0
        while(overallPick != len(draftPicks)):
            if (int(draftPicks[overallPick - 1]["round"]) != currentRound):
                currentRound += 1
                Draft.roundStart.append(overallPick - 1)
            overallPick += 1
        Draft.roundStart.append(len(draftPicks) - 1)

    @staticmethod
    def importCSV(self, selectedFile):
        #Start of Seth's code

        #opens the csv and puts all the data in a dictionary
        import csv
        with open(selectedFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            content = {}

            #puts all of the csv data into the dictionary "content"
            for row in csv_reader:
                if line_count == 0:
                    names = f'{" ".join(row)}'
                    #print(names)
                    if ("pick" in names):
                        print("yee")
                content[line_count] = row
                line_count += 1
                
            #print(content[0])
            #print(content[1])

            line_count = 0
            temp_dic = {}
            matched = []

            #organises all the player data into dictionaries that are inside the list "matched"
            while line_count < len(content):
                if line_count != 0:
                    mc = 0
                    while mc < len(content[0]):
                        temp_dic[content[0][mc]] = content[line_count][mc]
                        #print(temp_dic[content[0][mc]])
                        mc += 1
                    matched.append(temp_dic)
                    #print(matched[line_count - 1].get("pick"))
                    temp_dic = {}
                line_count += 1

            #you can access csv data using matched[x].get("data")
            #End of Seth's code

    @staticmethod
    def formatPick(pick):
        textColumn = re.sub(r"(\w)([A-Z])", r"\1 \2", pick["name"])
        valueColumns = (
            pick["college_team"],
            re.sub(r"(\w)([A-Z])", r"\1 \2", pick["position"]),
            pick["height"] + " in",
            pick["weight"] + " Ib",
            pick["pre_draft_grade"],
            pick["overall"]
        )
        return textColumn, valueColumns