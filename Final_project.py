import random
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from db.db_manipulation import Words


class HangmanGame(QtWidgets.QWidget):
    """Основной класс игры (графический интерфейс и обработка)."""

    def __init__(self):
        """Инициализатор класса. Наследует инициализатор родительского класса.
        """
        super().__init__()
        self.init_ui()
        self.word = ''
        self.guesses = []
        self.alphabet = 'абвгдежзиклмнопрстуфхцчшщъыьэюя'
        self.reset_game()
        self.start_game('Простой')
        self.guessed_letters = []
        self.attempts = 6

    def init_ui(self):
        """Метод класса реализующий графический интерфейс основного окна.
        """
        self.setWindowTitle('Виселица')
        self.setWindowIcon(QtGui.QIcon('.\\pic\\hang.png'))
        self.setFixedSize(QSize(450, 450))

        self.start_button = QtWidgets.QPushButton('Выбрать уровень сложности',
                                                  self)
        self.start_button.setFixedSize(QSize(200, 25))
        self.start_button.clicked.connect(self.select_difficulty)

        self.label_word = QtWidgets.QLabel(self, text='',
                                           font=QtGui.QFont('Arial', 20))
        self.label_letters = QtWidgets.QLabel(self, text='',
                                              font=QtGui.QFont('Arial', 10))

        self.label_attempts = QtWidgets.QLabel(self, text='',
                                               font=QtGui.QFont('Arial', 16))
        self.label_attempts.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.pixmap = QPixmap('.\\pic\\hung06.jpg').scaled(159, 330)
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

        self.image.move(280, 15)
        self.setLayout(layout)

    def select_difficulty(self):
        """Метод класса позволяющий выбрать уровень сложности игры при
        нажатии на кнопку "Выбор уровня сложности".
        После выбора уровня сложности передает управление методу start_game.
        """
        difficulty, ok = (
            QtWidgets.QInputDialog.getItem(self, 'Выбор уровня сложности',
                                           'Выберите уровень сложности:',
                                           ['Простой', 'Средний',
                                            'Сложный'], 0, False))
        if ok and difficulty:
            self.start_game(difficulty)

    def start_game(self, difficulty: str):
        """Метод класса получает из базы данных слово с учетом уровня
        сложности.

        Args:
            difficulty: Уровень сложности.
        """
        wd = Words('db/words.db')
        word = random.choice(wd.get(difficulty))
        self.word = word[0]
        self.reset_game()

    def reset_game(self):
        """Метод класса сбрасывающий счетчик неудачных попыток и названых
        букв.
        """
        self.guessed_letters = []
        self.attempts = 6
        self.update_display()

    def update_display(self):
        """Метод класса для вывода информации об угадываемом слове,
        использованных буквах, количестве оставшихся неудачных попыток,
        а также для отображения "виселицы".
        """
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
        """Метод класса для обработки вводимых букв, проверка, что все слово
        угадано, изменение счетчика неудачных попыток при вводе
        буквы, которой нет в слове и смены изображения "виселицы".
        """
        letter = self.input_letter.text().lower()
        self.input_letter.clear()
        if (letter in self.guessed_letters or len(letter) != 1 or
                not (letter in self.alphabet)):
            return
        self.guessed_letters.append(letter)
        if all(letter in self.guessed_letters for letter in self.word):
            self.update_display()
            QtWidgets.QMessageBox.information(self, 'Поздравляем!',
                                              f'Вы угадали слово: {self.word}')
            self.reset_game()
            self.select_difficulty()
            return
        if letter not in self.word:
            self.attempts -= 1
            self.pixmap = QPixmap(f'.\\pic\\hung{self.attempts}.png')
        self.update_display()
        if self.attempts == 0:
            self.end_game()

    def end_game(self):
        """Метод класса, завершающий текущую игру (вызывается при исчерпании
        количества неудачных попыток).
        """
        reply = QtWidgets.QMessageBox.question(
            self, 'Игра окончена', f'Загаданное слово: {self.word}\n'
                                   f'Хотите сыграть снова?',
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No)
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.reset_game()
            self.select_difficulty()
        else:
            self.close()

    def exit_game(self):
        """Метод класса позволяющий завершить игру и выйти из приложения (
        есть возможность посмотреть загаданное слово).
        """
        reply = QtWidgets.QMessageBox.question(
            self, 'Выход', 'Хотите увидеть загаданное слово?',
            QtWidgets.QMessageBox.StandardButton.Yes |
            QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            QtWidgets.QMessageBox.information(self, 'Загаданное слово',
                                              f'Загаданное слово: {self.word}')
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = HangmanGame()
    game.show()
    sys.exit(app.exec())
