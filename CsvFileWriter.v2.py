# Importing neccessary libraries

import os # used to check files

import csv # To write data


    
class CsvHome:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.columns: list = []
        self.rows: list = []
        
    
    # Cleans up a file
    def clean_file(self) -> None:
        return open(self.file_name, 'w').close()
    
    
    # Check is data in files exists
    def is_empty(self) -> bool:
        return os.path.isfile(self.file_name) and os.path.getsize(self.file_name) > 0
    
    
    # Prepares lengths for rown and headers 
    def _prepare_length(self, headers: list, *lines: list, 
                       fill_up: bool = False) -> None:
        """_summary_

        Args:
            headers (list): columns of data
            *lines (list): a list of lists(rows)
            
            fill_up (bool, optional): fills up short rows. Defaults to False.

        Raises:
            ValueError: if both headers and rows are empty raises this Error
            ValueError: if fill_up is false and one of headers or rows is empty
        """
        
        self.columns = headers
        self.rows = list(lines)
        
        headers_length = len(self.columns)
        rows_length = len(self.rows)

        # Let's prepare out data's length
        # Here we check if one or both of the headers and rows are empty
        if (not self.columns) and (not self.rows):
            raise ValueError('Empty :(')
            
        # Now let's check if lengths are similar or not
        # fills up empty with empty spaces or number is fill_up is True
        # cuts off to the shortest row or header if cut_off is True
        if fill_up: 
            
            # Adds extra elements to short rows
            if headers_length > rows_length:
                for _ in range(headers_length - rows_length):
                    self.rows.append([''])
            
            # Adds extra header if there isn't enought 
            if rows_length > headers_length:
                for new_head in range(rows_length - headers_length):
                    self.columns.append(str(new_head))
        
            rows_elem_length = [len(row) for row in self.rows]
              
            # Adds extra elements into rows
            if max(rows_elem_length) != min(rows_elem_length):
                for row in self.rows:
                    if len(row) != max(rows_elem_length):
                        while len(row) != max(rows_elem_length):
                            row.append('')
        
        else: # Here we cut off eveything to the shortest vesion
    
            # Can't just cut off without any data
            if not self.columns or not self.rows:
                raise ValueError("Can't make short:<")
            
            # Deletes headers untill it equals to the number of rows
            if headers_length > rows_length:
                for _ in range(headers_length - rows_length):
                    self.columns.pop()

            # deletes rows untill it equals to the number of headers
            if rows_length > headers_length:
                for _ in range(rows_length - headers_length):
                    self.rows.pop()
                    
            rows_elem_length = [len(row) for row in self.rows]
            
            # Takes the shortes length and make all the other rows short
            if max(rows_elem_length) != min(rows_elem_length):
                
                for row in self.rows:
                    # Deletes row's elements until it fits the shortest row
                    if len(row) != min(rows_elem_length):
                        while len(row) != min(rows_elem_length):
                            row.pop()


    # Structures data
    def structure_data(self, headers: list, *lines: list, 
                       fill_up: bool = False) -> list[list]:
        
        """_summary_

        Returns:
            list[list] return prepared rows
        """
        
        # First, prepares rows and headers to a desired length
        self._prepare_length(headers, *lines, fill_up=fill_up)
        
        # Will be used to write data to files
        structured_data = []
        
        # A point to add data particularly
        list_to_add: list = []

        # Prepares data for future writing
        # Takes each first element of each row and adds it to another list
        # After finishing adds this list to the output list
        for index in range(len(self.rows[0])):
            for value in self.rows:
                # the first element of each row
                list_to_add.append(value[index])
    
            # Adds the list to the final one and makes an empty list
            structured_data.append(list_to_add)
            list_to_add = []  
        
        return structured_data
    
    
    # Creates adn writes data into the file
    def write_file(self, headers: list, *rows: list,
                       fill_up_option: bool = False) -> None:

        # Cooked data :>
        prepared_data = self.structure_data(headers, *rows, 
                                            fill_up=fill_up_option)
        
        with open(self.file_name, 'w', newline='') as write_file:
            write_csv = csv.writer(write_file)
            write_csv.writerow(self.columns)
            write_csv.writerows(prepared_data)
    
    
    # Updates the file adding new rows
    def add_data(self, headers: list, *lines: list, 
                fill_up_option: bool = False,
                check_headers: bool = True) -> None:
        
        """_summary_
            check_headers: checks for headers in the file
            
        Raises:
            ValueError: if number of row's elements doesn't fit the existing one
        """
        
        prepared_data = self.structure_data(headers, *lines,
                                            fill_up=fill_up_option)
        
        # to check if there are any headers
        # If there aren't any headers we write them and continue
        if check_headers:
            with open(self.file_name, 'a', newline='') as addrows:
                
                # need to check if new data fits the in file format 
                # if file is empty writes headers
                if not self.is_empty():
                    writer_headers = csv.writer(addrows)
                    writer_headers.writerow(self.columns)
    
    
        # After checking headers in the file we write rows
        with open(self.file_name, 'r+', newline='') as add_data:
            
            # If headers were written
            # separates headers to check if new data fits existing data
            if check_headers:
                num_of_chars = add_data.readlines()[-1].split(',')
                
                # If false throws an error
                if (len(prepared_data[0]) != len(num_of_chars)):
                    raise ValueError('Rows and headers are not the same')
            
            # If headers weren't written we just add a row
            # now we write our new data
            write_rows = csv.writer(add_data)
            write_rows.writerows(prepared_data)


    # Gets data back from a file in the original form
    def take_back(self, line: int = 1, start: int = None,
                 end: int = None) -> list | list[list]:

        """_summary_

        Raises:
            ValueError: if file is empty
            ValueError: if line is empty

        Returns:
            list[list]: list of prepared rows or just a list
        """
        
        # If the file is empty return this message
        if not self.is_empty():
            raise ValueError('Empty file')
        
        # Used to add lists of the original form
        single = []
        
        # A list where original form data is added
        prepared = []
        
        with open(self.file_name, '+r') as databack:
            # If these two options are not None
            if (start is not None) and (end is not None):
                
                # Lines from start to end
                lines_back = databack.readlines()[start:end]
                
                # Separates values in the rows
                row_elme = [row.split(',') for row in lines_back]
                
                # Getting rid of '\n' from the last element in each row
                for row in row_elme:
                    row[-1] = row[-1][:row[-1].find('\n')]
                
                # Restructures data. Turning it back to the original form
                for index in range(len(row_elme[0])):
                    for val in row_elme:
                        single.append(val[index])
                    
                    prepared.append(single)
                    single = []
                        
            else: # if start and end options are None just gets the line's data back
                try:
                    curnt_line = databack.readlines()[line].split(',')
                    
                    # Also gets rids of '\n' in the end
                    curnt_line[-1] = curnt_line[-1][:curnt_line[-1].find('\n')]
                    
                    for el in curnt_line:
                        prepared.append([el])
                        
                except IndexError:
                    raise ValueError('Empty line')
                    
        return prepared
