import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime
from Exporter import Exporter

class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

class DateSelection(simpledialog.Dialog):
    
    def body(self, parent):
        mainLB = tk.Label(parent, text="Enter dates in format dd.mm.yyyy")
        mainLB.grid(row=0, column=0, columnspan=2, padx=5, pady=20)
        startDateLB = tk.Label(parent, text="Start Date:")
        startDateLB.grid(row=1, column=0, padx=5, pady=5)
        endDateLB = tk.Label(parent, text="End Date:")
        endDateLB.grid(row=2, column=0, padx=5, pady=5)
        
        self.startDateET = tk.Entry(parent)
        self.endDateET = tk.Entry(parent)
        self.startDateET.grid(row=1, column=1, padx=5, pady=5)
        self.endDateET.grid(row=2, column=1, padx=5, pady=5)
        return self.startDateET 
    
    def apply(self) -> None:
        startDate = self.startDateET.get()
        endDate = self.endDateET.get()
        try:
            startDate = datetime.strptime(startDate, '%d.%m.%Y')
            endDate = datetime.strptime(endDate, '%d.%m.%Y')
            self.result = (startDate, endDate)
        except:
            messagebox.showerror("Error", "Date must be in format dd.mm.yyyy")
            self.result = (None, None)


class MainGui(tk.Tk):

    def __init__(self, eFBColumns):
        self.__eFBColumns = eFBColumns
        tk.Tk.__init__(self)
        self.title("Garmin2eFB")
        self.minsize(width=500, height=200)
        self.__mainFrame = tk.Frame(self)
        self.__mainFrame.pack(anchor=tk.CENTER, padx=100, pady=50)
        placeHolderLB = tk.Label(self.__mainFrame, text="Garmin2eFB")
        placeHolderLB.pack()

    def createScrollableFrame(self, topFrame):
        self.canvas = tk.Canvas(topFrame, width=600, height=800)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(topFrame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        scrollableFrame = tk.Frame(self.canvas)
        self.canvas.create_window((300, 300), window=scrollableFrame, anchor=tk.NW)

        return scrollableFrame

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def getStartAndEndDate(self):
        dateSelection = DateSelection(self, "Timeframe Selection")
        return dateSelection.result
    
    def startUserInput(self, multiEntries, singleEntries):
        self.__currentMultiEntry = 0
        self.__currentSingleEntry = 0
        self.__multiEntries = multiEntries
        self.__singleEntries = singleEntries
        if len(multiEntries) > self.__currentMultiEntry:
            self.multipleEntry(multiEntries[0])
        elif len(singleEntries) > self.__currentSingleEntry:
            self.singleEntry(singleEntries[0])

    def singleEntry(self, entry):
        self.__clearMainFrame()
        singleEntriesFrame = tk.Frame(self.__mainFrame)
        singleEntriesFrame.pack(anchor=tk.N)
        self.__addSingleEntry(entry, singleEntriesFrame, 0, False)
        self.__addEntryFields(entry)
        self.__addControlButtons()

    def multipleEntry(self, listOfGarminEntries):
        self.__clearMainFrame()
        self.__scrollable = self.createScrollableFrame(self.__mainFrame)
        infoLB = tk.Label(self.__scrollable, 
                          text="\
There are multiple activities at the same place.\n \
Select all activities with same start- and endplace.")
        infoLB.pack(anchor=tk.N)
        multipleEntriesFrame = tk.Frame(self.__scrollable)
        multipleEntriesFrame.pack(anchor=tk.N)
        self.__addFirstRowMultipleEntry(multipleEntriesFrame)
        self.__multipleEntriesSelection = []
        row = 1
        for entry in listOfGarminEntries:
            singleEntry = self.__addSingleEntry(entry, multipleEntriesFrame, row)
            self.__multipleEntriesSelection.append(singleEntry)
            row = row+1
        self.__addEntryFields(listOfGarminEntries[0], self.__scrollable)
        self.__addControlButtons(True, self.__scrollable)

    def __addEntryFields(self, entry, frame=None):
        if not frame:
            frame = self.__mainFrame
        self.__startPlaceVar = tk.StringVar()
        self.__endPlaceVar = tk.StringVar()
        self.__riverVar = tk.StringVar()
        self.__insertValues(entry)
        entFrame = tk.Frame(frame)
        entFrame.pack(anchor=tk.N)
        startPlaceLB = tk.Label(entFrame, text="Start Place")
        startPlaceLB.grid(row=0, column=0, padx=5, pady=5)
        startPlaceEnt = tk.Entry(entFrame, textvariable=self.__startPlaceVar)
        startPlaceEnt.grid(row=0, column=1, padx=5, pady=5)
        endPlaceLB = tk.Label(entFrame, text="End Place")
        endPlaceLB.grid(row=1, column=0, padx=5, pady=5)
        endPlaceEnt = tk.Entry(entFrame, textvariable=self.__endPlaceVar)
        endPlaceEnt.grid(row=1, column=1, padx=5, pady=5)
        riverLB = tk.Label(entFrame, text="River")
        riverLB.grid(row=2, column=0, padx=5, pady=5)
        riverEnt = tk.Entry(entFrame, textvariable=self.__riverVar)
        riverEnt.grid(row=2, column=1, padx=5, pady=5)

    def __addControlButtons(self, multiple=False, frame=None):
        if not frame:
            frame = self.__mainFrame
        btnFrame = tk.Frame(frame)
        btnFrame.pack(anchor=tk.N)
        previousBtn = tk.Button(btnFrame, text="Previous", command=self.__previousEntry)
        previousBtn.grid(row=0, column=0, pady=5, padx=5)
        ignoreEntryBtn = tk.Button(btnFrame, text="Ignore Entry", command=self.__ignoreCurrentEntry)
        ignoreEntryBtn.grid(row=0, column=1, pady=5, padx=5)
        if multiple: 
            saveTogetherBtn = tk.Button(btnFrame, text="Save Selected", command=self.__saveSelected)
            saveTogetherBtn.grid(row=0, column=2, pady=5, padx=5)
        nextBtn = tk.Button(btnFrame, text="Next", command=self.__nextEntry)
        nextBtn.grid(row=0, column=3, pady=5, padx=5)

    def __insertValues(self, entry):
        if entry.startPlace:
            self.__startPlaceVar.set(entry.startPlace)
            self.__endPlaceVar.set(entry.endPlace)
            self.__riverVar.set(entry.river)

    def __previousEntry(self):
        if (self.__currentMultiEntry>=0) and (self.__currentMultiEntry != len(self.__multiEntries)):
            leftOverEntries = self.__saveSelected()
            if not leftOverEntries:
                self.__currentMultiEntry -= 1
                self.multipleEntry(self.__multiEntries[self.__currentMultiEntry])
        elif self.__currentSingleEntry>0:
            self.__saveSingleEntry(self.__singleEntries[self.__currentSingleEntry])
            self.__currentSingleEntry -= 1
            self.singleEntry(self.__singleEntries[self.__currentSingleEntry])
        elif self.__currentSingleEntry == 0:
            self.__saveSingleEntry(self.__singleEntries[self.__currentSingleEntry])
            self.__currentMultiEntry -= 1
            self.multipleEntry(self.__multiEntries[self.__currentMultiEntry])

    def __nextEntry(self):
        if self.__currentMultiEntry < len(self.__multiEntries)-1:
            leftoverEntries = self.__saveSelected()
            if not leftoverEntries:
                self.__currentMultiEntry += 1
                self.multipleEntry(self.__multiEntries[self.__currentMultiEntry])
        elif self.__currentMultiEntry == len(self.__multiEntries)-1:
            leftoverEntries = self.__saveSelected()
            if not leftoverEntries:
                self.__currentMultiEntry += 1
                self.singleEntry(self.__singleEntries[self.__currentSingleEntry])
        elif self.__currentSingleEntry < len(self.__singleEntries)-1:
            self.__saveSingleEntry(self.__singleEntries[self.__currentSingleEntry])
            self.__currentSingleEntry+=1
            self.singleEntry(self.__singleEntries[self.__currentSingleEntry])
        elif self.__currentSingleEntry == len(self.__singleEntries)-1:
            self.__saveSingleEntry(self.__singleEntries[self.__currentSingleEntry])
            if messagebox.askyesno("Finish Entry", "Do you want to stop the entry and export to csv?"):
                entries = self.__combineEntries()
                Exporter.exportToEFB(entries, self.__eFBColumns)
                self.quit()

    def __ignoreCurrentEntry(self):
        if self.__currentMultiEntry < len(self.__multiEntries)-1:
            self.__multiEntries.pop(self.__currentMultiEntry)
            self.multipleEntry(self.__multiEntries[self.__currentMultiEntry])
        elif self.__currentMultiEntry == len(self.__multiEntries)-1:
            self.__multiEntries.pop(self.__currentMultiEntry)
            self.singleEntry(self.__singleEntries[self.__currentSingleEntry])
        elif self.__currentSingleEntry < len(self.__singleEntries)-1:
            self.__singleEntries.pop(self.__currentSingleEntry)
            if self.__currentSingleEntry < len(self.__singleEntries):
                self.singleEntry(self.__singleEntries[self.__currentSingleEntry])

    def __saveSelected(self):
        leftOverEntries = []
        for entry in self.__multipleEntriesSelection:
            if entry[1].get() == 1:
                self.__saveSingleEntry(entry[0])
            else:
                leftOverEntries.append(entry[0])
        if leftOverEntries:
            self.multipleEntry(leftOverEntries)
            return True
        return False

    def __saveSingleEntry(self, entry):
        entry.setUserValues(
            self.__startPlaceVar.get(),
            self.__endPlaceVar.get(),
            "beendet",
            self.__riverVar.get()
        )

    def __addSingleEntry(self, entry, frame, row, checkbox=True):
        startDateLB = tk.Label(frame, text=entry.getStartDate())
        startDateLB.grid(row=row, column=0, padx=5, pady=5)
        placeLB = tk.Label(frame, text=entry.getPlace())
        placeLB.grid(row=row, column=1, padx=5, pady=5)
        distanceLB = tk.Label(frame, text=entry.getDistance())
        distanceLB.grid(row=row, column=2, padx=5, pady=5)
        if checkbox:
            checkBoxVar = tk.IntVar()
            checkBoxVar.set(1)
            checkBox = tk.Checkbutton(frame, text="", onvalue=1, offvalue=0, variable=checkBoxVar)
            checkBox.grid(row=row, column=3, padx=5, pady=5)
            return [entry, checkBoxVar]

    def __addFirstRowMultipleEntry(self, frame):
        startDateLB = tk.Label(frame, text="Start Date")
        startDateLB.grid(row=0, column=0, padx=5, pady=5)
        placeLB = tk.Label(frame, text="Place")
        placeLB.grid(row=0, column=1, padx=5, pady=5)
        distanceLB = tk.Label(frame, text="Distance")
        distanceLB.grid(row=0, column=2, padx=5, pady=5)
        checkBox = tk.Label(frame, text="Add to group")
        checkBox.grid(row=0, column=3, padx=5, pady=5)

    def __clearMainFrame(self):
        self.__mainFrame.destroy()
        self.__mainFrame = tk.Frame(self)
        self.__mainFrame.pack()
    
    def __combineEntries(self) -> list:
        entriesList = []
        for multientry in self.__multiEntries:
            for entry in multientry:
                entriesList.append(entry)
        for entry in self.__singleEntries:
            entriesList.append(entry)
        sortedEntries = sorted(entriesList, key=lambda x: x.getStartDatetime())
        return entriesList

if __name__ == "__main__":
    main = MainGui()
    result1, result2 = main.getStartAndEndDate()
    print(result1)