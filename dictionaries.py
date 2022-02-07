
telefonbuch = {
    "alice" : "111-1111",
    "bob" : "222-2222",
    "charlie" : "333-3333"
}

input = input("Name:\n-- ")

if input == "alice":
    print(telefonbuch.get("alice"))
elif input == "bob":
    print(telefonbuch.get("bob"))
elif input == "charlie":
    print(telefonbuch.get("charlie"))
else:
    print("Nicht Gefunden")