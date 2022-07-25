from collections import defaultdict

from config import wartosc_gdy_nie_pokazuje_sygnalu

class Wszyscy_Klienci_Olt_Lms():
    
    def __init__(self, lock):
        # tablica  [klient_olt,klient_lms] * x
        self.lista_klientow_olt_lms = []
        self.lock = lock

    def ilosc_klientow(self):
        return len(self.lista_klientow_olt_lms)
    
    def dodaj_klienta_do_listy(self,klient_olt,klient_lms):

        #sprawdz, czy taki juz istnieje
        with self.lock:
            for klient_koncowka,klient_z_lms in self.lista_klientow_olt_lms:
                if klient_koncowka == klient_olt and klient_z_lms == klient_lms:
                    #print("Mamy już takiego klienta w bazie")
                    return False

            self.lista_klientow_olt_lms.append(
                [klient_olt,klient_lms]
            )
            return True
        
    def znajdz_klienta_po_nazwie_klienta_lms(self,nazwa_klienta):

            for klient_olt,klient_lms in self.lista_klientow_olt_lms:
                if klient_lms.nazwa_klienta == nazwa_klienta:
                    return klient_olt,klient_lms
            return None,None

    def posortuj_liste_po_zmiennej_z_olt(self,poczym,czy_odwrotnie):
            self.lista_klientow_olt_lms.sort(
            key=lambda klient_olt_lms: klient_olt_lms[0]()[poczym],
            reverse=czy_odwrotnie
            )

    def posortuj_liste_po_zmiennej_z_lms(self,poczym,czy_odwrotnie):

            self.lista_klientow_olt_lms.sort(
            key=lambda klient_olt_lms: klient_olt_lms[1]()[poczym],
            reverse=czy_odwrotnie
            )

    def zwroc_klientow_po_filtrze(self,nazwa_k_filtr,miejscowosc_filtr,ulica_filtr):

        nazwa_k_filtr = nazwa_k_filtr.lower()
        miejscowosc_filtr = miejscowosc_filtr.lower()
        ulica_filtr = ulica_filtr.lower()

        for klient_olt,klient_lms in self:
            if klient_lms.nazwa_klienta.lower().find(nazwa_k_filtr)>-1:
                if klient_lms.miejscowosc.lower().find(miejscowosc_filtr)>-1:
                    if klient_lms.ulica.lower().find(ulica_filtr)>-1:
                        yield klient_olt,klient_lms


    def __iter__(self):

        for klient_olt,klient_lms in self.lista_klientow_olt_lms:
            yield klient_olt,klient_lms

    def pogrupuj_miejscowosc_ulica_dla_sygnal_analiza(self):

        slownik_na_zliczanie_wystapien = defaultdict(int)
        slownik_na_sume_rx_olt = defaultdict(int)
        slownik_na_sume_rx_onu = defaultdict(int)

        slownik_na_max_rx_olt = defaultdict(
            (lambda:-50)
        )
        slownik_na_min_rx_olt = defaultdict(
            (lambda:50)
        )
        slownik_na_max_rx_onu = defaultdict(
            (lambda:-50)
        )
        slownik_na_min_rx_onu = defaultdict(
            (lambda:50)
        )

        for klient_olt,klient_lms in self:

            rx_onu = klient_olt.sygnal_rx_onu
            rx_olt = klient_olt.sygnal_rx_olt
            if rx_onu == wartosc_gdy_nie_pokazuje_sygnalu or rx_onu==-40.0 or klient_lms.miejscowosc == "brak":
                continue
            
            miejscowosc = klient_lms.miejscowosc
            ulica = klient_lms.ulica
            miejsc_ul = miejscowosc+"_"+ulica
            rx_olt = klient_olt.sygnal_rx_olt
            rx_onu = klient_olt.sygnal_rx_onu
           
            slownik_na_zliczanie_wystapien[miejsc_ul] += 1
            slownik_na_sume_rx_olt[miejsc_ul] += rx_olt
            slownik_na_sume_rx_onu[miejsc_ul] += rx_onu

            if rx_olt > slownik_na_max_rx_olt[miejsc_ul]:
                slownik_na_max_rx_olt[miejsc_ul] = rx_olt
            if rx_olt < slownik_na_min_rx_olt[miejsc_ul]:
                slownik_na_min_rx_olt[miejsc_ul] = rx_olt

            if rx_onu > slownik_na_max_rx_onu[miejsc_ul]:
                slownik_na_max_rx_onu[miejsc_ul] = rx_onu
            if rx_onu < slownik_na_min_rx_onu[miejsc_ul]:
                slownik_na_min_rx_onu[miejsc_ul] = rx_onu

        #print(f"Liczba miejsco_ulic {slownik_na_zliczanie_wystapien}")
        #tab = []  
        for miejsc_ulic in slownik_na_zliczanie_wystapien.keys():

            miejscowosc,ulica = miejsc_ulic.split("_")

            srednia_rx_olt = round(slownik_na_sume_rx_olt[miejsc_ulic]/slownik_na_zliczanie_wystapien[miejsc_ulic],2)
            srednia_rx_onu = round(slownik_na_sume_rx_onu[miejsc_ulic]/slownik_na_zliczanie_wystapien[miejsc_ulic],2)

            min_rx_olt = slownik_na_min_rx_olt[miejsc_ulic]
            max_rx_olt = slownik_na_max_rx_olt[miejsc_ulic]

            min_rx_onu = slownik_na_min_rx_onu[miejsc_ulic]
            max_rx_onu = slownik_na_max_rx_onu[miejsc_ulic]
            
            yield [miejscowosc,ulica,srednia_rx_olt,srednia_rx_onu,min_rx_olt,max_rx_olt,min_rx_onu,max_rx_onu]
        #return tab

    def znajdz_klientow_po_miejscowosci_ulicy(self,miejscowosc,ulica):
        for klient_olt,klient_lms in self:
            if klient_lms.miejscowosc == miejscowosc:
                if klient_lms.ulica == ulica:
                    yield klient_olt,klient_lms


    @property
    def klienci_olt_lms(self):
        return self.lista_klientow_olt_lms


            
