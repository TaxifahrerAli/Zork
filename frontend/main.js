
const beschreibung = document.querySelector("#beschreibung"),
lebenspunkte = document.querySelector("#lebenspunkte"),
inventar = document.querySelector("#inventar"),
optionen = document.querySelector("#optionen")

function anfrage() {
  fetch('/api/game/', { method: 'GET', credentials: 'include' })
   .then(response => response.json())
   .then(data => {
          beschreibung.innerHTML = data.description;
          lebenspunkte.innerHTML = data.hp + "❤️";

          for (const key in data.inventory) {
              let list_el = document.createElement("li");
              list_el.innerHTML = data.inventory[key];
              inventar.appendChild(list_el);
          };

          for (const key in data.choices) {
              let container = document.createElement("div");
              container.setAttribute("style", "display:block; margin: 0 0 10px 0;");

              let list_el = document.createElement("li");
              list_el.setAttribute("style", "display:inline;");
              list_el.innerHTML = data.choices[key];

              let button = document.createElement("button");
              button.innerHTML = "Auswählen";
              button.setAttribute("style", "margin :0 0 0 10px;");
              button.setAttribute("id", `${key}`)
              button.addEventListener("click",() => {
                  fetch('/api/game/', { method: 'POST', body: `${key}`})
                      .then(() => {
                          clear();
                          anfrage();
                      });
              });

              container.appendChild(list_el);
              container.appendChild(button);
              optionen.appendChild(container);
          };
      console.log(data, "!");
  });
};

function clear() {
  beschreibung.innerHTML = "";
  lebenspunkte.innerHTML = "";
  inventar.innerHTML = "";

  while (document.getElementsByTagName("div").length > 0) {
      optionen.removeChild(optionen.firstChild);
  }
};

anfrage();