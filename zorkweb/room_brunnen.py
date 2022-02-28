def verarbeiten(state, choice):
    if choice == "position":
        state = {**state, "position": "Handler"}
    elif choice == "trinken":
        state = {**state, "brunnenNutzungen": state["brunnenNutzungen"] - 1, "hp": 5}
    return state


def erörtern(state):
    optionen = {"position": "Zum Händler gehen"}
    if state["brunnenNutzungen"] > 0:
        optionen = {**optionen, "trinken": "Aus dem Brunnen trinken"}
    beschreibung = "Du bist beim Brunnen, er enthält %s Schluck Heilwasser" % state["brunnenNutzungen"]
    return optionen, beschreibung
