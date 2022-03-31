import json
import pg8000
from random import randint
from flask import Flask, request, session, redirect, render_template
from . import room_eingang
from . import room_schatzkammer
from . import room_handler
from . import room_brunnen
from . import room_menue
from . import room_leerRaum


def optionen_verarbeiten(state, choice, nachbarraume):
    if state["position"] == "Eingang":
        state = room_eingang.verarbeiten(state, choice, nachbarraume)
    elif state["position"] == "Schatzkammer":
        state = room_schatzkammer.verarbeiten(state, choice, nachbarraume)
    elif state["position"] == "Handler":
        state = room_handler.verarbeiten(state, choice, nachbarraume)
    elif state["position"] == "Brunnen" and state["hp"] > 0:
        state = room_brunnen.verarbeiten(state, choice, nachbarraume)
    elif state["position"] == "Menue":
        state = room_menue.verarbeiten(state, choice)
    else:
        state = room_leerRaum.verarbeiten(state, choice, nachbarraume)
    return state


def optionen_erörtern(state, nachbarraume):
    nachbarraume = nachbarraume_eroertern(1, state["position"])
    if state["position"] == "Eingang":
        return room_eingang.erörtern(state, nachbarraume)
    elif state["position"] == "Schatzkammer":
        return room_schatzkammer.erörtern(state, nachbarraume)
    elif state["position"] == "Handler":
        return room_handler.erörtern(state, nachbarraume)
    elif state["position"] == "Brunnen":
        return room_brunnen.erörtern(state, nachbarraume)
    elif state["position"] == "Menue":
        return room_menue.erörtern()
    else:
        return room_leerRaum.erörtern(state, nachbarraume)
    # else:
    #     raise Exception("Unbekannte Position")


def nachbarraume_eroertern(eingangsid, raumname):
    conn, cursor = db_connect("zork", "zork", "zork")
    cursor.execute("select raumname, x, y from raum where id >= %s and id <= %s", [eingangsid, eingangsid + 13])
    norden, osten, sueden, westen = "", "", "", ""
    raume = cursor.fetchall()
    for i in raume:
        if i[0] == raumname:
            position = [i[0], i[1], i[2]]
    if raumname != "Menue":
        for i in raume:
            if i[1] == position[1] and i[2] - 1 == position[2]:
                norden = i[0]
            elif i[1] + 1 == position[1] and i[2] == position[2]:
                osten = i[0]
            elif i[1] == position[1] and i[2] + 1 == position[2]:
                sueden = i[0]
            elif i[1] - 1 == position[1] and i[2] == position[2]:
                westen = i[0]
    conn.close()
    return {"norden": norden, "osten": osten, "sueden": sueden, "westen": westen}


def optionen_darlegen(nachbarraume):
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


def db_connect(user, password, database):
    conn = pg8000.connect(user=user, password=password, database=database)
    cursor = conn.cursor()
    return (conn, cursor)


def load_game(userid):
    conn, cursor = db_connect("zork", "zork", "zork")
    cursor.execute("""
        select
            hp,
            position,
            dragonalive,
            treasureavail,
            swordAvail,
            brunnennutzungen
        from users
        where id = %s
        """,
        [userid]
    )
    state = cursor.fetchall()[0]
    state = {
        "hp": state[0],
        "position": state[1],
        "dragonAlive": state[2],
        "treasureAvail": state[3],
        "swordAvail": state[4],
        "brunnenNutzungen": state[5]
    }
    return state


def save_game(state, userid):
    conn, cursor = db_connect("zork", "zork", "zork")
    userid = session["userid"]
    cursor.execute("""
        update users set
            hp = %s,
            brunnennutzungen = %s,
            swordavail = %s,
            dragonalive = %s,
            treasureavail = %s,
            position = %s
            where id = %s
        """,
        [state["hp"], state["brunnenNutzungen"], state["swordAvail"],
        state["dragonAlive"], state["treasureAvail"], state["position"], userid]
    )
    conn.commit()
    conn.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sldfnalsdnf5'


@app.route("/zork", methods=["POST"])
def process_state():

    choice = request.form.get('choice')

    state = load_game(session["userid"])
    nachbarraume = nachbarraume_eroertern(1, state["position"])
    state = optionen_verarbeiten(state, choice, nachbarraume)

    save_game(state, session["userid"])

    return redirect("/zork", code=302)


@app.route("/zork", methods=["GET"])
def render_zork():

    state = load_game(session["userid"])
    nachbarraume = nachbarraume_eroertern(1, state["position"])

    optionen, beschreibung = optionen_erörtern(state, nachbarraume)
    print(optionen, beschreibung)

    return render_template(
        "template.html",
        beschreibung=beschreibung,
        optionen=optionen,
        state=state
    )


@app.route("/users", methods=["GET"])
def render_users():
    conn, cursor = db_connect("zork", "zork", "zork")
    cursor.execute("select id, username from users")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("userlist.html", users=rows)


@app.route("/users", methods=["POST"])
def user_delete():
    conn, cursor = db_connect("zork", "zork", "zork")

    userLöschen = request.form.get('choice')
    cursor.execute("delete from users where id = %s", [userLöschen])

    conn.commit()
    conn.close()
    return redirect("/users", code=302)


@app.route("/createuser", methods=["GET"])
def render_form():
    return render_template("createUser.html")


@app.route("/createuser", methods=["POST"])
def change_table():
    username = request.form.get('username')
    password = request.form.get('password')

    conn, cursor = db_connect("zork", "zork", "zork")
    cursor.execute("insert into users (username, password) values (%s, %s)",
        [username, password])
    conn.commit()
    conn.close()
    return redirect("/users", code=302)


@app.route("/login", methods=["GET"])
def render_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    conn, cursor = db_connect("zork", "zork", "zork")
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("""select id from users
        where username = %s
        and password = %s
        """, [username, password]
    )
    user = cursor.fetchall()
    if user:
        session["userid"] = user[0][0]
        return redirect("/profil", code=302)
    else:
        return redirect("/login", code=302)


@app.route("/profil", methods=["GET"])
def render_profil():
    conn, cursor = db_connect("zork", "zork", "zork")
    id = session["userid"]
    if id:
        cursor.execute("select username from users where id = %s", [id])
        username = cursor.fetchall()
        return render_template("profil.html", username=username[0][0])
    else:
        return render_template("profil.html", username="none")


# ==============================================================================


def raumname_erstellen(leerRaume, raum, koordinaten):
    zufallsraum = randint(1, 13)
    if zufallsraum < 10 and leerRaume > 0:
        raum["name"] = "leerRaum%s" % leerRaume
        leerRaume = leerRaume - 1
    elif zufallsraum == 11:
        raum["name"] = "Brunnen"
    elif zufallsraum == 12:
        raum["name"] = "Schatzkammer"
    elif zufallsraum == 13:
        raum["name"] = "Haendler"

    for key, value in koordinaten.items():
        if key == "Haendler" and raum["name"] == "Haendler":
            raum["name"] = ""
        elif key == "Brunnen" and raum["name"] == "Brunnen":
            raum["name"] = ""
        elif key == "Schatzkammer" and raum["name"] == "Schatzkammer":
            raum["name"] = ""
    
    return raum, leerRaume


def position_erstellen(raum, ausgangsPosition, koordinaten):
    positionErstellt = True
    zufallsrichtung = randint(1, 4)
    if zufallsrichtung == 1:
        raum["x"] = ausgangsPosition["x"]
        raum["y"] = ausgangsPosition["y"] + 1
    elif zufallsrichtung == 2:
        raum["y"] = ausgangsPosition["y"]
        raum["x"] = ausgangsPosition["x"] + 1
    elif zufallsrichtung == 3:
        raum["x"] = ausgangsPosition["x"]
        raum["y"] = ausgangsPosition["y"] - 1
    elif zufallsrichtung == 4:
        raum["y"] = ausgangsPosition["y"]
        raum["x"] = ausgangsPosition["x"] - 1

    for key, value in koordinaten.items():
        if raum["x"] == value[0] and raum["y"] == value[1]:
            positionErstellt = False

    return raum, positionErstellt


@app.cli.command()
def generate_level():

    conn, cursor = db_connect("zork", "zork", "zork")
    cursor.execute("insert into raum (raumname, x, y) values('Eingang', '0', '0')")
    koordinaten = {
        "Eingang" : (0, 0)
    }
    leerRaume = 10
    raumAnzahl = 13
    ausgangsPosition = {"x" : 0, "y" : 0}

    while raumAnzahl:
        raum = {
            "name" : "",
            "x" : 0,
            "y" : 0
        }

        raum, positionErstellt = position_erstellen(raum, ausgangsPosition, koordinaten)

        if positionErstellt:
            raum, leerRaume = raumname_erstellen(leerRaume, raum, koordinaten)

        if raum["name"]:
            koordinaten[raum["name"]] = (raum["x"], raum["y"])
            raumAnzahl = raumAnzahl -1
            print(raum)
            ausgangsPosition["x"] = raum["x"]
            ausgangsPosition["y"] = raum["y"]
            cursor.execute("insert into raum (raumname, x, y) values (%s, %s, %s)" , [raum["name"], raum["x"], raum["y"]])
    conn.commit()
    conn.close()
    print("Level wurde generiert!")
    print(nachbarraume_eroertern(15, ["Schatzkammer", 0,-2]))