from threading import Lock
from tkinter import ttk
from tkinter import *


from View.frame1 import Frame1
from View.frame2 import Frame2
from View.frame3 import Frame3
from ViewModel.mainviewmodel import MainViewModel
from config import ilosc_oltow

class Okienko():


    def __init__(self):
        
        height = 600
        width = 900
        
        self.wiersz = 0
        self.max_wiersz = 20
        
        self.rootofokienko = Tk()
        self.rootofokienko.title("Analizator olta")
        self.rootofokienko.resizable(False,False)
        self.rootofokienko.minsize(width,height)
        self.rootofokienko.maxsize(width,height)
        
        self.my_notebook = ttk.Notebook(self.rootofokienko,width=width,height=height)
        self.my_notebook.pack()
        
        self.lock = Lock()

        self.mainviewmodel = MainViewModel(self.lock)
        
        self.zajetosc = [False]*ilosc_oltow
        
        self.my_frame1 = Frame1(self.my_notebook, bg="green", lock = self.lock, zajetosc = self.zajetosc, mainviewmodel = self.mainviewmodel)
        
        self.my_frame2 = Frame2(self.my_notebook, bg="brown", lock = self.lock, zajetosc = self.zajetosc, mainviewmodel = self.mainviewmodel)
        
        self.my_frame3 = Frame3(self.my_notebook, bg="grey", lock = self.lock, zajetosc = self.zajetosc, mainviewmodel = self.mainviewmodel)
        
        
        self.my_frame1.pack(fill="both",expand=1)
        self.my_frame2.pack(fill="both",expand=1)
        self.my_frame3.pack(fill="both",expand=1)
        
        self.my_notebook.add(self.my_frame1,text="Sprawdzanie sygnału koncówka")
        self.my_notebook.add(self.my_frame3,text="Skanowanie oltów")
        self.my_notebook.add(self.my_frame2,text="Sygnały klientów w obszarach")
        
        
        
        
        self.rootofokienko.mainloop()



    
    
    

        





    
            

    
    

    

 

