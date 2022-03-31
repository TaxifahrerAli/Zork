def verarbeiten(state, choice, nachbarraume):
    if choice == "norden":
        state = {**state, "position" : nachbarraume["norden"]}
    elif choice == "sueden":
        state = {**state, "position" : nachbarraume["sueden"]}
    elif choice == "westen":
        state = {**state, "position" : nachbarraume["westen"]}
    elif choice == "osten":
        state = {**state, "position" : nachbarraume["osten"]}
    elif choice == "trinken":
        state = {**state, "brunnenNutzungen": state["brunnenNutzungen"] - 1, "hp": 5}
    return state


def erörtern(state, nachbarraume):
    optionen = {}
    if state["brunnenNutzungen"] > 0:
        optionen = {"trinken": "Aus dem Brunnen trinken"}
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
    beschreibung = """Du bist beim Brunnen, er enthält %s Schluck Heilwasser""" % state["brunnenNutzungen"]
    return optionen, beschreibung
