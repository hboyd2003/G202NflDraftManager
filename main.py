#    GM-AID is a tool designed to help NFL teams manage thier draft picks. It is built on Python utilizing Tkinter for GUI.
#    Copyright (C) 2021  Harrison Boyd, Seth Wiley, Thomas Jackson and Benjamin Hulsey
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License

from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import font, messagebox, ttk
from datetime import datetime
from Draft import Draft
import ast
import re
from sys import platform
try:
    from ctypes import windll
except ImportError:
    from AppKit import NSScreen
import cfbd
positionDictionary = {
    "Wide Receiver": ("widereceiver", "wr"),
    "Quarterback": ("Quarterback", "qb"),
    "Running Back": ("runningback", "rb"),
    "Tight End": ("tightend", "te"),
    "Offensive Tackle": ("offensivetackle", "ot"),
    "Cornerback": ("cornerback", "cb"),
    "Inside Linebacker": ("insidelinebacker", "ilb"),
    "Offensive Guard": ("offensiveguard", "og"),
    "Outside Linebacker": ("outsidelinebacker", "olb"),
    "Defensive End": ("defensiveend", "de"),
    "Safety": ("safety", "s"),
    "center": ("center", "c"),
    "Place Kicker": ("placekicker", "pk"),
    "Defensive Tackle": ("defensivetackle", "dt"),
    "Long Snapper": ("longsnapper", "ls"),
    "Punter": ("punter", "p")
}

class MainWindow(Tk):
    def __init__(self, master=None):
        Tk.__init__(self, master)
        self.master = master
        self.tk.call("source", "sun-valley.tcl")
        self.mainStyle = ttk.Style(self)

        self.tk.call("set_theme", "dark")
        self.mainStyle.theme_use("sun-valley-dark")
        #Changes font and increases size
        self.default_font = font.Font(family="Arial", size=16)
        self.body_font = font.Font(family="Arial", size=14)
        self.option_add("*Font", self.default_font)
        self.mainStyle.configure("Treeview.Heading", font=self.default_font)
        self.mainStyle.configure("TButton", font=self.body_font)

        self.scaleSetup()

        #Configures each column to a weight which incates how much of the windows it should take up
        self.columnconfigure(0, weight=25) #Round label and half of player pick treeview
        self.columnconfigure(1, weight=25) #Round entrybox, half of player pick treeview and + button
        self.columnconfigure(2, weight=5) #Spacer
        self.columnconfigure(3, weight=45) #Suggested pick players treeview
        self.rowconfigure(0, weight=5) 
        self.rowconfigure(1, weight=90)
        self.rowconfigure(2, weight=5)

        #Label for the round entrybox
        self.pickLabel = ttk.Label(self, text="Pick Position: ")
        self.pickLabel.grid(column=0, row=0)

        #Pick position entry box
        self.pickEntry_Text = tk.StringVar()
        self.pickPositionEntry = PickPositionEntry(master=self)
        self.pickPositionEntry.grid(column=1, row=0)

        self.nextRoundButton = ttk.Button(self, text="Next Round", command=self.nextRoundButton_Pressed)
        self.nextRoundButton.grid(column=3, row=2, sticky='e')

        self.addPick = ttk.Button(self, text="+", command=self.addPick)
        self.addPick.grid(column=1, row=2, sticky="nsew")

        self.suggestedPicksLabel = ttk.Label(self, text="Suggested Picks")
        self.suggestedPicksLabel.grid(column=3, row=0, sticky='')

        self.round = 0
        #Opens the import dialog and then confirms the app is still running
        self.wait_window(ImportDataDialog(master=self))
        try:
            self.winfo_exists()
        except:
            exit()

        self.treeViewsSetup()
        
        #Calls the draft function, thus running the code
        #self.draft(self.userInputPicks, self.userInputNeeds)

    def scaleSetup(self): #Sets up scaling for different resolution displays
        if (platform == "win32"):
            #Tells windows to not scale the program making it look blurry
            windll.shcore.SetProcessDpiAwareness(1)
            #Scale items using scale factor setting in Windows
            scalingFactor = windll.shcore.GetScaleFactorForDevice(0) / 100
        else:
            scalingFactor = NSScreen.mainScreen().backingScaleFactor()
        self.tk.call( #Default scaling for all of tk, scales most things
            'tk',
            'scaling',
            scalingFactor * 1.2)
        self.mainStyle.configure('Treeview', rowheight=int(self.body_font.metrics('linespace') * 1.6))
    

    def nextRoundButton_Pressed(self):
        currentNeeds = list(self.picksChoice.get_children())
        if (self.round != 0):
            pickForRound = ast.literal_eval(self.suggestedPicksView.item(self.suggestedPicksView.selection())['tags'][1])
            for position in positionDictionary.items():
                if (pickForRound['position'].lower() == position[1][0]): #Matches alternative names
                    for need in currentNeeds:
                        if (len(self.picksChoice.item(need)["tags"]) == 2):
                            currentNeeds.remove(need)
                        if (self.picksChoice.item(need)["text"] == position[0]):
                            self.picksChoice.item(need, tags=("defaultFont", "green"))
                            currentNeeds.remove(need)
                            break
                    break
        userInputNeeds = []
        self.round += 1
        for item in currentNeeds:
            userInputNeeds.append(positionDictionary[self.picksChoice.item(item)["text"]][0])
        Draft.calculateRoundLengths(self.draftPicks)
        self.suggestedPicksLabel.config(text="Suggested Picks for Round #" + str(self.round))
        self.addSuggested(Draft.draft(self.draftPicks, self.round, int(self.pickEntry_Text.get()), userInputNeeds))

    def treeViewsSetup(self):
        #Sets up pick player tree view
        self.picksChoice = ttk.Treeview(self)
        self.picksChoice.grid(column=0, row=1, columnspan=2, sticky="nsew")
        #Sets up treeview columns and heading
        self.picksChoice.heading("#0", text="Position", anchor=tk.CENTER)
        self.picksChoice.column('#0', stretch=tk.YES)
        self.picksChoice.bind("<Double-1>", self.onDoubleClick) #For editing an item
        self.picksChoice.bind("<Delete>", self.onDelete)
        self.picksChoice.bind("<BackSpace>", self.onDelete)
        #Creates tag to change font of items
        self.picksChoice.tag_configure("defaultFont", font=self.body_font)
        self.picksChoice.tag_configure("green", background='green')
        #for player in self.draftPicks:
        #    self.picksChoice.insert('', tk.END, text=player["name"] , values=player["position"], tags="defaultFont")

        #Sets up pick player tree view
        self.suggestedPicksView = ttk.Treeview(self,
            columns=("college", "position", "height", "weight", "pre-grade", "overall"))
        self.suggestedPicksView.grid(column=3, row=1, columnspan=2, sticky="nsew")
        #Sets up treeview columns and heading
        self.suggestedPicksView.heading("#0", text="Name", anchor=tk.CENTER)
        self.suggestedPicksView.heading("#1", text="College", anchor=tk.CENTER)
        self.suggestedPicksView.heading("#2", text="Position", anchor=tk.CENTER)
        self.suggestedPicksView.heading("#3", text="Height", anchor=tk.CENTER)
        self.suggestedPicksView.heading("#4", text="Weight", anchor=tk.CENTER)
        self.suggestedPicksView.heading("#5", text="Pre-Grade", anchor=tk.CENTER)
        self.suggestedPicksView.heading("#6", text="Overall", anchor=tk.CENTER)
        self.suggestedPicksView.bind("<Double-1>", self.onDoubleClick) #For editing an item
        self.suggestedPicksView.column('#0', stretch=tk.YES, width=300)
        self.suggestedPicksView.column('#1', stretch=tk.YES, width=150)
        self.suggestedPicksView.column('#2', stretch=tk.YES, width=300)
        self.suggestedPicksView.column('#3', stretch=tk.YES, width=120)
        self.suggestedPicksView.column('#4', stretch=tk.YES, width=120)
        self.suggestedPicksView.column('#5', stretch=tk.YES, width=170)
        self.suggestedPicksView.column('#6', stretch=tk.YES, width=130)
        
        #Creates tag to change font of items
        self.suggestedPicksView.tag_configure("defaultFont", font=self.body_font)
    
    def onDoubleClick(self, event): #Double click on the player choice tree view
        try:
            self.selectedItem = (self.picksChoice.selection()[0], self.picksChoice.identify_column(event.x)) #Gets specific item based on press location and selection
        except(IndexError): #For when the user clicks on blank space
            return

        itemBBox = list(self.picksChoice.bbox(self.selectedItem[0], self.selectedItem[1])) #Item bounding box relative to treeview
        offset = [self.picksChoice.winfo_x(), self.picksChoice.winfo_y()] #Gets treeview coords to offset with
        self.editEntry_Text = tk.StringVar()
        self.editEntry = ttk.Entry(self, textvariable = self.editEntry_Text, font = self.body_font)

        #Checks if selected item in column 0 or 1
        self.editEntry.insert(0, string = self.picksChoice.item(self.selectedItem[0], "text"))
        offset[0] += 15 #Offset for column 0 padding
        itemBBox[2] -= 15

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
    
    def onDelete(self, event):
        self.picksChoice.delete(self.picksChoice.selection())

    def addPick(self):
        self.picksChoice.insert('', tk.END, text="", tags="defaultFont")

    def finishedEntryEdit(self, event): #When you exit the entrybox
        positionMatched = FALSE
        for position in positionDictionary.items():
            if ((self.editEntry_Text.get().lower() == str.lower(position[0])) #Matches the display name (key)
            or (self.editEntry_Text.get().lower() in position[1])): #Matches alternative names
                self.picksChoice.item(self.selectedItem[0], text=position[0]) #Sets the box to the display name (key)
                positionMatched = TRUE
                break
        self.editEntry.destroy() #Deletes the entrybox
        if (positionMatched == FALSE): #If no match was found
            messagebox.showwarning(
                message=
                    "\"" + self.editEntry_Text.get().lower()
                    + "\" is not a valid position.")

    
    def addSuggested(self, suggestedPicks):
        for pick in suggestedPicks: 
            self.suggestedPicksView.insert('', tk.END, tags=("defaultFont", pick),
                text=re.sub(r"(\w)([A-Z])", r"\1 \2", pick["name"]),
                values=(
                    pick["college_team"],
                    re.sub(r"(\w)([A-Z])", r"\1 \2", pick["position"]),
                    pick["height"] + " in",
                    pick["weight"] + " Ib",
                    pick["pre_draft_grade"],
                    pick["overall"]
                )
            )
            self 
        self.suggestedPicksView.selection_add('I001')

class PickPositionEntry(ttk.Entry):
    def __init__(self, master, **kwargs):
        valideCommand = (master.register(self.validate), '%P')
        ttk.Entry.__init__(self, master, textvariable=master.pickEntry_Text, validate = 'key', validatecommand = valideCommand, **kwargs)
    def validate(self, valueIfAllowed):
        if valueIfAllowed:
            try:
                int(valueIfAllowed)
                return True
            except:
                return False
        return False

class ImportDataDialog(Toplevel):
    #User input for the picks that the user has as well as their top positional needs (Needs to be adjusted to be the actual user input)
    userInputPicks = ["12","47","89","124","186","222","256"]
    userInputNeeds = ["quarterback","defensiveend","runningback","cornerback"
                        ,"safety","safety","widereceiver"]

    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        self.protocol("WM_DELETE_WINDOW", self.closeEvent)
        self.master.draftPicks = None

        self.grid()

        importLabel = ttk.Label(self, text="Choose import location")
        importLabel.grid(row=0, column=0, columnspan=2)

        databaseButton = ttk.Button(self, text="CSV", command=self.csvButton_Pressed)
        databaseButton.grid(row=1, column=1)
        
        csvButton = ttk.Button(self, text="Database", command=self.databaseButton_Pressed)
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

        if (selectedFile == ""): #If no file was selected
            result = messagebox.askretrycancel( #User can either exit CSV choice or choose again
                title="Nothing was selected",
                message="No file was selcted\nWould you like to try again?")
            if (result): #If the press trey
                self.csvButton_Pressed()
            else:
                return
        else:
            self.importCSV(selectedFile = selectedFile)

    def databaseButton_Pressed(self):
        self.config(cursor="wait")
        self.grabDatabase()
        self.importDatabase()
        self.config(cursor="")
        self.grab_release()
        self.closeEvent()

    def importCSV(self, selectedFile):
        #Start of Seth's code

        #opens the csv and puts all the data in a dictionary
        import csv
        with open('/Users/sethwiley/Desktop/Draft2019.csv') as csv_file:
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
        #puts everything in game in a list and makes each item a string
        draftPicksTemp = str(self.draftPicksRaw)
        itemEnd = 0
        while(itemEnd < len(draftPicksTemp) - 2):
            itemStart = draftPicksTemp.find("{", itemEnd)
            itemEnd = draftPicksTemp.find("}", itemEnd + 1)
            itemTempEnd = itemEnd
            indentCount = draftPicksTemp.count("{", itemStart, itemEnd)
            i = 1

            while i < indentCount:
                itemEnd = draftPicksTemp.find("}", itemEnd + 1)
                i += 1
            listy.append(draftPicksTemp[itemStart + 1:itemEnd])
            #print("Appended")

            #draftPicksTemp = draftPicksTemp[itemEnd:]
        #for item in self.draftPicksRaw:
        #    item = str(item)
        #    thing = re.split(':|\n', item)
        #    listy.append(thing)
        
        everything = []
        #puts every item in a dictionary
        for item in listy:
            lines = item.splitlines()
            draftPick = {}
            for line in lines:
                line = line.replace("'", "")
                line = line.replace(" ", "")
                line = line.replace(",", "")
                line = line.replace("}", "")
                line = line.replace("{", "")
                lineSplit = line.split(":")
                draftPick[lineSplit[0]] = lineSplit[1]
            everything.append(draftPick)
        self.master.draftPicks = sorted(everything, key=lambda d: (int(d['round']), int(d['pick']))) 
        #End of Seth's 
        
    def closeEvent(self): #When theres no import or file selected when closing
        self.destroy() 
        if (self.master.draftPicks is None):
            self.master.destroy()

mainWindow = MainWindow(None) 
mainWindow.wm_title("IDK")
mainWindow.mainloop()
