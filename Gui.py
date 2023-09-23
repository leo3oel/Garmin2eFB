import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime

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

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Garmin2eFB")
        self.__mainFrame = tk.Frame(self)
        self.__mainFrame.pack(anchor=tk.CENTER, padx=100, pady=50)
        placeHolderLB = tk.Label(self.__mainFrame, text="Garmin2eFB")
        placeHolderLB.pack()

    def getStartAndEndDate(self):
        dateSelection = DateSelection(self, "Timeframe Selection")
        return dateSelection.result

    def multipleEntry(self, listOfGarminEntries):
        self.__clearMainFrame()
        infoLB = tk.Label(self.__mainFrame, 
                          text="\
There are multiple activities at the same place.\n \
Select all activities with same start- and endplace.")
        infoLB.pack(anchor=tk.N)
        multipleEntriesFrame = tk.Frame(self.__mainFrame)
        multipleEntriesFrame.pack(anchor=tk.N)
        self.__addFirstRowMultipleEntry(multipleEntriesFrame)
        self.__multipleEntriesSelection = []
        row = 1
        for entry in listOfGarminEntries:
            singleEntry = self.__addSingleEntryToList(entry, multipleEntriesFrame, row)
            self.__multipleEntriesSelection.append(singleEntry)
            row = row+1
        self.__addEntryFields(listOfGarminEntries[0])
        self.__addControlButtons(True)
        """
        TODO:
        entry fields for places/river
        buttons for previous/single entry/save/next
        
        Use the group number from above to make going backwards possible for multiple entries

        Call entry fields from inside main gui to make going back and forth between multiple entries and singlenetries possible
        """

    def __addEntryFields(self, entry):
        self.__startPlaceVar = tk.StringVar()
        self.__endPlaceVar = tk.StringVar()
        self.__riverVar = tk.StringVar()
        self.__insertValues(entry)
        entFrame = tk.Frame(self.__mainFrame)
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

    def __addControlButtons(self, multiple=False):
        btnFrame = tk.Frame(self.__mainFrame)
        btnFrame.pack(anchor=tk.N)
        previousBtn = tk.Button(btnFrame, text="Previous", command=self.__previousEntry)
        previousBtn.grid(row=0, column=0, pady=5, padx=5)
        if multiple: 
            saveTogetherBtn = tk.Button(btnFrame, text="Save Selected", command=self.__saveSelected)
            saveTogetherBtn.grid(row=0, column=1, pady=5, padx=5)
        nextBtn = tk.Button(btnFrame, text="Next", command=self.__nextEntry)
        nextBtn.grid(row=0, column=2, pady=5, padx=5)

    def __insertValues(self, entry):
        if entry.startPlace:
            self.__startPlaceVar = entry.startPlace
            self.__endPlaceVar = entry.endPlace
            self.__riverVar = entry.river

    def __previousEntry(self):
        pass

    def __nextEntry(self):
        pass

    def __saveSelected(self):
        leftOverEntries = []
        for entry in self.__multipleEntriesSelection:
            if entry[1].get() == 1:
                self.__saveSingleEntry(entry[0])
            else:
                leftOverEntries.append(entry[0])
        if leftOverEntries:
            self.multipleEntry(leftOverEntries)
        else:
            self.__nextEntry()

    def __saveSingleEntry(self, entry):
        entry.setUserValues(
            self.__startPlaceVar.get(),
            self.__endPlaceVar.get(),
            "beendet",
            self.__riverVar.get()
        )

    def __addSingleEntryToList(self, entry, frame, row):
        startDateLB = tk.Label(frame, text=entry.getStartDate())
        startDateLB.grid(row=row, column=0, padx=5, pady=5)
        placeLB = tk.Label(frame, text=entry.getPlace())
        placeLB.grid(row=row, column=1, padx=5, pady=5)
        distanceLB = tk.Label(frame, text=entry.getDistance())
        distanceLB.grid(row=row, column=2, padx=5, pady=5)
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
    

if __name__ == "__main__":
    main = MainGui()
    result1, result2 = main.getStartAndEndDate()
    print(result1)