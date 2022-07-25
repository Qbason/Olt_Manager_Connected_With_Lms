from os import path

#data log in to lms
username = "username for LMS"
password = "password for LMS"
url_lms = "full path to lms like http://192.168.1.2"

slownik_danych_logowania_karolinka = {
			"id": 1,
			"host": "adres_ip",
			"user": "user_name",
			"password": "password",
			"port": "port number!",
			"name":"name for olt"

		}
slownik_danych_logowania_biuro = {
			"id": 2,
			"host": "second adres ip",
			"user": "user_name",
			"password":"password",
			"port":"port number",
			"name":"name for olt"

		}

#data log in  to olt
lista_na_slowniki_danych_logowania = [
    slownik_danych_logowania_karolinka,
    slownik_danych_logowania_biuro
    ]

ilosc_oltow = len(lista_na_slowniki_danych_logowania)

sciezka = dirname = path.dirname(__file__)

#a max number of ont per slot
maksymalny_numer_id = 127

wyjatki_lms = [
	"some_desc_to_skip",
]
#set the value if the signal is not appeared in olt
wartosc_gdy_nie_pokazuje_sygnalu = -50