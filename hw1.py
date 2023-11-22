# Напишіть функціонал “Бібліотеки” яка зберікає книжки.
#
# Обʼєкт класу “Бібліотека”:
# Атрибути:
# назва
# дата створення (записується автоматично при створенні обʼєкта)
# Може бути створено тільки один бʼєкт класу “Бібліотека” (реалізуйте Singleton).
# Обʼєкт класу “Бібліотека” зберігає в собі тільки обʼєкти класу “Книжка”
# Обʼєкт класу “Бібліотека” має метод для додавання книжки (add_book)
# Обʼєкт класу “Бібліотека” має метод для видалення книжки по точному співпадінню назви (pop_book)
# Обʼєкт класу “Бібліотека” має метод для пошуку книжки/книжок по назві (search_by_name) включаючи часткове співпадіння
# Обʼєкт класу “Бібліотека” має метод для пошуку книжки/книжок по імені автора (search_by_author) включаючи часткове співпадіння
# Обʼєкт класу “Бібліотека” повинен ітеруватись:
# на кожній ітерації повинні вдаватись 10 книжок
# додайте окремий метод, який повертає ітератор книжок в алфавітному порядку по назві (реалізуйте за допомогою генератора)
# Обʼєкт класу “Бібліотеки” повинен репрезентуватися наступним чином - кількість книжок в бібліотеці
# Обʼєкт класу “Книжка”:
# Атрибути:
# назва
# автор
# кількість сторінок
# рік видання
# Створіть бібліотеку, створіть декілька книжок. Додайте книжки в бібліотеку. Виконайте пошук по назві та по автору. Видаліть книжку з бібліотеки. Проітеруйтесь по бібліотеці, проітеруйтесь по бібліотеці в алфавітному порядку.
#
# * Додайте перевірку вхідних даних для створення книжки за допомогою Pydantic. Додайте перевірку вхідних даних для створення бібліотеки за допомогою Pydantic. https://docs.pydantic.dev/latest/
#
# зклонуйте https://gitlab.com/Artem.Khriapa/pythonpronov2023
#
# створіть гілку <ваша_фамілія>_hw1 і додайте туди ваше рішення. пушніть гілку в репозиторій. створіть MergeRequest цієї гілки в main
import datetime
from pprint import pprint


class Book:
    def __init__(self, book_name: str, book_author: str, book_pages_amount: int, book_year_of_release: int):
        self.book_name = book_name
        self.book_author = book_author
        self.book_pages_amount = book_pages_amount
        self.book_year_of_release = book_year_of_release

    def __repr__(self):
        return f'Книжка під назвою {self.book_name}, автором якої є {self.book_author} з кількістю сторінок {self.book_pages_amount} була видана у {self.book_year_of_release} році.'


class Library:
    _instance = None

    def __new__(cls, library_name: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.library_name = library_name
            cls.books = []
            cls.date = datetime.datetime.now()
        return cls._instance

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)
        else:
            print(f'Book {book.book_name} is already added to the library')

    def pop_book(self, book_name):
        for book in self.books:
            if book.book_name == book_name:
                self.books.remove(book)
                break

    def search_by_name(self, book_name):
        return [i for i in self.books if book_name.lower() in i.book_name.lower()]

    def search_by_author(self, book_author):
        return [i for i in self.books if book_author.lower() in i.book_author.lower()]

    def __iter__(self):
        self._iteration_index = 0
        return self

    def __next__(self):
        if self._iteration_index < len(self.books):
            result = self.books[self._iteration_index: self._iteration_index + 10]
            self._iteration_index += 10
            return result
        else:
            raise StopIteration

    def books_sorted_name(self):
        for book in sorted(self.books, key=lambda value: value.book_name):
            yield book

    def __repr__(self):
        return f'Бібліотека під назвою {self.library_name}, вміщує в собі {len(self.books)} книжок.'


library = Library('Міська бібліотека')
book_1 = Book('Harry Potter', 'Joan Rowling', 464, 1997)
book_2 = Book('Don Kihot', 'Miguel de Servantes', 552, 1605)
book_3 = Book('Sherlock Holmes', 'Arthur Conan-Doyle', 768, 1887)
book_4 = Book('Don Juan', 'Molier', 256, 1819)

library.add_book(book_1)
library.add_book(book_2)
library.add_book(book_3)
library.add_book(book_4)
print('-----------------------------------------------------------')
pprint(library.search_by_name('Don'))
print('-----------------------------------------------------------')
pprint(library.search_by_author('joan'))
print('-----------------------------------------------------------')
library.pop_book('Don Kihot')

for book in library:
    pprint(book)
print('-----------------------------------------------------------')

for book in library.books_sorted_name():
    pprint(book)

print('-----------------------------------------------------------')
