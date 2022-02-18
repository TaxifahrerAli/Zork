from flask import Flask, request
from random import randint
import json
from random import randint


app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


# @app.route("/bye",methods=["GET","POST"])
# def goodbye_world():
#     return """
#         <p>Goodbye, World!%s </p>
#         <form action="/bye" method="POST">
#             <input name="name">
#             <input name="age"> 
#             <label><input type="radio" name="choice" value="a">Wahl A</label>
#             <label><input type="radio" name="choice" value="b">Wahl B</label>
#             <button type="submit">Ok</button>
#         </form>
#     """ % request.form.get('name')


@app.route("/zork",methods=["GET","POST"])
def zork_main():


    # === Spielstand berechnen === 
    try:
        with open("save.json","r") as fp:
            state = json.loads(fp.read())
    except:
        state = {
            "hp": 5,
            "position": "Eingang",
            "dragonAlive": True,
            "swordAvail": True,
            "treasureAvail": True,
        }
    def make_invetory():
        nachricht ="Du hast %s Lebenspunkte. "% state["hp"]
        nachricht +="Du hast den Schatz. " if not state["treasureAvail"] else ""
        nachricht +="Du hast ein Schwert." if not state["swordAvail"] else ""
        return nachricht

    choice = request.form.get('choice')

    if state["position"] == "Eingang":
        if choice == "position1":
            state = {**state, "position": "Schatzkammer"}
        elif choice == "position2":
            state = {**state, "position": "Handler"}
    elif state["position"] == "Schatzkammer":
        if choice == "position":
            state = {**state, "position": "Eingang"}
        elif choice == "drachenBekämpfen" and state["hp"] > 0:
            randomint = randint(1, 6)
            if ((randomint < 4 and not state["swordAvail"])
                    or (randomint == 6 and state["swordAvail"])):
                state = {**state, "dragonAlive": False, "treasureAvail": True}
            else:
                state = {**state, "hp": state["hp"] - 1}
        elif choice == "schatzAufheben":
            state = {**state, "treasureAvail": False}
    elif state["position"] == "Handler":
        if choice == "position":
            state = {**state, "position": "Eingang"}
        elif choice == "schwertKaufen":
            state = {**state, "swordAvail": False}


    # === Ausgabe berechnen ===
    if state["position"] == "Eingang":
        positionsnachricht = "Du bist im Eingang."
        optionen = {
            "position1": "In die Schatzkammer gehen",
            "position2": "Zum Händler gehen",
        }
    elif state["position"] == "Schatzkammer":
        positionsnachricht = "Du bist in der Schatzkammer."
        hpnachricht = "Du hast %s Lebenspunkte."% state["hp"]
        schatznachricht = "Du hast den Schatz." if not state["treasureAvail"] else ""
        schwertnachricht = "Du hast ein Schwert." if not state["swordAvail"] else ""
        if state["dragonAlive"]:
            optionen = {
                "position": "In den Eingang gehen",
                "drachenBekämpfen": "Drachen bekämpfen"
            }
        elif not state["dragonAlive"] and state["treasureAvail"]:
            optionen = {
                "position": "In den Eingang gehen",
                "schatzAufheben": "Schatz aufheben"
            }
        elif not state["treasureAvail"] and not state["dragonAlive"]:
            optionen = {
                "position": "In den Eingang gehen"
            }
    elif state["position"] == "Handler":
        positionsnachricht = "Du bist beim Händler."
        hpnachricht = "Du hast %s Lebenspunkte."% state["hp"]
        schatznachricht = "Du hast den Schatz." if not state["treasureAvail"] else ""
        schwertnachricht = "Du hast ein Schwert." if not state["swordAvail"] else ""
        if state["swordAvail"]:
            optionen = {
                "position": "In den Eingang gehen",
                "schwertKaufen": "Schwert kaufen"
            }
        else:
            optionen = {
                "position": "In den Eingang gehen"
            }
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


    # === Spielstand (vorläufig) in der json speichern ===
    with open('save.json', 'w') as fp:
        fp.write(json.dumps(state))

    # === Spielstand wiedergeben ===
    return """
        <h4>Zork</h4>
        <p>%s %s</p>
        <form action="/zork" method="POST">
            %s
            <button type="submit">OK</button>
        </form
    """ % (positionsnachricht, make_invetory(), optionsnachricht)
