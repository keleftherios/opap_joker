# OPAP Joker Statistics
The **opap_joker_statistics.py** is a python script that displays several statistics for OPAP Joker game.

## Description
The opap_joker_statistics.py script is mainly for educational and self-training purposes.
It downloads all Excel files from the official OPAP site and process the data of every draw since 1998.
Please note that currently there is a difference of approx. 58 draws between the OPAP official site and the script statistics.
This means that there is a **small deviation** between the official statistics from the OPAP site and the script statistics,
so, results are not accurate.

## Official OPAP site
All Excel files are downloaded from link below: \
https://media.opap.gr/Excel_xlsx/5104/

## OPAP statistics
All statistics are in a dictionary format.

### Number Statistics
Contains how many times each number (1 - 45) has been appeared in all draws. \
Key is the number of appearance of a number(s). \
Value is the actual number(s).\
E.g.:

OPAP Numbers Statistics: \
{365: ['29', '37'], 361: ['34'], 355: ['31', '13'], 351: ['27'], 349: ['5'], 341: ['41', '32'], 339: ['14'], \
337: ['36', '24'], 336: ['11'], 335: ['8', '28'], 333: ['26'], 332: ['23'], 331: ['18'], 330: ['17'], 329: ['21'], \
328: ['12'], 327: ['4'], 324: ['40', '7'], 322: ['39', '42'], 321: ['16'], 320: ['25'], 319: ['15'], 318: ['30'], \
317: ['20', '44', '9'], 316: ['1'], 315: ['38'], 314: ['19'], 313: ['10', '2'], 310: ['43', '33'], 309: ['3'], \
308: ['22'], 306: ['35', '6'], 302: ['45']}

_Explanation:_ \
Numbers '29' and '37' have been appeared 365 times.

### Joker Statistics
Contains how many times each joker number (1 - 20) has been appeared in all draws.\
Key is the number of appearances of a number(s).\
Value is the actual number(s).\
E.g.:

OPAP Joker Statistics: \
{160: ['3'], 159: ['1'], 158: ['8'], 157: ['18', '6'], 155: ['16'], 150: ['19', '15'], \
149: ['4'], 148: ['9'], 147: ['2', '10'], 146: ['7'], 143: ['13'], 142: ['5'], 140: ['11'], \
139: ['14'], 138: ['12'], 135: ['17'], 131: ['20']}

_Explanation:_ \
Joker number '3' has been appeared 160 times.

### Odd/Even statistics (both for numbers and joker numbers)
Contains statistics about Even/Odd numbers and its appearance.\
Keys: OddNumbers, EvenNumbers_1, EvenNumbers_2, EvenNumbers_3, EvenNumbers_4, EvenNumbers, EvenJoker and OddJoker.\
Values: Are the number or odd/even appearances of the numbers.\
E.g.:

Total Odd/Even Statistics: \
{'OddNumbers': 76, 'EvenNumbers_1': 496, 'EvenNumbers_2': 982, 'EvenNumbers_3': 941, 'EvenNumbers_4': 385, 'EvenNumbers': 71, 'EvenJoker': 1478, 'OddJoker': 1473}

_Explanation:_ \
OddNumbers = 76 (All numbers are odd, happened 76 times).\
EvenNumbers_1 = 496 (One number is even out of five, happened 496 times).\
EvenNumbers_2 = 982 (Two numbers are even out of five, happened 982 times).\
EvenNumbers_3 = 941 (Three numbers are even out of five, happened 941 times).\
EvenNumbers_4 = 385 (Four numbers are even out of five, happened 385 times).\
EvenNumbers = 71 (All numbers are even, happened 71 times).\
EvenJoker = 1478 (Joker number is even, happened 1478 times).\
OddJoker = 1473 (Joker number is odd, happened 1473 times).

### Last 5 Draws Statistics
Contains statistics about the 5 last draws.\
Key is the number of appearances of a number(s).\
Value is the actual number(s).\
E.g.:

Last 5 Draws Number Statistics: \
{3: ['13'], 2: ['44', '3', '37'], \
1: ['43', '33', '7', '27', '15', '22', '29', '16', '28', '20', '17', '24', '31', '26', '2', '39']}

Last 5 Draws Joker Statistics: \
{2: ['14'], 1: ['17', '18', '10']}

<pre>2947 Draw: |  7 13 33 43 44 | 17 | 
2948 Draw: |  3 13 15 22 27 | 18 | 
2949 Draw: | 16 28 29 37 44 | 14 | 
2950 Draw: |  3 17 20 24 31 | 14 | 
2951 Draw: |  2 13 26 37 39 | 10 | </pre>

_Explanation:_ \
Number '13' has been appeared 3 times in the last 5 draws.\
Numbers '44', '3', and '37' have been appeared 2 times in the last 5 draws.

## Usage
* Put the script in a file location of your choice (e.g. /home/my_user_name).
* During 1st execution, the script will create a new folder named "excel_data_files" and will download
all Excel files from the official OPAP site. 
* The script will create and save all the draws and its results, in file _'/home/my_user_name/excel_data_files/Joker_results.txt'_.

In order to run the script, open a Linux terminal and run the following command:\
**python3 -i opap_joker_statistics.py**

## Dependencies
Pandas python library needs to be installed in the system. \
e.g.: \
pip install pandas

## License 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
