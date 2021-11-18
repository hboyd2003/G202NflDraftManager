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
        print("Done")
        self.controller.draftPicks = everything
        print(everything[0])
        #End of Seth's code
    def get_draftPicks(self):
        return self.draftPicks
        
root.wm_title("IDK")
frm.grid()
mainWindow = MainWindow(master=frm)
root.mainloop()