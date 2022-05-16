from . import room_common

def verarbeiten(state, choice):
    if choice == "schwertKaufen":
        state = {**state, "swordAvail": False}
    return state


def erörtern(state):
    beschreibung = "Du bist beim Haendler"
    optionen = {}
    if state["swordAvail"]:
        optionen = {**optionen, "schwertKaufen": "Schwert kaufen"}
    return optionen, beschreibung
