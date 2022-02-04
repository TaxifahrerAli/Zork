from random import randint

position = "Eingang"
fightOver = False
hp = 5
memory = ""
sword = ""
randomint = 0
swordAvail = True
treasureAvail = True

print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer Klammer schreiben: z.B. '1)'.")#Zusatzidee

while hp > 0:
    if position == "Eingang":
        print("Du befindest dich im EINGANG.","Du kannst in die Schatzkammer oder zum Händler gehen.")
        print("Du hast %d Lebenspunkte." % hp, "%s" % sword)
        if treasureAvail == True:
            memory = input("1) Schatzkammer\n2) Händler\n-- ")
            if memory == "1)": 
                position = "Schatzkammer"
            elif memory == "2)":
                position = "Handler"
        elif treasureAvail == False:
            memory = input("1) Schatzkammer\n2) Händler\n3) Beenden\n-- ")
            if memory == "1)": 
                position = "Schatzkammer"
            elif memory == "2)":
                position = "Handler"
            elif memory == "3)":
                hp = 0
    elif position == "Schatzkammer":
        print("Du befindest dich in der SCHATZKAMMER.","Du musst nun gegen den Drachen kämpfen, indem du würfelst oder du gehst zurück.")
        print("Du hast %d Lebenspunkte." % hp, "%s" % sword)
        if fightOver == False:
            memory = input("1) Drachen bekämpfen\n2) Zurück\n-- ")
            if memory == "1)":
                randomint = randint(1,6)
                if ((randomint < 4 and swordAvail == False) or (randomint == 6 and swordAvail == True)) and hp > 0:
                    print("Du hast den Drachen besiegt!")
                    fightOver = True
                elif hp == 0:
                    hp = hp -1
                    if hp == 0:
                        fightOver = True
            elif memory == "2)":
                    position = "Eingang"
        elif fightOver == True and treasureAvail == True:
            memory = input("1) Schatz aufheben\n2) Zurück\n-- ")
            if memory == "1)":
                print("Schatz aufgehoben!")
                treasureAvail = False
            elif memory == "2)":
                position = "Eingang"
        elif fightOver == True and treasureAvail != True:
            if input("1) Zurück\n-- ") == "1)":
                position = "Eingang"
    elif position == "Handler":
        print("Du befindest dich beim HÄNDLER.","Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück gehen.")
        print("Du hast %d Lebenspunkte." % hp, "%s" % sword)
        if swordAvail == True:
            memory = input("1) Schwert Kaufen\n2) Zurück\n-- ")
            if memory == "1)":
                sword = "Du hast ein Schwert"
                randomMax = 3
                swordAvail = False
                hp = hp -1 #Zusatzidee
            elif memory == "2)":
                position = "Eingang"
        elif swordAvail == False:
            memory = input("1) Zurück\n-- ")
            if memory == "1)":
                position = "Eingang"