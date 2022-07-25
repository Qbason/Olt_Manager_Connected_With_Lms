import requests
from os import path


from config import url_lms,username,password,sciezka,wyjatki_lms
from bs4 import BeautifulSoup
from Model.klienci_lms import Klient_LMS
from Model.klienci_olt import Klient_Koncowka

class Obsluga_LMS():
	def __init__(self):
		url = url_lms
		self.session = requests.session()
		response = self.session.post(
			url,
			data={"loginform[login]":username,"loginform[pwd]":password,"loginform[submit]":"Zaloguj się"}
		)
		if not (response.status_code==200):
			self.close_session()
			raise "Nie udało się zalogować"


	def close_session(self):
		self.session.close()

	def zarejestruj_klientow_bez_odpowiednika_w_lms(self,nazwa_z_olta):
		filename = path.join(sciezka, 'nie_znaleziono.txt')
		with open(filename,"a+") as file:
			file.write(nazwa_z_olta+"\n")


	def utworz_klienta_po_koncowce(self,Klient:Klient_Koncowka):

		info = ""

		url_test = f"http://192.168.100.247/?m=quicksearch&ajax=1&mode=node&what={Klient.nazwa}"
  
		response = self.session.get(
			url_test
		)
  
		lista_nazw,lista_linkow = self.dekoduj_tekst_na_dane(response.text)
  
		if len(lista_nazw)!=0:
			if len(lista_nazw)>=1:
				#to oznacza, że mamy więcej klientow odpowiadajacym temu wpisowi!
				rezultat_success,info_o,Klient_Lms = self.utworz_obiekt_klienta_lms(lista_nazw[0],lista_linkow[0])
				info = info_o
			if not rezultat_success:
				info = info_o
				return [False,info,Klient_Lms]
			return [True,info,Klient_Lms]
		else:
			#sprawdzamy, czy nazwa należy do wyjątków
			#print(f"Moja nazwa to: {Klient.nazwa},\nwyjatki to: {wyjatki_lms}")
			if Klient.nazwa in wyjatki_lms:
				#print("test")
				info = f"Utworzono pustego klienta lms dla\n{Klient.nazwa} {Klient.wyjscie_olt}"
				Klient_Lms = self.utworz_pustego_klienta_lms(Klient.nazwa)
				return [True,info,Klient_Lms]


			#request nic nie znalazł 
			info = "Nie znaleziono koncowki w Lms"
			self.zarejestruj_klientow_bez_odpowiednika_w_lms(f"{Klient.nazwa} {Klient.wyjscie_olt}")
			return [False,info,None]

  
	def utworz_pustego_klienta_lms(self,nazwa):
		return Klient_LMS(
			id_klienta=0,
			nazwa_klienta=nazwa,
			miejscowosc="brak",
			ulica = "brak",
			numer_domu="brak",
			adres_ip="brak"
		)
  
  
	def wyluskaj_lokalizacje(self,soup):
		lokalizacja_pelna_wybrana = soup.select('td > img[alt="Lokalizacja:"]')
		if lokalizacja_pelna_wybrana:
			lokalizacja_pelna = lokalizacja_pelna_wybrana[0].parent.parent.select("td")[1].text.strip()
			lokalizacja_splitted = lokalizacja_pelna.split(", ul. ")
			miejscowosc = lokalizacja_splitted[0]
			ulica_numerdomu = lokalizacja_splitted[1].split(" ")
			ulica = " ".join(ulica_numerdomu[0:-1])
			numer_domu = ulica_numerdomu[-1]
			return [miejscowosc,ulica,numer_domu]
		return ["","",""]
  
  
	def wyluskaj_nazwe_klienta(self,soup)->str:
		nazwa_klienta_wybrana = soup.select('td > img[src="img/customer.gif"]')
		if nazwa_klienta_wybrana:
			nazwa_klienta = nazwa_klienta_wybrana[0].parent.select("b")[1].text.strip().split(" (")[0]
   
			return nazwa_klienta
		return ""

  
	def wyluskaj_adres_ip(self,soup)->str:
		adres_ip_wybrany = soup.select('td > img[alt="Adres IP:"]')
		if adres_ip_wybrany:
			adres_ip = adres_ip_wybrany[0].parent.parent.select("td")[1].text.strip()
			return adres_ip
		return ""
  
  
  
	def utworz_obiekt_klienta_lms(self,nazwa:str,link:str):
		info = ""
		try:
			soup = BeautifulSoup(self.session.get(url_lms+link).text,"html.parser")
	
			id = int(link.split("=")[-1])

			miejscowosc,ulica,numer_domu = self.wyluskaj_lokalizacje(soup)
			nazwa_klienta = self.wyluskaj_nazwe_klienta(soup)
			adres_ip = self.wyluskaj_adres_ip(soup)
   
			if miejscowosc=="":
				raise ValueError("Problem z odczytem miejscowości.")
			if nazwa_klienta=="":
				raise ValueError("Problem z odczytem nazwy klienta.")
			if adres_ip=="":
				raise ValueError("Problem z odczytem adresu ip.")
			
   
			Klient_Lms_Nowy = Klient_LMS(id,nazwa_klienta,miejscowosc,ulica,numer_domu,adres_ip)

			info = f"Pomyślnie dodano klienta\n{nazwa_klienta[:40]}"
			return [True,info,Klient_Lms_Nowy]
		except Exception as e:
			info = f"{e} Nazwa: {nazwa}"
			filename = path.join(sciezka,'bledne.txt')
			with open(filename,"a+") as file:
				file.write(info)

			return [False,info,None]
  
  
	def dekoduj_tekst_na_dane(self,tekst):
		try:
			if tekst!="false;\n":
				nazwy,_,linki = [tekst.split(" = ")[1][1:-1] for tekst in tekst.split(";")[:-1]]
				lista_nazw = [user[1:-1] for user in nazwy.split(",")]
				lista_linkow = [link[1:-1] for link in linki.split(",")]
				return [lista_nazw,lista_linkow]
			return [list(),list()]
		except:
			#print("Problem z dekodowaniem tekstu!")
			return [list(),list()]