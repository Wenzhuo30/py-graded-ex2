## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.

from admin import (
    load_library,
    save_library,
    find_book,
   
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):
    target_category = category.strip().lower()
    matching_books = []
    for book_id, book_info in books.items():
        if book_info['category'].lower() == target_category:
            matching_books.append(book_id)
    return matching_books

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    target = search_text.strip().lower()
    matching_books = []
    for book_id, book_info in books.items():
        if target in book_info['title'].lower():
            matching_books.append(book_id)
    return matching_books
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    book_id = find_book(books, search_text)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    
    if not borrower.strip():
        return "EMPTY_NAME"
    
    if not books[book_id]['available']:
        return "NOT_AVAILABLE"
    
    books[book_id]['available'] = False
    loans.append({
        "book_id": book_id,
        "borrower": borrower
    })
    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    book_id = find_book(books, book_title)
    if book_id is None:
        return "BOOK_NOT_FOUND"
    
    if not borrower.strip():
        return "EMPTY_NAME"
    
    matching_loan = None
    for loan in loans:
        if loan['book_id'] == book_id and loan['borrower'] == borrower:
            matching_loan = loan
            break
    
    if matching_loan is None:
        return "NOT_ON_LOAN"
    
    loans.remove(matching_loan)
    books[book_id]['available'] = True
    return "OK"

    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    try:
        library_data = load_library('library_data.json')
    except FileNotFoundError:
        library_data = {
            "library": {"name": "", "branch": "", "year": ""},
            "categories": [],
            "books": {},
            "loans": []
        }
    
    books = library_data['books']
    loans = library_data['loans']
    
    while True:
        print("\nLIBRARY USER SYSTEM")
        print("=" * 40)
        print("1. Search by Title")
        print("2. Search by Category")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")
        
        choice = input("Please select an option: ").strip()
        
        if choice == '1':
            title = input("Enter title keyword: ")
            results = search_by_title(books, title)
            if results:
                print("\nMatching Books:")
                for bid in results:
                    book = books[bid]
                    status = "Available" if book['available'] else "On Loan"
                    print(f"  {bid}: {book['title']} by {book['author']} - {status}")
            else:
                print("\nNo books found matching that title.")
        
        elif choice == '2':
            category = input("Enter category: ")
            results = books_in_category(books, category)
            if results:
                print("\nBooks in Category:")
                for bid in results:
                    book = books[bid]
                    status = "Available" if book['available'] else "On Loan"
                    print(f"  {bid}: {book['title']} - {status}")
            else:
                print("\nNo books found in that category.")
        
        elif choice == '3':
            book_id = input("Enter book ID: ")
            borrower_name = input("Enter your full name: ")
            result = borrow_book(books, loans, book_id, borrower_name)
            if result == "OK":
                print("\nBook borrowed successfully!")
            elif result == "BOOK_NOT_FOUND":
                print("\nError: Book not found. Please check the ID.")
            elif result == "EMPTY_NAME":
                print("\nError: Borrower name cannot be empty.")
            elif result == "NOT_AVAILABLE":
                print("\nError: Book is currently not available for borrowing.")
        
        elif choice == '4':
            book_id = input("Enter book ID: ")
            borrower_name = input("Enter your full name: ")
            result = return_book(books, loans, book_id, borrower_name)
            if result == "OK":
                print("\nBook returned successfully!")
            elif result == "BOOK_NOT_FOUND":
                print("\nError: Book not found. Please check the ID.")
            elif result == "EMPTY_NAME":
                print("\nError: Borrower name cannot be empty.")
            elif result == "NOT_ON_LOAN":
                print("\nError: This book is not on loan to you.")
        
        elif choice == '5':
            save_library(library_data, 'library_data.json')
            print("\nLibrary data saved. Goodbye!")
            break
        
        else:
            print("\nInvalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

