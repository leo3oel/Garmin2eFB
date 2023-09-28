import tkinter.filedialog
import csv

class Exporter:

    @staticmethod
    def exportToEFB(entries, eFBColumns):
        outputFileName = Exporter.getOutputFilename()
        with open(outputFileName, 'w', newline='') as outputFile:
            writer = csv.writer(outputFile, delimiter=';')
            writer.writerow(Exporter.getFirstLine(eFBColumns))
            for entry in entries:
                writer.writerow(Exporter.getRow(entry))

    @staticmethod
    def getOutputFilename():
        fileTypes = [('csv-Tables', '.csv')]
        fileName = tkinter.filedialog.asksaveasfilename(filetypes=fileTypes, defaultextension='filetypes')
        return fileName
    
    @staticmethod
    def getFirstLine(eFBColumns):
        firstLine = [
            eFBColumns["startdate"],
            eFBColumns["startTime"],
            eFBColumns["endDate"],
            eFBColumns["endTime"],
            eFBColumns["status"],
            eFBColumns["river"],
            eFBColumns["startPlace"],
            eFBColumns["endPlace"],
            eFBColumns["startdate"],
            eFBColumns["distance"]
        ]
        return firstLine

    @staticmethod
    def getRow(entry):
        entryDict = entry.returnEfbDict()
        row = [
            entryDict["startDate"],
            entryDict["startTime"],
            entryDict["endDate"],
            entryDict["endTime"],
            entryDict["status"],
            entryDict["river"],
            entryDict["startPlace"],
            entryDict["endPlace"],
            entryDict["distance"]
        ]
        return row
