from . import room_common

def verarbeiten(state, choice):
    if choice == "beenden":
        state = {**state, "position": "Menue"}
    return state


def erörtern(state):
    beschreibung = "Du bist im Eingang"
    optionen = {}
    if not state["treasureAvail"]:
        optionen = {**optionen, "beenden": "Spiel beenden"}
    return optionen, beschreibung
