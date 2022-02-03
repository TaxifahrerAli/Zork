from random import randint

position = "Eingang"
kampfBeendet = False
lebenspunkte = 5
auswahl = ""
schwert = ""
zahl = 6
schwertVerfugb = True

while input("Gib START ein, um das Spiel zu starten. -- ") == "START": 
    print("=== Spiel gestartet! ===")
    print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer Klammer schreiben: z.B. '1)'.")

    while lebenspunkte > 0 or position != "TOD":
        if position == "Eingang":
            print("Du befindest dich im EINGANG.","Du kannst in die Schatzkammer oder zum Händler gehen.")
            print("Du hast %d Lebenspunkte." % lebenspunkte, "%s" % schwert)
            auswahl = input("1) Schatzkammer\n2) Händler\n-- ")
            if auswahl == "1)": 
                position = "Schatzkammer"
            elif auswahl == "2)":
                position: "Handler"
                print(position)
        elif position == "Schatzkammer":
            print("Du befindest dich in der SCHATZKAMMER.","Du musst nun gegen den Drachen kämpfen, indem du würfelst oder du gehst zurück.")
            print("Du hast %d Lebenspunkte." % lebenspunkte, "%s" % schwert)
            while kampfBeendet == False and position != "Eingang":
                auswahl = input("1) Würfeln\n2) Zurück\n-- ")
                if auswahl == "1)":
                    if randint(1,zahl) == 6:
                        print("Du hast den Drachen besiegt!")
                        kampfBeendet = True
                    else:
                        lebenspunkte = lebenspunkte -1
                        if lebenspunkte == 0:
                            kampfBeendet = True
                            position = "TOD"
                        print("Du hast %d Lebenspunkte." % lebenspunkte)
                elif auswahl == "2)":
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
                elif auswahl == "2)":
                    position = "Eingang"
            elif schwertVerfugb == False:
                auswahl = input("1) Zurück\n-- ")
                if auswahl == "1)":
                    position = "Eingang"
    auswahl = input("Zum Beenden schreibe ENDE, zum reseten RESET-- ")
    if auswahl == "RESET":
        lebenspunkte = 5
        position = "Eingang"
    elif auswahl == "ENDE":
        print("Ende")