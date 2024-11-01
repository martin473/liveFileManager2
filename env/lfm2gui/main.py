import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import os
import time
from glob import glob
import platform
import datetime
import json
from tinydb import TinyDB, Query

#windows needs to convert filepath \ into / to comply with os fpath requirements

#CREATE LISTBOX
class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""
    def __init__(self):
        self.tree = None
        self._setup_widgets() #builds gui for treebox
        self._build_tree() #builds dataset for treebox

    def _setup_widgets(self):
        s = """click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)

        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=headers, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    #DB FILE I/O
#This creates the db. This needs to be separated.
#headers needs to be grepped as the keys from the first item in the db
#data needs to be read iteratively from db for document in db for item in document column = item
    def _build_tree(self):
        for col in headers: #refers to global headers
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in fileList: #refers to global file list
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(headers[ix],width=None)<col_w:
                    self.tree.column(headers[ix], width=col_w)

#SORT ON CLICK
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

def makeDb(fpath):
    #loop creates a list of filepaths and names
    results = [y for x in os.walk(fpath) for y in glob(os.path.join(x[0], '*.als'))]
    #if windows, replace the incorrect slash created by os library 
    if platform.system() == 'Windows':
        for i, result in enumerate(results):
            results[i] = result.replace("\\","/")
    #create a new list with just the filename for display
    #these are all global vars for the earlier classes which should be refactored
    fileList = []
    dbJson =[]
    for filePath in results:
        discard, fname = os.path.split(filePath)
        #dummy star rating
        #{'id': count, 'data': {'filepath': ///, 'filename': ///, 'created': datetime, 'opened': datetime, 'rating': 0, 'tags': [],}}
        dbJson.append({'id': count, 
            'data': {'filepath': filePath, 
                'filename': fname, 
                'created': os.path.getctime(filePath), 
                'opened': os.path.getmtime(filePath), 
                'rating': 0, 
                'tags': []
                }
            })
        fileList.append((filePath, '0'))
    headers = ['File', 'Rating']
    fileDict = dict(zip(results, fileList))

#DATABASE CREATE/LOAD
if glob("db*.json"): #if db load db
    listbox = MultiColumnListbox() #load db
elif fpath: #elif path, create db
    makeDb("FOLDER TO SEARCH")
    #timezone independent (can use %z for utc offset or %Z for timezone name but it's returning blank)
    dbCreateTime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    db = TinyDB('db' + dbCreateTime + '.json')
else: #else ask for path
    print("need path dummy statement")

#GUI CREATE
window = tk.Tk()
window.title("Live File Manager")
window.mainloop()