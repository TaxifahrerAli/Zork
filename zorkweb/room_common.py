def position_darlegen(nachbarraume):
    optionen = {}
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
    return optionen


def position_wechseln(choice, state, nachbarraume):
    if choice == "norden":
        state = {**state, "position" : nachbarraume["norden"]}
    elif choice == "sueden":
        state = {**state, "position" : nachbarraume["sueden"]}
    elif choice == "westen":
        state = {**state, "position" : nachbarraume["westen"]}
    elif choice == "osten":
        state = {**state, "position" : nachbarraume["osten"]}
    return state