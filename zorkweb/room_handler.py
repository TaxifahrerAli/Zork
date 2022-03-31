def verarbeiten(state, choice, nachbarraume):
    if choice == "norden":
        state = {**state, "position" : nachbarraume["norden"]}
    elif choice == "sueden":
        state = {**state, "position" : nachbarraume["sueden"]}
    elif choice == "westen":
        state = {**state, "position" : nachbarraume["westen"]}
    elif choice == "osten":
        state = {**state, "position" : nachbarraume["osten"]}
    elif choice == "schwertKaufen":
        state = {**state, "swordAvail": False}
    return state


def erörtern(state, nachbarraume):
    optionen = {}
    beschreibung = "Du bist beim Händler"
    if state["swordAvail"]:
        optionen = {"schwertKaufen": "Schwert kaufen"}
    for key, value in nachbarraume.items():
        if value:
            if key == "norden":
                optionen = {**optionen, key : "Nach Norden"}
            elif key == "sueden":
                optionen = {**optionen, key : "Nach Sueden"}
            elif key == "westen":
                optionen = {**optionen, key : "Nach Westen"}
            elif key == "osten":
                optionen = {**optionen, key : "Nach Osten"}
    return optionen, beschreibung
