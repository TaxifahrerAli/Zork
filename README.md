# Zork

## Iteration 1

Jede Runde startet mit der Ausgabe der Beschreibung des Raums und einer Liste
der möglichen Aktionen. Es gibt noch keine Möglichkeit, das Spiel zu Beenden.

Es gibt zwei Räume, die Eingangshalle und die Schatzkammer

Beispiel Eingangshalle:

    Du bist in der Eingangshalle. Vor dir ist eine Tür zur Schatzkammer.

    1) Durch die Tür gehen

Beispiel Schatzkammer:

    Du bist in der Schatzkammer. Vor dir liegt ein Schatz. Hinter dir ist eine
    Tür zur Eingangshalle

    1) Durch die Tür gehen

## Iteration 2

Die Schatzkammer soll die Aktion "Schatz nehmen" bekommen. Ist der Schatz
genommen, soll die Aktion nicht mehr zur Verfügung stehen.

Wenn der Spieler den Schatz genommen hat, soll in der Eingangshalle die Aktion
"Spiel beenden" zur Verfügung stehen, die das Spiel beendet.

## Iteration 3

### Lebensenergie

Der Spieler bekommt 5 Punkte Lebensenergie. Die Beschreibung der Räume wird
so ergänzt, dass der aktuelle Stand der Lebensenergie angezeigt wird.

Beispiel:

    Du bist in der Eingangshalle. Vor dir ist eine Tür zur Schatzkammer.
    Du hast 5 Punkte Lebensenergie

    1) Durch die Tür gehen

Sinkt die Lebensenergie auf oder unter 0, ist das Spiel vorbei.

### Drache

In der Schatzkammer ist ein Drache.
Solange der Drache lebt, kann der Spieler den Schatz nicht aufheben.

Der Spieler bekommt in der Schatzkammer die Option "Drache bekämpfen".
Wählt der Spieler diese Option, soll gewürfelt werden:

* bei einer 6 wird der Drache besiegt und verschwindet.
* bei 1-5 verliert der Spieler einen Punkt Lebensenergie


## Iteration 4

### Händler

Ein weiterer Raum namens "Händler" wird eingefügt. Er ist aus der Eingangshalle
aus erreichbar

### Schwert kaufen

Im Raum des Händlers soll der Spieler ein Schwert kaufen können.
Hat er das Schwert gekauft, soll er es nicht noch einmal kaufen können.
Hat er das Schwert gekauft, soll es am Anfang der Runde, analog zur
Lebensenergie angezeigt werden, Beispiel:

    Du hast 5 Punkte Lebensenergie
    Du hast ein Schwert

### Kampf mit Schwert

Wenn der Spieler das Schwert hat, soll er beim Kampf gegen den Drachen
bei 1-3 gewinnen.

## Iteration 5

### Zwischenspiel: Dictionaries

Versuche herauszubekommen, wie `Dictionaries` in Python funktionieren (Tipp: es besteht
eine Ähnlichkeit zu Javascript-Objekten).

Zur Überprüfung programmiere ein "Telefonbuch":

* beim Start fragt das Programm nach einem Namen ('alice', 'bob', 'charlie')
* das Programm antwortet mit der Nummer ('111-1111', '222-2222', '333-3334') oder mit 'Nicht gefunden'
* das Programm soll die Nummern aus einem Dictionary holen.

### Zwischenspiel: Scope

Versuche herauszubekommen, wie `Scope` ("Gültigkeitsbereich") in Python funktioniert.
Du solltest am Ende deiner Forschung einem hypothetischen dritten, der gerade Python lernt,
erklären können

1) warum dieser Code einen Fehler wirft:

        value = 1
    
        def increase_value():
            value = value + 1
            print(value)

2) dieser Code wie erwartet funktioniert:

         state = {"value": 1}
    
         def increase_value():
             state['value'] = state['value'] + 1
             print(state['value'])

### Refactoring: Gamestate als Dictionary

Refactore das Spiel so, dass der gesammte Gamestate in einem Dictionary, nicht in getrennten Variablen
gespeichert ist.
        
### Refactoring: Räume als Transformationsfunktionen

Refactore das Spiel so, dass die Funktionalität der einzelnen Räume in Funktionen *gekapselt* ist, d.h.,
aus

    # ...
    if state['position'] == 'Eingang':
       print("Du stehst im Eingang")
       choice = input()
       if choice == '1':
           # ...

das hier wird:

    if state['position'] == 'Eingang':
        state = raum_eingang(state)
        
    # ...
    
    def raum_eingang(state):
        print("Du stehst im Eingang")
        # ...

## Iteration 6

### Speichern/Laden

Der Spieler soll am Anfang die Möglichkeit bekommen, das Spiel zu laden:

     Wilkommen.
     
     1) Neues Spiel
     2) Spiel laden
     
wenn der Spieler das Spiel laden will, soll es aus einer Datei namens 'save.json' geladen werden.

Der Spieler soll in jedem Zug die option bekommen, das spiel zu speichern:

    1) Zum Drache gehen
    2) Zum Händler gehen
    S) Spiel speichern

wird das spiel gespeichert, soll der Gamestate als json in eine Datei 'save.json' geschrieben werden,
dass Spiel soll normal weiter gehen.

## Iteration 7

### Abfragen als Daten

Schreibe eine Funktion, die wie folgt aufgerufen werden kann:

    choice = ask_user({'eingang': 'Zur Eingangshalle gehen', 'schatzkammer': 'Zur Schatzkammer gehen'})
    
Die Funktion soll dem User die Werte des Dictionaries durchnummeriert als Wahlmöglichkeiten präsentieren,
also fürs obengenannte Beispiel

    1) Zur Eingangshalle gehen
    2) Zur Schatzkammer gehen

Gibt der User die Zahl einer Option an, soll *der Key* der Option zurückgegeben werden.
Gibt der User etwas ungültiges (i.e. keine Zahl, oder eine Zahl ausserhalb der Liste), soll er erneut gefragt werden.

Refactore den Code so, dass du die Funktion an allen stellen nutzt, wo du den User nach eingaben Fragst.
Es ist ok, wenn die Zahlen der Optionen nicht mehr die gleichen sind, wie vorher.
Es ist ok, wenn Speichern nicht per S ausgewählt wird.

Hinweis: per `dict.items` erhält man eine Liste, aller key/value-Päärchen des Dictionaries, d.H. folgender Code
listet alle Keys und Values eines Dictionaries auf.

    x = {'a': 'Alice', 'b': 'Bob'}
    for key, value in x.items():
        print("Der Key ist %s, der Value ist %s" % (key, value))

## Iteration 8

### Level Pro User

* Erweitere die Raumtabelle um einen `Foreign Key` auf die Usertabelle
* Sorge dafür dass die bisherige Funktionalität auf dem Level des eingeloggten
    Users ausgeführt wird
* Erweitere die Datenbankbeschreibung um passendes SQL, um die neue Usertabelle
    anzulegen oder zu ändern
### Neue Level

* Programmiere einen Controller `/level/`, auf dem ein Formular mit nur
    einem Button 'Neues Level' angezeigt wird, welcher, wenn man ihn anclickt,
    ein neues Level für den aktuell eingeloggten User erstellt, und ein
    eventuell vorher existierendes verwirft.

## Iteration 9

Kopiere den GET '/zork/' Controller, so dass er unter '/api/game/' ist. Ändere
ihn so, dass er als antwort kein Template zurückgibt, sondern ein JSON-Objekt,
in der Form:

    {
        "description": "Du bist beim Brunnen, er enthält 5 Schluck Heilwasser",
        "hp": 5,
        "inventory": [
          "Schwert",
        ],
        "choices": {
            "trinken": "Aus dem Brunnen trinken",
            "norden": "Nach Norden"
        }
    }


Erstelle einen neuen Controller, '/zorkjs/', der ein neues Template rendert. In
dieses Template kommt das Javascript.

Das Javascript soll eine HTTP-Anfrage stellen (siehe JavaScript-Grundlagen/HTTP-Anfrage),
das Ergebnis soll auf der Webseite angezeigt werden (siehe
JavaScript-Grundlagen/Inhalte auf der Seite ändern).

Beispielsweise sollte für die Antwort oben die seite in etwa so aussehen:

    Du bist beim Brunnen, er enthält 5 Schluck Heilwasser

    5❤️

    Du hast
      - Schwert

    [Aus dem Brunnen Trinken]
    [Nach Norden]

Die Choices müssen noch keine Wirkung haben.

## Hilfreiches

### Gameloop

Viele Spiele funktionieren so, dass sie in einer großen Schleife implementiert sind,
die in etwa so funktioniert:

    while True:  # ewig loopen
        # Anzeige des Spielstands
        # Abfrage der Benutzeraktionen (tastendrücke, maus, etc)
        # Ändern des Spielstandes anhand der Benutzeraktionen

### Usereingaben

Eine Usereingabe kann wie folgt ausgelesen werden:

    result = input('Bitte gebe etwas ein: ')
    
Die Benutzereingabe ist danach als string in der variable `result` gespeichert.

### Zufallszahlen

Eine Zufallszahl kann wie folgt erzeugt werden:

    from random import randint
    wuerfel = randint(1, 6)

### Serialisierung/JSON

JSON ist ein einfaches, menschen- und maschinenlesbares Format, um strukturiert Daten
in Textform zu speichern.

Beispiel:

    {
       "nichname": "Alice",
       "hp" 50,
       "inventar": [
           {
                "name": "diamond pickaxe",
                "amount": 1,
           },
           {
                "name": "cobblestone",
                "amount" 64,
           }
       ]
   }

Python bietet deine (Bibliothek)[https://docs.python.org/3/library/json.html] dafür

     import json
     
     # pythonstruktur aus String lesen
     data = json.loads('{"name": "Alice"}')
     print(data['name'])  # Alice

     # pythonstruktur in String umwandelm
     text = json.dumps({"name": "Alice"})
     print(text)
     
### Dateien

Dateien speichern Daten in einem Dateisystem, sie werden durch einen Pfad
identifiziert (z.B. c:\Users\Alice\Desktop\README.txt).

Betriebssysteme bieten die Möglichkeit, sie zu *öffnen*, und zu *schliessen*.
Für eine geöffnete Datei erhält man ein *Filepointer*.

    fp = open('datei.txt', 'r')  # 'r' -> zum lesen öffnen
    fp.close()

Mittels eines Filepointers kann man in die Datei schreiben...

    fp = open('datei.txt', 'w')  # 'w' -> zum lesen öffnen
    fp.write('Hallo, welt!')
    fp.close()

...und aus ihr lesen:

    fp = open('datei.txt', 'r')
    content = fp.read()
    print(content)
    fp.close()

Als Bequemlichkeit, damit die Datei immer geschlossen wird, erlaubt python
folgendes:

    with open('datei.txt', 'r') as fp:
        print(fp.read())

    # merke: close erfolgt automatisch

### Ajax

Normalerweise funktioniert ein Browser so, dass per

* URL Eingeben
* Link anklicken
* Formular auslösen

eine HTTP-Anfrage gestellt wird, und das Ergebnis der HTTP-Anfrage das aktuell
angezeigte Dokument im Browser wird.

Beispiele:

* Es wird http://google.de in die Adresszeile eingeben, Browser stellt eine Anfrage
  an dieser URL, als Antwort kommt die Suchformularseite, die dann angezeigt wird.

* Es wird 'how is babby formed' ins Suchformular eingegeben, der Browser fragt
  die URL https://www.google.com/search?q=how+is+babby+formed an, als Anwort kommt
  die Ergebnisseite, die dann angezeit wird

Mittels JavaScript auf einer Webseite kann eine HTTP-Anfrage gestellt werden, welche
nicht das angezeigte Dokument ersetzt, sondern im JavaScript-Programm zur
Verfügung steht.

Dabei werden oft nicht Menschenlesbare Webseiten übermittelt, sondern
Maschinenlesbare Daten.

Die ersten Programme, die JavaScript so nutzten, fragten XML-Dokumente ab,
weshalb HTTP-Anfragen aus JavaScript heraus "AJAX" genannt werden
(Asynchronous JavaScript and XML).

### Grundlagen Javascript

Doku: https://developer.mozilla.org/en-US/docs/Web

Javascript in einer HTML-Seite einbinden:

  <script>
    console.log("Hello world!");
  </script> 

Vorhandene Elemente auf der Seite finden:

    // <button id="okbutton">Ich bin der OK-Button</button>
    // <div><span>Ich bin ein Span in einem Div</span></div>

    const button = document.querySelector('#okbutton');
    const span = document.querySelector('div span');

Inhalte auf der Seite ändern:

    // wenn HTML
    span.innerHTML = 'Ich bin der <strong>neue</strong> Inhalt vom SPAN'

    // wenn Text
    span.innerText = 'Ich bin der <strong>neue</strong> Inhalt vom SPAN'

HTTP-Anfrage:

    fetch('/irgendwas/', { method: 'GET', credentials: 'include' })
      .then(response => response.json())
      .then(data => {
          // hier kann die Antwort verarbeitet werden.
          console.log(data)
      })

Eventhandler:

    button.addEventHandler('click', () => {
      console.log('der button wurde angeclickt');
    })