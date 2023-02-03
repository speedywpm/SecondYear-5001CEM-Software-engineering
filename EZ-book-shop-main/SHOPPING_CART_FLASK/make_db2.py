from flask import Flask
from flask import render_template
import sqlite3 

con = sqlite3.connect('products.db')

con.execute('CREATE TABLE products(id INT unsigned, name VARCHAR(255), code VARCHAR(255) PRIMARY KEY, image TEXT, price DOUBLE, description VARCHAR(4000), date VARCHAR(50), tradeprice DOUBLE, quantity INT, author VARCHAR(50))')

#con.close()  
#con = sqlite3.connect('products.db')

#con.execute('INSERT INTO products(id, name, code, image, price, description, date, tradeprice, quantity, author) VALUES (1, "The Attic on Queen Street", "9780451475251", "product-images/theatticonqueenstreet.jfif", 27.00, "Return to the house on Tradd Street one last time in this hauntingly spectacular finale to the bestselling series featuring psychic medium Melanie Trenholm. After the devastating events of the past few months, the last thing Melanie Trenholm wants is to think about the future.  Why, when her husband, Jack, has asked for a separation—a separation that might have been her fault?  Nevertheless, with twin toddlers, a stepdaughter leaving for college soon, a real estate career to resume and a historic home that is still being restored, Melanie doesn’t have much time to wonder where it all went wrong—but that doesn’t stop her from trying to win her husband back.", "2021-11-02", 27.00, 4, Karen White);')

con.commit()
con.close()  







