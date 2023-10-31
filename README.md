# Reseptien-hallintasovellus

Sovelluksen avulla käyttäjä voi järjestää ja tallentaa omia reseptejään.

Sovelluksen toimivat ominaisuudet:

- Käyttäjä voi luoda uuden tunnuksen.
- Käyttäjä voi kirjautua sisään ja ulos.
- Käyttäjä voi lisätä uuden reseptin tietokantaan.
- Lisätylle reseptille voi laittaa nimen, ainesosat ja valmistusohjeet.
- Käyttäjä voi muokata tarvittaessaan omaa reseptiään.
- Käyttäjä voi poistaa oman/omat reseptin/reseptinsä.
- Reseptejä voi hakea nimen perusteella.
- Käyttäjä voi kommentoida reseptejä, muokata ja poistaa niitä.
- Käyttäjät voivat tykätä suosikkireseptejään.
- Käyttäjä voi luoda haluamastaan reseptistä ostoslistan.

## Käyttöohje

- Kloonaa repositorio koneellesi
- Asenna python3.11-venv esim sudo apt install python3.11-venv
- Luo Pythonin virtuaaliympäristö kansion sisään komennolla python3 -m venv venv
- Aktivoi virtuaaliympäristö: source venv/bin/activate
- Asenna flask pip install flask
- Asenna riippuvuudet pip install -r requirements.txt
- Aseta oma PostgreSQL-tietokanta nimi .env kohtaan "postgresql:///{tietokannan nimi}"
- Aseta oma salainen avain __init__.py tiedoston kohtaan app.config["SECRET_KEY"] = "salainen avain"
- Luo schema.sql -tiedoston mukaiset tietokantataulut PostgreSQL-komentoikkunassa
- Aloita sovelluksen käyttäminen Reseptien-hallintasovellus -kansiossa

