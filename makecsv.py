from csv import reader
from datetime import datetime, timedelta

def convertcsv(input):
    """"
    Takes a Garmin export as input and generates a file that can be read by eFB

1.  Filter by Activity:
        now: delete everything except kajakfahren
        later: select needed Activitys

2.  Only keep:
    Startdatum
    Startzeit
    Zeit (dauer)
    Distanz
    Ort (aus Titel)
    
3.  Download gpx files and check start and end place:
    Later

4.  Make a new CSV like:
    Startdatum;Startzeit;Enddatum;Endzeit;Status;Gewässer;von;bis;Kilometer;Bemerkung;Bootsname

        Calculate Endzeit from Startzeit + dauer
        Status = beendet
        Gewässer = input
            maybe later: extract it from 3.
        von; bis; = input
            maybe later: extract it from 3.
        Bemerkung = input
        Bootsname = select
    """

    # Set outoutlist    
    headeroutput = ["Startdatum", "Startzeit", "Enddatum", "Endzeit", "Status", "Gewässer", "von", "bis", "Kilometer", "Bemerkung", "Bootsname"]
    outputlist = []

    # TODO: change filename to inserted filename
    with open("export_garmin.csv") as garmin:
        garmin_csv = list(reader(garmin))

    # Only keep: Aktivitätstyp, Datum, Titel, Distanz, Zeit
    for item in garmin_csv:
        index = garmin_csv.index(item)
        if index>0:
            garmin_csv[index] = [item[0],datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S'),item[3],item[4],datetime.strptime(item[6][0:8],'%H:%M:%S')]

    garmin_csv.pop(0)
    #* Start making new List
    for index, item in enumerate(garmin_csv):
        startdatum = f"{item[1].day}.{item[1].month}.{item[1].year}"
        enddatum = startdatum
        startzeit = f"{item[1].hour}:{item[1].minute}"
        endzeitdatetime = item[1] + timedelta(hours=item[4].hour, minutes=item[4].minute)
        endzeit = f"{endzeitdatetime.hour}:{endzeitdatetime.minute}"
        gewaesser = "gewässer"
        
        # get startort:
        startort = ""
        for char in item[2]:
            if char == " ":
                break
            else:
                startort += char
        von = startort
        bis = "Endort"
        km = item[3]
        bemerkung = ""
        bootsname = ""

        if item[0] == "Kajakfahren":
            outputlist.append([startdatum, startzeit, enddatum, endzeit, "beendet", gewaesser, von, bis, km, bemerkung, bootsname])

    return outputlist

for item in convertcsv(None):
    print(item)