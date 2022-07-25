import pickle
from os import path
from Model.klienci_lms import Klient_LMS
from Model.klienci_olt import Klient_Koncowka
from Model.klienci_wszyscy import Wszyscy_Klienci_Olt_Lms
from ViewModel.lms import Obsluga_LMS
from ViewModel.olt import Olt_Analiza,Olt_Komunikacja
from config import sciezka




class MainViewModel():
    
	def __init__(self,lock):
		self.obsluga_lms = Obsluga_LMS()
		self.wszyscy_klienci = Wszyscy_Klienci_Olt_Lms(lock)
		self.lock = lock

	def przeskanuj_calego_olta(self,numer_olta:int):
		
		object_klient,object_client_lms = None,None

		try:
			olt_komunikacja = Olt_Komunikacja(numer_olta)
		except Exception as e:
			yield [False,e,object_klient,object_client_lms]
			
		olt_analiza = Olt_Analiza()
		olt_komunikacja.zaloguj_do_trybu_konfiguracji()
		numery_plyt = list(range(2))
		numery_wyjsc = list(range(8))
		for numer_plyty in numery_plyt:
			olt_komunikacja.zaloguj_do_plyty(numer_plyty)
			for numer_wyjscia in numery_wyjsc:
				
				#sprawdzenie od razu nas może zalogować!
				ile = self.sprawdz_ilosc_koncowek_na_wyjsciu(olt_analiza,olt_komunikacja,numer_olta,numer_plyty,numer_wyjscia,czy_wylogowac_z_plyty=False)
				if ile == -1:
					yield [False,"Problem ze sprawdzeniem ilości końcówek!",object(),object()]
				numery_id = list(range(1,ile+1))
				
				for numer_id in numery_id:
					#wyjscie_olt = f'0/{numer_plyty}/{numer_wyjscia}/{numer_id}'
					succ,info,object_klient = self.sprawdz_sygnal_koncowki_na_olcie_skan(
						olt_analiza,
						olt_komunikacja,
						numer_plyty,
						numer_wyjscia,
						numer_id,
						czy_zalogowac_do_plyty=False
					)
					if succ:
						succ,info,object_client_lms = self.obsluga_lms.utworz_klienta_po_koncowce(object_klient)
						if succ:
							#jeżeli wszystko przebiegnie prawidłowo należy dodać obiekty do klasy!!!
							self.wszyscy_klienci.dodaj_klienta_do_listy(object_klient,object_client_lms)
							#tablica_tymczasowa.append([object_klient,object_client_lms])
							yield [True,info,object_klient,object_client_lms]
							continue
						
	
	
					yield[False,info,object_klient,object_client_lms]
					
				
					
			olt_komunikacja.wyloguj_z_plyty()
		olt_komunikacja.zamknij_sesje()


		#print("Koniec skanowania")
		yield [False,f"Dodawanie końcówek dla olta numer\n{numer_olta} zakończone",object_klient,object_client_lms]


	def zapisz_liste_obiektow_do_pliku(self):

		nazwa_plika_pelna_sciezka = path.join(sciezka,'obiekty')

		with open(nazwa_plika_pelna_sciezka,'wb') as outp:
			pickle.dump(self.wszyscy_klienci.klienci_olt_lms)



	def sprawdz_ilosc_koncowek_na_wyjsciu(self,olt_analiza:Olt_Analiza,komunikacja_z_olt:Olt_Komunikacja,olt_numer:int,numer_plyty:int,numer_wyjscia:int,czy_wylogowac_z_plyty=False):
		"""
		Ważne! używać dopiero po załadowaniu komunikacji do olta! i po zalogowaniu do płyty!
		"""
		try:	

			ilosc_koncowek_kontent = komunikacja_z_olt.sprawdz_ilosc_koncowek(wyjscie=numer_wyjscia)
			ile_koncowek = olt_analiza.odczytaj_ilosc_koncowek_ont(ilosc_koncowek_kontent)

			if czy_wylogowac_z_plyty == True:
				komunikacja_z_olt.wyloguj_z_plyty()
	
			return ile_koncowek
		except Exception as e:
			return -1

	
	def sprawdz_sygnal_koncowki_na_olcie_skan(self,olt_analiza:Olt_Analiza,komunikacja_z_olt:Olt_Komunikacja,numer_plyty:int,numer_wyjscia:int,numer_id:int,czy_zalogowac_do_plyty=False):
		
		
		obj_klient_koncowka = None
		
		if czy_zalogowac_do_plyty:
			komunikacja_z_olt.zaloguj_do_plyty(numer_plyty)

		opis_koncowki = komunikacja_z_olt.wyswietl_koncowke(numer_wyjscia,numer_id)
		opis_koncowki_optyczny = komunikacja_z_olt.wyswietl_sygnal_koncowki(numer_wyjscia,numer_id)

		wyjscie_olt = f"0/{komunikacja_z_olt.numer_plyty}/{numer_wyjscia}/{numer_id}"
		czy_mozna,info = olt_analiza.czy_mozna_pokazac_koncowke_info(opis_koncowki,opis_koncowki_optyczny)

		info = info + f"\n0\{numer_plyty}\{numer_wyjscia}\{numer_id}"
	
		if czy_mozna:
			
			nazwa_urzadzenia,sygnal_rx_olt,sygnal_rx_onu = olt_analiza.przeksztalc_opisy_koncowki_na_odpowiednie_dane(opis_koncowki,opis_koncowki_optyczny)
			obj_klient_koncowka = Klient_Koncowka(komunikacja_z_olt.numer_olta,nazwa_urzadzenia,sygnal_rx_olt,sygnal_rx_onu,wyjscie_olt)
				
		return [czy_mozna,info,obj_klient_koncowka]
	

	def znajdz_koncowke_klienta_lms(self,olt_numer:int,numer_plyty:int,numer_wyjscia:int,numer_id:str):
		
		object_klient = None
		object_lms = None
  
  
		succ,info,object_klient = self.sprawdz_sygnal_koncowki_na_olcie(
                olt_numer,
                numer_plyty,
                numer_wyjscia,
                numer_id
            )

		if not succ:
			return succ,info,object_klient,object_lms

		succ,info,object_lms = self.obsluga_lms.utworz_klienta_po_koncowce(object_klient)
		self.wszyscy_klienci.dodaj_klienta_do_listy(klient_olt=object_klient,klient_lms=object_lms)
		return succ,info,object_klient,object_lms


	def sprawdz_sygnal_koncowki_na_olcie(self,olt_numer:int,numer_plyty:int,numer_wyjscia:int,numer_id:str):
		

		obj_klient_koncowka = object()
		komunikacja_z_olt = Olt_Komunikacja(olt_numer)
		analiza_olta = Olt_Analiza()
	
		komunikacja_z_olt.zaloguj_do_trybu_konfiguracji()
		komunikacja_z_olt.zaloguj_do_plyty(numer_plyty)
		
		
		opis_koncowki = komunikacja_z_olt.wyswietl_koncowke(numer_wyjscia,numer_id)
		opis_koncowki_optyczny = komunikacja_z_olt.wyswietl_sygnal_koncowki(numer_wyjscia,numer_id)
	
		wyjscie_olt = f"0/{numer_plyty}/{numer_wyjscia}/{numer_id}"
		czy_mozna,info = analiza_olta.czy_mozna_pokazac_koncowke_info(opis_koncowki,opis_koncowki_optyczny)
		
		info = info + f"\n0\{numer_plyty}\{numer_wyjscia}\{numer_id}"

		if czy_mozna:
			
			nazwa_urzadzenia,sygnal_rx_olt,sygnal_rx_onu = analiza_olta.przeksztalc_opisy_koncowki_na_odpowiednie_dane(opis_koncowki,opis_koncowki_optyczny)
			obj_klient_koncowka = Klient_Koncowka(komunikacja_z_olt.numer_olta,nazwa_urzadzenia,sygnal_rx_olt,sygnal_rx_onu,wyjscie_olt)
			
		
		komunikacja_z_olt.zamknij_sesje()
		return [czy_mozna,info,obj_klient_koncowka]


	def znajdz_klienta_lms_po_nazwie_klienta(self,nazwa_klienta):
		
		return self.wszyscy_klienci.znajdz_klienta_po_nazwie_klienta_lms(nazwa_klienta)

	def zwroc_posortowanych_klientow_po(self,poczym,czy_odwrotnie):
		
		lista_nazw_zmiennych_koncowka = Klient_Koncowka.zwroc_nazwy_zmiennych_klasy()
		lista_nazw_zmiennych_klient_lms = Klient_LMS.zwroc_nazwy_zmiennych_klasy()

		if poczym in lista_nazw_zmiennych_koncowka:
			self.wszyscy_klienci.posortuj_liste_po_zmiennej_z_olt(poczym,czy_odwrotnie)
		else:
			if poczym in lista_nazw_zmiennych_klient_lms:
				self.wszyscy_klienci.posortuj_liste_po_zmiennej_z_lms(poczym,czy_odwrotnie)

		
		for klient_olt,klient_lms in self.wszyscy_klienci.klienci_olt_lms:
			yield klient_olt,klient_lms


	def zwroc_nazwy_wszystkich_zmiennych_wartosci_false_klas_koncowka_lms(self):
		nazwy_klasy_koncowka = Klient_Koncowka.zwroc_nazwy_zmiennych_klasy()
		nazwy_klasy_klient_lms = Klient_LMS.zwroc_nazwy_zmiennych_klasy()

		razem_nazwy = nazwy_klasy_koncowka + nazwy_klasy_klient_lms

		slownik_false = {klucz: False for klucz in razem_nazwy}

		return slownik_false

	def zwracaj_klient_koncowka_lms_po_filtrach(self,nazwa_k_filtr,miejscowosc_filtr,ulica_filtr):

		return self.wszyscy_klienci.zwroc_klientow_po_filtrze(nazwa_k_filtr,miejscowosc_filtr,ulica_filtr)


	def pogrupuj_po_miejscowosci_ulicy_dla_sygnalow_srednia_max_min(self):
		return self.wszyscy_klienci.pogrupuj_miejscowosc_ulica_dla_sygnal_analiza()

	def znajdz_nazwy_i_numery_domow_po_miejscowosci_ulicy(self,miejscowosc,ulica):
		for _,klient_lms in self.wszyscy_klienci.znajdz_klientow_po_miejscowosci_ulicy(miejscowosc,ulica):
			yield klient_lms.nazwa_klienta,klient_lms.numer_domu




