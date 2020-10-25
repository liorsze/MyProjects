import sqlite3
import sys
import os


def main(args):
    databaseexisted = os.path.isfile('moncafe.db')
    if databaseexisted:  # delete database
        os.remove('moncafe.db')
    dbcon = sqlite3.connect('moncafe.db')
    with dbcon:
        cursor = dbcon.cursor()
        cursor.execute(
            "CREATE TABLE Coffee_stands (id  INTEGER  PRIMARY KEY,location   TEXT    NOT NULL,number_of_employees  INTEGER )")
        cursor.execute(
            "CREATE TABLE Employees(id INTEGER PRIMARY KEY, name TEXT NOT NULL, salary REAL NOT NULL,coffee_stand INTEGER REFERENCES Coffee_stands(id))")
        cursor.execute("CREATE TABLE Suppliers (id  INTEGER  PRIMARY KEY,name TEXT NOT NULL, contact_information TEXT)")
        cursor.execute(
            "CREATE TABLE Products ( id  INTEGER  PRIMARY KEY,description TEXT NOT NULL, price REAL NOT NULL,quantity INTEGER NOT NULL )")
        cursor.execute("CREATE TABLE Activities (product_id  INTEGER,quantity INTEGER NOT NULL, activator_id INTEGER NOT NULL,date  DATE  NOT NULL, FOREIGN KEY(product_id) REFERENCES Products(id))")

        input = args[1]
        with open(input) as file:
            for line in file:
                splitter = line.split(', ')
                if splitter[0] == 'C':  # coffee stand
                    cursor.execute("INSERT INTO Coffee_stands VALUES (?,?,?)",(splitter[1], splitter[2], splitter[3]))
                elif splitter[0] == 'E':  # employee
                    cursor.execute("INSERT INTO Employees VALUES (?,?,?,?)",(splitter[1], splitter[2], splitter[3], splitter[4]))
                elif splitter[0] == 'S':  # supplier
                    cursor.execute("INSERT INTO Suppliers VALUES (?,?,?)",(splitter[1], splitter[2], splitter[3].rstrip()))
                elif splitter[0] == 'P': # products
                    cursor.execute("INSERT INTO Products VALUES (?,?,?,?)",(splitter[1], splitter[2], splitter[3] , 0))

    #do we need to print here
    #printDataBase()

    dbcon.commit()
    dbcon.close()
#TODO close dbconn

if __name__ == '__main__':
    main(sys.argv)