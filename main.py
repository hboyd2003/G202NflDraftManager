from tkinter import *
import tkinter as tk
import tkinter.simpledialog
from tkinter import ttk
from datetime import datetime
import cfbd
root = Tk()
frm = ttk.Frame(root, padding=10)


class MainWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master = master
        self.csvButton = tk.Button(self, text="CSV")
        self.csvButton.grid(column=2, row=1)
        ImportDataDialog(root)
        self.picksChoice = ttk.Treeview(columns=("Name", "Pick", "Height"), show="headings")
        self.picksChoice.grid(column=0, row=0)
    def dataImported(self):
        self.picksChoice.insert('', tk.END, values=draftPicks)

class ImportDataDialog(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
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
        MainWindow.dataImported()
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
        global draftPicks
        draftPicks  = api_instance.get_draft_picks(year=datetime.now().year)
        return

    def importDatabase(self):
        #Start of Seth's code
        listy = []
        import re
        #puts everything in game in a list and makes each item a string
        for line in draftPicks:
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
            
        draftPicks=everything
        print(everything[0])
        #End of Seth's code
        
root.wm_title("IDK")
frm.grid()
mainWindow = MainWindow(master=frm)
root.mainloop()
dlg = Toplevel(root)
def removeDlg():
    dlg.grab_release()
    dlg.destroy()
def importDataDialog():
    ttk.Entry(root).grid() # something to interact with
    ttk.Label(dlg, text="Choose import location").grid(column=0, row=0)
    ttk.Button(dlg, text="CSV", command=removeDlg).grid(column=1, row=1)
    ttk.Button(dlg, text="Database", command=grabDatabase).grid(column=2, row=1)
    dlg.protocol("WM_DELETE_WINDOW", root.destroy) #Close closes whole program
    dlg.transient(root)
    dlg.wait_visibility()
    dlg.grab_set()
    dlg.wait_window()
def grabDatabase():
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = 'PrEoN+4gLLbOFbNh9Fevv0hRyYTBNVmQ3DLnhwvTQn06OJqatwpxvTVhR5nLrjFx'
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    api_instance = cfbd.DraftApi(cfbd.ApiClient(configuration))
    global games
    games = api_instance.get_draft_picks(year=2018)
    removeDlg()
    
    #Start of Seth's code
    listy = []
    import re
    #puts everything in game in a list and makes each item a string
    for line in games:
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

    print(everything[0])
    #End of Seth's code
        
    
def openMainWindows():
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Random").grid(column=0, row=0)
    importDataDialog()
#def importCSV:

openMainWindows()
root.mainloop()
