from flask import Flask, request, redirect
from random import randint
import json
from random import randint



def make_invetory(state):
    if state["position"] != "Menue":
        nachricht ="Du hast %s Lebenspunkte. "% state["hp"]
        nachricht +="Du hast den Schatz. " if not state["treasureAvail"] else ""
        nachricht +="Du hast ein Schwert." if not state["swordAvail"] else ""
        return nachricht
    else:
        return ""


def optionen_verarbeiten_eingang(state, choice):
    if choice == "position1":
        state = {**state, "position": "Schatzkammer"}
    elif choice == "position2":
        state = {**state, "position": "Handler"}
    elif choice == "beenden":
        state = {**state, "position": "Menue"}
    return state

def optionen_erörtern_eingang(state):
    beschreibung = "Du bist im Eingang"
    optionen = {
        "position1": "In die Schatzkammer gehen",
        "position2": "Zum Händler gehen",
    }
    if not state["treasureAvail"]:
        optionen = {**optionen, "beenden": "Spiel beenden"}
    return optionen, beschreibung




def optionen_verarbeiten_schatzkammer(state, choice):
    if choice == "position":
        state = {**state, "position": "Eingang"}
    elif choice == "drachenBekämpfen":
        randomint = randint(1, 6)
        if ((randomint < 4 and not state["swordAvail"])
                or (randomint == 6 and state["swordAvail"])):
            state = {**state, "dragonAlive": False, "treasureAvail": True}
        else:
            state = {**state, "hp": state["hp"] - 1}
            if state["hp"] == 0:
                state = {**state, "position": "Menue"}
    elif choice == "schatzAufheben":
        state = {**state, "treasureAvail": False}
    return state

def optionen_erörtern_schatzkammer(state):
    beschreibung = "Du bist in der Schatzkammer"
    optionen = {"position" : "In den Eingang gehen"}
    if state["dragonAlive"]:
        optionen = {**optionen, "drachenBekämpfen": "Drachen bekämpfen"}
    elif not state["dragonAlive"] and state["treasureAvail"]:
        optionen = {**optionen, "schatzAufheben": "Schatz aufheben"}
    return optionen, beschreibung




def optionen_verarbeiten_handler(state, choice):
    if choice == "position1": 
        state = {**state, "position": "Eingang"}
    elif choice == "position2":
        state = {**state, "position": "Brunnen"}
    elif choice == "schwertKaufen":
        state = {**state, "swordAvail": False}
    return state

def optionen_erörtern_handler(state):
    beschreibung = "Du bist beim Händler"
    optionen = {
            "position1": "In den Eingang gehen",
            "position2": "Zum Brunnen gehen"
        }
    if state["swordAvail"]:
        optionen = {**optionen, "schwertKaufen": "Schwert kaufen"}
    return optionen, beschreibung




def optionen_verarbeiten_brunnen(state, choice):
    if choice == "position":
        state = {**state, "position": "Handler"}
    elif choice == "trinken":
        state = {**state, "brunnenNutzungen": state["brunnenNutzungen"] - 1, "hp": 5}
    return state

def optionen_erörtern_brunnen(state):
    optionen = {"position": "Zum Händler gehen"}
    if state["brunnenNutzungen"] > 0:
        optionen = {**optionen, "trinken" : "Aus dem Brunnen trinken"}
    beschreibung = "Du bist beim Brunnen, er enthält %s Schluck Heilwasser" % state["brunnenNutzungen"]
    return optionen, beschreibung




def optionen_verarbeiten_menue(state, choice):
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

def optionen_erörtern_menue(state):
    beschreibung = "Du bist im Menü"
    optionen = {"neuesSpiel": "Neues Spiel starten"}
    return optionen, beschreibung




def optionen_verarbeiten(state, choice):
    if state["position"] == "Eingang":
        state = optionen_verarbeiten_eingang(state, choice)
    elif state["position"] == "Schatzkammer":
        state = optionen_verarbeiten_schatzkammer(state, choice)
    elif state["position"] == "Handler":
        state = optionen_verarbeiten_handler(state, choice)
    elif state["position"] == "Brunnen" and state["hp"] > 0: 
        state = optionen_verarbeiten_brunnen(state, choice)
    elif state["position"] == "Menue": # -- Zusatzidee: Möglichkeit, im Menü neues Spiel zu starten --
        state = optionen_verarbeiten_menue(state, choice)
    return state

def optionen_erörtern(state):
    if state["position"] == "Eingang":
        return optionen_erörtern_eingang(state)
    elif state["position"] == "Schatzkammer":
        return optionen_erörtern_schatzkammer(state)
    elif state["position"] == "Handler":
        return optionen_erörtern_handler(state)
    elif state["position"] == "Brunnen": 
         return optionen_erörtern_brunnen(state)
    elif state["position"] == "Menue":
        return optionen_erörtern_menue(state)
    else:
        raise Exception("Unbekannte Position")


def load_game():
    try:
        with open("save.json","r") as fp:
            state = json.loads(fp.read())
    except:
        state = {
            "hp": 5,
            "position": "Menue",
            "dragonAlive": True,
            "swordAvail": True,
            "treasureAvail": True,
            "brunnenNutzungen": 5
        }
    return state


def save_game(state):
    with open('save.json', 'w') as fp:
        fp.write(json.dumps(state))


app = Flask(__name__)


@app.route("/zork",methods=["POST"])
def process_state():

    #=== Wahl abspeichern
    choice = request.form.get('choice')

    state = load_game()
    state = optionen_verarbeiten(state,choice)

    save_game(state)

    return redirect("/zork", code = 302)


@app.route("/zork",methods=["GET"])
def show_game():

    state = load_game()

    optionen,beschreibung = optionen_erörtern(state)

    optionsnachricht = "<ol>"
    for key, value in optionen.items():
        optionsnachricht += (
            """<li>
                    <label>
                        %s
                        <input 
                            type='radio'
                            name='choice'
                            value= %s
                        >
                    </label>
                </li>
            """ % (value, key)
        )
    optionsnachricht += "</ol>"

    # === HTML wiedergeben ===
    return """
        <h4>Zork</h4>
        <p>%s<p>
        <p>%s</p>
        <form action="/zork" method="POST">
            %s
            <button type="submit">OK</button>
        </form
    """ % (beschreibung, make_invetory(state), optionsnachricht) 
