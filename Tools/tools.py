import os
from config import maksymalny_numer_id


class Dodatkowe_Narzedzia():

    @staticmethod
    def clean_cmd():
        os.system('cls')

    @staticmethod
    def try_parse_to_int(numer_id):
        try:
            int(numer_id)
            return True
        except ValueError:
            return False

    @staticmethod
    def try_parse_to_float(text):
        try:
            float(text)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def check_if_int_number_is_in_range_include(value,from_num,to_num):
        #konwersja na int
        value = int(value)
        if (value >= from_num) and (value <= to_num):
            return True
        return False
    
    @staticmethod
    def check_if_text_is_equal_to_text(text,phrase):
        
        if text == phrase:
            return True
        return False
          
    @staticmethod
    def check_if_text_int_is_bigger_than_zero(text):
        if int(text)>0:
            return True
        return False
    
    @staticmethod
    def check_if_int_or_text_equal_text(text,text2):
        t1 = Dodatkowe_Narzedzia.try_parse_to_int(text)
        t2 = Dodatkowe_Narzedzia.check_if_text_is_equal_to_text(text,text2)
        
        if t1 or t2:
            return True
        return False
    
    
    @staticmethod
    def do_validation_input_and_info(text,from_num,to_num):
        """
        Sprawdzamy, czy input przechodzi nastepujce testy
        Test 1 - czy int
        Test 2 - czy miesci się w przedziale

        Zwraca:
        True,"" - gdy przejdzie testy
        False,"opis problemu" - gdy jeden z nich nie przejdzie
        
        """
        dict_validations = {
            "test_int":[Dodatkowe_Narzedzia.try_parse_to_int,[text],"Niepoprawny znak!"],
            "test_range":[Dodatkowe_Narzedzia.check_if_int_number_is_in_range_include,[text,from_num,to_num],"Liczba nie jest w zakresie"]
        }


        
        for f,par,info in dict_validations.values():
            if not f(*par):
                return [False,info]
            
        return [True,""]
    
    @staticmethod
    def do_validation_input_and_info_for_id(text):
        """
        Sprawdzamy, czy input przechodzi przez testy:
        Test 1 - sprawdzamy czy jest int
        Test 2 - sprawdzamy, czy jest rowny wartosci przypisanej z pliku config ("wszystkie")
        

        True - gdy jeden z testów przejdzie
        False - gdy żaden nie przejdzie testów
        """
        #print(text)
        dict_validations = {
            "test_int_all":[Dodatkowe_Narzedzia.try_parse_to_int,[text],f"To nie jest liczba"],
            "test_bigger_than_zero":[Dodatkowe_Narzedzia.check_if_int_number_is_in_range_include,[text,1,maksymalny_numer_id],f"To nie jest liczba dodatnia mniejsza równa od {maksymalny_numer_id}"],
        }
        
        for f,par,info in dict_validations.values():
            if not f(*par):
                return [False,info]
            
        return [True,""]