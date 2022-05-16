/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./frontend/main.js":
/*!**************************!*\
  !*** ./frontend/main.js ***!
  \**************************/
/***/ (() => {

eval("\r\nconst beschreibung = document.querySelector(\"#beschreibung\"),\r\nlebenspunkte = document.querySelector(\"#lebenspunkte\"),\r\ninventar = document.querySelector(\"#inventar\"),\r\noptionen = document.querySelector(\"#optionen\")\r\n\r\nfunction anfrage() {\r\n  fetch('/api/game/', { method: 'GET', credentials: 'include' })\r\n   .then(response => response.json())\r\n   .then(data => {\r\n          beschreibung.innerHTML = data.description;\r\n          lebenspunkte.innerHTML = data.hp + \"❤️\";\r\n\r\n          for (const key in data.inventory) {\r\n              let list_el = document.createElement(\"li\");\r\n              list_el.innerHTML = data.inventory[key];\r\n              inventar.appendChild(list_el);\r\n          };\r\n\r\n          for (const key in data.choices) {\r\n              let container = document.createElement(\"div\");\r\n              container.setAttribute(\"style\", \"display:block; margin: 0 0 10px 0;\");\r\n\r\n              let list_el = document.createElement(\"li\");\r\n              list_el.setAttribute(\"style\", \"display:inline;\");\r\n              list_el.innerHTML = data.choices[key];\r\n\r\n              let button = document.createElement(\"button\");\r\n              button.innerHTML = \"Auswählen\";\r\n              button.setAttribute(\"style\", \"margin :0 0 0 10px;\");\r\n              button.setAttribute(\"id\", `${key}`)\r\n              button.addEventListener(\"click\",() => {\r\n                  fetch('/api/game/', { method: 'POST', body: `${key}`})\r\n                      .then(() => {\r\n                          clear();\r\n                          anfrage();\r\n                      });\r\n              });\r\n\r\n              container.appendChild(list_el);\r\n              container.appendChild(button);\r\n              optionen.appendChild(container);\r\n          };\r\n      console.log(data, \"!\");\r\n  });\r\n};\r\n\r\nfunction clear() {\r\n  beschreibung.innerHTML = \"\";\r\n  lebenspunkte.innerHTML = \"\";\r\n  inventar.innerHTML = \"\";\r\n\r\n  while (document.getElementsByTagName(\"div\").length > 0) {\r\n      optionen.removeChild(optionen.firstChild);\r\n  }\r\n};\r\n\r\nanfrage();\n\n//# sourceURL=webpack://Zork-Frontend/./frontend/main.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./frontend/main.js"]();
/******/ 	
/******/ })()
;