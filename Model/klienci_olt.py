
class Klient_Koncowka():
    
	def __init__(self,id_olta:int,nazwa:str,sygnal_rx_olt:float,sygnal_rx_onu:float,wyjscie_olt:str):
		
		self.nr_olta = id_olta
		self.nazwa = nazwa
		self.sygnal_rx_olt = sygnal_rx_olt
		self.sygnal_rx_onu = sygnal_rx_onu
		self.wyjscie_olt = wyjscie_olt

	@classmethod
	def zwroc_nazwy_zmiennych_klasy(cls):
		obj = cls(0,"brak",-50,-50,"0/0/0/0")
		nazwy_zmiennych = list(obj.__dict__.keys())
		return nazwy_zmiennych
  
	def __str__(self):
		return(f"Nazwa koncowki: {self.nazwa}\nSygnal_rx_olt: {self.sygnal_rx_olt}\nSygnal_rx_onu: {self.sygnal_rx_onu}\nWyjscie_olt = {self.wyjscie_olt}\n"
		)

	def __call__(self):
		return self.__dict__

	def __eq__(self,other):
		if self.nazwa == other.nazwa and self.wyjscie_olt == other.wyjscie_olt:
			return True
		return False