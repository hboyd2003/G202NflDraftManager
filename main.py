from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from ctypes import windll
import cfbd
draftPicks = None



class MainWindow(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.master = master
        mainStyle = ttk.Style(self)

        #Changes font and increases size
        default_font = font.Font(family="Arial", size=16)
        body_font = font.Font(family="Arial", size=14)
        self.option_add("*Font", default_font)
        font.nametofont("TkHeadingFont").configure(family="Arial", size=16)

        #Tells windows to not scale the program making it look blurry
        windll.shcore.SetProcessDpiAwareness(1)
        #Scale items using scale factor setting in Windows
        scalingFactor = windll.shcore.GetScaleFactorForDevice(0) / 100
        self.tk.call( #Default scaling for all of tk, scales most things
            'tk',
            'scaling',
            scalingFactor)
        mainStyle.theme_use('clam')
        print(body_font.metrics('linespace'))
        print(body_font.metrics('linespace') * 2)
        mainStyle.configure('Treeview', rowheight=int(body_font.metrics('linespace') * 1.6))


        #Configures each column to a weight which incates how much of the windows it should take up
        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=50)
        self.columnconfigure(2, weight=100)
        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=10)

        self.addPick = tk.Button(self, text="+")
        self.addPick.grid(column=2, row=2, sticky="nsew")

        #Opens the import dialog and then confirms the app is still running
        self.wait_window(ImportDataDialog(master=self, controller=self))
        try:
            self.winfo_exists()
        except:
            exit()

        #Sets up tree view
        self.picksChoice = ttk.Treeview(self, columns=("position"))
        self.picksChoice.grid(column=0, row=0, columnspan=2, sticky="nsew")
        #Sets up treeview columns and heading
        self.picksChoice.heading("#0", text="Name", anchor=tk.CENTER)
        self.picksChoice.heading("#1", text="Position", anchor=tk.CENTER)
        self.picksChoice.column('#0', stretch=tk.YES)
        self.picksChoice.column('#1', stretch=tk.YES)
        self.picksChoice.bind("<Double-1>", self.onDoubleClick) #For editing an item
        #Creates tag to change font of items
        self.picksChoice.tag_configure("defaultFont", font=body_font)
        for player in self.draftPicks:
            self.picksChoice.insert('', tk.END, text=player["name"] , values=player["position"], tags="defaultFont")
    
    def onDoubleClick(self, event):
        self.selectedItem = (self.picksChoice.selection()[0], self.picksChoice.identify_column(event.x)) #Gets specific item based on press location and selection
        itemBBox = list(self.picksChoice.bbox(self.selectedItem[0], self.selectedItem[1])) #Item location relative to treeview
        offset = (self.picksChoice.winfo_x(), self.picksChoice.winfo_y()) #Gets treeview coords to offset with
        self.editEntry_Text = tk.StringVar()
        self.editEntry = tk.Entry(self, textvariable=self.editEntry_Text)

        #Checks if selected item in column 0 or 1
        if (self.selectedItem[1] == "#0"): #Column 0
            self.editEntry.insert(0, string = self.picksChoice.item(self.selectedItem[0], "text"))
            offset[0] += 15 #Offset for column 0 padding
            itemBBox[2] -= 15
        else: #Column 1
            self.editEntry.insert(0, string = self.picksChoice.item(self.selectedItem[0], "values")[0])
        self.editEntry.place(
            x = itemBBox[0] + offset[0],
            y = itemBBox[1] + offset[1],
            width=itemBBox[2],
            height=itemBBox[3])

        #Forces curser to be in entrybox
        self.editEntry.focus_force()
        #When you exit the entrybox
        self.editEntry.bind('<Return>', func=self.finishedEntryEdit)
        self.editEntry.bind('<FocusOut>', func=self.finishedEntryEdit)

    def finishedEntryEdit(self, event): #When you exit the entrybox
        if (self.selectedItem[1] == "#0"): #Sets text based on column
            self.picksChoice.item(self.selectedItem[0], text=self.editEntry_Text.get())
        else:
            self.picksChoice.item(self.selectedItem[0], values=self.editEntry_Text.get())
        self.editEntry.destroy() #Deletes the entrybox


class ImportDataDialog(Toplevel):
    #User input for the picks that the user has as well as their top positional needs (Needs to be adjusted to be the actual user input)
    userInputPicks = ["12","47","89","124","186","222","256"]
    userInputNeeds = ["quarterback","defensiveend","runningback","cornerback"
                        ,"safety","safety","widereceiver"]

    def __init__(self, master, controller):
        Toplevel.__init__(self, master)
        self.controller = controller
        self.master = master
        self.protocol("WM_DELETE_WINDOW", self.closeEvent)
        self.controller.draftPicks = None

        self.grid()

        importLabel = tk.Label(self, text="Choose import location")
        importLabel.grid(row=0, column=0, columnspan=2)

        databaseButton = tk.Button(self, text="CSV", command=self.csvButton_Pressed)
        databaseButton.grid(row=1, column=1)
        
        csvButton = tk.Button(self, text="Database", command=self.databaseButton_Pressed)
        csvButton.grid(row=1, column=0)

        self.transient(master)
        self.grab_set()
        
    def csvButton_Pressed(self):
        acceptedFiletypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
        )
        selectedFile = askopenfilename(
            title = 'Select CSV file',
            filetypes=acceptedFiletypes
        )
        self.importCSV(selectedFile = selectedFile)

    def databaseButton_Pressed(self):
        self.config(cursor="wait")
        self.grabDatabase()
        self.importDatabase()
        self.config(cursor="")
        self.grab_release()
        self.closeEvent()
        #Calls the draft function, thus running the code
        self.draft(self.userInputPicks, self.userInputNeeds)

    def importCSV(self, selectedFile):
        print("Not implemented")

    def grabDatabase(self):
        configuration = cfbd.Configuration()
        configuration.api_key['Authorization'] = 'PrEoN+4gLLbOFbNh9Fevv0hRyYTBNVmQ3DLnhwvTQn06OJqatwpxvTVhR5nLrjFx'
        configuration.api_key_prefix['Authorization'] = 'Bearer'
        api_instance = cfbd.DraftApi(cfbd.ApiClient(configuration))
        self.draftPicksRaw = api_instance.get_draft_picks(year=datetime.now().year)
        return

    def importDatabase(self):
        #Start of Seth's code
        listy = []
        import re
        #puts everything in game in a list and makes each item a string
        for line in self.draftPicksRaw:
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
        #End of Seth's 
        
    def closeEvent(self):
        if (self.controller.draftPicks is None):
            result = messagebox.askretrycancel(
                title="Nothing was selected",
                message="No file or import option was selcted\nWould you like to try again?")
            if (result == 'retry'):
                self.__init__()
            else:
                self.master.destroy()
        else:
            self.destroy()

    #Start of Thomas' Code
    #Gets three reccomended selections for a user pick and set of needs
    def getRecPicks(self, pickNumber, numOfNeeds):
        pickOverall = int(self.userInputPicks[pickNumber])
        pickTally = pickOverall
        draftPicks = self.controller.draftPicks
        recPicks = []
        numNeeds = len(numOfNeeds)
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
                pos1 = (draftPicks[pickOverall+counta2].get("position")).lower()
                if(pos1 == self.userInputNeeds[counta]):
                    counter4 = 0
                    appendOrNo2 = 0
                    while(counter4 < len(recPicks)):
                        if(recPicks[counter4] == draftPicks[pickOverall+counta2]):
                            appendOrNo2 = 1
                        counter4+=1
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
                numNeeds = len(self.userInputNeeds)
                counter2=0
                while(counter2 < numNeeds):
                    if(stop == 0):
                        if(pos == self.userInputNeeds[counter2]):
                            counter3 = 0
                            appendOrNo = 0
                            while(counter3 < len(recPicks)):
                                if(recPicks[counter3] == draftPicks[pickTally]):
                                    appendOrNo = 1
                                counter3+=1
                            if(appendOrNo == 0):
                                recPicks.append(draftPicks[pickTally])
                    if(len(recPicks) == 3):
                        stop = 1
                        counter2+=numNeeds
                        pickTally+=(len(draftPicks))
                    counter2 += 1
                pickTally+=1
        pickTally = pickOverall
        #If the previous two loops still do not produce three picks, this loop goes through the picks until it finds enough selections, regardless of the user needs,
        #or until it runs out of picks
        if(len(recPicks) != 3):
            while(pickTally<len(draftPicks)):
                if(len(recPicks) != 3):
                    counterAgain = 0
                    appendOrNo3 = 0
                    while(counterAgain < len(recPicks)):
                        if(recPicks[counterAgain] == draftPicks[pickTally]):
                            appendOrNo3 = 1
                        counterAgain+=1
                    if(appendOrNo3 == 0):
                        recPicks.append(draftPicks[pickTally])
                else:
                    pickTally+=len(draftPicks)
                pickTally+=1                        
        return recPicks

    #Runs the draft process using the list of user picks and list of user needs, going through each round providing three reccomened players
    #and allowing the user to select from the three. Removes positions from the list of needs when a player with said position is selected by the user.
    #At the end, prints a list of the selected user picks.
    def draft(self, listOfPicks, listOfNeeds):
        selectedPlayers = []
        draftCount = 0
        reccoPicks = []
        userInputNum = 0
        while(draftCount < len(listOfPicks)):
            reccoPicks = self.getRecPicks(draftCount, listOfNeeds)
            xer = len(reccoPicks)
            counr = 0
            while(counr < xer):
                print(reccoPicks[counr])
                print("\n")
                counr+=1
            print("Select Player")
            userInputNum = 1
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

mainWindow = MainWindow(None) 
mainWindow.wm_title("IDK")
mainWindow.mainloop()
