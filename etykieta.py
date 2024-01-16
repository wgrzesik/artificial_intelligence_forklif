import secrets, string

class Etykieta:
    def __init__(self, nadawca, adres, imie, nazwisko, telefon, priorytet):
        self.nadawca = nadawca
        self.adres = adres
        self.imie = imie
        self.nazwisko = nazwisko
        self.telefon = telefon
        self.priorytet = priorytet
        self.id = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(9))