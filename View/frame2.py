from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from tkinter import END, Button, Frame,Label, Scrollbar
from tkinter.messagebox import showinfo
from tkinter.ttk import Treeview

from ViewModel.mainviewmodel import MainViewModel


class Frame2(Frame):
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

        self.b_run_analize_frame3 = Button(
            self,
            text="Odśwież",
            font=("Arial",12,"bold"),
            borderwidth=2,
            relief="raised",
            command=self.dokonaj_analizy_sygnalu_na_ulicach
        )
        self.b_run_analize_frame3.grid(
            row=0,
            column=0,
            columnspan=7,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        self.l_output_analize_frame3 = Label(
            self,
            text="",
            font=("Arial",12,"bold"),
            borderwidth=2,
        )
        self.l_output_analize_frame3.grid(
            row=0,
            column=7,
            columnspan=13,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        columns = ('miejscowosc', 'ulica', 'rx_olt_srednie','rx_onu_srednie','rx_olt_min','rx_olt_max','rx_onu_min','rx_onu_max')
        self.tree = Treeview(self, columns=columns, show='headings')

        self.data_for_view = [

        ]

        # define headings
        self.tree.column(
            "miejscowosc",minwidth=60,width=60
        )
        self.tree.column(
            "ulica",minwidth=120,width=120
        )
        self.tree.column(
            "rx_olt_srednie",minwidth=60,width=60
        )
        self.tree.column(
            "rx_onu_srednie",minwidth=60,width=60
        )
        self.tree.column(
            "rx_olt_min",minwidth=60,width=60
        )
        self.tree.column(
            "rx_olt_max",minwidth=60,width=60
        )
        self.tree.column(
            "rx_onu_min",minwidth=60,width=60
        )
        self.tree.column(
            "rx_onu_max",minwidth=60,width=60
        )
     


        self.tree.heading('miejscowosc', text='Miejscowość',command=lambda: self.sortuj_po(0))
        self.tree.heading('ulica', text='Ulica',command=lambda: self.sortuj_po(1))
        self.tree.heading('rx_olt_srednie', text='Rx olt średnia',command=lambda: self.sortuj_po(2))
        self.tree.heading('rx_onu_srednie', text='Rx onu średnia',command=lambda: self.sortuj_po(3))
        self.tree.heading('rx_olt_min', text='Rx olt min',command=lambda: self.sortuj_po(4))        
        self.tree.heading('rx_olt_max', text='Rx olt max',command=lambda: self.sortuj_po(5))
        self.tree.heading('rx_onu_min', text='Rx onu min',command=lambda: self.sortuj_po(6))
        self.tree.heading('rx_onu_max', text='Rx onu max',command=lambda: self.sortuj_po(7))


 
        self.tree.grid(
            row=1,
            rowspan=19,
            column=0,
            columnspan=19,
            sticky="nsew"
        )
        self.tree.bind("<<TreeviewSelect>>",self.wybrany_element)
        self.dict_for_heading_state = defaultdict(bool)

        self.scrollbar = Scrollbar(self,command=self.tree.yview)
        self.scrollbar.grid(
            row=1,
            rowspan=19,
            column=19,
            sticky="nsew",
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)


        self.czy_dokonywana_jest_analiza = False

    def wybrany_element(self,event):
           for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                miejscowosc = item['values'][0]
                ulica = item['values'][1]


                text_otp = "\n------\n".join((f'Nazwa klienta: {nazwa_klienta}\n\tNumer domu: {numer_domu}'  for nazwa_klienta,numer_domu in self.mainviewmodel.znajdz_nazwy_i_numery_domow_po_miejscowosci_ulicy(miejscowosc,ulica)))
                

                showinfo(title='Informacje dodatkowe', message=text_otp)
 
    def dokonaj_analizy_sygnalu_na_ulicach(self):
        if not self.czy_dokonywana_jest_analiza:
            executor = ThreadPoolExecutor()
            executor.submit(self.dokonaj_analizy_sygnalu_na_ulicach_thread)
            #self.dokonaj_analizy_sygnalu_na_ulicach_thread()
        else:
            self.generate_info_frame2("Proszę czekać na zakończenie analizy!")

    def dokonaj_analizy_sygnalu_na_ulicach_thread(self):

        with self.lock:
            self.czy_dokonywana_jest_analiza = True

        self.tree.delete(*self.tree.get_children())
        self.data_for_view = []
        ile = 0

        for miejscowosc,ulica,srednia_rx_olt,srednia_rx_onu,min_rx_olt,max_rx_olt,min_rx_onu,max_rx_onu in self.mainviewmodel.pogrupuj_po_miejscowosci_ulicy_dla_sygnalow_srednia_max_min():
            ile += 1
            self.data_for_view.append(
                [miejscowosc,ulica,srednia_rx_olt,srednia_rx_onu,min_rx_olt,max_rx_olt,min_rx_onu,max_rx_onu]
            )
            self.generuj_wiersze_frame2(
                miejscowosc,ulica,srednia_rx_olt,srednia_rx_onu,min_rx_olt,max_rx_olt,min_rx_onu,max_rx_onu
            )
        self.generate_info_frame2(f"Wygenerowano raport w ilości: {ile} ")

        with self.lock:
            self.czy_dokonywana_jest_analiza = False

    def generate_info_frame2(self,text):

        self.l_output_analize_frame3['text'] = text
        return True

    def sortuj_po(self,num):
        # executor = ThreadPoolExecutor()
        # executor.submit(self.sortuj_po_thread,num)
        self.sortuj_po_thread(num)
      


    def sortuj_po_thread(self,num):
        self.data_for_view.sort(
            key=lambda wiersz:wiersz[num],reverse=self.dict_for_heading_state[num]
        )
        self.tree.delete(*self.tree.get_children())
        for wiersz in self.data_for_view:
            self.generuj_wiersze_frame2(
                *wiersz
            )

        self.dict_for_heading_state[num] = not self.dict_for_heading_state[num]

    def generuj_wiersze_frame2(self,*args):
        self.tree.insert('',END,values=args)
        