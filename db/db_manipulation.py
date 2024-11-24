# db_manipulation.py
import os.path
import sqlite3

from db.create_db import create_table


class Words:
    """Класс описывающий базу со словами."""

    def __init__(self, path: str = 'words.db'):
        """Инициализатор класса.

        Args:
            path: Путь к базе данных. Ао умолчанию - в текущей директории.
            conn: Соединение с БД.
            cursor: Положение курсора в БД.
        """
        self.path = path
        self.conn = None
        self.cursor = None

    def conn_database(self):
        """Метод класса для соединения с БД
        """
        if os.path.exists(self.path):
            self.conn = sqlite3.connect(self.path)
            self.cursor = self.conn.cursor()
        else:
            raise ValueError('Подключение к БД не удалось, проверьте наличие '
                             'файла БД.')

    def check_table(self):
        """Метод класса для проверки наличия таблицы в БД.
        """
        self.conn_database()
        try:
            self.cursor.execute('SELECT * FROM words')
        except sqlite3.OperationalError:
            raise ValueError('Таблица в базе не существует!')

    @staticmethod
    def check_word(word: str):
        """Метод для проверки корректности вводимых слов.

        Args:
            word: Слово.
        """
        if not word.isalpha():
            raise ValueError("Слово не должно содержать цифры.")

    @staticmethod
    def check_difficulty(difficulty: str):
        """Метод класса для проверки корректности вводимого уровня сложности.

        Args:
            difficulty: Уровень сложности слова.
        """
        if difficulty not in ('Простой', 'Средний', 'Сложный'):
            raise ValueError('Сложность задается одной из трех градаций '
                             '"Простой", "Средний", "Сложный"!')

    def add(self, word: str, difficulty: str):
        """Метод класса для добавления слов в базу данных.

        Args:
            word: Слово.
            difficulty: Уровень сложности слова.
        """
        self.check_word(word)
        self.check_difficulty(difficulty)
        self.conn_database()
        self.check_table()
        try:
            self.cursor.execute('INSERT INTO words (word, difficulty) VALUES '
                                '(?, ?)', (word, difficulty))
        except sqlite3.IntegrityError:
            print(f'Добавляемое слово {word} уже есть в таблице!')
        self.conn.commit()
        self.conn.close()

    def get(self, difficulty: str) -> list:
        """Метод класса для поиска слов по уровню сложности.

        Args:
            difficulty: Уровень сложности слов.

        Returns: Список слов.
        """
        self.conn_database()
        self.check_table()
        self.cursor.execute('SELECT word FROM words WHERE difficulty = ?',
                            (difficulty,))
        result = self.cursor.fetchall()
        self.conn.close()
        return result

    def get_all(self) -> list:
        """Метод класса для вывода всех записей в базе.

        Returns: Список всех строк базы.
        """
        self.conn_database()
        self.check_table()
        self.cursor.execute('SELECT * FROM words')
        result = self.cursor.fetchall()
        self.conn.close()
        return result

    def delete(self, id: int):
        """Метод класса для удаления записи по ее id.

        Args:
            id: Идентификатор записи.
        """
        self.conn_database()
        self.check_table()
        self.cursor.execute('DELETE FROM words WHERE id = ?', (id,))
        self.conn.commit()
        self.conn.close()

    def update(self, id, word=None, difficulty=None):
        """Метод класса для внесения изменений в базу по id. Можно менять
        слово и/или его уровень сложности.

        Args:
            id: Идентификатор записи.
            word: Слово.
            difficulty: Сложность.
        """
        self.conn_database()
        self.check_table()
        if word:
            self.check_word(word)
            self.cursor.execute('UPDATE words SET word = ? WHERE id = ?',
                                (word, id))
        if difficulty:
            self.check_difficulty(difficulty)
            self.cursor.execute('UPDATE words SET difficulty = ? WHERE id = ?',
                                (difficulty, id))
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    list_easy = ['бор', 'перо', 'кот', 'дом', 'люк', 'мел', 'рак', 'ядро',
                 'бак', 'баян']
    list_avr = ['слово', 'город', 'право', 'книга', 'школа', 'земля', 'спорт',
                'лохань', 'ложка', 'кость']
    list_diff = ['собака', 'цунами', 'кортик', 'снегирь', 'солома', 'зарница',
                 'корабль', 'лошадь', 'телега', 'колесо']

    wd = Words()
    create_table()
    for word in list_easy:
        wd.add(word, 'Простой')
    for word in list_avr:
        wd.add(word, 'Средний')
    for word in list_diff:
        wd.add(word, 'Сложный')
