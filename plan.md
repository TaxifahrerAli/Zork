Jeder Raum ist ein Objekt und hat die Keys Osten, Norden, Westen und Süden, sowie den Key raumVorhanden.
Die Objekte jedes Raumes werden zu Anfang des Spiels erstellt
Jeder Raum hat außerdem zwei Koordinaten X und y, die in ein gemeinsames Objekt geschrieben werden.
Der Eingang hat die Koordinaten (0 / 0)(x / y)

# Generierung der Räume:
1. Ausgangslage ist in jedem Schritt der Eingang. Es wird eine Zahl zwischen 1
und 4 ausgewählt für die Himmelsrichtungen, die dafür sorgt, dass darüber entschieden wird,
wo ein neuer Raum enstehen soll. Sollte an dieser Position schon ein Raum existieren,
wird dieser Raum als Ausgangslage genommen und erneut gewürfelt.
2. Im Anschluss daran wird eine Zahl zwischen 1 und 5 ausgewählt, um
darüber zu entscheiden, was für ein Raum (Schatzkammer, leerer Raum, usw.)
an der Stelle erstellt wird. Außerdem wird mithilfe der Variable raumVorhanden überprüft, ob es den Raum schonmal
gab (im Falle eines Klassischen Raumes) oder, ob die maximale Anzahl an Räumen
(im Falle der leeren Rüume) erreicht wurde. Falls ja, wird erneut gewürfelt.
3. Die Position und der Name des Raumes aus der Sicht des Ursprungsraumes wird in das
Objekt des Ursprungsraumes geschrieben.
4. Es wird ein Objekt mit den Himmelsrichtungen erstellt und die Position des
Ursprungsraumes, also Eingang wird in die Korrekte Himmelsrichtung des neuen Raumes geschrieben
Dazu werden am Anfang des Prozesses die "Gegenteil-Variablen" der Himmelsrichtungen
festgelegt: Wenn ein Raum im Süden des Ursprungsraumes erstellt wird, ist die Position
des Ursprungsraumes aus der Sicht des neuen Raumes Norden. Das gleiche gilt für
Westen und Osten, Osten und Westen ,Norden und Süden.
5. Das Objekt bekommt bedingt durch die Koordinate das Ursprungsraumes und die ausgewürfelte 
Himmelsrichtung ebenso eine Koordinate. Wenn die Koordinaten des Ursprungs-
raumes (0 / 0) ist und der neue Raum im Osten entsteht, wird die neue Koordinate
wie folgt berechnet: (0 + 1 / 0). Bei Westen (0 - 1/ 0), bei Norden (0 /0 + 1)
und bei Süden (0 / 0 - 1). Die Koordinaten und der Name jedes Raumes werden in ein Objekt
gepackt.
6. Danach wird das Koordinaten-Objekt durchgagangen und es wird anhand der Koordinaten überprüft, ob es einen
Raum gibt, der an dem neuen Raum benachbart und gleichzeitig nicht der Ursprungsraum ist.
Sollte es einen solchen Raum geben, wird seine Himmelsichtung aus der Sicht
des neuen Raumes berechnet und in das Objekt eingetragen. Dann wird mithilfe
der Gegenteilvariable auch die Himmelsrichtung des neuen Raumes aus der SIcht
des benachbarten Raumes in sein Objekt eingetragen.

Der Prozess wird solange wiederholt, bis keine Räume mehr übrig sind.

# Spielbedienung:
Sollte ein Wert der Himmelsrichtungen einer der leeren Räume oder ein klassischer Raum sein,
bekommt der Spieler angezeigt, sich nach dort zu bewegen.
Alle anderen Eigenschaften eines Raumes werden wie üblich geladen.
