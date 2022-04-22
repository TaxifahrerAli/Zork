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
from . import room_common


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
    else:
        state = room_leerRaum.verarbeiten(state, choice)
    return state


def optionen_erörtern(state, userid):
    nachbarraume = nachbarraume_eroertern(userid, state["position"])
    if state["position"] == "Eingang":
        return room_eingang.erörtern(state)
    elif state["position"] == "Schatzkammer":
        return room_schatzkammer.erörtern(state)
    elif state["position"] == "Handler":
        return room_handler.erörtern(state)
    elif state["position"] == "Brunnen":
        return room_brunnen.erörtern(state)
    elif state["position"] == "Menue":
        return room_menue.erörtern(state)
    else:
        return room_leerRaum.erörtern(state)


def nachbarraume_eroertern(userid, raumname):
    """
    Findet die Nachbarräume von [raumname] im Level von [userid]
    Antowrt: {"norden": (), "osten": (), "sueden": (), "westen": "Schatzkammer"}
    """
    if raumname == "Menue":
        return {"norden": (), "osten": (), "sueden": (), "westen": ()}

    conn, cursor = db_connect("zork", "zork", "zork")

    cursor.execute("select x, y from raum where userid = %s and raumname = %s", [userid, raumname])
    koords = cursor.fetchall()
    print(koords)
    x, y = koords[0]

    cursor.execute("""
    select raumname, x, y from raum where
    (x = %s and y - 1 = %s or
    x - 1 = %s and y = %s or
    x = %s and y + 1 = %s or
    x + 1 = %s and y = %s) and userid = %s
    """, [x, y, x, y, x, y, x, y, userid])
    raume = cursor.fetchall()

    norden, osten, sueden, westen = (), (), (), ()
    for name, rx, ry in raume:
        if rx == x and ry - 1 == y:
            norden = name
        elif rx + 1 == x and ry == y:
            osten = name
        elif rx == x and ry + 1 == y:
            sueden = name
        elif rx - 1 == x and ry == y:
            westen = name

    conn.close()
    return {"norden": norden, "osten": osten, "sueden": sueden, "westen": westen}


def generate_level(userid):

    conn, cursor = db_connect("zork", "zork", "zork")

    cursor.execute("""
        update users set
            (hp,
            position,
            dragonalive,
            swordavail,
            treasureavail,
            brunnennutzungen)
        =
            (5,
            'Eingang',
            true,
            true,
            true,
            5)
        where id = %s
        """ , [userid])

    cursor.execute("delete from raum where userid = %s", [userid])
    cursor.execute("insert into raum (raumname, x, y, userid) values('Eingang', '0', '0', %s)", [userid])
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
            cursor.execute("insert into raum (raumname, x, y, userid) values (%s, %s, %s, %s)" , [raum["name"], raum["x"], raum["y"], userid])
    conn.commit()
    conn.close()
    print("Level wurde generiert!")


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


def get_inventory(state):
    inventory = []
    if not state["treasureAvail"]:
        inventory.append("Schatz")
    if not state["swordAvail"]:
        inventory.append("Schwert")
    return inventory


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sldfnalsdnf5'


@app.route("/zork", methods=["POST"])
def process_state():

    choice = request.form.get('choice')

    state = load_game(session["userid"])
    nachbarraume = nachbarraume_eroertern(session["userid"], state["position"])

    state = optionen_verarbeiten(state, choice)
    state = room_common.position_wechseln(choice, state, nachbarraume)

    save_game(state, session["userid"])

    return redirect("/zork", code=302)


@app.route("/zork", methods=["GET"])
def render_zork():

    state = load_game(session["userid"])
    print(state["position"], state)
    nachbarraume = nachbarraume_eroertern(session["userid"], state["position"])

    raumoptionen, beschreibung = optionen_erörtern(state, session["userid"])
    bewegungsoptionen = room_common.position_darlegen(nachbarraume)
    optionen = {**raumoptionen, **bewegungsoptionen}

    return render_template(
        "template.html",
        beschreibung=beschreibung,
        optionen=optionen,
        state=state
    )


@app.route("/api/game/", methods=["GET"])
def render_game():

    state = load_game(session["userid"])
    print(state["position"], state)
    nachbarraume = nachbarraume_eroertern(session["userid"], state["position"])

    raumoptionen, beschreibung = optionen_erörtern(state, session["userid"])
    bewegungsoptionen = room_common.position_darlegen(nachbarraume)
    optionen = {**raumoptionen, **bewegungsoptionen}

    return {
        "description": beschreibung,
        "hp": state["hp"],
        "inventory":get_inventory(state),
        "choices": optionen
    }


@app.route("/zorkjs/", methods=["GET"])
def render_templatee():
    return render_template("javascript.html")


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


@app.route("/level", methods=["POST"])
def levels():
    generate_level(session["userid"])
    return redirect("/level", code=302)


@app.route("/level", methods=["GET"])
def render_levels():
    return render_template("level.html")
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
