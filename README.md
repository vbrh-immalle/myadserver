# AdBlockers

Opgelet tijdens het testen: als je AdBlocker's hebt geïnstalleerd in je webbrowser,
kunnen afbeeldingen soms geblokkeerd worden!
Disable dus AdBlocker's voor localhost!

# Over de tests

Run de tests in `db_test.py` door simpelweg `pytest` uit te voeren in de directory.
`pytest` moet wel (globaal) geïnstalleerd zijn.

Er wordt een **fixture** gebruikt die een eventuele bestaande test_db eerst verwijdert en opnieuw aanmaakt.
Dit gebeurt normaal gezien voor *elke* test opnieuw.
Elke test begint dus steeds met dezelfde db (en tests kunnen elkaar niet beïnvloeden).

De fixture wordt in alle testen als parameter meegegeven.

# Browser-cache

Gebruik `shift-F5` om een 'harde' refresh te doen v.d. pagina.

Ook bij het registreren van clicks moet je opletten dat niet de cache gebruikt wordt.
Controleer daarom altijd het Netwerk-development-tab om te zien wat er echt gebeurt.
Open links eventueel in een ander (of incognito-) venster of zoek een manier om de cache uit te schakelen.
