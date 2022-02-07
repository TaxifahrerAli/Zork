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


def room_eingang(state):
    newstate = state
    print("Du befindest dich im EINGANG.",
        "Du kannst in die Schatzkammer oder zum Händler gehen.")
    show_invetory()
    if state["treasureAvail"]:
        memory = input("1) Schatzkammer\n2) Händler\n-- ")
        if memory == "1)":
            newstate["position"] = "Schatzkammer"
        elif memory == "2)":
            newstate["position"] = "Handler"
    elif not state["treasureAvail"]:
        memory = input("1) Schatzkammer\n2) Händler\n3) Beenden\n-- ")
        if memory == "1)":
            newstate["position"] = "Schatzkammer"
        elif memory == "2)":
            newstate["position"] = "Handler"
        elif memory == "3)":
            newstate["hp"] = 0
    return newstate



def room_schatzk(state):
    newstate = state
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
                newstate["dragonAlive"] = False
            else:
                newstate["hp"] = state["hp"] - 1
        elif memory == "2)":
            newstate["position"] = "Eingang"
    elif not state["dragonAlive"] and state["treasureAvail"]:
        memory = input("1) Schatz aufheben\n2) Zurück\n-- ")
        if memory == "1)":
            print("Schatz aufgehoben!")
            newstate["treasureAvail"] = False
        elif memory == "2)":
            newstate["position"] = "Eingang"
    elif not state["dragonAlive"] and not state["treasureAvail"]:
        if input("1) Zurück\n-- ") == "1)":
            newstate["position"] = "Eingang"
    return newstate



def room_handler(state):
    newstate = state
    print("Du befindest dich beim HÄNDLER.",
        " Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück"
        " gehen.")
    show_invetory()

    if state["swordAvail"]:
        memory = input("1) Schwert Kaufen\n2) Zurück\n-- ")
        if memory == "1)":
            newstate["swordAvail"] = False
            newstate["hp"] = state["hp"] - 1  # Zusatzidee
        elif memory == "2)":
            newstate["position"] = "Eingang"
    else:
        memory = input("1) Zurück\n-- ")
        if memory == "1)":
            newstate["position"] = "Eingang"
    return newstate


print("Um eine Richtung auszuwählen musst du lediglich die Zahl mit einer"
    " Klammer schreiben: z.B. '1)'.")  # Zusatzidee

while state["hp"] > 0:
    if state["position"] == "Eingang":
        state = room_eingang(state)

    elif state["position"] == "Schatzkammer":
        state = room_schatzk(state)

    elif state["position"] == "Handler":
        state = room_handler(state)
