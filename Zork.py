from random import randint

hp = 5
position = "Eingang"
dragonAlive = True
swordAvail = True
treasureAvail = True


def show_invetory():
    print("Du hast %d Lebenspunkte." % hp,
        "Du hast ein Schwert" if not swordAvail else "",
        "Du hast den Schatz" if not treasureAvail else "")


print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer"
    " Klammer schreiben: z.B. '1)'.")  # Zusatzidee

while hp > 0:

    if position == "Eingang":
        print("Du befindest dich im EINGANG.",
            "Du kannst in die Schatzkammer oder zum Händler gehen.")
        show_invetory()
        if treasureAvail:
            memory = input("1) Schatzkammer\n2) Händler\n-- ")
            if memory == "1)":
                position = "Schatzkammer"
            elif memory == "2)":
                position = "Handler"
        elif not treasureAvail:
            memory = input("1) Schatzkammer\n2) Händler\n3) Beenden\n-- ")
            if memory == "1)":
                position = "Schatzkammer"
            elif memory == "2)":
                position = "Handler"
            elif memory == "3)":
                hp = 0

    elif position == "Schatzkammer":
        print("Du befindest dich in der SCHATZKAMMER."
            " Du musst nun gegen den Drachen kämpfen,"
            " indem du würfelst oder du gehst zurück.")
        show_invetory()

        if dragonAlive:
            memory = input("1) Drachen bekämpfen\n2) Zurück\n-- ")
            if memory == "1)":
                randomint = randint(1, 6)
                if ((randomint < 4 and not swordAvail)
                        or (randomint == 6 and swordAvail)):
                    print("Du hast den Drachen besiegt!")
                    dragonAlive = False
                else:
                    hp = hp - 1
            elif memory == "2)":
                position = "Eingang"
        elif not dragonAlive and treasureAvail:
            memory = input("1) Schatz aufheben\n2) Zurück\n-- ")
            if memory == "1)":
                print("Schatz aufgehoben!")
                treasureAvail = False
            elif memory == "2)":
                position = "Eingang"
        elif not dragonAlive and not treasureAvail:
            if input("1) Zurück\n-- ") == "1)":
                position = "Eingang"

    elif position == "Handler":
        print("Du befindest dich beim HÄNDLER.",
            " Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück"
            " gehen.")
        show_invetory()

        if swordAvail:
            memory = input("1) Schwert Kaufen\n2) Zurück\n-- ")
            if memory == "1)":
                sword = "Du hast ein Schwert"
                swordAvail = False
                hp = hp - 1  # Zusatzidee
            elif memory == "2)":
                position = "Eingang"
        else:
            memory = input("1) Zurück\n-- ")
            if memory == "1)":
                position = "Eingang"
