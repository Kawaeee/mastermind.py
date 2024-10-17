import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9991))  # Ensure this matches the server's address and port

    while True:
        response = client.recv(1024).decode('utf-8')
        print(response)

        # Check for game-ending conditions
        if "guessed the code correctly" in response.lower() or "has ended" in response.lower():
            print("The game has ended! Thanks for playing!")
            break

        if "no one guessed the code correctly" in response.lower():
            print("The game has ended! Thanks for playing!")
            break

        # Continue waiting for players if the game hasn't started
        if "waiting for more players" in response.lower():
            continue

        # If the game is ongoing, prompt for a guess
        if "enter your 6-digit guess" in response.lower() or "your turn" in response.lower():
            while True:
                guess = input("Input: ")
                if len(guess) == 6 and guess.isdigit():
                    client.send(guess.encode('utf-8'))
                    break  # Exit the guess input loop if the guess is valid
                else:
                    print("[WARNING] Guess must be a 6-digit number. Please try again.")

    # Close the client connection once the game has ended
    client.close()

if __name__ == "__main__":
    main()