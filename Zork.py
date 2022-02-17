from random import randint
import json

state = {
    "hp": 5,
    "position": "Menue",
    "dragonAlive": True,
    "swordAvail": True,
    "treasureAvail": True,
}


def ask_user(obj):
    auswahlString = ""
    auswahlNummer = 1
    for key, value in obj.items():
        print("%s) %s" % (auswahlNummer,value))
        auswahlNummer = auswahlNummer + 1
    auswahlString = input("-- ")
    auswahlNummer = 1
    for key, value in obj.items():
        if auswahlString == "%d" % auswahlNummer:
            return key
        auswahlNummer += 1
    return ask_user(obj)


def show_invetory():
    print("Du hast %d Lebenspunkte." % state["hp"],
        "Du hast ein Schwert." if not state["swordAvail"] else "",
        "Du hast den Schatz." if not state["treasureAvail"] else "")


def save_game(choice, state):
    if choice == "speichernBeenden":
        with open('save.json', 'w') as fp:
            fp.write(json.dumps(state))
        return {**state, "hp": 0}
    else:
        return state


def spiel_menue(state):
    class SpeichernFehler(Exception):
        pass
    choice = ask_user({"neuesSpiel": "Neues Spiel", "spielLaden": "Spiel laden"})
    if choice == "neuesSpiel":
        print("Spiel wird gestartet...") #Zusatzidee
        return {**state, "position" : "Eingang"}
    elif choice == "spielLaden":
        try:
            with open("save.json","r") as fp:
                return json.loads("%s" %fp.read())
        except json.decoder.JSONDecodeError:
            raise SpeichernFehler("Der Speicherstand hat keinen Inhalt.")
    return state


def room_eingang(state):
    print("Du befindest dich im EINGANG.",
        "Du kannst in die Schatzkammer oder zum Händler gehen.")
    show_invetory()
    choices = {
        "schatzkammer": "Schatzkammer",
        "handler": "Händler",
        "speichernBeenden": "Speichern und Beenden"
    }
    if not state["treasureAvail"]:
        choices["beenden"] = "Beenden"

    choice = ask_user(choices)
    if choice == "schatzkammer":
        return {**state, "position": "Schatzkammer"}
    elif choice == "handler":
        return {**state, "position": "Handler"}
    elif choice == "beenden":
        return {**state, "hp": 0}
    else:
        return save_game(choice, state)

    return state


def room_schatzk(state):
    print("Du befindest dich in der SCHATZKAMMER."
        " Du musst nun gegen den Drachen kämpfen,"
        " indem du würfelst oder du gehst zurück.")
    show_invetory()
    choices = {
        "schatzAufheben": "Schatz aufheben",
        "drachenBekampfen": "Drachen bekämpfen",
        "zurück": "Zurück",
        "speichernBeenden": "Speichern und Beenden"
    }
    if state["dragonAlive"]:
        del choices["schatzAufheben"]
    elif not state["dragonAlive"] and state["treasureAvail"]:
        del choices["drachenBekampfen"]
    elif not state["dragonAlive"] and not state["treasureAvail"]:
        del choices["drachenBekampfen"]
        del choices["schatzAufheben"]
    choice = ask_user(choices)

    if choice == "drachenBekampfen":
        randomint = randint(1, 6)
        if ((randomint < 4 and not state["swordAvail"])
                or (randomint == 6 and state["swordAvail"])):
            print("Du hast den Drachen besiegt!")
            return {**state, "dragonAlive": False}
        else:
            return {**state, "hp": state["hp"] - 1}
    elif choice == "schatzAufheben":
        print("Schatz aufgehoben!")
        return {**state, "treasureAvail": False}
    elif choice == "zurück":
        return {**state, "position": "Eingang"}
    elif choice == "speichernBeenden":
        return save_game(choice, state)

    return state


def room_handler(state):
    print("Du befindest dich beim HÄNDLER.",
        "Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück"
        " gehen.")
    show_invetory()
    choices = {
        "schwertKaufen" : "Schwert kaufen",
        "zurück" : "Zurück",
        "speichernBeenden" : "Speichern und Beenden"
    }
    if not state["swordAvail"]:
        del choices["schwertKaufen"]
    choice = ask_user(choices)

    if choice == "schwertKaufen":
        return {**state, "swordAvail": False}
    elif choice == "zurück":
        return {**state, "position" : "Eingang"}
    elif choice == "speichernBeenden":
        return save_game(choice, state)

    return state


while state["hp"] > 0:
    if state["position"] == "Menue":
        state = spiel_menue(state)

    elif state["position"] == "Eingang":
        state = room_eingang(state)

    elif state["position"] == "Schatzkammer":
        state = room_schatzk(state)

    elif state["position"] == "Handler":
        state = room_handler(state)
