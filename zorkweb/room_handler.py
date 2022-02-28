def verarbeiten(state, choice):
    if choice == "position1":
        state = {**state, "position": "Eingang"}
    elif choice == "position2":
        state = {**state, "position": "Brunnen"}
    elif choice == "schwertKaufen":
        state = {**state, "swordAvail": False}
    return state


def erörtern(state):
    beschreibung = "Du bist beim Händler"
    optionen = {
        "position1": "In den Eingang gehen",
        "position2": "Zum Brunnen gehen"
    }
    if state["swordAvail"]:
        optionen = {**optionen, "schwertKaufen": "Schwert kaufen"}
    return optionen, beschreibung
