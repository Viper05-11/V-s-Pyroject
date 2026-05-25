import math 
import numpy as np
import pandas as pd
from numerize.numerize import numerize
from CurrentProject import CsvFileWriter as cfw
from CurrentProject import MyNumbersMethods as mnm



class Calculator:
    def __init__(self, file_name: str) -> None:
        """_summary_

        Args:
            file_name (str): used to save results in  python(primarily in the CSV format)
        """
        
        self.file = file_name

        self.fields = ['Signs', 'Results', 'Status','Errors']
        self.data_rows = {
            self.fields[0]: [],
            self.fields[1]: [],
            self.fields[2]: [],
            self.fields[3]: []
        }
        
        self.basic_signs = ['+', '-', '*', '/', '**', '%']
        self.advanced_signs = ['!', 'sqrt', 'isfib', 'fibseq', 
                               'evod', 'iseven', 'isodd', 'isprime', 
                               'tobin', 'revnums']
        
        self.signs_table = '''\
        | +, -, *, /, %, **, |
        | '!', 'sqrt', 'isfib', |
        | 'iseven', 'isodd', 'isprime' |
        '''
        
    
    def __add_up(self, num1: int | float, num2: int | float, option: bool) -> int | float:
        return round(num1 + num2) if option is True else num1 + num2
    
    
    def __subtract(self, num1: int | float, num2: int | float, option: bool) -> int | float:
        return round(num1 - num2) if option is True else num1 - num2

    
    def __multiply(self, num1: int | float, num2: int | float, option: bool) -> int | float:
        return round(num1 * num2) if option is True else num1 * num2
    
    
    def __divide(self, num1: int | float, num2: int | float, option: bool) -> int | float:
        return round(num1 / num2) if option is True else num1 / num2
    
    
    def __to_the_power_of(self, num1: int | float, num2: int | float, option: bool) -> int | float:
        return round(num1 ** num2) if option is True else num1 ** num2
    
    
    def __modulo(self, num1: int | float, num2: int | float, option: bool) -> int | float:
        return round(num1 % num2) if option is True else num1 % num2
     
    
    def __square_root(self, num: int | float, option: bool) -> int | float:
        return round(math.sqrt(num)) if option is True else  math.sqrt(num)
    
    
    def __factorial(self, num: int) -> int:
        return math.factorial(round(num)) if isinstance(num, float) else math.factorial(num)

    
    def basic_operations(self, n1: int | float,
                         n2: int | float,
                         entered_sign: str,
                         option: str) -> int | float:
        """_summary_

        Args:
            n1 (int | float): takes the first number from the user
            
            n2 (int | float): takes the second number from the user
            
            entered_sign (str): is used to perfrom operations
            
            option (str): is used to determine whether to round the results or not

        Returns:
            int | float: the output can be either an integer or a floating point number
        """
        
        save_data = cfw(self.file)
        
        match option:
            case 'yes':
                option = True
            
            case _:
                option = False
                
            
        try:
            match entered_sign:
                case '+':
                    result = self.__add_up(n1, n2, option)
            
                case '-':
                    result = self.__subtract(n1, n2, option)
                    
                case '*':
                    result = self.__multiply(n1, n2, option)
                
                case '/':
                    result = self.__divide(n1, n2, option)
                
                case '**':
                    result = self.__to_the_power_of(n1, n2, option)
                    
                case '%':
                    result = self.__modulo(n1, n2, option)
            
            if len(numerize(result)) >= 7:
                result = format(result, '.4e')
                
            else:
                result = numerize(result)
            
        except ZeroDivisionError:
            self.data_rows['Status'].append(1)
            self.data_rows['Errors'].append('ZeroDivisionError')
            result = np.NaN
            
        except OverflowError:
            self.data_rows['Status'].append(1)
            self.data_rows['Errors'].append('OverflowError')
            result = np.NaN
        
        else:
            self.data_rows['Status'].append(0)
            self.data_rows['Errors'].append('NoErrorDetected')   
                    
            self.data_rows['Signs'].append(entered_sign)
            self.data_rows['Results'].append(result)
        
        
        if save_data.check_data_exists():
            save_data.add_data(self.fields,self.data_rows['Signs'],
                               self.data_rows['Results'],self.data_rows['Status'], 
                               self.data_rows['Errors'],
                               fill_up_emp=True, lengh_err=False)
            
        else:
            save_data.write_csv_file(self.fields, self.data_rows['Signs'],
                                    self.data_rows['Results'],self.data_rows['Status'],
                                    self.data_rows['Errors'],
                                    fill_up_emp=True, length_error=False)
            
        return result
    
    
    def advanced_operations(self, adv_sign: str,
                            num: int | float, 
                            rounded: str) -> int | float:  
        """_summary_

        Args:
            adv_sign (str): takes user's sign to perform operations
            
            num (int | float): takes user's number(s) for operations
            
            rounded (str): used to round results or not

        Returns:
            int | float: the result can be either integer or floating point number
        """
        
        my_numbers = mnm(num)
        
        match rounded: 
            case 'yes':
                rounded = True
            
            case _:
                rounded = False
                
        try:   
            match adv_sign:
                case '!':
                    num = int(num)
                    
                    result = self.__factorial(num)
                
                case 'sqrt':
                    result = self.__square_root(num, rounded)

                case 'isfib':
                    result = my_numbers.is_fib_num()
                    
                case 'iseven':
                    result = my_numbers.is_even_int()
                    
                case 'isodd':
                    result = my_numbers.is_odd_int()
                    
                case 'isprime':
                    result = my_numbers.is_prime()
                 
            if len(numerize(result)) >= 7:
                result = format(result, '.4e')
                
            else:
                result = numerize(result)
            
        except TypeError:
            self.data_rows['Status'].append(1)
            self.data_rows['Errors'].append('TypeError')
            result = np.NaN
            
        except OverflowError:
            self.data_rows['Status'].append(1)
            self.data_rows['Errors'].append('OverflowError')
            result = np.NaN
            
        else:
            self.data_rows['Status'].append(0)
            self.data_rows['Errors'].append('NoErrorDetected')

            self.data_rows['Signs'].append(adv_sign)
            self.data_rows['Results'].append(result)
        
        
        if cfw(self.file).check_data_exists():
            cfw(self.file).add_data(self.fields,self.data_rows['Signs'],
                                    self.data_rows['Results'],self.data_rows['Status'], 
                                    self.data_rows['Errors'],
                                    fill_up_emp=True, lengh_err=False)
            
        else:
            cfw(self.file).write_csv_file(self.fields, self.data_rows['Signs'],
                                          self.data_rows['Results'],self.data_rows['Status'],
                                          self.data_rows['Errors'],
                                          fill_up_emp=True, length_error=False)
        
        return result
    
    
    def main_calculator(self):
        """_summary_
            Function to call to use the calculator
        """
        
        print(self.signs_table)
        while True:
            assistant = input('Assistant: ', )
            match assistant:
                case '/Show':
                    last_result = pd.read_csv(self.file)['Results']
                    print(last_result.loc[len(last_result)-1])
            
            
                case '/Signs':
                    print(self.signs_table)
                
                case '/Stop':
                    print('Bye!')
                    exit()
                    
                
            opt_to_round = None
            
            signs = input('Signs: ').strip()
            try:
                if signs in self.advanced_signs:
                    sep_num = float(input('Number: '))
                    if signs == 'sqrt':
                        opt_to_round = input('Round: ')
                    
                    print(self.advanced_operations(signs, sep_num, opt_to_round))
                    continue
                
                if signs in self.basic_signs:
                    first_num = float(input('First number: '))
                    second_num = float(input('Second number: '))
                    round_opt = input('Round? ')
                    
                    print(self.basic_operations(first_num, second_num, signs, round_opt))
                    continue
                
                else:
                    print('No such options:(')
                    
            except ValueError:
                self.data_rows['Status'].append(1)
                self.data_rows['Errors'].append('ValueError')
                print('No letters:=')
                
            else:
                self.data_rows['Status'].append(0)
                self.data_rows['Errors'].append('NoErrorDetected')
                