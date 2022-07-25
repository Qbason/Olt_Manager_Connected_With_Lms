from threading import Thread
from tkinter import END, Entry, Frame,Label,Scrollbar,Button
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox,Treeview
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from ViewModel.mainviewmodel import MainViewModel#na cele typowania



class Frame3(Frame):
    def __init__(self,master,lock,zajetosc,mainviewmodel:MainViewModel,**kwargs):
        super().__init__(master, **kwargs)
        self.zajetosc = zajetosc
        self.mainviewmodel = mainviewmodel
        self.lock = lock

        my_frame3_row = 20
        my_frame3_cols = 20
        
        for i in range(0,my_frame3_cols):
            self.columnconfigure(i,weight=1)
        for i in range(0,my_frame3_row):
            self.rowconfigure(i,weight=1)
        
        
        self.l_olt_types_frame3 = Label(
            self,
            text="Wybierz olta:",
            foreground="black",
            bg="white",
            font=("Arial",12,"bold"),
            relief="solid",
            borderwidth=2
        )
        self.l_olt_types_frame3.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,

        )
        
        self.dict_for_olt = {
            "Karolinka":1,
            "Biuro":2,
        }
        
        self.c_olt_types_frame3 = Combobox(
            self,
            state="readonly",
            values = list(self.dict_for_olt)+["Wszystkie"],
            justify="center",
            width=7
        )
        
        self.c_olt_types_frame3.grid(
            row=0,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
            ipadx=0,
            ipady=0

        )
        self.c_olt_types_frame3.current(0)

        self.b_scan_frame3 = Button(
            self,
            text="Skanuj",
            font=("Arial",12,"bold"),
            borderwidth=2,
            relief="raised",
            command=self.skanuj_olty
        )
        self.b_scan_frame3.grid(
            row=0,
            column=4,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
        )
        
        
        self.info_output_frame3 = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
            height=1,
            width=20

        )
        self.info_output_frame3.grid(
            row=0,
            column=6,
            columnspan=7,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.info_output_frame3_2 = Label(
            self,
            text="",
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
            height=1,
            width=20

        )
        self.info_output_frame3_2.grid(
            row=0,
            column=13,
            columnspan=7,
            sticky="nsew",
            padx=5,
            pady=5,
        )
        self.l_output_list = [
            self.info_output_frame3,
            self.info_output_frame3_2
        ]
        
        self.l_name_client = Label(
            self,
            text="Nazwa klienta:",
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
            height=1
        )
        self.l_name_client.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.e_name_client = Entry(
            self,
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
        )
        self.e_name_client.grid(
            row=1,
            column=3,
            columnspan=5,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.l_place = Label(
            self,
            text="Miejscowość:",
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
            height=1
        )
        self.l_place.grid(
            row=1,
            column=8,
            columnspan=3,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.e_place = Entry(
            self,
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
        )
        self.e_place.grid(
            row=1,
            column=11,
            columnspan=4,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.l_street = Label(
            self,
            text="Ulica:",
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
            height=1
        )
        self.l_street.grid(
            row=1,
            column=15,
            columnspan=2,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.e_street = Entry(
            self,
            foreground="black",
            bg="white",
            font=("Arial",8,"bold"),
            width=8
        )
        self.e_street.grid(
            row=1,
            column=17,
            columnspan=3,
            sticky="nsew",
            padx=5,
            pady=5,
        )
        
        self.e_name_client.bind("<KeyRelease>",self.filtruj_wyniki)
        self.e_place.bind("<KeyRelease>",self.filtruj_wyniki)
        self.e_street.bind("<KeyRelease>",self.filtruj_wyniki)
        
        columns = ('nr_olt', 'nazwa_device', 'rx_olt','rx_onu','wyjscie','nazwa_klienta')

        self.tree = Treeview(self, columns=columns, show='headings')

        # define headings
        self.tree.column(
            "nr_olt",minwidth=30,width=30
        )
        self.tree.column(
            "rx_olt",minwidth=60,width=60
        )
        self.tree.column(
            "rx_onu",minwidth=60,width=60
        )
        self.tree.column(
            "nazwa_device",minwidth=120,width=120
        )
        self.tree.column(
            "wyjscie",minwidth=60,width=60
        )
        self.tree.heading('nr_olt', text='Nr. olta',command=lambda: self.sortuj_po_treeview('nr_olta'))
        self.tree.heading('nazwa_device', text='Nazwa',command=lambda: self.sortuj_po_treeview('nazwa'))
        self.tree.heading('rx_olt', text='Rx olt',command=lambda: self.sortuj_po_treeview('sygnal_rx_olt'))
        self.tree.heading('rx_onu', text='Rx onu',command=lambda: self.sortuj_po_treeview('sygnal_rx_onu'))
        self.tree.heading('wyjscie', text='Wyjście',command=lambda: self.sortuj_po_treeview('wyjscie_olt'))
        self.tree.heading('nazwa_klienta', text='Nazwa klienta',command=lambda: self.sortuj_po_treeview('nazwa_klienta'))
        
        self.sorting_mark_order = mainviewmodel.zwroc_nazwy_wszystkich_zmiennych_wartosci_false_klas_koncowka_lms()
        #print(self.sorting_mark_order)

        
        self.tree.grid(
            row=2,
            rowspan=18,
            column=0,
            columnspan=19,
            sticky="nsew"
            )

        
        self.scrollbar = Scrollbar(self,command=self.tree.yview)
        self.scrollbar.grid(
            row=2,
            column=19,
            rowspan=18,
            sticky="nsew",
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.bind("<<TreeviewSelect>>",self.wybrany_element)


        self.czy_wykonywane_operacje_na_danych = False

        self.dane_widoku = []
        
    def filtruj_wyniki_thread(self):

        self.czy_wykonywane_operacje_na_danych = True
        
        self.tree.delete(*self.tree.get_children())
        nazwa_klienta = self.e_name_client.get()
        miejscowosc = self.e_place.get()
        ulica = self.e_street.get()

        for klient_olt,klient_lms in self.mainviewmodel.zwracaj_klient_koncowka_lms_po_filtrach(nazwa_klienta,miejscowosc,ulica):
                self.generuj_wiersze_frame3_po_obiektach(klient_olt,klient_lms)        


        self.czy_wykonywane_operacje_na_danych = False


    def filtruj_wyniki(self,event):
        if not self.czy_wykonywane_operacje_na_danych:
            # executor = ThreadPoolExecutor()
            # future = executor.submit(self.filtruj_wyniki_thread)
            self.filtruj_wyniki_thread()


    def sortuj_po_treeview_thread(self,poczym):

        self.czy_wykonywane_operacje_na_danych = True

        odwrotnie = self.sorting_mark_order[poczym]
        
        self.tree.delete(*self.tree.get_children())
        for klient_olt,klient_lms in self.mainviewmodel.zwroc_posortowanych_klientow_po(poczym,odwrotnie):
                self.generuj_wiersze_frame3_po_obiektach(klient_olt,klient_lms)
        self.sorting_mark_order[poczym] = not self.sorting_mark_order[poczym]

        with self.lock:
            self.czy_wykonywane_operacje_na_danych = False


    def sortuj_po_treeview(self,poczym):
        if not self.czy_wykonywane_operacje_na_danych:
            # executor = ThreadPoolExecutor()
            # future = executor.submit(self.sortuj_po_treeview_thread,poczym)
            self.sortuj_po_treeview_thread(poczym)
        #self.sortuj_po_treeview_thread(poczym)

    
    def wybrany_element_thread(self):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            nazwa_klienta = item['values'][-1]
            
            klient_koncowka,klient_lms = self.mainviewmodel.znajdz_klienta_lms_po_nazwie_klienta(nazwa_klienta)
            
            showinfo(title='Informacje o kliencie/koncowce', message=f'{klient_koncowka}{klient_lms}')
        
    def wybrany_element(self,event):
        executor = ThreadPoolExecutor()
        future = executor.submit(self.wybrany_element_thread) 
        
    def skanuj_olty(self):
        
        ktory_olt = self.c_olt_types_frame3.current()+1
        
        #1-Karolina 2-Biuro 3-wszystkie
        if ktory_olt == 1:
            if not self.zajetosc[0]:
                self.generate_info_frame3(f"Zaczynam skanowanie olt Karolinka(1)...",ktory_olt)
                #Thread(target=self.skanuj_olty_thread,args=(1,)).start()
                self.skanuj_olty_thread(1)
            else:
                self.generate_info_frame3("W trakcie pracy!",ktory_olt)
                
        elif ktory_olt == 2:
            if not self.zajetosc[1]:
                self.generate_info_frame3(f"Zaczynam skanowanie olt Biuro(2)...",ktory_olt)
                #Thread(target=self.skanuj_olty_thread,args=(2,)).start()
                self.skanuj_olty_thread(2)
            else:
                self.generate_info_frame3("W trakcie pracy!",ktory_olt)

        elif ktory_olt==3:
            if not self.zajetosc[0] and not self.zajetosc[1]:
                self.generate_info_frame3(f"Zaczynam skanowanie olt Karolinka(1)...",1)
                self.generate_info_frame3(f"Zaczynam skanowanie olt Biuro(2)...",2)

                #Thread(target=self.skanuj_olty_thread,args=(1,)).start()
                #Thread(target=self.skanuj_olty_thread,args=(2,)).start()
                self.skanuj_olty_thread(1)
                self.skanuj_olty_thread(2)
            else:
                self.generate_info_frame3("W trakcie pracy!",1)
                self.generate_info_frame3("W trakcie pracy!",2)

                

    def skanuj_olty_thread(self,numer_olta):
        executor = ThreadPoolExecutor()
        future = executor.submit(self.skan_olta_numer,numer_olta)   
        # wyjatek = future.exception()
        # if wyjatek:
        #     self.generate_info_frame3(wyjatek,numer_olta)
        

    def skan_olta_numer(self,numer_olta:int):
        
        self.zajetosc[numer_olta-1] = True
        
        for succ,info,object_device,object_lms_client in self.mainviewmodel.przeskanuj_calego_olta(numer_olta):

            if succ:
                self.generuj_wiersze_frame3_po_obiektach(object_device,object_lms_client)

            self.generate_info_frame3(info,numer_olta)
        
        self.zajetosc[numer_olta-1] = False
                
    def generate_info_frame3(self,text,ktory_olt):

        self.l_output_list[ktory_olt-1]['text'] = text
        return True
    

    def generuj_wiersze_frame3_po_obiektach(self,klient_olt,klient_lms):
        nazwa = klient_olt.nazwa
        sygnal_rx_olt = klient_olt.sygnal_rx_olt
        sygnal_rx_onu = klient_olt.sygnal_rx_onu
        wyjscie_olt = klient_olt.wyjscie_olt
        numer_olta = klient_olt.nr_olta
        
        nazwa_klienta = klient_lms.nazwa_klienta
        self.generuj_wiersze_frame3(
                        numer_olta,
                        nazwa,
                        sygnal_rx_olt,
                        sygnal_rx_onu,
                        wyjscie_olt,
                        nazwa_klienta
                    )

    def generuj_wiersze_frame3(self,*args):
        self.tree.insert('',END,values=args)