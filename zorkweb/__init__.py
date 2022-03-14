import json
import pg8000
from flask import Flask, request, session, redirect, render_template
from . import room_eingang
from . import room_schatzkammer
from . import room_handler
from . import room_brunnen
from . import room_menue


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
    except:
        state = {"position": "Menue"}
    return state


def save_game(state):
    with open('save.json', 'w') as fp:
        fp.write(json.dumps(state))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sldfnalsdnf5'


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

    return render_template("template.html", beschreibung=beschreibung, optionen=optionen, state=state)

@app.route("/users", methods=["GET"])
def userliste_rendern():
    conn = pg8000.connect(user="zork", password="zork", database="zork")
    cursor = conn.cursor()
    cursor.execute("select id, username from users")
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("userlist.html", users=rows)

@app.route("/users", methods=["POST"])
def user_löschen():
    conn = pg8000.connect(user="zork", password="zork", database="zork")
    cursor = conn.cursor()

    userLöschen = request.form.get('choice')
    cursor.execute("delete from users where id = %s", [userLöschen])

    conn.commit()
    conn.close()
    return redirect("/users", code=302)


@app.route("/createuser", methods=["GET"])
def form_rendern():
    return render_template("createUser.html")

@app.route("/createuser", methods=["POST"])
def datenbank_bearbeiten():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = pg8000.connect(user="zork", password="zork", database="zork")
    cursor = conn.cursor()
    cursor.execute("insert into users (username, password) values (%s, %s)" , [username, password])
    conn.commit()
    conn.close()
    return redirect("/users", code=302)

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def pruefung():
    conn = pg8000.connect(user="zork", password="zork", database="zork")
    cursor = conn.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)
    cursor.execute("select id from users where username = %s and password = %s", [username, password])
    user = cursor.fetchall()
    if user:
        session["userid"] = user[0][0]
        print(user)
        return redirect("/profil", code=302)
    else:
        return redirect("/login", code=302)

@app.route("/profil", methods=["GET"])
def sofjds():
    conn = pg8000.connect(user="zork", password="zork", database="zork")
    cursor = conn.cursor()
    id = session["userid"]
    if id:
        cursor.execute("select username from users where id = %s", [id])
        username = cursor.fetchall()
        return render_template("profil.html", username=username[0][0])
    else:
        return render_template("profil.html", username="none")