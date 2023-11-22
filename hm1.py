import datetime

class Book:
    def __init__(self, book_name, author_book, page_book, year_book):
        self.Book_Name = book_name
        self.Author_Book = author_book
        self.Page_Book = page_book
        self.Year_Book = year_book

    def __repr__(self):
        return f"Book(Book_Name='{self.Book_Name}', Author_Book='{self.Author_Book}', Page_Book='{self.Page_Book}', Year_Book='{self.Year_Book}')"

class Library:
    _instance = None

    def __new__(cls, name):
        if not cls._instance:
            cls._instance = super(Library, cls).__new__(cls)
            cls._instance.name = name
            cls._instance.books = []
            cls._instance.creation_date = datetime.datetime.now()
        return cls._instance

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)
        else:
            print(f"The book '{book.Book_Name}' is already in the library.")

    def pop_book(self, title):
        try:
            book_to_remove = next(book for book in self.books if book.Book_Name == title)
            self.books.remove(book_to_remove)
            print(f"Book '{title}' removed from the library.")
        except StopIteration:
            print(f"Book '{title}' not found in the library.")

    def get_books(self):
        return self.books[:10]

    def search_title(self, title):
        return [b for b in self.books if title.lower() in b.Book_Name.lower()]

    def search_author(self, author):
        return [b for b in self.books if author.lower() in b.Author_Book.lower()]

    def alphabetical_iterator(self):
        sorted_books = sorted(self.books, key=lambda book: book.Book_Name.lower())
        for book in sorted_books:
            yield book

    def remove_book(self, title):
        for book in self.books:
            if book.Book_Name == title:
                self.books.remove(book)
                print(f"Book '{title}' removed from the library.")
                break
        else:
            print(f"Book '{title}' not found in the library.")


book1 = Book("Майстер і Маргарита", "Михайло Булгаков", 432, 1966)
book2 = Book("1984", "Джордж Оруелл", 328, 1949)
book3 = Book("Гаррі Поттер і філософський камінь", "Дж. К. Роулінг", 336, 1997)

library_instance = Library("Library")
library_instance.add_book(book1)
library_instance.add_book(book2)
library_instance.add_book(book3)

print(library_instance.search_author('Михайло Булгаков'))

for book in library_instance.alphabetical_iterator():
    print(book)