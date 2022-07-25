import time
import telnetlib

from config import lista_na_slowniki_danych_logowania,wartosc_gdy_nie_pokazuje_sygnalu
from Tools.tools import Dodatkowe_Narzedzia

class Olt_Komunikacja():

	def __init__(self,ktory_olt):
		self.numer_plyty = -1 # domyślnie niezalogowany
		self.wartosc_gdy_nie_pokazuje_sygnalu = wartosc_gdy_nie_pokazuje_sygnalu

		for olt in lista_na_slowniki_danych_logowania:
			if olt["id"] == ktory_olt:
				host = olt["host"]
				user = olt["user"]
				password = olt["password"]
				port = olt["port"]

				#host,user,password,port,nazwa_olta = 
				try:
					self.telnet_object = telnetlib.Telnet(host,port,timeout=2)
				except:
					raise RuntimeError("Nie udało połączyć się z oltem")
				#self.telnet_object.set_debuglevel(100)
				self.user = user
				self.password = password
				#self.telnet_object.set_debuglevel(100)
				#1 - KArolinka 2 - Biuro
				self.numer_olta = ktory_olt
				return
		raise ValueError("Nie ma takiego olta!")



	def zaloguj_do_systemu(self):
		try:
			self.telnet_object.read_until(b"name:")
			self.telnet_object.write(self.user.encode('utf-8') + b"\n")
			time.sleep(.2)
			self.telnet_object.read_until(b"password:")
			self.telnet_object.write(self.password.encode("utf-8") + b"\n")
			time.sleep(.2)
			if self.numer_olta == 1:
				self.telnet_object.write(b" ")
			return True
		except Exception as e:
			#("Error logowanie: ",e)
			return False

	def tryb_configuracji(self):
		self.telnet_object.write("enable".encode("utf-8")+ b"\n")
		time.sleep(.1)
		self.telnet_object.write("config".encode("utf-8")+ b"\n")
		time.sleep(.1)
		self.telnet_object.read_until(b"config)#").decode("utf-8")
		
	def zaloguj_do_plyty(self,numer_plyty):
		if self.numer_plyty == -1:
			self.numer_plyty = numer_plyty
			polecenie = "interface gpon 0/" +str(numer_plyty)
			self.telnet_object.write(polecenie.encode("utf-8")+ b"\n")
			time.sleep(.1)
			
			self.telnet_object.read_until(b"#").decode("utf-8")
		else:
			raise ValueError("Już zalogowano do płyty!")
  
  
	def wyloguj_z_plyty(self):
		if self.numer_plyty!=-1:
			polecenie = "quit"
			self.telnet_object.write(polecenie.encode("utf-8")+ b"\n")
			time.sleep(.1)
			self.telnet_object.read_until(b"#").decode("utf-8")
			self.numer_plyty = -1
		else:
			raise ValueError("Nie można wylogować z niezalogowanej płyty")
		
  
	def wyswietl_koncowke(self,wyjscie,numer):
		polecenie = "display ont info " +str(wyjscie)+" "+str(numer)
		self.telnet_object.write(polecenie.encode("utf-8")+ b"\n")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		time.sleep(.01)
		return self.telnet_object.read_until(b"#").decode("utf-8")

	def wyswietl_sygnal_koncowki(self,wyjscie,numer):
		polecenie = "display ont optical-info " +str(wyjscie)+" "+str(numer)
		self.telnet_object.write(polecenie.encode("utf-8")+ b"\n")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		return self.telnet_object.read_until(b"#").decode("utf-8")
		
	def sprawdz_ilosc_koncowek(self,wyjscie):
		polecenie = "display ont info " +str(wyjscie)+" all"
		self.telnet_object.write(polecenie.encode("utf-8")+ b"\n")
		time.sleep(.01)
		self.telnet_object.write(b" ")
		self.telnet_object.write(b" ")
		self.telnet_object.write(b" ")
		self.telnet_object.write(b" ")
		self.telnet_object.write(b" ")
		self.telnet_object.write(b" ")
		self.telnet_object.write(b" ")
  
		return self.telnet_object.read_until(b"#").decode("utf-8")
  
  
	def zaloguj_do_trybu_konfiguracji(self):
		self.zaloguj_do_systemu()
		self.tryb_configuracji()

	def zamknij_sesje(self):
		self.telnet_object.close()
  
  
class Olt_Analiza():


	wartosc_gdy_nie_pokazuje_sygnalu = wartosc_gdy_nie_pokazuje_sygnalu

	polecenia = {
		"name":"Description",
		"noexist":"Failure: The ONT does not exist",#for info/optical-info if not exist
		"offline":"Failure: The ONT is not online",#for optical-info if is not online
		"rx_onu":"Rx optical power(dBm)",
		"rx_olt":"OLT Rx ONT optical power(dBm)",
		"total_ont":"the total of ONTs are: "
	}


	def czy_fraza_w_tekscie(self,tekst:str,fraza:str):
		linie_podzielone = (linia for linia in tekst.split("\n"))
		for linia in linie_podzielone:
			if linia.find(fraza) > -1:
				return True
		return False
                
                
	def znajdz_fraze_w_tekscie_i_zwroc(self,tekst:str,fraza:str):
		linie_podzielone = (linia for linia in tekst.split("\n"))
		for linia in linie_podzielone:
			if linia.find(fraza) > -1:
				return linia

		raise "Nie znaleziono nazwy frazy"
                

	def odczytaj_nazwe_koncowki(self,opis_koncowki):
     
		nazwa_urzadzenia_opis = self.znajdz_fraze_w_tekscie_i_zwroc(opis_koncowki,self.polecenia["name"])
		nazwa_urzadzenia = (nazwa_urzadzenia_opis.split(": ")[-1]).split(" ")[0].strip()

		return nazwa_urzadzenia

	def sprawdz_czy_koncowka_offline(self,opis_koncowki_optyczny):
		
		return self.czy_fraza_w_tekscie(opis_koncowki_optyczny,self.polecenia["offline"])


	def odczytaj_sygnal_olt(self,opis_koncowki_optyczny,ktory_sygnal):
     
		rx_opis = self.znajdz_fraze_w_tekscie_i_zwroc(opis_koncowki_optyczny,ktory_sygnal)
		#dzielimy tekst i bierzemy tylko wartosc
		sygnal_rx = (rx_opis.split(": ")[-1]).split(",")[0]
		return sygnal_rx
  
	def sprawdz_czy_sygnal_istnieje_i_zwroc_wartosc(self,sygnal):
		t1 = Dodatkowe_Narzedzia.try_parse_to_float(sygnal)
		if t1:
			return float(sygnal)
		return self.wartosc_gdy_nie_pokazuje_sygnalu

	def odczytaj_ilosc_koncowek_ont(self,opis_koncowki_all):
		ilosc_koncowek_na_wyjsciu_opis = self.znajdz_fraze_w_tekscie_i_zwroc(opis_koncowki_all,self.polecenia['total_ont'])
		ilosc_koncowek_na_wyjsciu = ilosc_koncowek_na_wyjsciu_opis.split("are: ")[1].split(",")[0].strip()

		return int(ilosc_koncowek_na_wyjsciu)


	def czy_mozna_pokazac_koncowke_info(self,opis_koncowki:str, opis_koncowki_optyczny:str):
		
		"""
		Pierwszy element mowi, czy mozna pokazac koncowke
		Drugi, zawiera stosowany komunikat
		Returns:
			list:[bool,"info"]
		"""
  
		czy_nie_istnieje_koncowka = self.sprawdz_czy_koncowka_nie_istnieje(opis_koncowki)
	
		#print("Czy ta koncowka nie istnieje: ",czy_nie_istnieje_koncowka)
	
		if czy_nie_istnieje_koncowka:
			return [False,f"Taka końcówka nie istnieje"]

		czy_jest_offline = self.sprawdz_czy_koncowka_offline(opis_koncowki_optyczny)
		#print("Czy ta koncowka jest offline: ",czy_jest_offline)
		if czy_jest_offline:
			return [False,f"Taka końcówka jest offline"]

		return [True,f"Końcówka jest istnieje i jest online"]


	def przeksztalc_opisy_koncowki_na_odpowiednie_dane(self,opis_koncowki:str,opis_koncowki_optyczny:str):

		nazwa_koncowki = self.odczytaj_nazwe_koncowki(opis_koncowki=opis_koncowki)

		sygnal_rx_olt = self.odczytaj_sygnal_olt(opis_koncowki_optyczny=opis_koncowki_optyczny,ktory_sygnal = self.polecenia["rx_olt"])
		sygnal_rx_onu = self.odczytaj_sygnal_olt(opis_koncowki_optyczny=opis_koncowki_optyczny,ktory_sygnal = self.polecenia["rx_onu"])
		
		sygnal_rx_olt = self.sprawdz_czy_sygnal_istnieje_i_zwroc_wartosc(sygnal_rx_olt)
		sygnal_rx_onu = self.sprawdz_czy_sygnal_istnieje_i_zwroc_wartosc(sygnal_rx_onu)
			
		return nazwa_koncowki,sygnal_rx_olt,sygnal_rx_onu
   

	def sprawdz_czy_koncowka_nie_istnieje(self,opis_koncowki):
     
		czy_nie_istnieje = self.czy_fraza_w_tekscie(opis_koncowki,self.polecenia["noexist"])
  
		return czy_nie_istnieje
