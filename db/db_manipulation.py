# db_manipulation.py
import random
import sqlite3

from db.create_db import create_table


class Words:
    """Класс описывающий базу слов.

    """
    def __init__(self, path='words.db'):
        """Инициализатор класса вызывающий внешнюю функцию, создающую базу
        данных.

        Args:
            path: Путь к базе данных.
        """
        self.path = path

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
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO words (word, difficulty) VALUES (?, ?)',
                       (word, difficulty))
        conn.commit()
        conn.close()

    def get(self, difficulty: str) -> list:
        """Метод класса для поиска слов по уровню сложности.

        Args:
            difficulty: Уровень сложности слов.

        Returns: Список слов.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT word FROM words WHERE difficulty = ?',
                       (difficulty,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_all(self) -> list:
        """Метод класса для вывода всех записей в базе.

        Returns: Список всех строк базы.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM words')
        result = cursor.fetchall()
        conn.close()
        return result

    def delete(self, id: int):
        """Метод класса для удаления записи по ее id.

        Args:
            id: Идентификатор записи.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM words WHERE id = ?', (id,))
        conn.commit()
        conn.close()

    def update(self, id, word=None, difficulty=None):
        """Метод класса для внесения изменений в базу по id. Можно менять
        слово и/или его уровень сложности.

        Args:
            id: Идентификатор записи.
            word: Слово.
            difficulty: Сложность.
        """
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        if word:
            self.check_word(word)
            cursor.execute('UPDATE words SET word = ? WHERE id = ?',
                           (word, id))
        if difficulty:
            self.check_difficulty(difficulty)
            cursor.execute('UPDATE words SET difficulty = ? WHERE id = ?',
                           (difficulty, id))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    create_table()
    list_easy = ['бор', 'перо', 'кот', 'дом', 'люк', 'мел', 'рак', 'ядро',
                 'бак', 'баян']
    list_avr = ['слово', 'город', 'право', 'книга', 'школа', 'земля', 'спорт',
                'лохань', 'ложка', 'кость']
    list_diff = ['собака', 'цунами', 'кортик', 'снегирь', 'солома', 'зарница',
                 'корабль', 'лошадь', 'телега', 'колесо']
    wd = Words()
    #for word in list_easy:
    #    wd.add(word, 'Простой')
    #for word in list_avr:
    #    wd.add(word, 'Средний')
    #for word in list_diff:
    #    wd.add(word, 'Сложный')
    print(wd.get('Простой'))
    xwd = (random.choice(wd.get('Простой')))
    print(xwd[0])
    #wd.update(1, word='бор')
    #wd.update(1, difficulty='Простой')
    #print(wd.get('Простой'))
    #print(wd.get('Средний'))
