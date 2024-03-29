# Lambda Calculus Expression Calculator

This project is a lambda calculus expression calculator that can be executed by terminal and by a Telegram Bot, see Usage to differenciate the two versions. It allows you to evaluate, save (with MACROS) and simplify expressions using lambda calculus, applying α-conversions and β-reductions.


# Features

- Evaluates and simplifies lambda calculus expressions.
- Telegram chat interface for interacting with the bot.
- Terminal execution of the program.
- Supports MACROS, α-conversions and β-reductions.


# Requirements

- Python 3.x


# Installation

## 1. Clone this repository:

   git clone https://github.com/Loparc/Achurch


## 2. Navigate to the project directory:

cd Achurch

## 3. Install the dependencies using pip:

### For the terminal version & Telegram bot

pip install antlr4-tools

pip install antlr4-python3-runtime

### For Telegram bot

pip install python-telegram-bot

pip install pydot

sudo apt install graphviz


# Usage

#### For both versions you need to, first of all, execute this commands on the Achurch directory:

antlr4 -Dlanguage=Python3 -no-listener -visitor lc.g4

## Usage Terminal Version

1. Run the following command to start:

python3 achurch.py

2. Start sending commands/macros/lambda expressions to be evaluated and simplified.

## Execute Telegram Version

1. Obtain the token for your Telegram bot by following the official Telegram documentation.

2. Create a token.txt file and paste the <TOKEN> on it.

3. Run the following command to start the bot:

python3 achurch_Telegram.py

4. Open Telegram and search for your bot's name. Start sending commands/macros/lambda expressions to be evaluated and simplified.