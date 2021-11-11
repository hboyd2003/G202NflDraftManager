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
    
def openMainWindows():
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="Random").grid(column=0, row=0)
    importDataDialog()
#def importCSV:

openMainWindows()
root.mainloop()