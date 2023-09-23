from datetime import datetime, timedelta

class GarminEntry:

    def __init__(self, startDate: datetime.date, duration: datetime.time, place: str, distance: float) -> None:
        self.__startDate = startDate
        self.__duration = duration
        self.__endDate = self.__getEndDate(self.__startDate, self.__duration)
        self.__place = place
        self.__distance = distance
        self.startPlace = None
        self.endPlace = None
        self.__status = None
        self.river = None

    def __getEndDate(self, startDate: datetime.date, duration: datetime.time) -> datetime.date:
        endTime = startDate + timedelta(hours=duration.hour, minutes=duration.minute)
        return endTime
    
    def getPlace(self) -> str:
        return self.__place
    
    def getStartDate(self) -> str:
        return self.__startDate.strftime('%d.%m.%Y')
    
    def getDistance(self) -> str:
        return str(self.__distance)
    
    def setUserValues(self, startPlace: str, endPlace: str, status: str, river: str) -> None:
        self.startPlace = startPlace
        self.endPlace = endPlace
        self.__status = status
        self.river = river

    def returnEfbDict(self) -> dict:
        efbDict = {
            'startDate': self.__startDate.strftime('%d.%m.%Y'),
            'startTime': self.__startDate.strftime('%H:%M'),
            'endDate': self.__endDate.strftime('%d.%m.%Y'),
            'endTime': self.__endDate.strftime('%H:%M'),
            'status': self.__status,
            'river': self.river,
            'startPlace': self.startPlace,
            'endPlace': self.endPlace
        }
        return efbDict
