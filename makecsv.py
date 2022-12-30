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