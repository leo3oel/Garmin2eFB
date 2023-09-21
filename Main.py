import csv
from datetime import datetime, timedelta, time
from tkinter.filedialog import askopenfile
import configparser, locale

from GarminEntry import GarminEntry
from Gui import MainGui

class Main:
    
    __garminEntries = []

    def __init__(self) -> None:
        self.__readConfig()
        self.__readGarminFile()
        self.__mainGui = MainGui()
        self.__getEntriesToInclude()
        self.__mainGui.multipleEntry(self.__garminEntries[:3])
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