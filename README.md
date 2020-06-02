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
