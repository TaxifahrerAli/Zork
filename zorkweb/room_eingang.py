def verarbeiten(state, choice, nachbarraume):
    if choice == "norden":
        state = {**state, "position" : nachbarraume["norden"]}
    elif choice == "sueden":
        state = {**state, "position" : nachbarraume["sueden"]}
    elif choice == "westen":
        state = {**state, "position" : nachbarraume["westen"]}
    elif choice == "osten":
        state = {**state, "position" : nachbarraume["osten"]}
    elif choice == "beenden":
        state = {**state, "position": "Menue"}
    return state


def erörtern(state, nachbarraume):
    optionen = {}
    beschreibung = "Du bist im Eingang"
    if not state["treasureAvail"]:
        optionen = {"beenden": "Spiel beenden"}
    for key, value in nachbarraume.items():
        if value:
            if key == "norden":
                optionen = {**optionen, key : "Nach Norden"}
            elif key == "sueden":
                optionen = {**optionen, key : "Nach Sueden"}
            elif key == "westen":
                optionen = {**optionen, key : "Nach Westen"}
            elif key == "osten":
                print(optionen)
                optionen = {**optionen, key : "Nach Osten"}
    return optionen, beschreibung
