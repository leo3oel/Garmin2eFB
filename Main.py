import csv
from datetime import datetime, timedelta, time
from tkinter.filedialog import askopenfile
import configparser, locale

from GarminEntry import GarminEntry
from Gui import MainGui

class Main:
    
    __garminEntries = []
    __multiEntries = []
    __singleEntries = []

    def __init__(self) -> None:
        self.__readConfig()
        self.__readGarminFile()
        self.__mainGui = MainGui()
        self.__getEntriesToInclude()
        self.__sortEntries()
        self.__mainGui.startUserInput(self.__multiEntries, self.__singleEntries)
        self.__mainGui.mainloop()

    def __readConfig(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.__garminRows = config['garmin.rows']
        self.__activityTypes = config['garmin.activitytypes']['typesToAdd'].split(",")
        self.__efbColumns = config['efbColumns']

    def __readGarminFile(self) -> None:
        fileName = askopenfile()
        with open (fileName.name, encoding="utf-8") as garminFile:
            garminCsv = list(csv.reader(garminFile))
        self.__createEntries(garminCsv)

    def __createEntries(self, garminCsv) -> None:
        for row in garminCsv:
            activityType = row[int(self.__garminRows['activityType'])]
            if activityType in self.__activityTypes:
                self.__garminEntries.append(
                    GarminEntry(
                        self.__formatDate(row[int(self.__garminRows['startDate'])]),
                        time.fromisoformat(row[int(self.__garminRows['duration'])]),
                        self.__getPlace(row[int(self.__garminRows['title'])]),
                        locale.atof(row[int(self.__garminRows['distance'])])
                    )
                )

    def __sortEntries(self) -> None:
        ignoreList =[]
        for index, entry in enumerate(self.__garminEntries):
            multiEntries = [entry]
            for innerLoopIndex in range(index+1, len(self.__garminEntries)):
                innerEntry = self.__garminEntries[innerLoopIndex]
                if innerEntry.getPlace() == entry.getPlace() and innerEntry not in ignoreList:
                    multiEntries.append(innerEntry)
                    ignoreList.append(innerEntry)
            if len(multiEntries) > 1:
                self.__multiEntries.append(multiEntries)
            elif entry not in ignoreList:
                self.__singleEntries.append(entry)
        for entry in self. __multiEntries:
            entry = sorted(entry, key=lambda x:x.getStartDate(), reverse=True)
        self.__singleEntries = sorted(self.__singleEntries, key=lambda x:x.getStartDate(), reverse=True)

    def __formatDate(self, stringDate) -> datetime.date:
        date = datetime.strptime(stringDate, '%Y-%m-%d %H:%M:%S')
        return date
    
    def __getPlace(self, title) -> str:
        words = title.split(" ")
        place = " ".join(words[:-1])
        return place

    def __getEntriesToInclude(self) -> None:
        return None
        startDate, endDate = self.__mainGui.getStartAndEndDate()


if __name__ == "__main__":

    # Set locale to system
    locale.setlocale(locale.LC_ALL, '')
    main = Main()