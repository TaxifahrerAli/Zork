# Tabelle anlegen
create table NAME (
    SPALTENNAME DATENTYP,
);
create table sortiment (
    produkt text,
    preis int
);
# Aus der Tabelle Daten selektieren
select * from NAME where BEDINGUNG
select * from sortiment where produkt = 'Muesli' and price = '2,99'
# Daten hinzufügen
insert into NAME (SPALTENNAME) values (WERT)
insert into sortiment (produkt, preis) values ('Banane', '0,5')
# Daten löschen
delete from NAME where BEDINGUNG
delete from sortiment where preis = '1'
