#
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
# Створіть бібліотеку, створіть декілька книжок. Додайте книжки в бібліотеку.
# Виконайте пошук по назві та по автору. Видаліть книжку з бібліотеки.
# Проітеруйтесь по бібліотеці, проітеруйтесь по бібліотеці в алфавітному порядку.
#
# * Додайте перевірку вхідних даних для створення книжки за допомогою Pydantic.
# Додайте перевірку вхідних даних для створення бібліотеки за допомогою Pydantic.
# https://docs.pydantic.dev/latest/










import datetime


class Book:
    def __init__(self, title, autor, quantity_pages, year_of_publ):
        self.title = title
        self.autor = autor
        self.quantity_pages = quantity_pages
        self.year_of_publ = year_of_publ

    def __repr__(self):
        return f'книжка  {self.title}  написана {self.autor} у {self.year_of_publ} році,має {self.quantity_pages} сторінок'

    def __str__(self):
        return self.__repr__()
class Library():
    _instance = None

    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super(Library, cls).__new__(cls)
            cls._instance.name = name
            cls._instance.books = []
            cls._instance.creation_date = datetime.datetime.now()
        return cls._instance

    def add_book(self, book):
        try:
            if isinstance(book,Book):
                self.books.append(book)
            else:
                raise TypeError('Обʼєкт не є екземпляром классу Book')
        except TypeError as e:
            print(f'помилка при додаванні книги {e}')

    def pop_book(self, title):
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                break

    def search_title(self,title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_autor(self,autor):
        return [b for b in self.books if autor.lower() in b.autor.lower()]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self.books):
            result = self.books[self._index: self._index + 10]
            self._index += 10
            return result
        raise StopIteration

    def books_sorted_title(self):
        for book in sorted(self.books, key = lambda x: x.title):
            yield book


    def __repr__(self):
        return f'Бібіліотека {self.name} має {len(self.books)} книжок'

    def __str__(self):
        return self.__repr__()


library = Library('Залиманська бібліотека')

book1 = Book('Чиста архітектура', 'Мартін Р.', '352', '2018')
book2 = Book('Вивчаєм Python', 'Лутц М.','832','2023')
book3 = Book('Python для програмування криптовалют ', 'Сонг Д.','370','2021')
book4 = Book('Основи ШІ', 'Постолит А.','448','2021')
book5 = Book('Чистий Python', 'Бейдер Д.','288','2018')


library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)
library.add_book(book5)

print(library.search_title('Чиста архітектура'))
print(library.search_autor('Лутц М'))

library.pop_book('Чистий Python')

for book in library:
    print(book)

for book in library.books_sorted_title():
    print(book)

