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
        auswahlString = auswahlString + "%s)" % auswahlNummer + " %s\n" % value
        auswahlNummer = auswahlNummer + 1
    auswahlString = input(auswahlString + "-- ")
    if auswahlString == "1)":
        return list(obj)[0]
    elif auswahlString == "2)":
        return list(obj)[1]
    elif auswahlString == "3)":
        return list(obj)[2]
    elif auswahlString == "4)":
        return list(obj)[3]
    else:
        return ask_user(obj)


def show_invetory():
    print("Du hast %d Lebenspunkte." % state["hp"],
        "Du hast ein Schwert." if not state["swordAvail"] else "",
        "Du hast den Schatz." if not state["treasureAvail"] else "")


def speichern(choice, state):
    if choice == "speichernBeenden":
        with open('save.json', 'w') as fp:
            fp.write(json.dumps(state))
        return {**state, "hp": 0}
    else:
        return state


def spiel_menue(state):
    choice = ask_user({"neuesSpiel" : "Neues Spiel", "spielLaden" : "Spiel laden"})
    if choice == "neuesSpiel":
        print("Spiel wird gestartet...") #Zusatzidee
        return {**state, "position" : "Eingang"}
    elif choice == "spielLaden":
        try:
            with open("save.json","r") as fp:
                return json.loads("%s" %fp.read())
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError("Der Speicherstand hat keinen Inhalt.", "C:\projects\Zork\Zork.py")
    return state


def room_eingang(state):
    print("Du befindest dich im EINGANG.",
        "Du kannst in die Schatzkammer oder zum Händler gehen.")
    show_invetory()
    if state["treasureAvail"]:
        choice = ask_user({"schatzkammer" : "Schatzkammer", "handler" : "Händler", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "schatzkammer":
            return {**state, "position" : "Schatzkammer"}
        elif choice == "handler":
            return {**state, "position" : "Handler"}
        else:
            return speichern(choice, state)
    elif not state["treasureAvail"]:
        choice = ask_user({"schatzkammer" : "Schatzkammer", "handler" : "Händler", "beenden" : "Beenden", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "schatzkammer":
            return {**state, "position" : "Schatzkammer"}
        elif choice == "handler":
            return {**state, "position" : "Handler"}
        elif choice == "beenden":
            return {**state, "hp": 0}
        else:
            return speichern(choice, state)
    return state

def room_schatzk(state):
    print("Du befindest dich in der SCHATZKAMMER."
        " Du musst nun gegen den Drachen kämpfen,"
        " indem du würfelst oder du gehst zurück.")
    show_invetory()

    if state["dragonAlive"]:
        choice = ask_user({"drachenBekampfen" : "Drachen bekämpfen", "zurück" : "Zurück", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "drachenBekampfen":
            randomint = randint(1, 6)
            if ((randomint < 4 and not state["swordAvail"])
                    or (randomint == 6 and state["swordAvail"])):
                print("Du hast den Drachen besiegt!")
                return {**state, "dragonAlive": False}
            else:
                return {**state, "hp": state["hp"] - 1}
        elif choice == "zurück":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(choice, state)
    elif not state["dragonAlive"] and state["treasureAvail"]:
        choice = ask_user({"schatzAufheben" : "Schatz aufheben", "zurück" : "Zurück", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "schatzAufheben":
            print("Schatz aufgehoben!")
            return {**state, "treasureAvail": False}
        elif choice == "zurück":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(choice, state)
    elif not state["dragonAlive"] and not state["treasureAvail"]:
        choice = ask_user({"zurück" : "Zurück", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "zurück":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(choice, state)
    return state


def room_handler(state):
    print("Du befindest dich beim HÄNDLER.",
        " Du kannst ein Schwert für einen Lebenspunkt kaufen oder zurück"
        " gehen.")
    show_invetory()

    if state["swordAvail"]:
        choice = ask_user({"schwertKaufen" : "Schwert kaufen", "zurück" : "Zurück", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "schwertKaufen":
            return {**state, "swordAvail": False, "hp": state["hp"] - 1}
        elif choice == "zurück":
            return {**state, "position" : "Eingang"}
    else:
        choice = ask_user({"zurück" : "Zurück", "speichernBeenden" : "Speichern und Beenden"})
        if choice == "zurück":
            return {**state, "position" : "Eingang"}
        else:
            return speichern(choice, state)
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
