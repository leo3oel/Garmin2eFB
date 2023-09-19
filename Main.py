import csv
from datetime import datetime, timedelta, time
from tkinter.filedialog import askopenfile
import configparser, locale

from GarminEntry import GarminEntry

class Main:
    
    __garminEntries = []

    def __init__(self) -> None:
        self.__readConfig()
        self.__readGarminFile()
        pass

    def __readConfig(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.__garminRows = config['garmin.rows']
        self.__activityTypes = config['garmin.activitytypes']['typesToAdd'].split(",")
        self.__efbColumns = config['efbColumns']

    def __readGarminFile(self) -> None:
        fileName = askopenfile()
        with open (fileName.name) as garminFile:
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


if __name__ == "__main__":

    # Set locale to system
    locale.setlocale(locale.LC_ALL, '')
    main = Main()