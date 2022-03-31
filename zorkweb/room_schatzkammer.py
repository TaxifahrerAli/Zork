from random import randint
from . import __init__

def verarbeiten(state, choice, nachbarraume):
    if choice == "norden":
        state = {**state, "position" : nachbarraume["norden"]}
    elif choice == "sueden":
        state = {**state, "position" : nachbarraume["sueden"]}
    elif choice == "westen":
        state = {**state, "position" : nachbarraume["westen"]}
    elif choice == "osten":
        state = {**state, "position" : nachbarraume["osten"]}
    elif choice == "drachenBekämpfen":
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


def erörtern(state, nachbarraume):
    beschreibung = "Du bist in der Schatzkammer"
    optionen = __init__.optionen_darlegen(nachbarraume)
    if state["dragonAlive"]:
        optionen = {**optionen, "drachenBekämpfen": "Drachen bekämpfen"}
    elif not state["dragonAlive"] and state["treasureAvail"]:
        optionen = {**optionen, "schatzAufheben": "Schatz aufheben"}
    return optionen, beschreibung
