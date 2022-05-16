from . import room_common

def verarbeiten(state, choice):
    return state


def erörtern(state):
    optionen = {}
    beschreibung = "Du bist im Raum %s" % state["position"]
    return optionen, beschreibung
