from random import randint

position = "Eingang"
kampfBeendet = False
lebenspunkte = 5
auswahl = ""
schwert = ""
zahl = 6
schwertVerfugb = True
schatzVerfugb = True

print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer Klammer schreiben: z.B. '1)'.")

while lebenspunkte > 0:
    if position == "Eingang":
        print("Du befindest dich im EINGANG.","Du kannst in die Schatzkammer oder zum Händler gehen.")
        print("Du hast %d Lebenspunkte." % lebenspunkte, "%s" % schwert)
        auswahl = input("1) Schatzkammer\n2) Händler\n-- ")
        if auswahl == "1)": 
            position = "Schatzkammer"
        elif auswahl == "2)":
            position = "Handler"
    elif position == "Schatzkammer":
        print("Du befindest dich in der SCHATZKAMMER.","Du musst nun gegen den Drachen kämpfen, indem du würfelst oder du gehst zurück.")
        print("Du hast %d Lebenspunkte." % lebenspunkte, "%s" % schwert)
        if kampfBeendet == False:
            auswahl = input("1) Drachen bekämpfen\n2) Zurück\n-- ")
            if auswahl == "1)":
                if randint(1,zahl) < 4 and zahl == 3:
                    print("Du hast den Drachen besiegt!")
                    kampfBeendet = True
                elif randint(1,zahl) == 6 and zahl == 6:
                    print("Du hast den Drachen besiegt!")
                    kampfBeendet = True
                else:
                    lebenspunkte = lebenspunkte -1
                    if lebenspunkte == 0:
                        kampfBeendet = True
            elif auswahl == "2)":
                    position = "Eingang"
        elif kampfBeendet == True and schatzVerfugb == True:
            auswahl = input("1) Schatz aufheben\n2) Zurück\n-- ")
            if auswahl == "1)":
                print("Schatz aufgehoben!")
                schatzVerfugb = False
            elif auswahl == "2)":
                position = "Eingang"
        elif kampfBeendet == True and schatzVerfugb != True:
            if input("1) Zurück\n-- ") == "1)":
                position = "Eingang"
    elif position == "Handler":
        print("Du befindest dich beim HÄNDLER.","Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück gehen.")
        print("Du hast %d Lebenspunkte." % lebenspunkte, "%s" % schwert)
        if schwertVerfugb == True:
            auswahl = input("1) Schwert Kaufen\n2) Zurück\n-- ")
            if auswahl == "1)":
                schwert = "Du hast ein Schwert"
                zahl = 3
                schwertVerfugb = False
                lebenspunkte = lebenspunkte -1
            elif auswahl == "2)":
                position = "Eingang"
        elif schwertVerfugb == False:
            auswahl = input("1) Zurück\n-- ")
            if auswahl == "1)":
                position = "Eingang"