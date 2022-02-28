def verarbeiten(state, choice):
    if choice == "position1":
        state = {**state, "position": "Schatzkammer"}
    elif choice == "position2":
        state = {**state, "position": "Handler"}
    elif choice == "beenden":
        state = {**state, "position": "Menue"}
    return state


def erörtern(state):
    beschreibung = "Du bist im Eingang"
    optionen = {
        "position1": "In die Schatzkammer gehen",
        "position2": "Zum Händler gehen",
    }
    if not state["treasureAvail"]:
        optionen = {**optionen, "beenden": "Spiel beenden"}
    return optionen, beschreibung
