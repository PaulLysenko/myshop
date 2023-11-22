# Напишіть функціонал “Бібліотеки” яка зберікає книжки.
#
# Обʼєкт класу “Бібліотека”: Атрибути: назва дата створення (записується автоматично при створенні обʼєкта) Може бути
# створено тільки один бʼєкт класу “Бібліотека” (реалізуйте Singleton). Обʼєкт класу “Бібліотека” зберігає в собі
# тільки обʼєкти класу “Книжка” Обʼєкт класу “Бібліотека” має метод для додавання книжки (add_book) Обʼєкт класу
# “Бібліотека” має метод для видалення книжки по точному співпадінню назви (pop_book) Обʼєкт класу “Бібліотека” має
# метод для пошуку книжки/книжок по назві (search_by_name) включаючи часткове співпадіння Обʼєкт класу “Бібліотека”
# має метод для пошуку книжки/книжок по імені автора (search_by_author) включаючи часткове співпадіння Обʼєкт класу
# “Бібліотека” повинен ітеруватись: на кожній ітерації повинні вдаватись 10 книжок додайте окремий метод,
# який повертає ітератор книжок в алфавітному порядку по назві (реалізуйте за допомогою генератора) Обʼєкт класу
# “Бібліотеки” повинен репрезентуватися наступним чином - кількість книжок в бібліотеці Обʼєкт класу “Книжка”:
# Атрибути: назва автор кількість сторінок рік видання Створіть бібліотеку, створіть декілька книжок. Додайте книжки
# в бібліотеку. Виконайте пошук по назві та по автору. Видаліть книжку з бібліотеки. Проітеруйтесь по бібліотеці,
# проітеруйтесь по бібліотеці в алфавітному порядку.
#
# * Додайте перевірку вхідних даних для створення книжки за допомогою Pydantic. Додайте перевірку вхідних даних для
# створення бібліотеки за допомогою Pydantic. https://docs.pydantic.dev/latest/


from datetime import datetime


class Book:
    def __init__(self, title, author, pages, year):
        self.title = title
        self.author = author
        self.pages = pages
        self.year = year

    def __repr__(self):
        return f"Book('{self.title}',written '{self.author}',pages {self.pages} ,a year {self.year})"


class Library:
    _instance = None

    def __new__(cls, name):
        if cls._instance is None:
            cls._instance = super(Library, cls).__new__(cls)
            cls._instance.name = name
            cls._instance.creation_date = datetime.now()
            cls._instance.books = []
        return cls._instance

    def add_book(self, book):
        self.books.append(book)

    def pop_book(self, title):
        self.books = [b for b in self.books if b.title != title]

    def search_by_name(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def iterate_books(self):
        for i in range(0, len(self.books), 10):
            yield self.books[i:i + 10]

    def alphabetical_iterator(self):
        for book in sorted(self.books, key=lambda x: x.title):
            yield book

    def __repr__(self):
        return f"Library('{self.name}', {len(self.books)} books, Created on {self.creation_date})"


if __name__ == "__main__":
    book1 = Book("The Green Mile", "Stephen King", 384, 1996)
    book2 = Book("Der Funke Leben", "Erich Maria Remarque", 480, 1952)
    book3 = Book("Alchemist", "Paulo Coelho", 288, 1988)

    library = Library("My Library")

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    print("Search by Name:")
    print(library.search_by_name("Mile"))

    print("\nSearch by Author:")
    print(library.search_by_author("Stephen King"))

    library.pop_book("Der Funke Leben")

    print("\nIterating through the Library:")
    for books in library.iterate_books():
        print(books)

    print("\nIterating through the Library in Alphabetical Order:")
    for book in library.alphabetical_iterator():
        print(book)

    print("\nLibrary Information:")
    print(library)
