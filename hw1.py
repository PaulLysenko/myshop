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
    name = 'library'
    _instance = None

    def __init__(self):
        self.books = []
        self.date = datetime.now()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_book(self, book_instance):
        self.books.append(book_instance)
        return f'The "{book_instance}" has been successfully added to your library!'

    def pop_book(self, book_instance):
        for book in self.books:
            if book_instance == book.book_name:
                self.books.remove(book)
                return f'The "{book_instance}" has been successfully removed from your library!'
        return f'It seems that you don\'t have "{book_instance}" in your library! Perhaps try again?'

    def search_by_name(self, book_instance):
        book_lst = []
        for book in self.books:
            if book_instance in book.book_name:
                book_lst.append(book)
        if book_lst:
            return f'Were you looking for "{str(book_lst)[1:-1]}"?'
        else:
            return f'There are no books with "{book_instance}" name!'

    def search_by_author(self, author_instance):
        author_lst = []
        for book in self.books:
            if author_instance in book.author:
                author_lst.append(book)
        if author_lst:
            return f'Here is the list of book written by {author_instance}: "{str(author_lst)[1:-1]}".'
        else:
            return f'There are no authors with "{author_instance}" name!'

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self.books):
            if self.idx < 10:
                book = self.books[self.idx]
                self.idx += 1
                return book
        raise StopIteration

    def __repr__(self):
        return f'Hi, I\'m a {self.name}! Currently I have {len(self.books)} books.'

    @staticmethod
    def book_name_key(book):
        return book.book_name

    def sorted_gen(self):
        for book in sorted(self.books, key=self.book_name_key):
            yield book.book_name


lib = Library()

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

iterator = iter(lib)
print(next(iterator))

print(lib.__repr__())
print(lib.search_by_name('Beyond Good'))
print(lib.search_by_author('George'))
print(lib.pop_book('Beyond Good and Evil'))
