import sqlite3
import sys

def printdb():
    dbcon = sqlite3.connect('moncafe.db')
    with dbcon:
        cursor = dbcon.cursor()

        # 1 print
        cursor.execute("SELECT * FROM Activities ORDER BY Activities.date ASC")
        activitiesList = cursor.fetchall()
        print('Activities')
        for act in activitiesList:
            print(str(act))

        cursor.execute("SELECT * FROM Coffee_stands ORDER BY Coffee_stands.id ASC")
        coffeStandList = cursor.fetchall()
        print('Coffee stands')
        for stand in coffeStandList:
            print(str(stand))

        cursor.execute("SELECT * FROM Employees ORDER BY Employees.id ASC")
        employeeList = cursor.fetchall()
        print('Employees')
        for empl in employeeList:
            print(str(empl))

        cursor.execute("SELECT * FROM Products ORDER BY Products.id ASC")
        productsList = cursor.fetchall()
        print('Products')
        for prod in productsList:
            print(str(prod))

        cursor.execute("SELECT * FROM Suppliers ORDER BY Suppliers.id ASC")
        supplierList = cursor.fetchall()
        print('Suppliers')
        for supplier in supplierList:
            print(str(supplier))
        print('')

        # 2 print
        print('Employees report')
        cursor.execute("SELECT * FROM Employees ORDER BY Employees.name ASC")
        emploees = cursor.fetchall()
        for line in emploees:
            total=0
            employeID=line[0]
            employeName = line[1]
            employeeSalary=line[2]
            employeeStand=line[3]
            cursor.execute("SELECT location FROM Coffee_stands WHERE Coffee_stands.id=?",[employeeStand])
            coffeStand=cursor.fetchone()
            tmp = str(coffeStand)
            coffeStand = tmp[2:-3]

            cursor.execute("SELECT * FROM Activities")
            activityList=cursor.fetchall()
            for activ in activityList:
                if activ[2]==employeID:
                    prodID=activ[0]
                    quantitySale=activ[1]
                    cursor.execute("SELECT price FROM Products WHERE id=?",[prodID])
                    price=cursor.fetchone()
                    tmp = str(price)
                    price=tmp[1:-2]

                    total=total+float(price)*float(quantitySale)*-1
            print(employeName,employeeSalary,coffeStand,total)



        cursor.execute(
            "CREATE TEMPORARY TABLE Report(id INTEGER, name TEXT NOT NULL, salary REAL NOT NULL, location TEXT NOT NULL,income REAL DEFAULT 0)")  # temp table and local
        cursor.execute(
            "INSERT INTO Report(id,name,salary,location) SELECT Employees.id, Employees.name, Employees.salary, Coffee_stands.location FROM Employees LEFT JOIN Coffee_stands ON Employees.coffee_stand=Coffee_stands.id")

        cursor.execute(
            "CREATE TEMPORARY TABLE temp (id INTEGER, quantity INTEGER,product_id INTEGER, price REAL,total REAL DEFAULT 0)")
        cursor.execute(
            "INSERT INTO temp (id, quantity,product_id,price)SELECT Activities.activator_id, Activities.quantity, Activities.product_id, Products.price FROM Activities LEFT JOIN Products ON Activities.product_id=Products.id INNER JOIN Employees ON Activities.activator_id=Employees.id")
        cursor.execute("UPDATE temp SET total=(SELECT quantity*price*-1)")

        cursor.execute("UPDATE Report SET income=(SELECT SUM(total) FROM temp WHERE Report.id=temp.id)")
        cursor.execute("UPDATE Report SET income=0 WHERE income IS NULL")

        cursor.execute("SELECT Report.name , Report.salary , Report.location, Report.income FROM Report")
        replist = cursor.fetchall()
        #for row in replist:
            #if row[3]==0.0:
                #print(row[0],row[1],row[2],0)
            #else:
                #print(row[0], row[1], row[2], row[3])

        # 3 print
        cursor.execute("SELECT COUNT(product_id) FROM Activities")
        fetched = cursor.fetchone()
        tmp = str(fetched)
        activitiesSize = tmp[1:-2]
        if int(activitiesSize) > 0:
            print("")
            print('Activities')
            cursor.execute(
                "CREATE TEMPORARY TABLE print3(date DATE, desc TEXT, quantity INTEGER, nameSeller TEXT, nameSupp TEXT)")
            cursor.execute(
                "INSERT INTO print3(date,desc,quantity,nameSeller,nameSupp)SELECT Activities.date, Products.description,Activities.quantity,Employees.name, Suppliers.name FROM Activities LEFT JOIN Products ON Activities.product_id = Products.id LEFT JOIN Employees ON Employees.id=Activities.activator_id LEFT JOIN Suppliers ON Suppliers.id=Activities.activator_id")
            cursor.execute("SELECT * FROM print3 ORDER BY date ASC")
            pint3 = cursor.fetchall()
            for p in pint3:
                print(str(p))

    dbcon.commit()
    dbcon.close()

def main(args):
    printdb()

if __name__ == '__main__':
    main(sys.argv)