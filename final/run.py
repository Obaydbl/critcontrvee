from cs50 import SQL
db = SQL("sqlite:///z.db")

db.execute('insert into address_book (indx, name, address, city, zipcode, country) Values(?, ?, ?, ?, ?, ?);', 2, 'Lyndhurst Research Facility', '18 Greenwood Drive', 'Lyndhurst', '84330', 'Norton')
db.execute('insert into address_book (indx, name, address, city, zipcode, country) Values(?, ?, ?, ?, ?, ?);', 3, 'Carinasford DNA Analysis Unit', '112 Riverbend Parkway', 'Carinasford', '78219', 'Norton')
