from random import randint

state = {
    "hp": 5,
    "position": "Eingang",
    "dragonAlive": True,
    "swordAvail": True,
    "treasureAvail": True
}


def show_invetory():
    print("Du hast %d Lebenspunkte." % state["hp"],
        "Du hast ein Schwert" if not state["swordAvail"] else "",
        "Du hast den Schatz" if not state["treasureAvail"] else "")


def room_eingang():
    print("Du befindest dich im EINGANG.",
        "Du kannst in die Schatzkammer oder zum Händler gehen.")
    show_invetory()
    if state["treasureAvail"]:
        memory = input("1) Schatzkammer\n2) Händler\n-- ")
        if memory == "1)":
            state["position"] = "Schatzkammer"
        elif memory == "2)":
            state["position"] = "Handler"
    elif not state["treasureAvail"]:
        memory = input("1) Schatzkammer\n2) Händler\n3) Beenden\n-- ")
        if memory == "1)":
            state["position"] = "Schatzkammer"
        elif memory == "2)":
            state["position"] = "Handler"
        elif memory == "3)":
            state["hp"] = 0


def room_schatzk():
    print("Du befindest dich in der SCHATZKAMMER."
        " Du musst nun gegen den Drachen kämpfen,"
        " indem du würfelst oder du gehst zurück.")
    show_invetory()

    if state["dragonAlive"]:
        memory = input("1) Drachen bekämpfen\n2) Zurück\n-- ")
        if memory == "1)":
            randomint = randint(1, 6)
            if ((randomint < 4 and not state["swordAvail"])
                    or (randomint == 6 and state["swordAvail"])):
                print("Du hast den Drachen besiegt!")
                state["dragonAlive"] = False
            else:
                state["hp"] = state["hp"] - 1
        elif memory == "2)":
            state["position"] = "Eingang"
    elif not state["dragonAlive"] and state["treasureAvail"]:
        memory = input("1) Schatz aufheben\n2) Zurück\n-- ")
        if memory == "1)":
            print("Schatz aufgehoben!")
            state["treasureAvail"] = False
        elif memory == "2)":
            state["position"] = "Eingang"
    elif not state["dragonAlive"] and not state["treasureAvail"]:
        if input("1) Zurück\n-- ") == "1)":
            state["position"] = "Eingang"


def room_handler():
    print("Du befindest dich beim HÄNDLER.",
        " Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück"
        " gehen.")
    show_invetory()

    if state["swordAvail"]:
        memory = input("1) Schwert Kaufen\n2) Zurück\n-- ")
        if memory == "1)":
            state["swordAvail"] = False
            state["hp"] = state["hp"] - 1  # Zusatzidee
        elif memory == "2)":
            state["position"] = "Eingang"
    else:
        memory = input("1) Zurück\n-- ")
        if memory == "1)":
            state["position"] = "Eingang"


print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer"
    " Klammer schreiben: z.B. '1)'.")  # Zusatzidee


while state["hp"] > 0:
    if state["position"] == "Eingang":
        room_eingang()

    elif state["position"] == "Schatzkammer":
        room_schatzk()

    elif state["position"] == "Handler":
        room_handler()
