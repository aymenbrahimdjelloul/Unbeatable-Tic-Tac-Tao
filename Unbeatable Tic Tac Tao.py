"""
@author : Aymen Brahim Djelloul
version : 1.0
date : 13.07.2024
License : MIT


    // This my Unbeatable Tic Tac Tao Game !

 - This is a Python implementation of an unbeatable Tic Tac Toe game using the PyQt5 framework for the graphical
    user interface. The game allows a human player to compete against a computer opponent that uses
    the minimax algorithm to make optimal moves, ensuring that it never loses. The minimax algorithm evaluates all possible
    moves and selects the one that maximizes the computer's chances of winning or minimizing the chances of losing.
    The game interface is simple and intuitive, featuring a 3x3 grid with reset functionality to start new games.
    This project demonstrates the power of game theory and algorithmic decision-making in creating intelligent game opponents.


"""

# IMPORTS
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

# DEFINE VARIABLES
AUTHOR: str = "Aymen Brahim Djelloul"


class Game(QWidget):

    BOARD: dict = {0: '', 1: '', 2: '',
                   3: '', 4: '', 5: '',
                   6: '', 7: '', 8: ''}

    PLAY_TURN: str = "X"

    def __init__(self):
        super(Game, self).__init__(parent=None)

        # Set up the game board
        self.setWindowTitle("Unbeatable Tic Tac Toe")
        self.setFixedSize(430, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon("icon.ico"))

        # Set the Current player always 'X'
        self.current_play_turn = "X"
        self.buttons = []
        x = 70
        y = 20

        # Draw the tic tac tao board using nested loop
        for i in range(3):
            for j in range(3):
                button = QPushButton('', self)
                button.move(x, y)
                button.setFont(QFont("Ubuntu", 16))
                button.setCursor(Qt.PointingHandCursor)
                button.setStyleSheet("""
                QPushButton {
                    width: 70px;
                    height: 70px;
                    border: 2px solid;
                    border-radius: 7px;
                    border-color: #A490C7;
                    padding: 7px;
                    color: #738995;
                }
                QPushButton::hover {
                    background-color: #cfcfcf;
                }
                """)
                button.clicked.connect(lambda _, row=i, col=j: self.on_play(row, col))
                self.buttons.append(button)

                x += 100

            x -= 100 * 3
            y += 100

        # Create the reset button
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.move(185, 320)
        self.reset_button.setFont(QFont("Helvetica", 11))
        self.reset_button.clicked.connect(self.reset_game)
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.setStyleSheet("""
        QPushButton {
            width: 60px;
            height: 30px;
            border: 1px solid;
            border-radius: 5px;
            border-color: #A490C7;
            color: #A490C7;
            background-color: transparent;
        }
        QPushButton::hover {
            color: #706f70;
            border-color: #706f70;
        }
        """)

        # Create the developed by label
        developed_by_label = QLabel(f"Developed by {AUTHOR}", self)
        developed_by_label.move(90, 370)
        developed_by_label.setFont(QFont("Ubuntu", 11))
        developed_by_label.setStyleSheet("""
        color: #738995;
        weight: 600;
        """)

    def on_play(self, row, col):
        """ This method will handle the action when the user will play"""

        index = row * 3 + col
        # Check if the played square is empty
        if self.BOARD[index] == '':
            self.BOARD[index] = self.current_play_turn
            self.buttons[index].setText(self.current_play_turn)

            # Check for winner
            if self.check_winner(self.BOARD, self.current_play_turn):
                self.display_winner("Bot")
                return

            # Check if Draw
            if self.is_draw():
                # Display the Draw message
                self.setWindowTitle("Draw !")
                # disable buttons
                for button in self.buttons:
                    button.setEnabled(False)

                return

            # Switch the current play turn
            self.current_play_turn = 'O' if self.current_play_turn == 'X' else 'X'

            # Engage the bot to play
            if self.current_play_turn == 'O':
                self.bot_play()

    def bot_play(self):
        """ This method will handle the action when the Bot is playing"""

        index = self.minimax(self.BOARD, 'O')['index']
        self.BOARD[index] = (''
                             'O')
        self.buttons[index].setText('O')
        if self.check_winner(self.BOARD, 'O'):
            self.display_winner('Bot')
        else:
            self.current_play_turn = 'X'

    def minimax(self, new_board, player):
        """ This method is a simple and straight-forward implementation for MiniMax algorithm"""

        avail_spots = [key for key, value in new_board.items() if value == '']

        if self.check_winner(new_board, 'X'):
            return {'score': -10}
        elif self.check_winner(new_board, 'O'):
            return {'score': 10}
        elif len(avail_spots) == 0:
            return {'score': 0}

        moves = []
        for i in avail_spots:
            move: dict = {}
            move['index'] = i
            new_board[i] = player

            if player == 'O':
                result = self.minimax(new_board, 'X')
                move['score'] = result['score']
            else:
                result = self.minimax(new_board, 'O')
                move['score'] = result['score']

            new_board[i] = ''
            moves.append(move)

        best_move = None
        if player == 'O':
            best_score = -10000
            for move in moves:
                if move['score'] > best_score:
                    best_score = move['score']
                    best_move = move
        else:
            best_score = 10000
            for move in moves:
                if move['score'] < best_score:
                    best_score = move['score']
                    best_move = move

        return best_move

    def reset_game(self):
        """This method will reset the game when the game is ended"""

        self.BOARD = {i: '' for i in range(9)}

        # Reset the buttons
        for button in self.buttons:
            button.setText('')
            button.setEnabled(True)

        # Reset the current play turn
        self.current_play_turn = "X"

        # Reset the window title
        self.setWindowTitle("Unbeatable Tic Tac Tao")

    @staticmethod
    def check_winner(board: dict, player: str) -> bool:
        """ This method will check for the win or draw and stop the game when it finds it """
        # print(board)
        win_cond = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                    (0, 3, 6), (1, 4, 7), (2, 5, 8),
                    (0, 4, 8), (2, 4, 6)]

        # Check for win
        return True if any(board[a] == board[b] == board[c] == player for a, b, c in win_cond) else False

    def is_draw(self) -> bool:
        """ This method will check for draw on the game"""
        return True if all(value != '' for value in self.BOARD.values()) else False

    def display_winner(self, player):
        """ This method will display the win or draw message when it occurred"""

        # Disable buttons
        for button in self.buttons:
            button.setEnabled(False)

        # Display who wins using the window Title
        self.setWindowTitle(f"Player {player} Wins!") if player != "Bot" else self.setWindowTitle("Bot Wins !")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_game = Game()
    my_game.show()
    app.exec()
