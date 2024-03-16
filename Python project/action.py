import sqlite3
import sys
import os
from printdb  import printdb

def main(args):
    dbcon = sqlite3.connect('moncafe.db')
    with dbcon:
        cursor = dbcon.cursor()
        input = args[1]
        with open(input) as file:
            for line in file:
                splitter = line.split(', ')
                if float(splitter[1]) > 0: #supplier adds product
                    cursor.execute("INSERT INTO Activities VALUES (?,?,?,?)",(splitter[0], splitter[1], splitter[2], splitter[3]))
                    productId = int(splitter[0])
                    quant = int(splitter[1])
                    cursor.execute("UPDATE Products SET quantity = (?) where id =(?)", (quant, productId))
                else: #sales
                    prodId = int(splitter[0])
                    reqQuantity = int(splitter[1])
                    cursor.execute("SELECT quantity FROM Products WHERE id=?",[prodId])
                    fetched = cursor.fetchone()
                    tmp=str(fetched)
                    currentQuantity = tmp[1:-2]

                    if float(currentQuantity)>=abs(reqQuantity):
                        cursor.execute("INSERT INTO Activities VALUES (?,?,?,?)",(splitter[0], splitter[1], splitter[2], splitter[3]))
                        leftAfterSale = float(currentQuantity)+reqQuantity
                        cursor.execute("UPDATE Products SET quantity = (?) where id =(?)", (leftAfterSale, prodId))

    printdb()
    dbcon.commit()
    dbcon.close()



if __name__ == '__main__':
    main(sys.argv)