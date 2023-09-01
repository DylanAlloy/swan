import os, csv
from .fancy_print import _f
from .utils import check_headers, dateme

class Receipts:
    def __init__(self, path, data=None, head: list = None):
        """
        The function initializes an object with a given path, data, and header, and checks if the data
        and path exist.
        
        :param path: The `path` parameter is a string that represents the file path where the data is
        located
        :param data: The `data` parameter is used to specify the data that will be stored in the object.
        It can be any type of data, such as a string, list, dictionary, or custom object. This data will
        be associated with the object and can be accessed and manipulated using the methods and
        attributes of
        :param head: The "head" parameter represents the header or column names of the data. It is used
        to specify the names of the columns in the dataset
        :return: The code is returning a message based on certain conditions. If the `data` parameter is
        `None`, it returns a fatal error message saying "data not found". If the `path` does not exist,
        it returns a warning message saying "path not found". If both conditions are met, it returns
        `None`.
        """
        self.path = path
        self._schema = {
            "data": data
            , "header": head
        }
        return _f('fatal', 'data not found') if data==None else _f('warn', 'path not found') if not self.check() else None
    def check(self):
        """
        The function checks if a file or directory exists at the specified path.
        :return: a boolean value indicating whether the path specified by `self.path` exists or not.
        """
        return os.path.exists(self.path)
    def create(self, o: bool = False, ts: bool = True):
        """
        The function creates a CSV file with a specified path and writes the header row based on the
        schema, including a timestamp column if specified.
        
        :param o: The parameter "o" is a boolean flag that determines whether to overwrite an existing
        file with the same name. If it is set to False (default), and the file already exists, a warning
        message will be returned. If it is set to True, the existing file will be overwritten, defaults
        to False (optional)
        :param ts: The `ts` parameter is a boolean flag that determines whether a timestamp column
        should be added to the CSV file. If `ts` is `True`, then a timestamp column will be added. If
        `ts` is `False`, then no timestamp column will be added, defaults to True (optional)
        :return: The code is returning a warning message if the file already exists and the `o`
        parameter is set to `False`. If the file does not exist or the `o` parameter is set to `True`,
        the code creates a new file and writes the header row to it. Finally, an info message is printed
        indicating that the file has been created.
        """
        _e = self.check()
        if _e and not o:
            return _f('warn', f'{self.path} exists')
        with open(self.path, 'w') as _:
            io = csv.writer(_)
            check_headers(self) if self._schema['data'] is not None else None
            self._schema['header'].append('ts') if ts else None
            io.writerow(self._schema['header']) if self._schema['data'] is not None else None, _f('info', f'[{", ".join(self._schema["header"])}] header used')
        _f('info', f'created {self.path}')
    def seek(self, line: str | int = None, all: bool = False):
        """
        The `seek` function is used to search for specific lines or all lines in a CSV file and return
        the matching lines.
        
        :param line: The `line` parameter is used to specify the line number or string to search for in
        the data. If `line` is an integer, it will return the data at that line number. If `line` is a
        string, it will search for that string in the data and return all matching
        :param all: The `all` parameter is a boolean flag that determines whether to return all the data
        from the file or not. If `all` is set to `True`, the function will return all the data from the
        file. If `all` is set to `False` (default), the function will, defaults to False (optional)
        :return: The code is returning different values based on the conditions:
        """
        if all:
            if line is not None:
                return _f('fatal','you have `line` and `all` set')
            with open(self.path, 'r') as _:
                o = [x for x in csv.DictReader(_)]
                return o
        check_headers(self)
        _ = [x for x in csv.DictReader(open(self.path, 'r'))]
        if self._schema['data'] is None:
            return _f('fatal', 'no data passed')
        if isinstance(line, int):
            try:
                return _[line]
            except Exception as e:
                _f('fatal', 'index error')
        if isinstance(line, str):
            _r = []
            for datum in _:
                if [x for x in datum.values() if line in x]:
                    _r.append(datum)
                _f('info', f'found {line} in data')
            return _r
    def write(self, o: bool = False, ts: bool = True, v: bool = False):
        """
        The function writes data to a file in CSV format, including a timestamp if specified, and
        returns a success message or a fatal error message if the file path is not found.
        
        :param o: The parameter `o` is a boolean flag that determines whether to overwrite the file
        (`True`) or append to the file (`False`), defaults to False (optional)
        :param ts: The `ts` parameter is a boolean flag that determines whether to include a timestamp
        column in the output file. If `ts` is `True` and the timestamp column (`ts`) is not already
        present in the header, it will be appended to the header, defaults to True (optional)
        :param v: The parameter `v` is a boolean flag that determines whether to include additional
        information in the success message. If `v` is `True`, the success message will include the
        entire `self._schema` object. If `v` is `False`, the success message will include the number of
        items, defaults to False (optional)
        """
        _e = self.check()
        _h = check_headers(self)
        self._schema['header'].append('ts') if ts and 'ts' not in self._schema['header'] else None
        if _e:
            with open(self.path, 'w+' if o else 'a') as _:
                io = csv.DictWriter(_) if isinstance(self._schema['data'], dict) else csv.writer(_)
                io.writerow(self._schema['header']) if _h and o else None
                [dateme(x) for x in self._schema['data']]
                [io.writerow(x.values()) for x in self._schema['data']]
                _f('success', f'{self._schema}' if v else f'{len(self._schema["data"])} written to {self.path}')
        else:
            _f('fatal', 'path not found')
    def destroy(self, confirm: str = None):
        """
        The `destroy` function removes a file if the confirmation matches the file name, otherwise it
        displays an error message.
        
        :param confirm: The `confirm` parameter is used to confirm the destruction of a file. It should
        be set to the name of the file that you want to destroy
        """
        if confirm==self.path.split('/')[-1]:
            os.remove(self.path), _f('warn', f'{confirm} destroyed from {self.path}') 
        else:
            _f('fatal','you did not confirm - `Receipts.destroy(confirm="file_name")`')
        