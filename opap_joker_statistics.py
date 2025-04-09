import pandas as pd
import os
import datetime as dt
import warnings
import subprocess
import errno
import collections


def is_number_even(number) -> bool:
    """
    Check if number is even.
    :return: True | False
    """
    return number % 2 == 0


def copy_file(source, target) -> None:
    """ Copy file to directory """
    if not os.path.isdir(target):
        raise InvalidDirectory(target)

    if not os.path.isfile(source):
        print(FileNotFoundError(errno.ENOENT, "No such file", source))
        # raise FileNotFoundError(errno.ENOENT, "No such file", source)
        exit(errno.ENOENT)

    cmd = f"mv {source} {target}"

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = p.communicate()
    if p.returncode:
        print(f"Failed to copy file... {stderr.strip().decode('utf-8')}")
        exit(errno.ENOENT)


def pretty_dictionary(data) -> dict:
    """
    Returns a dictionary, by grouping the total number of appearance of each number.
    E.g.:
    new_data = {365: ['29'], 364: ['37'], 361: ['34'], 354: ['13', '31'], ...}
    key is the number of appearance
    value is a list that contains the numbers that have been appeared the same.
    Number '29' has been appeared 365 time.
    Numbers '13' and '31' have been appeared 354 times.
    """
    new_data = collections.defaultdict(list)
    for number, appearance in data.items():
        new_data[appearance].extend([number])
    return dict(sorted(new_data.items(), reverse=True))


def get_excel_files_from_directory(directory) -> list:
    """ Get Excel files from directory """
    data_files_in_directory = os.listdir(directory)
    return [excel_file for excel_file in data_files_in_directory if excel_file.split('.')[-1] == 'xlsx']


class InvalidDirectory(OSError):
    """ Custom Exception Invalid directory """
    def __init__(self, directory):
        super().__init__(errno.ENOENT, "Invalid directory", directory)


class OpapWebSite:
    """
    A class that downloads OPAP Joker Excel files to a predefined directory.
    This class accepts an absolute directory path as argument, and in this directory
    the Excel files will be downloaded.
    e.g. OpapWebSite(<my_directory>)
    """
    opapSite = "https://media.opap.gr/Excel_xlsx/5104/"

    def __init__(self, data_path):
        self.data_path = data_path
        self.file_extension = '.xlsx'
        self.year = str(dt.datetime.now().year)

    def wget_all_opap_files(self, path=None):
        """
        Method that downloads all Excel files, from OPAP site.
        OPAP site: 'https://media.opap.gr/Excel_xlsx/5104/'
        OPAP Excel file name format: 'Joker_2025.xlsx'
        This method will use linux wget command, to download the files,
        from 1998 to current year.
        Method accepts an optional argument, that specifies the (absolute) directory where the
        files will be downloaded. If no argument is specified, then it will be
        downloaded to default 'self.dataPath' directory.
        """
        if path is None:
            path = self.data_path

        for year in range(1998, int(self.year) + 1):
            excel_file_name = "Joker_" + str(year) + self.file_extension
            print(f"Downloading file {excel_file_name} ")
            opap_data_file = self.opapSite + excel_file_name
            os.system(f"wget --quiet --read-timeout=5 --tries=0 {opap_data_file} -P {path}")

    def wget_opap_file(self, year=None):
        """
        Method that downloads a single Excel file from OPAP site.
        Method accepts an optional argument, that specifies the year of the file to be downloaded.
        If no year argument is specified, that the current year is taken as the default year.
        """
        # If no argument provided, then get current year - last Excel file.
        if year is not None:
            self.year = str(year)
        excel_file = "Joker_" + self.year + self.file_extension

        excel_files = get_excel_files_from_directory(self.data_path)

        if excel_file in excel_files:
            self.backup_file(excel_file)

        opap_data_file = self.opapSite + excel_file
        print(f"Downloading file {excel_file}")
        # Do not add the -P flag, because if the file already exists, it will download
        # it with a different format e.g. Joker_2025.xlsx.1
        # Better save it to current directory and copy the file to self.dataPath.
        os.system(f"wget --quiet --read-timeout=5 --tries=0  {opap_data_file}")

        copy_file(excel_file, self.data_path)

    def backup_file(self, filename):
        """ Backup Excel file """
        excel_file = self.data_path + os.sep + filename
        backup_file = excel_file + '.back'

        print(f"Backup file: {filename}")
        try:
            os.rename(excel_file, backup_file)
        except PermissionError as error:
            print(f"{error}")


class JokerDb:
    """
    A Class that reads the OPAP Excel files from a specific location
    and creates several statistics for the game.
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.results_file_name = 'Joker_results.txt'
        self.results_file = self.data_path + os.sep + self.results_file_name
        self.last_draws = 5
        self.excel_files = []
        self.game_data = []
        self.statistics_numbers = collections.defaultdict(int)
        self.statistics_joker = collections.defaultdict(int)
        self.lastDrawsNums = {}
        self.lastDrawsJoker = {}
        self.oddEvenNums = collections.OrderedDict(OddNumbers=0,
                                                   EvenNumbers_1=0,
                                                   EvenNumbers_2=0,
                                                   EvenNumbers_3=0,
                                                   EvenNumbers_4=0,
                                                   EvenNumbers=0,
                                                   EvenJoker=0,
                                                   OddJoker=0)

    def __repr__(self):
        return f"OPAP Numbers Statistics: \n{pretty_dictionary(self.statistics_numbers)}" \
               f"\n\nOPAP Joker Statistics: \n{pretty_dictionary(self.statistics_joker)}" \
               f"\n\nLast {self.last_draws} Draws Number Statistics: \n{pretty_dictionary(self.lastDrawsNums)}" \
               f"\n\nLast {self.last_draws} Draws Joker Statistics: \n{pretty_dictionary(self.lastDrawsJoker)}" \
               f"\n\nTotal Odd/Even Statistics: \n{dict(self.oddEvenNums)} \n"

    def get_excel_files(self):
        """ Get Excel files from self.data_path """
        self.excel_files = get_excel_files_from_directory(self.data_path)

    def create_data_array(self):
        """
        This method processes the Excel files and creates a data array that has all the draws since 1998.
        Each list in the array represents a draw and has 6 numbers.
        First five numbers in the list are numbers 1 - 45.
        Last number in the list, is the joker number (1 - 20)
        E.g: [[18, 8, 28, 21, 36, 1], [27, 14, 31, 30, 34, 12], [43, 38, 14, 19, 23, 19], ...,
             [27, 15, 22, 13, 3, 18], [37, 29, 44, 16, 28, 14]]
        """
        print("\nProcessing Years: ")
        for data_file in self.excel_files:
            year = data_file.split('.')[0].split('_')[-1]
            print(f"{year}", end=' ')
            excel_file = self.data_path + os.sep + data_file
            if year in ["1998", "1999", "2002"]:
                data = pd.read_excel(excel_file, usecols="C:G,I", skiprows=3).squeeze(1)
            elif year == "2001":
                data = pd.read_excel(excel_file, usecols="C:H", skiprows=3).squeeze(1)
            else:
                data = pd.read_excel(excel_file, usecols="C:H", skiprows=2).squeeze(1)

            # Convert ndarray data (data.values) to list and extend it to arrData.
            self.game_data.extend(data.values[::-1].tolist())
        print("\n")

    def write_data_to_file(self):
        """
        This method saves data array in a file.
        Each line in the file is in the form of:
               1 Draw: |  8 18 21 28 36 |  1 |
               2 Draw: | 14 27 30 31 34 | 12 |
            ...
            2949 Draw: | 16 28 29 37 44 | 14 |
        """
        try:
            with open(self.results_file, 'w') as f:
                for draw, data in enumerate(self.game_data, 1):
                    numbers = ' '.join(f"{i:>2}" for i in sorted(data[:5]))
                    line = f"{draw:>5} Draw: | {numbers} | {data[-1]:>2} | \n"
                    f.write(line)
        except FileNotFoundError:
            print(f"\n\n{FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.results_file)}")
            exit(errno.ENOENT)

    def create_statistics(self):
        """
        This method creates several dictionaries that contain statistics for each draw.

        Dictionary 'self.statistics_numbers':
            Contains how many times each number (1 - 45) has been appeared in the all draws.
        Dictionary 'self.statistics_joker':
            Contains how many times each joker number (1 - 20) has been appeared in the all draws.
        Both dictionaries are in the form of: {'1': 316, '2': 312, '3': 308, '4': 327, '5': 349, '6': 306,... }
        Key is the number in the draw
        Value is the appearance of the number.
        E.g: '1' has been appeared 316 times in total, '2' has been appeared 312 times in total, etc...

        Dictionary 'self.oddEvenNums':
            Contains statistics about Even/Odd numbers and its appearance.
        Keys: EvenNumbers, OddNumbers, EvenNumbers_1, EvenNumbers_2, EvenNumbers_3, EvenNumbers_4, EvenJoker, OddJoker
        Values: The number of Even/Odd appearances.
        Dictionary is in the form:
        {'OddNumbers': 76, 'EvenNumbers_1': 496, 'EvenNumbers_2': 981, 'EvenNumbers_3': 941,
        'EvenNumbers_4': 385, 'EvenNumbers': 71, 'EvenJoker': 1477, 'OddJoker': 1473}

        E.g: OddNumbers = 76 (All numbers are odd, appeared 76 times).
             EvenNumbers_1 = 496 (One number is even out of five, appeared 496 times).
             EvenNumbers_2 = 981 (Two numbers are even out of five, appeared 981 times).
             EvenNumbers_3 = 941 (Three numbers are even out of five, appeared 941 times).
             EvenNumbers_4 = 385 (Four numbers are even out of five, appeared 385 times).
             EvenNumbers = 71 (All numbers are even, appeared 71 times).
             EvenJoker = 1477 (Joker number is even, appeared 1477 times).
             OddJoker = 1473 (Joker number is odd, appeared 1473 times).
        """
        for draw in self.game_data:
            numbers = draw[:-1]
            joker = draw[-1]

            odd_even_numbers = list(map(is_number_even, numbers)).count(True)
            odd_even_joker = is_number_even(joker)

            if odd_even_numbers == 5:
                self.oddEvenNums['EvenNumbers'] += 1
            elif odd_even_numbers == 0 :
                self.oddEvenNums['OddNumbers'] += 1
            else:
                self.oddEvenNums['EvenNumbers_' + str(odd_even_numbers)] += 1

            if odd_even_joker:
                self.oddEvenNums['EvenJoker'] += 1
            else:
                self.oddEvenNums['OddJoker'] += 1

            for number in numbers:
                self.statistics_numbers[str(number)] += 1

            self.statistics_joker[str(joker)] += 1

    def get_last_draws_data(self):
        """
        This method creates two new dictionaries that have statistics
        for numbers and joker, according to self.last_draws variable.
        Variable self.last_draws, are the last draws in the game (e.g. last 5 draws).
        Dictionary '': self.lastDrawsNums
        Dictionary '': self.lastDrawsJoker
        Both dictionaries are in the form:
        {3: ['37'], 2: ['3', '28', '20', '27', '13', '44'], 1: ['24', '4', '32', '43', '33', '7', '15', '22', '29', '16']}
        E.g.
        Number 37 has been appeared 3 times in the last 5 draws.
        Numbers 3, 28, 20, 27, 13, and 44 have been appeared 2 times in the last 5 draws.
        """
        last_draws_nums = collections.defaultdict(int)
        last_draws_joker = collections.defaultdict(int)

        for data in self.game_data[-self.last_draws:]:
            for num in data[:-1]:
                last_draws_nums[str(num)] += 1
            last_draws_joker[str(data[-1])] += 1

        self.lastDrawsNums = last_draws_nums.copy()
        self.lastDrawsJoker = last_draws_joker.copy()

    def show_last_draws(self):
        """
        This method open, reads and prints the last results from the self.results_file.
        Last results are taken from variable self.last_draws.
        E.g. self.last_draws = 5, method will print the 5 last draws.
        1st raw is the draw number.
        2nd raw are the OPAP numbers (sorted).
        3rd raw is the OPAP Joker number.

            2946 Draw: |  4 20 27 32 37 |  5 |
            2947 Draw: |  7 13 33 43 44 | 17 |
            2948 Draw: |  3 13 15 22 27 | 18 |
            2949 Draw: | 16 28 29 37 44 | 14 |
            2950 Draw: |  3 17 20 24 31 | 14 |
        """
        try:
            with open(self.results_file, 'r') as stats_file:
                last_lines = stats_file.readlines()[-self.last_draws:]

            for line in last_lines:
                print(line.replace("\n", ''))
        except FileNotFoundError:
            print(f"\n\n{FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.results_file)}")
            exit(errno.ENOENT)

    def print_number_statistics(self):
        """
        Method prints the OPAP Number Statistics.
        E.g:
        OPAP Numbers Statistics:
        {365: ['29'], 364: ['37'], 361: ['34'], 355: ['31'], 354: ['13'], ..., 341: ['41', '32'], ...}
        Number 29 has been appeared 365 times.
        Number 37 has been appeared 364 times.
        Numbers 41 and 32 have been appeared 341 times.
        """
        print(f"OPAP Numbers Statistics: \n{pretty_dictionary(self.statistics_numbers)} \n")

    def print_joker_statistics(self):
        """
        Method prints the OPAP Joker Statistics.
        E.g:
        OPAP Joker Statistics:
        {160: ['3'], 159: ['1'], 158: ['8'], 157: ['18', '6'], ...}
        Joker number 3 has been appeared 160 times.
        Joker numbers 18 and 6 have been appeared 157 times.
        """
        print(f"OPAP Joker Statistics: \n{pretty_dictionary(self.statistics_joker)} \n")

    def print_odd_even_statistics(self):
        """
        Method prints statistics about Odd/Even numbers.
        E.g:
        Total Odd/Even Statistics:
        {'OddNumbers': 76, 'EvenNumbers_1': 496, 'EvenNumbers_2': 981, 'EvenNumbers_3': 941,
        'EvenNumbers_4': 385, 'EvenNumbers': 71, 'EvenJoker': 1477, 'OddJoker': 1473}

        OddNumbers = 76 (All numbers are odd, appeared 76 times).
        EvenNumbers_1 = 496 (One number is even out of five, appeared 496 times).
        EvenNumbers_2 = 981 (Two numbers are even out of five, appeared 980 times).
        EvenNumbers_3 = 941 (Three numbers are even out of five, appeared 941 times).
        EvenNumbers_4 = 385 (Four numbers are even out of five, appeared 385 times).
        EvenNumbers = 71 (All numbers are even, appeared 71 times).
        EvenJoker = 1477 (Joker number is even, appeared 1476 times).
        OddJoker = 1473 (Joker number is odd, appeared 1473 times).
        """
        print(f"Total Odd/Even Statistics: \n{dict(self.oddEvenNums)} \n")

    def print_last_draws_statistics(self, last_draws=None):
        """
        Method prints statistics for numbers and Joker numbers, according to last_draws argument.
        If no argument is given, then it takes by default the last 5 draws.
        E.g:
        Last 5 Draws Number Statistics:
        {2: ['27', '20', '37', '13', '44', '3'],
        1: ['4', '32', '43', '33', '7', '15', '22', '29', '16', '28', '17', '24', '31']}

        (Numbers 27, 20, 37, 13, 44 and 3 have been appeared 2 times in the last 5 draws)

        Last 5 Draws Joker Statistics:
        {2: ['14'], 1: ['5', '17', '18']}

        (Joker Number 14 has been appeared 2 times in the last 5 draws)
        """
        if last_draws is not None:
            self.last_draws = last_draws

        self.get_last_draws_data()
        print(f"Last {self.last_draws} Draws Number Statistics: \n{pretty_dictionary(self.lastDrawsNums)} \n")
        print(f"Last {self.last_draws} Draws Joker Statistics: \n{pretty_dictionary(self.lastDrawsJoker)} \n")


    def print_statistics(self, last_draws=None):
        """ Method that prints all the statistics for numbers and Joker numbers. """
        if last_draws is not None:
            self.last_draws = last_draws

        print()
        self.print_number_statistics()
        self.print_joker_statistics()
        self.print_odd_even_statistics()
        self.print_last_draws_statistics()
        self.show_last_draws()


if __name__ == "__main__":

    warnings.filterwarnings("ignore", message="Workbook contains no default style", category=UserWarning)

    project_path = os.getcwd()
    excel_files_path = project_path + os.sep + 'excel_data_files'

    opap_files = OpapWebSite(excel_files_path)

    if not os.path.isdir(excel_files_path):
        print(f"Creating directory {excel_files_path}")
        os.mkdir(excel_files_path)
    excel_data_files = os.listdir(excel_files_path)

    if not excel_data_files:
        print(f"Downloading OPAP excel files.")
        opap_files.wget_all_opap_files()
    else:
        updateFiles = input("Do yoy want to update OPAP excel files (yes/no)?: ")
        if updateFiles.lower() in ("y", "yes"):
            years = input("Enter the year(s) of the files (space separated): ")
            for year in years.split():
                opap_files.wget_opap_file(year)

    gameDb = JokerDb(excel_files_path)
    gameDb.get_excel_files()
    gameDb.create_data_array()
    gameDb.create_statistics()
    gameDb.write_data_to_file()
    gameDb.print_statistics()

