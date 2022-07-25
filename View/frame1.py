from tkinter import Frame,Label,Entry,Button
from tkinter.ttk import Combobox
from concurrent.futures import ThreadPoolExecutor

from Tools.tools import Dodatkowe_Narzedzia
from ViewModel.mainviewmodel import MainViewModel #import tylko na cele typowania 


class Frame1(Frame):
    def __init__(self,master,lock,zajetosc,mainviewmodel:MainViewModel,**kwargs):
        super().__init__(master, **kwargs)
        self.zajetosc = zajetosc
        self.mainviewmodel = mainviewmodel
        self.obsluga_lms = mainviewmodel.obsluga_lms
        self.lock = lock
        
        
        self_row = 10
        self_cols = 8
        
        for i in range(0,self_cols):
            self.columnconfigure(i,weight=1)
        for i in range(0,self_row):
            self.rowconfigure(i,weight=1)
        
        
        #main title
        self.l_gen_info = Label(
            self,
            text="Sprawdź sygnał na danym olcie",
            foreground="black",
            bg="white",
            font=("Arial bold",14,"bold"),
            borderwidth=2,
            relief="raised"
        )
        self.l_gen_info.grid(
            row=0,
            column=0,
            columnspan=8,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing olt label
        self.l_olt_types = Label(
            self,
            text="Wybierz olta:",
            foreground="black",
            bg="white",
            font=("Arial",12,"bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_olt_types.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing olt combobox
        self.dict_for_olt = {
            "Karolinka":1,
            "Biuro":2,
        }
        
        self.c_olt_types = Combobox(
            self,
            width=10,
            state="readonly",
            values = list(self.dict_for_olt)
        )
        self.c_olt_types.current(0)
        self.c_olt_types.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        
        #for choosing board number label
        self.l_board_numer = Label(
            self,
            text="Podaj numer płyty:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_board_numer.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing board number combobox
        board_numbers = 1
        
        self.c_board_numer = Combobox(
            self,
            width=10,
            state="readonly",
            values = list(range(board_numbers+1))
        )
        self.c_board_numer.current(0)
        self.c_board_numer.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing exit number label
        self.l_number_exit = Label(
            self,
            text="Podaj numer wyjscia:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
            
        )
        self.l_number_exit.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing exit number combobox
        numbers_of_exits = 7
        
        self.c_number_exit = Combobox(
            self,
            width=10,
            state="readonly",
            values = list(range(numbers_of_exits+1))
        )
        self.c_number_exit.current(0)
        self.c_number_exit.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing number id label
        self.l_number_id = Label(
            self,
            text="Podaj numer id:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
            
        )
        self.l_number_id.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        #for choosing number id Entry
        self.e_number_id = Entry(
            self,
            width=10,
            justify="center",

        )
        
        self.e_number_id.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.b_search = Button(
            self,
            text="Szukaj",
            font=("Arial",12,"bold"),
            borderwidth=2,
            relief="raised",
            command=self.szukaj_koncowke
        )
        self.b_search.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            
        )
        
        self.l_name_device = Label(
            self,
            text="Nazwa końcówki:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        
        self.l_name_device.grid(
            row=1,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_name_device_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),

        )
        
        self.l_name_device_output.grid(
            row=2,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_rx_olt = Label(
            self,
            text="Sygnał rx olt:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_rx_olt.grid(
            row=3,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_rx_olt_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),

        )
        self.l_rx_olt_output.grid(
            row=4,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )        
        
        
        self.l_rx_onu = Label(
            self,
            text="Sygnał rx onu:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_rx_onu.grid(
            row=5,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_rx_onu_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),

        )
        self.l_rx_onu_output.grid(
            row=6,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )  
        
        self.l_exit_desc = Label(
            self,
            text="Wyjście:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_exit_desc.grid(
            row=7,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_exit_desc_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),

        )
        self.l_exit_desc_output.grid(
            row=8,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        ) 
        
        
        self.list_for_mess_output = []
        

        
        self.l_name_client = Label(
            self,
            text="Nazwa klienta:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_name_client.grid(
            row=1,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_name_client_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),
        )
        self.l_name_client_output.grid(
            row=2,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_name_place = Label(
            self,
            text="Miejscowość:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_name_place.grid(
            row=3,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_name_place_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),
        )
        self.l_name_place_output.grid(
            row=4,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        
        self.l_name_street = Label(
            self,
            text="Ulica:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_name_street.grid(
            row=5,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_name_street_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),
        )
        self.l_name_street_output.grid(
            row=6,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_number_house = Label(
            self,
            text="Numer domu:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_number_house.grid(
            row=7,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_number_house_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),
        )
        self.l_number_house_output.grid(
            row=8,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_ip_adres = Label(
            self,
            text="Adres ip:",
            foreground="black",
            bg="white",
            font=("Arial","12","bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_ip_adres.grid(
            row=1,
            column=6,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        self.l_ip_adres_output = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),
            width=10
        )
        self.l_ip_adres_output.grid(
            row=2,
            column=6,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        
        self.info_ouput_frame1 = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial","12"),
            height=2,
            justify="center"
        )
        
        self.info_ouput_frame1.grid(
            row=9,
            column=2,
            columnspan=6,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )
        
        
    def szukaj_koncowke_thread(self):
        
        
        olt_number = self.dict_for_olt[self.c_olt_types.get()]

        self.zajetosc[olt_number-1] = True

        numer_id = self.e_number_id.get()
        result,info = Dodatkowe_Narzedzia.do_validation_input_and_info_for_id(numer_id)
        
        if not result:
            self.generate_info("Błędnie podany numer id\n" +info)
        else:
            
            board_number = self.c_board_numer.current()
            exit_number = self.c_number_exit.current()
            number_id = self.e_number_id.get()
            succ,info,object_klient,object_klient_lms = self.mainviewmodel.znajdz_koncowke_klienta_lms(
                olt_number,
                board_number,
                exit_number,
                number_id
            )
            
            if succ:
                dict_data = object_klient()
                self.l_name_device_output['text'] = dict_data['nazwa']
                self.l_rx_olt_output['text'] = str(dict_data['sygnal_rx_olt'])
                self.l_rx_onu_output['text'] = str(dict_data['sygnal_rx_onu'])
                self.l_exit_desc_output['text'] = dict_data['wyjscie_olt']
                
                dict_data_lms_client = object_klient_lms()
                self.l_name_client_output['text'] = dict_data_lms_client["nazwa_klienta"]
                self.l_name_place_output['text'] = dict_data_lms_client['miejscowosc']
                self.l_name_street_output['text'] = dict_data_lms_client['ulica']
                self.l_number_house_output['text'] = dict_data_lms_client['numer_domu']
                self.l_ip_adres_output['text'] = dict_data_lms_client['adres_ip']
            
                    
            self.l_exit_desc_output['text'] = f"0/{board_number}/{exit_number}/{number_id}"
            self.generate_info(info)

        self.zajetosc[olt_number-1] = False

           
    def szukaj_koncowke(self):
        
        olt_number = self.dict_for_olt[self.c_olt_types.get()]
        
        if self.zajetosc[olt_number-1] == False:
            executor = ThreadPoolExecutor()
            executor.submit(self.czysc_pola)
            executor.submit(self.generate_info,"Trwa wykonywanie operacji..")
            executor.submit(self.szukaj_koncowke_thread)
            # self.czysc_pola()
            # self.generate_info("Trwa wykonywanie operacji")
            # self.szukaj_koncowke_thread()
            
            
        else:
            self.generate_info("Proszę czekać na zakończenie zadania")
            
            
            
    def czysc_pola(self):
        self.l_name_device_output['text'] = ""
        self.l_rx_olt_output['text'] = ""
        self.l_rx_onu_output['text'] = ""
        self.l_exit_desc_output['text'] = ""
        self.l_name_client_output['text'] = ""
        self.l_name_place_output['text'] = ""
        self.l_name_street_output['text'] = ""
        self.l_number_house_output['text'] = ""
        self.l_ip_adres_output['text'] = ""
            
    def generate_info(self,text):
        self.info_ouput_frame1['text'] = text
        return True