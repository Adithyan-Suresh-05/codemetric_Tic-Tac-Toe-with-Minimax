import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player_symbol = 'X'
        self.computer_symbol = 'O'
        self.buttons = [[None]*3 for _ in range(3)]
        self.board = [['']*3 for _ in range(3)]
        self.player_score = 0
        self.computer_score = 0

        self.choose_symbol()
        self.build_gui()

    def choose_symbol(self):
        symbol = simpledialog.askstring("Choose Symbol", "Do you want to be X or O?")
        if symbol and symbol.upper() in ['X', 'O']:
            self.player_symbol = symbol.upper()
            self.computer_symbol = 'O' if self.player_symbol == 'X' else 'X'
        else:
            messagebox.showinfo("Default", "Invalid choice. You'll play as X by default.")

    def build_gui(self):
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 14))
        self.score_label.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text="", font=('Arial', 24), width=5, height=2,
                                command=lambda row=i, col=j: self.on_click(row, col))
                btn.grid(row=i+1, column=j)
                self.buttons[i][j] = btn

    def get_score_text(self):
        return f"Player ({self.player_symbol}): {self.player_score}   Computer ({self.computer_symbol}): {self.computer_score}"

    def on_click(self, row, col):
        if self.buttons[row][col]['text'] == "" and not self.check_winner():
            self.buttons[row][col].config(text=self.player_symbol)
            self.board[row][col] = self.player_symbol

            if self.check_winner():
                self.player_score += 1
                self.score_label.config(text=self.get_score_text())
                self.end_game(f"You win!")
                return

            if self.is_draw():
                self.end_game("It's a draw!")
                return

            self.root.after(500, self.computer_move)

    def computer_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = self.computer_symbol
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            row, col = best_move
            self.buttons[row][col].config(text=self.computer_symbol)
            self.board[row][col] = self.computer_symbol

            if self.check_winner():
                self.computer_score += 1
                self.score_label.config(text=self.get_score_text())
                self.end_game("Computer wins!")
            elif self.is_draw():
                self.end_game("It's a draw!")

    def minimax(self, board, depth, is_maximizing):
        winner = self.get_winner()
        if winner == self.player_symbol:
            return -1
        elif winner == self.computer_symbol:
            return 1
        elif self.is_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.computer_symbol
                        score = self.minimax(board, depth+1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.player_symbol
                        score = self.minimax(board, depth+1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        winner = self.get_winner()
        if winner:
            for i in range(3):
                if self.board[i][0] == self.board[i][1] == self.board[i][2] == winner:
                    self.highlight([self.buttons[i][0], self.buttons[i][1], self.buttons[i][2]])
                if self.board[0][i] == self.board[1][i] == self.board[2][i] == winner:
                    self.highlight([self.buttons[0][i], self.buttons[1][i], self.buttons[2][i]])
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == winner:
                self.highlight([self.buttons[0][0], self.buttons[1][1], self.buttons[2][2]])
            if self.board[0][2] == self.board[1][1] == self.board[2][0] == winner:
                self.highlight([self.buttons[0][2], self.buttons[1][1], self.buttons[2][0]])
            return True
        return False

    def get_winner(self):
        lines = (
            [self.board[i] for i in range(3)] +  # rows
            [[self.board[i][j] for i in range(3)] for j in range(3)] +  # columns
            [[self.board[i][i] for i in range(3)]] +  # diagonal
            [[self.board[i][2 - i] for i in range(3)]]  # anti-diagonal
        )
        for line in lines:
            if line[0] != '' and all(cell == line[0] for cell in line):
                return line[0]
        return None

    def is_draw(self):
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.reset_board()

    def highlight(self, winning_buttons):
        for btn in winning_buttons:
            btn.config(bg='lightgreen')

    def reset_board(self):
        self.board = [['']*3 for _ in range(3)]
        for row in self.buttons:
            for btn in row:
                btn.config(text='', bg='SystemButtonFace')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
