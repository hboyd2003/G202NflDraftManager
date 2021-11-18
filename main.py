from tkinter import *
import tkinter as tk
import tkinter.simpledialog
from tkinter import ttk
from datetime import datetime
import cfbd
root = Tk()
frm = ttk.Frame(root, padding=10)
draftPicks = None


class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master = master
        self.csvButton = tk.Button(self, text="CSV")
        self.csvButton.grid(column=2, row=1)
        root.wait_window(ImportDataDialog(master=root, controller=self))

        self.picksChoice = ttk.Treeview(columns=("position"))
        self.picksChoice.grid(column=2, row=2)
        self.picksChoice.heading("#0", text="Name", anchor=tk.CENTER)
        self.picksChoice.heading("#1", text="Position", anchor=tk.CENTER)
        self.picksChoice.column('#0', stretch=tk.YES)
        self.picksChoice.column('#1', stretch=tk.YES)
        self.picksChoice.bind("<Double-1>", self.onDoubleClick)
        for player in self.draftPicks:
            self.picksChoice.insert('', tk.END, text=player["name"] , values=player["position"])

        self.addPick = self.csvButton = tk.Button(self, text="+")
        self.csvButton.grid(column=2, row=1)
    
    def onDoubleClick(self, event):
        selectItem = self.picksChoice.selection()[0]
        selectColumn = self.picksChoice.identify_column(event.x)
        itemTuple = self.picksChoice.bbox(selectItem, selectColumn)
        offsetTuple = self.bbox(self.picksChoice)
        finalTuple = [itemTuple[0], itemTuple[1], itemTuple[2], itemTuple[3]]
        finalTuple[0] += offsetTuple[0]
        finalTuple[1] += offsetTuple[1]
        finalTuple[2] += offsetTuple[2]
        finalTuple[3] += offsetTuple[3]
        print(offsetTuple)

        if (selectColumn == "#0"):
            first_text = self.picksChoice.item(selectItem, "text")
        else:
            first_text = self.picksChoice.item(selectItem, "values")[0]
        edit = tk.Entry(root, textvariable=first_text)
        print(itemTuple)
        edit.place(x = finalTuple[0],
            y = finalTuple[1],
            width=finalTuple[3] - finalTuple[0],
            height=finalTuple[2] - finalTuple[1])
        print("you clicked on", first_text)
        

class ImportDataDialog(Toplevel):
    def __init__(self, master, controller):
        Toplevel.__init__(self, master)
        self.controller = controller
        self.dlgFrame = Frame(self)
        self.dlgFrame.grid()

        importLabel = tk.Label(self.dlgFrame, text="Choose import location")
        importLabel.grid(row=0, column=0)

        databaseButton = tk.Button(self.dlgFrame, text="CSV", command=self.csvButton_Pressed)
        databaseButton.grid(row=1, column=1)
        
        csvButton = tk.Button(self.dlgFrame, text="Database", command=self.databaseButton_Pressed)
        csvButton.grid(row=1, column=0)

        self.transient(root)
        self.grab_set()
        
    def csvButton_Pressed(self):
        self.destroy()

    def databaseButton_Pressed(self):
        root.config(cursor="wait")
        self.grabDatabase()
        self.importDatabase()
        root.config(cursor="")
        self.grab_release()
        self.destroy()

    def importCSV(self):
        print("Not implemented")

    def grabDatabase(self):
        configuration = cfbd.Configuration()
        configuration.api_key['Authorization'] = 'PrEoN+4gLLbOFbNh9Fevv0hRyYTBNVmQ3DLnhwvTQn06OJqatwpxvTVhR5nLrjFx'
        configuration.api_key_prefix['Authorization'] = 'Bearer'
        api_instance = cfbd.DraftApi(cfbd.ApiClient(configuration))
        self.draftPicks = api_instance.get_draft_picks(year=datetime.now().year)
        return

    def importDatabase(self):
        #Start of Seth's code
        listy = []
        import re
        #puts everything in game in a list and makes each item a string
        for line in self.draftPicks:
            line = str(line)
            thing = re.split(':|\n', line)
            listy.append(thing)
        
        #print(games[0])
        #print(listy[0])
        total = {}
        everything = []

        #puts every item in a dictionary
        for thing in listy:
            counter = 0
            for item in thing:
                #print(counter)
                #print(item)
                if (counter < 9):
                    if (counter < len(thing) - 2) and (counter % 2 == 0):
                        thing[counter] = thing[counter].replace(",", "")
                        thing[counter + 1] = thing[counter + 1].replace(",", "")
                        thing[counter] = thing[counter].replace("'", "")
                        thing[counter + 1] = thing[counter + 1].replace("'", "")
                        thing[counter] = thing[counter].replace(" ", "")
                        thing[counter + 1] = thing[counter + 1].replace(" ", "", 1)
                        thing[counter] = thing[counter].replace("{", "")
                        total[thing[counter]] = thing[counter + 1]
                        #print(total)
                else:
                    if (counter < len(thing) - 2) and (counter % 2 == 0):
                        thing[counter + 2] = thing[counter + 2].replace(",", "")
                        thing[counter + 1] = thing[counter + 1].replace(",", "")
                        thing[counter + 2] = thing[counter + 2].replace("'", "")
                        thing[counter + 1] = thing[counter + 1].replace("'", "")
                        thing[counter + 2] = thing[counter + 2].replace(" ", "")
                        thing[counter + 1] = thing[counter + 1].replace(" ", "", 1)
                        thing[counter + 2] = thing[counter + 2].replace("{", "")
                        thing[counter + 2] = thing[counter + 2].replace("}", "")
                        total[thing[counter + 1]] = thing[counter + 2]
                        #print(total)
                counter += 1
            #print(total)
            #print("NEW LINE--------")
            total_copy = total.copy()
            everything.append(total_copy)
            total.clear()
        #print("Done")
        self.controller.draftPicks = everything
        x=0
        #while(x<70):
           #print(everything[x])
           #x+=1
        #print(everything[217])
        #End of Seth's code

        #Start of Thomas' Code

        #User input for the picks that the user has as well as their top positional needs (Needs to be adjusted to be the actual user input)
        userInputPicks = ["12","47","89","124","186","222","256"]
        userInputNeeds = ["quarterback","defensiveend","runningback","cornerback"
                          ,"safety","safety","widereceiver"]
        
        #Gets three reccomended selections for a user pick and set of needs
        def getRecPicks(pickNumber, numOfNeeds):
            pickOverall = int(userInputPicks[pickNumber])
            pickTally = pickOverall
            recPicks = []
            numNeeds = len(numOfNeeds)
            stop = 0
            counta = 0
            stopper = 0
            #Goes through each poitional need in order and sees if there are any players with that position available in the 10 picks after and including the user pick
            while(counta<numNeeds):
                counta2=0
                picksAfter = 10
                if( (pickOverall + 10) > (len(everything)) ):
                    picksAfter = (len(everything)) - pickOverall
                while(counta2<picksAfter):
                    pos1 = (everything[pickOverall+counta2].get("position")).lower()
                    if(pos1 == userInputNeeds[counta]):
                        counter4 = 0
                        appendOrNo2 = 0
                        while(counter4 < len(recPicks)):
                            if(recPicks[counter4] == everything[pickOverall+counta2]):
                                appendOrNo2 = 1
                            counter4+=1
                        if(appendOrNo2 == 0):
                            recPicks.append(everything[pickOverall+counta2])
                            counta2+=10
                    counta2+=1
                if(len(recPicks) == 3):
                    stopper = 1
                    counta+=numNeeds
                counta+=1
            #If the previous loop does not produce three picks, this loop goes through the picks until it finds enough selections that fit under user needs or until it runs out of picks
            if(stopper == 0):
                while(pickTally<len(everything)):
                    pos = (everything[pickTally].get("position")).lower()
                    numNeeds = len(userInputNeeds)
                    counter2=0
                    while(counter2 < numNeeds):
                        if(stop == 0):
                            if(pos == userInputNeeds[counter2]):
                                counter3 = 0
                                appendOrNo = 0
                                while(counter3 < len(recPicks)):
                                    if(recPicks[counter3] == everything[pickTally]):
                                        appendOrNo = 1
                                    counter3+=1
                                if(appendOrNo == 0):
                                    recPicks.append(everything[pickTally])
                        if(len(recPicks) == 3):
                            stop = 1
                            counter2+=numNeeds
                            pickTally+=(len(everything))
                        counter2 += 1
                    pickTally+=1
            pickTally = pickOverall
            #If the previous two loops still do not produce three picks, this loop goes through the picks until it finds enough selections, regardless of the user needs,
            #or until it runs out of picks
            if(len(recPicks) != 3):
                while(pickTally<len(everything)):
                    if(len(recPicks) != 3):
                        counterAgain = 0
                        appendOrNo3 = 0
                        while(counterAgain < len(recPicks)):
                            if(recPicks[counterAgain] == everything[pickTally]):
                                appendOrNo3 = 1
                            counterAgain+=1
                        if(appendOrNo3 == 0):
                            recPicks.append(everything[pickTally])
                    else:
                        pickTally+=len(everything)
                    pickTally+=1                        
            return recPicks
        

        selectedPlayers = []

        #Runs the draft process using the list of user picks and list of user needs, going through each round providing three reccomened players
        #and allowing the user to select from the three. Removes positions from the list of needs when a player with said position is selected by the user.
        #At the end, prints a list of the selected user picks.
        def draft(listOfPicks, listOfNeeds):
            draftCount = 0
            reccoPicks = []
            userInputNum = 0
            while(draftCount < len(listOfPicks)):
                reccoPicks = getRecPicks(draftCount, listOfNeeds)
                xer = len(reccoPicks)
                counr = 0
                while(counr < xer):
                    print(reccoPicks[counr])
                    print("\n")
                    counr+=1
                print("Select Player")
                userInputNum = int(input())
                userChoice = reccoPicks[userInputNum]
                selectedPlayers.append(userChoice)
                posCounter = 0
                posPos = userChoice.get("position").lower()
                while(posCounter < len(listOfNeeds)):
                    if(posPos == listOfNeeds[posCounter]):
                        listOfNeeds.pop(posCounter)
                        posCounter += len(listOfNeeds)
                    posCounter+=1
                draftCount+=1
            print("Your Selections: \n")
            xer2 = len(selectedPlayers)
            counr2 = 0
            while(counr2 < xer2):
                print(selectedPlayers[counr2])
                print("\n")
                counr2+=1

        #Calls the draft function, thus running the code
        draft(userInputPicks, userInputNeeds)


        #reccyPicks = getRecPicks(6, userInputNeeds)
        #xer = len(reccyPicks)
        #counr = 0
        #while(counr < xer):
            #print(reccyPicks[counr])
            #counr+=1
                
            


        
    def get_draftPicks(self):
        return self.draftPicks
        
root.wm_title("IDK")
frm.grid()
mainWindow = MainWindow(master=frm)
root.mainloop()
