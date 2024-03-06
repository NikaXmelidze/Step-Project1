import json
from faker import Faker
import os

fake = Faker()


class Book:
    def __init__(self, title, author, publication_year):
        # Initialize a Book object with title, author, and publication year.
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def __str__(self):
        # Return a string representation of the Book object.
        return f"Title: {self.title}, Author: {self.author}, Publication Year: {self.publication_year}"


class BookManager:
    def __init__(self):
        # Initialize a BookManager object.
        self.books = []

    @staticmethod
    def is_json_file_empty(filename):
        # Check if the JSON file is empty.
        return not os.path.exists(filename) or os.path.getsize(filename) == 0

    @staticmethod
    def custom_encoder(obj):
        # Custom JSON encoder for Book objects.
        if isinstance(obj, Book):
            return {
                "title": obj.title,
                "author": obj.author,
                "publication_year": obj.publication_year,
            }
        return obj

    @staticmethod
    def custom_decoder(json_data):
        # Custom JSON decoder for Book objects.
        return Book(json_data['title'], json_data['author'], json_data['publication_year'])

    @staticmethod
    def write_data(lst):
        # Write data to a JSON file.
        with open("book_data.json", "w") as json_file:
            json.dump(lst, json_file, default=BookManager.custom_encoder, indent=4)

    @staticmethod
    def read_data():
        # Read data from a JSON file.
        with open("book_data.json", "r") as read_json:
            python_data = json.load(read_json, object_hook=BookManager.custom_decoder)
            return python_data

    def generate_fake_books(self, num_books):
        # Generate fake books using Faker and write them to the JSON file.
        self.books = []
        for _ in range(num_books):
            title = fake.catch_phrase()
            author = fake.name()
            publication_year = fake.year()
            self.books.append(Book(title, author, publication_year))
        self.write_data(self.books)

    def add_book(self, title, author, publication_year):
        # Add a new book to the list and write it to the JSON file.
        self.books = self.read_data()
        self.books.append(Book(title, author.capitalize(), publication_year))
        self.write_data(self.books)
        print("Book added successfully!")

    def display_books(self):
        # Display all the books
        self.books = self.read_data()
        if self.books:
            print("Added books:")
            for book in self.books:
                print(book)

    def search_book_by_title(self, title):
        # Search for a book by title and display the matching books.
        self.books = self.read_data()
        found_books = [book for book in self.books if book.title.lower() == title.lower()]

        if found_books:
            print("Matching books found:")
            for book in found_books:
                print(book)
        else:
            print("No matching books found.")


def main():
    # Main function to run the program.
    manager = BookManager()

    if manager.is_json_file_empty("book_data.json"):
        manager.generate_fake_books(10)

    while True:
        print("\nMenu:")
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Search Book by Title")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the book: ")

            while True:
                try:
                    author = input("Enter the author of the book: ").capitalize()
                    if not author.replace(" ", "").isalpha():
                        raise ValueError("Invalid author. Author must contain only alphabets and spaces.")
                    break
                except ValueError as e:
                    print(str(e))

            while True:
                try:
                    publication_year = int(input("Enter the publication year of the book: "))
                    if not (publication_year <= 2024):
                        raise ValueError("Invalid publication year. Publication year must be less than 2024.")
                    break
                except ValueError as e:
                    print(str(e))

            books = manager.read_data()
            found_book = [book for book in books
                          if book.title.lower() == title.lower() and book.author.lower() == author.lower()]

            if found_book:
                print(f"There is already such a book: {found_book[0]}")
            else:
                manager.add_book(title, author, publication_year)


        elif choice == "2":
            manager.display_books()

        elif choice == "3":
            title = input("Enter the title to search: ")
            manager.search_book_by_title(title)

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == '__main__':
    main()
