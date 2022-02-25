from flask import Flask, request, redirect
from random import randint
import json
from random import randint


#=== Inventar machen ===
def make_invetory(state):
    if state["position"] != "Menue":
        nachricht ="Du hast %s Lebenspunkte. "% state["hp"]
        nachricht +="Du hast den Schatz. " if not state["treasureAvail"] else ""
        nachricht +="Du hast ein Schwert." if not state["swordAvail"] else ""
        return nachricht
    else:
        return ""

#=== Optionen verarbeiten ===
def optionen_verarbeiten(state, choice):
    if state["position"] == "Eingang" and state["hp"] > 0:
        if choice == "position1":
            state = {**state, "position": "Schatzkammer"}
        elif choice == "position2":
            state = {**state, "position": "Handler"}
        elif choice == "beenden":
            state = {**state, "position": "Menue"}
    elif state["position"] == "Schatzkammer" and state["hp"] > 0:
        if choice == "position":
            state = {**state, "position": "Eingang"}
        elif choice == "drachenBekämpfen":
            randomint = randint(1, 6)
            if ((randomint < 4 and not state["swordAvail"])
                    or (randomint == 6 and state["swordAvail"])):
                state = {**state, "dragonAlive": False, "treasureAvail": True}
            else:
                state = {**state, "hp": state["hp"] - 1}
        elif choice == "schatzAufheben":
            state = {**state, "treasureAvail": False}
    elif state["position"] == "Handler" and state["hp"] > 0:
        if choice == "position":
            state = {**state, "position": "Eingang"}
        elif choice == "schwertKaufen":
            state = {**state, "swordAvail": False}
    elif state["position"] == "Menue": # -- Zusatzidee: Möglichkeit, im Menü neues Spiel zu starten --
        if choice == "neuesSpiel":
            state = {
                "hp": 5,
                "position": "Eingang",
                "dragonAlive": True,
                "swordAvail": True,
                "treasureAvail": True
            }
    return state

# === Optionen erörtern ===
def optionen_erörtern(state):
    if state["position"] == "Eingang":
        optionen = {
            "position1": "In die Schatzkammer gehen",
            "position2": "Zum Händler gehen",
        }
        if not state["treasureAvail"]:
            optionen = {**optionen, "beenden": "Spiel beenden"}
    elif state["position"] == "Schatzkammer":
        optionen = {"position" : "In den Eingang gehen"}
        if state["dragonAlive"]:
            optionen = {**optionen, "drachenBekämpfen": "Drachen bekämpfen"}
        elif not state["dragonAlive"] and state["treasureAvail"]:
            optionen = {**optionen, "schatzAufheben": "Schatz aufheben"}
    elif state["position"] == "Handler":
        optionen = {"position" : "In den Eingang gehen"}
        if state["swordAvail"]:
            optionen = {**optionen, "schwertKaufen": "Schwert kaufen"}
    elif
    elif state["position"] == "Menue":
        optionen = {"neuesSpiel": "Neues Spiel starten"}
    return optionen

# === Position wiedergeben ===
def position(state):
    if state["position"] != "Menue":
        return "Deine Position lautet %s." % state["position"]
    else:
        return "Du bist im Menü"

# === Spielstand laden === 
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
        }
    return state

# === Spielstand (vorläufig) in der json speichern ===
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

    optionen = optionen_erörtern(state)

    #=== Optionsnachricht erschaffen ===
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

    # === Spielstand wiedergeben ===
    return """
        <h4>Zork</h4>
        <p>%s %s</p>
        <form action="/zork" method="POST">
            %s
            <button type="submit">OK</button>
        </form
    """ % (position(state), make_invetory(state), optionsnachricht)
