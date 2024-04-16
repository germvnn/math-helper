# Math Helper CLI

Math Helper CLI is a command-line interface for generating and solving arithmetic exercises,
including operations like addition, subtraction, multiplication, and division, as well
as their fractional counterparts.

## Installation

Before running the CLI, ensure you have Python 3.6+ installed on your system.
It's also recommended to use a virtual environment.

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

To use the CLI, navigate to the project's root directory and run the cli.py script using Python.
You'll need to specify the operation, level, and amount using command-line arguments

```bash
python cli.py -operation [OPERATION] -level [LEVEL] -amount [AMOUNT]
```

Replace [OPERATION] with one of the following: addition, subtraction, multiplication, division,
faddition (fraction addition), fsubtraction, fmultiplication, fdivision, paddition (percent addition), psubtraction

Replace [LEVEL] with the difficulty level of the exercises (as an integer).

Replace [AMOUNT] with the number of exercises to generate (as an integer).

### Example

To generate 5 addition exercises at level 1, use the following command:

```bash
python cli.py -operation paddition -level 2 -amount 15
```

The CLI will output two .pdf files with exercises and their solutions.

![alt text](https://i.imgur.com/zFB7dXv.png)

## Contirbuting
Feel free to fork the repository, make your changes, and submit a pull request if you have a new feature or bug fix.