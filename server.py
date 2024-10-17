import random
import os
import socket
import threading

from dotenv import load_dotenv

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", None)
SERVER_PORT = int(os.getenv("SERVER_PORT", None))
N_PLAYERS = int(os.getenv("N_PLAYERS", None))
N_ROUNDS = int(os.getenv("N_ROUNDS", None))


class GameServer:
    def __init__(self):
        self.clients = []
        self.code = None
        self.turn_index = 0
        self.game_started = False  # Flag to track if the game has started
        self.rounds_played = {}  # Track rounds for each player

    def generate_code(self):
        return "".join(random.sample([str(i) for i in range(10)], 6))

    def start_game(self):
        self.code = self.generate_code()
        self.game_started = True  # Set the game started flag
        print("Game started. Generated code:", self.code)
        self.notify_clients("The game has started! The code is hidden.")

    def validate_guess(self, guess):
        correct_value_correct_position = sum(1 for i in range(6) if guess[i] == self.code[i])
        correct_value_incorrect_position = (
            sum(min(guess.count(digit), self.code.count(digit)) for digit in set(guess))
            - correct_value_correct_position
        )
        return correct_value_correct_position, correct_value_incorrect_position

    def handle_client(self, client_socket):
        client_id = len(self.clients) + 1
        self.clients.append(client_socket)
        self.rounds_played[client_id] = 0  # Initialize rounds for the new player

        print(f"Client {client_id} has connected.")
        client_socket.send(f"Waiting for more players. Current players: {len(self.clients)}".encode("utf-8"))

        # Wait until enough players have joined
        while len(self.clients) < N_PLAYERS:
            threading.Event().wait(1)  # Wait for a second

        # Start the game if it hasn't started yet
        if len(self.clients) == N_PLAYERS and not self.game_started:
            self.start_game()

        while True:
            if self.game_started:
                if client_id == self.turn_index + 1:  # Adjust for 0-indexing

                    # Notify the current player that it's their turn
                    client_socket.send(b"Your turn to guess. Enter your 6-digit guess: ")

                    guess = client_socket.recv(1024).decode("utf-8").strip()

                    if not (len(guess) == 6 and guess.isdigit()):
                        client_socket.send(b"[WARNING] Guess must be a 6-digit number. Please try again.")
                        continue

                    correct_value_correct_position, correct_value_incorrect_position = self.validate_guess(guess)
                    response = f"\nClient {client_id} guessed: {correct_value_correct_position} {correct_value_incorrect_position} ({' '.join(list(guess))})"

                    if correct_value_correct_position == 6:
                        response += f"\** Client {client_id} guessed the code correctly! The code was {self.code}!!"
                        self.notify_clients(response)
                        self.cleanup_game()
                        break  # End the client loop

                    self.rounds_played[client_id] += 1

                    # Check if max rounds reached for all players
                    total_rounds = sum(self.rounds_played.values())
                    if total_rounds >= N_ROUNDS * len(self.clients):
                        self.notify_clients(f"No one guessed the code correctly. The code was {self.code}.")
                        self.cleanup_game()
                        break  # End the client loop
                    self.turn_index = (self.turn_index + 1) % len(self.clients)
                    self.notify_clients(response.strip())
                else:
                    threading.Event().wait(1)  # Wait a bit before checking again
            else:
                break  # Exit if the game has not started

        # Safely close the client socket
        client_socket.close()

        # Safely remove the player's round tracking and client from the game
        self.rounds_played.pop(client_id, None)  # Safely remove rounds tracking
        if client_socket in self.clients:  # Only remove if present
            self.clients.remove(client_socket)

        # If no clients left, reset the game
        if not self.clients:
            print("No clients left. Resetting the game.")
            self.reset_game()

    def notify_clients(self, message):
        for client in self.clients:
            try:
                client.send(message.encode("utf-8"))
            except Exception as e:
                print(f"Error notifying client: {e}")

    def cleanup_game(self):
        # Notify all clients that the game is ending and disconnect them
        for client in self.clients[:]:  # Iterate over a copy of the list
            client.send(b"\nDisconnecting...")
            client.close()
        self.clients.clear()
        self.rounds_played.clear()  # Clear rounds tracking safely
        self.reset_game()

    def reset_game(self):
        self.turn_index = 0
        self.code = None
        self.game_started = False  # Reset the game started flag


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, int(SERVER_PORT)))
    server.listen(5)
    print(f"Server listening on port {SERVER_PORT}")
    print("Total rounds: {N_ROUNDS}, Total players: {N_PLAYERS}")

    game_server = GameServer()

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=game_server.handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    main()
