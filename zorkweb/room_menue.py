def verarbeiten(state, choice):
    if choice == "neuesSpiel":
        state = {
            "hp": 5,
            "position": "Eingang",
            "dragonAlive": True,
            "swordAvail": True,
            "treasureAvail": True,
            "brunnenNutzungen": 5
        }
    return state


def erörtern(state):
    beschreibung = "Du bist im Menü"
    optionen = {"neuesSpiel": "Neues Spiel starten"}
    return optionen, beschreibung
