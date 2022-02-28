from flask import Flask, request, redirect
import json
from . import room_eingang
from . import room_schatzkammer
from . import room_handler
from . import room_brunnen
from . import room_menue


def make_invetory(state):
    if state["position"] != "Menue":
        nachricht = "Du hast %s Lebenspunkte. " % state["hp"]
        nachricht += "Du hast den Schatz. " if not state["treasureAvail"] else ""
        nachricht += "Du hast ein Schwert." if not state["swordAvail"] else ""
        return nachricht
    return ""


def optionen_verarbeiten(state, choice):
    if state["position"] == "Eingang":
        state = room_eingang.verarbeiten(state, choice)
    elif state["position"] == "Schatzkammer":
        state = room_schatzkammer.verarbeiten(state, choice)
    elif state["position"] == "Handler":
        state = room_handler.verarbeiten(state, choice)
    elif state["position"] == "Brunnen" and state["hp"] > 0:
        state = room_brunnen.verarbeiten(state, choice)
    elif state["position"] == "Menue":
        state = room_menue.verarbeiten(state, choice)
    return state


def optionen_erörtern(state):
    if state["position"] == "Eingang":
        return room_eingang.erörtern(state)
    elif state["position"] == "Schatzkammer":
        return room_schatzkammer.erörtern(state)
    elif state["position"] == "Handler":
        return room_handler.erörtern(state)
    elif state["position"] == "Brunnen":
        return room_brunnen.erörtern(state)
    elif state["position"] == "Menue":
        return room_menue.erörtern()
    else:
        raise Exception("Unbekannte Position")


def load_game():
    try:
        with open("save.json", "r") as fp:
            state = json.loads(fp.read())
    except json.decoder.JSONDecodeError:
        state = {"position": "Menue"}
    return state


def save_game(state):
    with open('save.json', 'w') as fp:
        fp.write(json.dumps(state))


app = Flask(__name__)


@app.route("/zork", methods=["POST"])
def process_state():

    choice = request.form.get('choice')

    state = load_game()
    state = optionen_verarbeiten(state, choice)

    save_game(state)

    return redirect("/zork", code=302)


@app.route("/zork", methods=["GET"])
def show_game():

    state = load_game()

    optionen, beschreibung = optionen_erörtern(state)

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

    return """
        <h4>Zork</h4>
        <p>%s<p>
        <p>%s</p>
        <form action="/zork" method="POST">
            %s
            <button type="submit">OK</button>
        </form
    """ % (beschreibung, make_invetory(state), optionsnachricht)
