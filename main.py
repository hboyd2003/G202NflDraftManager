from tkinter import *
from tkinter import ttk
import cfbd
root = Tk()
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
