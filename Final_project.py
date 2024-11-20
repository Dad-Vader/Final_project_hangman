import sys
import random
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class HangmanGame(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.word = ""
        self.guesses = []
        self.reset_game()

    def initUI(self):
        self.setWindowTitle('Виселица')
        self.setGeometry(100, 100, 450, 450)

        self.start_button = QtWidgets.QPushButton('Выбрать уровень сложности', self)
        self.start_button.clicked.connect(self.select_difficulty)

        self.label_word = QtWidgets.QLabel(self, text='', font=QtGui.QFont(
            'Arial', 20))
        self.label_letters = QtWidgets.QLabel(self, text='', font=QtGui.QFont(
            'Arial', 10))

        self.label_attempts = QtWidgets.QLabel(self, text='', font=QtGui.QFont('Arial', 16))
        self.label_attempts.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.pixmap = QPixmap('.\\pic\\hung06.jpg').scaled(154, 320)
        self.image = QLabel(self)

        self.image.setPixmap(self.pixmap)
        self.image.resize(190, 300)

        self.input_letter = QtWidgets.QLineEdit(self)
        self.input_letter.setMaxLength(1)
        self.input_letter.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.button_guess = QtWidgets.QPushButton('Угадать', self)
        self.button_guess.clicked.connect(self.guess_letter)

        self.button_restart = QtWidgets.QPushButton('Начать сначала', self)
        self.button_restart.clicked.connect(self.reset_game)

        self.button_exit = QtWidgets.QPushButton('Выход', self)
        self.button_exit.clicked.connect(self.exit_game)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.label_word)
        layout.addWidget(self.label_letters)
        layout.addWidget(self.label_attempts)
        layout.addWidget(self.input_letter)
        layout.addWidget(self.button_guess)
        layout.addWidget(self.button_restart)
        layout.addWidget(self.button_exit)
        self.image.move(280, 20)
        self.setLayout(layout)

    def select_difficulty(self):
        difficulty, ok = QtWidgets.QInputDialog.getItem(self, 'Выбор уровня сложности',
            'Выберите уровень сложности:', ['Простой', 'Средний', 'Сложный'], 0, False)
        if ok and difficulty:
            self.start_game(difficulty)

    def start_game(self, difficulty):
        words = {
            'Простой': ['кот', 'собака', 'дом'],
            'Средний': ['машина', 'дерево', 'книга'],
            'Сложный': ['программирование', 'алгоритм', 'интерфейс']
        }
        self.word = random.choice(words[difficulty])
        self.guessed_letters = []
        self.attempts = 6
        self.update_display()

    def reset_game(self):
        self.guessed_letters = []
        self.attempts = 6
        self.update_display()

    def update_display(self):
        displayed_word = ''.join([letter if letter in self.guessed_letters
                                  else '_ ' for letter in self.word])
        self.label_word.setText(displayed_word)
        sorted_guessed_letters = sorted(self.guessed_letters)
        self.label_letters.setText(''.join(sorted_guessed_letters))
        self.label_attempts.setText(f'Осталось попыток: {self.attempts}')
        self.pixmap = QPixmap(f'.\\pic\\hung{self.attempts}.png').scaled(154,
                                                                         320)
        self.image.setPixmap(self.pixmap)

    def guess_letter(self):
        letter = self.input_letter.text().lower()
        self.input_letter.clear()
        if letter in self.guessed_letters or len(letter) != 1:
            return
        self.guessed_letters.append(letter)
        if all(letter in self.guessed_letters for letter in self.word):
            self.update_display()
            QtWidgets.QMessageBox.information(self, 'Поздравляем!',
                                          f'Вы угадали слово: {self.word}')
            self.reset_game()
        if letter not in self.word:
            self.attempts -= 1
            self.pixmap = QPixmap(f'.\\pic\\hung{self.attempts}.png')
        self.update_display()
        if self.attempts == 0:
            self.end_game()

    def end_game(self):
        reply = QtWidgets.QMessageBox.question(self, 'Игра окончена', f'Загаданное слово: {self.word}\nХотите сыграть снова?',
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.reset_game()
        else:
            self.close()

    def exit_game(self):
        reply = QtWidgets.QMessageBox.question(self, 'Выход', 'Хотите увидеть загаданное слово?',
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QMessageBox.information(self, 'Загаданное слово', f'Загаданное слово: {self.word}')
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec())
