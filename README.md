# Math Helper CLI

Math Helper CLI is a command-line interface for generating and solving arithmetic exercises,
including operations like addition, subtraction, multiplication, and division, as well
as their fractional counterparts.

### 17 April 2024 - Math Helper supports Quadratic equations|inequalities!
### 23 April 2024 - Math Helper supports Linear equations|inequalities!

## Installation

Before running the CLI, ensure you have Python 3.10+ installed on your system.
It's also recommended to use a virtual environment.

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

Make sure that you have installed MiKTeX with following packages from
file <span style="color: cyan;">miktex_packages.txt</span>

## Usage

To use the CLI, navigate to the project's root directory and run the cli.py script using Python.
You'll need to specify the operation, level, and amount using command-line arguments

```bash
python cli.py -operation [OPERATION] -level [LEVEL] -amount [AMOUNT]
```

### Replace <span style="color: red;">[OPERATION]</span> with one of the following:<br>
Simple Arithmetic Operations: <span style="color: red;">addition, subtraction, multiplication, division</span><br>
Fraction Arithmetic Operations: <span style="color: red;">faddition, fsubtraction, fmultiplication, fdivision</span><br>
Percent Arithmetic Operations: <span style="color: red;">paddition, psubtraction</span><br><br>
Quadratic Operations:
- <span style="color: red;">quadratic</span> - Quadratic exercises with random operator
- <span style="color: red;">qequation</span> - Quadratic Equations
- <span style="color: red;">qinequationl</span> - Quadratic Inequality (less)
- <span style="color: red;">qinequationg</span> - Quadratic Inequality (greater)
- <span style="color: red;">qequalless</span> - Quadratic Inequality (less or equal)
- <span style="color: red;">qequalgreater</span> - Quadratic Inequality (greater or equal)

Linear Operations:
- <span style="color: red;">linear</span> - Linear exercises with random operator
- <span style="color: red;">lequation</span> - Linear Equations
- <span style="color: red;">linequationl</span> - Linear Inequality (less)
- <span style="color: red;">linequationg</span> - Linear Inequality (greater)
- <span style="color: red;">lequalless</span> - Linear Inequality (less or equal)
- <span style="color: red;">lequalgreater</span> - Linear Inequality (greater or equal)

### Replace <span style="color: blue;">[LEVEL]</span> with the difficulty level of the exercises (<span style="color: blue;">integer</span>).

### Replace <span style="color: green;">[AMOUNT]</span> with the number of exercises to generate (<span style="color: green;">integer</span>).

## Example

To generate <span style="color: green;">2</span> quadratic inequality (<span style="color: red;">qequalgreater</span>)
exercises at level <span style="color: blue;">3</span>, use the following command:

```bash
python cli.py -operation qequalgreater -level 3 -amount 2
```

The CLI will output two .pdf files with exercises and their solutions.

![alt text](https://i.imgur.com/tbahpEU.png)

## Contirbuting
Feel free to fork the repository, make your changes, and submit a pull request if you have a new feature or bug fix.