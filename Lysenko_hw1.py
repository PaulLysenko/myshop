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

from datetime import datetime
from pydantic import BaseModel, ValidationError
import threading


class BookModel(BaseModel):
    title: str
    author: str
    sheets: int
    year: int


class Book:
    title = None
    author = None
    sheets = None
    year = None

    def __init__(self, title, author, sheets, year):
        try:
            book_data = BookModel(title=title, author=author, sheets=sheets, year=year)
            self.title = book_data.title
            self.author = book_data.author
            self.sheets = book_data.sheets
            self.year = book_data.year
        except ValidationError as e:
            print(f'Error creating Book instance: {e}')


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Library(metaclass=SingletonMeta):
    library_name = None
    date = None
    limit = 0
    current = 0
    book_list = []

    def __init__(self, lib_name):
        self.library_name = lib_name
        self.date = datetime.now()

    def __iter__(self):
        return self

    def __next__(self):
        self.limit += 1
        self.current = self.limit
        if self.limit >= 11:
            raise StopIteration
        else:
            return f'{self.book_list[self.current - 1].title} by {self.book_list[self.current - 1].author} {self.book_list[self.current - 1].year}'
        # return self.book_list[self.current - 1].title

    def add_book(self, book):
        if isinstance(book, Book):
            self.book_list.append(book)
            print(f'"{book.title}" by {book.author} was added to {self.library_name}')
        else:
            print(f'{book} isn\'t an object of a Book class')

    def pop_book(self, title):
        found = False
        for book in self.book_list:
            if title.lower() == book.title.lower():
                self.book_list.remove(book)
                print(f'\t"{book.title}" by {book.author} was removed from {self.library_name}')
                found = True
            elif title.lower() in book.title.lower():
                print(f'Maybe you meant to remove "{book.title}"?')
                found = True
        if not found:
            print(f'There are no books to remove named "{title}"')

    def search_by_title(self, title):
        found = False
        for book in self.book_list:
            if title.lower() == book.title.lower() or title.lower() in book.title.lower():
                print(f'\tHere we go "{book.title}" by {book.author}')
                found = True
        if not found:
            print(f'Unfortunately there is no "{title}" in {self.library_name}')

    def search_by_author(self, author):
        found = False
        for book in self.book_list:
            if author.lower() == book.author.lower() or author.lower() in book.author.lower():
                print(f'\tBook by {book.author}: "{book.title}"')
                found = True
        if not found:
            print(f'There are no books in {self.library_name} written by {author}')

    def sorted_by_alphabet(self):
        sorted_books = sorted(self.book_list, key=lambda book: book.title.lower())
        for book in sorted_books:
            yield book.title

    def __repr__(self):
        return f'\tLibrary: {self.library_name}, Number of books: {len(self.book_list)}'


b1 = Book("The Catcher in the Rye", "J.D. Salinger", 234, 1951)
b2 = Book("To Kill a Mockingbird", "Harper Lee", 281, 1960)
b3 = Book("1984", "George Orwell", 328, 1949)
b4 = Book("The Great Gatsby", "F. Scott Fitzgerald", 180, 1925)
b5 = Book("One Hundred Years of Solitude", "Gabriel García Márquez", 417, 1967)
b6 = Book("Brave New World", "Aldous Huxley", 311, 1932)
b7 = Book("The Lord of the Rings", "J.R.R. Tolkien", 1178, 1954)
b8 = Book("Pride and Prejudice", "Jane Austen", 279, 1813)
b9 = Book("The Hobbit", "J.R.R. Tolkien", 310, 1937)
b10 = Book("The Harry Potter series", "J.K. Rowling", 4100, 1997)
b11 = Book("The Chronicles of Narnia", "C.S. Lewis", 767, 1950)
b12 = Book("The Shining", "Stephen King", 447, 1977)
b13 = Book("The Da Vinci Code", "Dan Brown", 454, 2003)
b14 = Book("The Alchemist", "Paulo Coelho", 197, 1988)
b15 = Book("The Hunger Games", "Suzanne Collins", 374, 2008)
books = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15]
lib = Library('My_Library')
for book in books:
    lib.add_book(book)
print('\nStart of iteration:')
for book in lib:
    print(book)
print('End of iteration.\n')
print('\nIn alphabet order: ')
for book in lib.sorted_by_alphabet():
    print(book)
print('End of alphabet order.\n')
lib.search_by_author('Tolkien')
lib.search_by_title('hunger games')
lib.pop_book('The Great Gatsby')
print(lib)
