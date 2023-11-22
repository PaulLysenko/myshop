from datetime import datetime


class Book:
    """
    represents a book in the library

    attributes:
    book_name (str): is a book name
    author (str): is an author of a given book
    pages (int): provides the number of pages in a certain book
    year (int): provides the information about a year a book was published in
    """
    book_name = None
    author = None
    pages = None
    year = None

    def __init__(self, book, author, pages, year):
        self.book_name = book
        self.author = author
        self.pages = pages
        self.year = year

    def __repr__(self):
        return f'{self.book_name}'


class Library:
    """
    is a library itself. collects book

    attributes:
    name (str): the name of the library
    _instance (None): Singleton instance of the library

    instances:
    books (list): list that collects the books
    date: the date the library object is created
    idx: iteration index for the books
    """
    lib_name = None
    date = None
    _instance = None

    def __init__(self, lib_name):
        self.books = []
        self.lib_name = lib_name
        self.date = datetime.now()

    def __new__(cls, lib_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_book(self, book_instance):
        if isinstance(book_instance, Book):
            self.books.append(book_instance)
        return f'The "{book_instance}" has been successfully added to your library!'

    def pop_book(self, book_title):
        for book in self.books:
            if book_title == book.book_name:
                self.books.remove(book)
                return f'"{book_title}" has been successfully removed from your library!'
        return f'It seems that you don\'t have "{book_title}" in your library! Perhaps try again?'

    def search(self, book_data):
        book_lst = []
        for book in self.books:
            book_keys = book.author.lower().split(' ') + book.book_name.lower().split(' ')
            if book_data.lower() in book_keys:
                book_lst.append(book)
        return book_lst

    def iter_books(self, elements=10):
        for i in range(0, len(self.books), elements):
            yield self.books[i:i + elements]

    def __repr__(self):
        return f'Hi, I\'m a {self.lib_name}! Currently I have {len(self.books)} books.'

    def sorted_gen(self):
        for book in sorted(self.books, key=lambda book: book.book_name.lower()):
            yield book


lib = Library('library')

book1 = Book('Kobzar', 'Taras Shevchenko', 350, 1840)
book2 = Book('Beyond Good and Evil', 'Friedrich Nietzsche', 240, 1886)
book3 = Book('1984', 'George Orwell', 330, 1949)
book4 = Book('Prosper\'s Demon', 'K.J. Parker', 250, 2020)

print(lib.add_book(book1))
print(lib.add_book(book2))
print(lib.add_book(book3))
print(lib.add_book(book4))

gen = lib.sorted_gen()
for book_name in gen:
    print(book_name)

next_books = lib.iter_books()
for book_ in next_books:
    print(book_)

print(lib.__repr__())
print(lib.search('evil'))
print(lib.search('george'))
print(lib.pop_book('Beyond Good and Evil'))
