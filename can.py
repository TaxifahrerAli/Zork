from random import randint

eingabe = ""
position = "Eingang"
# schatzGeöffnet = False
kampfBeendet = False
lebenspunkte = 5
auswahl = ""

if input("Gib START ein, um das Spiel zu starten. -- ") == "START": 
    print("Spiel gestartet!")
    print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer Klammer schreiben: z.B. '1)'.")

    print("Du befindest dich im %s." % position, "Du kannst in die Schatzkammer.","\nDu hast %s Lebenspunkte." % lebenspunkte)
    if input("1) Reingehen\n-- ") == "1)": 
        position = "Schatzkammer"
        print("Du befindest dich im %s." % position,"\nDu hast %s Lebenspunkte." % lebenspunkte)
        print("Du musst nun gegen den Drachen kämpfen, indem du würfelst.")
        while kampfBeendet == False:
            auswahl = input("1) Würfeln\n2) Zurück\n-- ")
            if auswahl == "1)":
                if randint(1,6) == 66:
                    print("Du hast den Drachen besiegt!")
                    auswahl = ""
                    kampfBeendet = True
                else:
                    lebenspunkte = lebenspunkte -1
                    print("Du hast %d Lebenspunkte." % lebenspunkte)
                if lebenspunkte == 0:
                    auswahl = ""
                    print("Verloren!")
                    kampfBeendet = True
            else:
                if input("Gib ENDE zum beenden ein.\n-- ") == "ENDE":
                    position = "TOD"
                    kampfBeendet = True
                    print("Ende")
        