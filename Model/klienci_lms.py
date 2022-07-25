

class Klient_LMS():
    
	def __init__(self,id_klienta:int,nazwa_klienta:str,miejscowosc:str,ulica:str,numer_domu:str,adres_ip:str):
		self.id_klienta = id_klienta
		self.nazwa_klienta = nazwa_klienta
		self.miejscowosc = miejscowosc
		self.ulica = ulica
		self.numer_domu = numer_domu
		self.adres_ip = adres_ip

	@classmethod
	def zwroc_nazwy_zmiennych_klasy(cls):
		obj = cls(
			id_klienta=0,
			nazwa_klienta="brak",
			miejscowosc="brak",
			ulica = "brak",
			numer_domu = "brak",
			adres_ip = "brak"
			)

		nazwy_zmiennych = list(obj.__dict__.keys())
		return nazwy_zmiennych
		

	def __str__(self) -> str:
		return f'Nazwa klienta: {self.nazwa_klienta}\nId klienta: {self.id_klienta}\nAdres ip: {self.adres_ip}\nMiejscowość: {self.miejscowosc}\nUlica: {self.ulica}\nNumer_domu: {self.numer_domu}\n'

	def __call__(self):
		return self.__dict__

	def __eq__(self,other):
		if self.nazwa_klienta == other.nazwa_klienta:
			return True
		return False









