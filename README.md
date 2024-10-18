# mastermind.py

The Mastermind Game is a number-guessing game where the server selects a 6-digit number with unique digits. Players must guess the number, and the server gives feedback on how many digits are correct and in the right or wrong positions.

## **Game Rules:**

1. The game requires at least two players: a server and more than 2 or equal clients.
2. The server selects a 6-digit number with no repeating digits.
3. Players take turns guessing the number, and after each guess, the server provides feedback on:
   * The number of correct digits in the right position.
   * The number of correct digits in the wrong position.
4. Players have a maximum of n(based on server configuration) guesses to find the correct number.
5. If a player guesses the number correctly within n attempts, they win. If not, they lose.
6. The game ends when the correct number is guessed or the maximum number of attempts is reached.
7. Invalid guesses, such as numbers with repeating digits, must be handled by the server with appropriate feedback.

## **Game Example:**

For example, if the server's secret number is 482913:
* 1st guess (493257): The server responds with "21(493257)," meaning 2 digits are correct and in the right position, while 1 digit is correct but in the wrong position.
* 2nd guess (128943): The server responds with "33(128943)," meaning 3 digits are correct and in the right position, and 3 digits are correct but in the wrong position.
* 3rd guess (482391): The server responds with "52(482391)," meaning 5 digits are correct and in the right position, and 2 digits are correct but in the wrong position.

## Getting Started

* Clone the repository
```bash
git clone https://github.com/Kawaeee/mastermind.py.git
cd mastermind.py
```

* Install requirements
```bash
pip install -r requirements.txt
```

* Copy .env.example to .env
```bash
cp .env.example .env
```

* Start the server
```bash
python server.py
```

* Start client at least 2 instances
```bash
# Shell 1
python client.py

# Shell 2
python client.py
```

* Have fun!
