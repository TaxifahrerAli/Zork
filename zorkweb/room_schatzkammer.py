from random import randint
from . import room_common

def verarbeiten(state, choice):
    if choice == "drachenBekämpfen":
        randomint = randint(1, 6)
        if ((randomint < 4 and not state["swordAvail"])
                or (randomint == 6 and state["swordAvail"])):
            state = {**state, "dragonAlive": False, "treasureAvail": True}
        else:
            state = {**state, "hp": state["hp"] - 1}
            if state["hp"] == 0:
                state = {**state, "position": "Menue"}
    elif choice == "schatzAufheben":
        state = {**state, "treasureAvail": False}
    return state


def erörtern(state):
    beschreibung = "Du bist in der Schatzkammer"
    optionen = {}
    if state["dragonAlive"]:
        optionen = {**optionen, "drachenBekämpfen": "Drachen bekämpfen"}
    elif not state["dragonAlive"] and state["treasureAvail"]:
        optionen = {**optionen, "schatzAufheben": "Schatz aufheben"}
    return optionen, beschreibung
