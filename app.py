from models import Base, session, Book, engine
import csv
import time


def menu():
    '''
    Main menu for the application
    Returns menu choice from user
    '''
    while True:  # while loop - only end when the choice is returned and return will always cancel and stop a loop
        print('''
          \nPROGRAMMING BOOKS
          \r1) Add book
          \r2) View all books
          \r3) Search for a book
          \r4) Book Analysis
          \r5) Exit
          ''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            input('Please choose one of the menu items above. '
                  'A number between 1-5.\nPress enter.')


# add function
# edit function
# delete function
# search function


def clean_date(date):
    '''
    Cleans the date string
    '''
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    split = date.split(' ')
    try:
        month = int(months.index(split[0]) + 1)
        day = int(split[1].split(',')[0])
        year = int(split[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''\n******** Date Error ********
              \rThe date format should include a valid Month Day, Year from the past.
              \rEx: January 13, 2003.
              \rPress enter to try again.
              \r*******************************''')
        return
    else:
        return return_date


def clean_price(price):
    '''
    Cleans the price string
    '''
    try:
        price_float = float(price)
    except ValueError:
        input('''\n ******** Price Error ********
              \rThe price should be a number without a currency symbol.
              \rExample: 10.99
              \rPress enter to try again.
              \r***********************************
              ''')
        return
    else:
        price_cents = price_float * 100
        return int(price_cents)


def add_csv():
    '''
    Add books from csv to database 
    if they aren't in the DB already
    '''
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            date = clean_date(row[2])
            price = clean_price(row[3])
            # either return the book or return none
            book_in_db = session.query(Book).filter(
                Book.title == row[0]).one_or_none()
            if book_in_db == None:  # it only gets created if it is not in the database
                new_book = Book(
                    title=row[0], author=row[1], published_date=date, price=price)
                session.add(new_book)
    session.commit()


def app():
    '''
    Main application function
    '''
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # add book
            title = input('Title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                date = input('Published Date (Ex: October 25, 2017): ')
                date = clean_date(date)
                if type(date) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Ex: 25.64): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author,
                            published_date=date, price=price)
            session.add(new_book)
            session.commit()
            print('Book added!')
            time.sleep(1.5)
        elif choice == '2':
            # view books
            for book in session.query(Book):
                print(f'{book.id} | {book.title} | {book.author}')
            input('\nPress enter to return to the main menu.')
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        else:
            print('GOODBYE')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
