from models import Base, session, Book, engine
import csv
import datetime
import time


def menu():
    '''
    Main menu for the application
    Returns menu choice from user
    '''
    while True:
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

def sub_menu():
    '''
    Sub menu for edit/delete entries
    '''
    while True:
        menu_choice = input('''
                            \n1) Edit entry
                            \r2) Delete entry
                            \r3) Return to main menu
                            \n What would you like to do? ''')
        if menu_choice not in ['1', '2', '3']:
            input('Please choose one of the menu items above. '
                'A number between 1-3.\nPress enter.')
        else:
            return menu_choice
        

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

def clean_id(id_str, options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
              \n****** ID ERROR ******
              \rThe id should be a number.
              \rPress enter to try again.
              \r*************************''')
        return
    else:
        if book_id in options:
            return book_id
        else:
            input(f'''
              \n****** ID ERROR ******
              \rOptions: {options}
              \rPress enter to try again.
              \r*************************''')
            return


def edit_check(column_name, current_value):
    print(f'\n**** EDIT {column_name} ****')
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to? ')
            if column_name == 'Date':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to? ')
                    

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
            book_in_db = session.query(Book).filter(Book.title==row[0]).one_or_none()
            if book_in_db == None:
                new_book = Book(title=row[0], author=row[1], published_date=date, price=price)
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
            print('\nAdd a New Book')
            title = input('Book title: ')
            author = input('Author: ')
            date_error = True
            while date_error:
                published = input('Published (Example: January 13, 2003): ')
                published = clean_date(published)
                if type(published) == datetime.date:
                    date_error = False
            price_error = True
            while price_error:
                price = input('Price (Example: 10.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Book(title=title, author=author, published_date=published, price=price)
            session.add(new_book)
            session.commit()
            print('Book added!')
            time.sleep(1.5)
        elif choice == '2':
            for book in session.query(Book):
                print(f'\n{book.id} | {book.title} | {book.author}')
            input('\nPress enter to return to the main menu.')
        elif choice == '3':
            id_options = []
            for book in session.query(Book):
                id_options.append(book.id)
            id_error = True
            while id_error:
                book_id = input(f'''\nOptions: {id_options}
                                \rWhat is the book's id? ''')
                book_id = clean_id(book_id, id_options)
                if type(book_id) == int:
                    id_error = False
            the_book = session.query(Book).filter(Book.id == book_id).first()
            print(f'''
                  \n{the_book.title} by {the_book.author}
                  \rPublished: {the_book.published_date}
                  \rCurrent Price: ${the_book.price/100}
                  ''')
            menu_choice = sub_menu()
            if menu_choice == '1':
                #edit
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.published_date = edit_check('Published Date', the_book.published_date)
                the_book.price = edit_check('Price', the_book.price)
                # print(session.dirty)
                session.commit()
                print('Book updated!')
                time.sleep(1.5)
            elif menu_choice == '2':
                #delete
                session.delete(the_book)
                print('Book deleted!')
                time.sleep(1.5)
        elif choice == '4':
            pass
        else:
            print('GOODBYE')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()
