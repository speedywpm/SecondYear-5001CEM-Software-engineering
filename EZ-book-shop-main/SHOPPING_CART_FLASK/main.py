from flask import Flask
import sqlite3 
from flask import flash, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
from flask import abort
from flask import make_response
import sqlalchemy
from hashlib import md5
#all of the above are modules used for the code to work
#some code lines have no explanation to them as they are either duplicate or are very primitive enough to understand
#to reference the code 5001CEM module week 1,2,3,4,5,6 lab tasks were used, part of the shopping cart and product display was the main template of this work, references in some parts might be very short, detailed explanation in the project report references section
app = Flask(__name__)
app.secret_key = "secret key" #used for secure checkout
sid = 'YxfIMEp1a2Vib3g=' #used for secure checkout
pid = 'payment1' #used for secure checkout
secret = 'QSDZ1zhECGazdOC9_ygF3pUUOfIA' #used for secure checkout

@app.route('/register', methods=['GET', 'POST']) #used to create url directories, methods methods used for the html forms to make a connection between them

def register():
    if request.method == 'POST':
        return do_the_registration(request.form['uname'], request.form['pwd']) #grabbing username and password from the register form
    else:
        return show_the_registration_form();
    
def do_the_registration(u,p):
    con = sqlite3.connect('registered_users.db') #connects to registered_users database
    try:
        con.execute('CREATE TABLE users (name TEXT, pwd INT)') #if table users does not exists creates a new one with name and pwd attributes
        print ('Table created successfully');
    except:
        pass #if table users exists, skips the "try:" part
    
    con.close()  #closes connection of the connected database
    
    con = sqlite3.connect('registered_users.db')
    con.execute("INSERT INTO users values(?,?);", (u, p)) #inserting username and password into the database whilst values are taken from the register() function
    con.commit()
    con.close()  

    return show_the_login_form()

def show_the_registration_form():
    return render_template('register.html',page=url_for('register')) #page=url_for is used to redirect to exact function

@app.route('/', methods=['GET', 'POST']) #route only is with a slash as this is the main page - login
def login():
    if request.method == 'POST':
        return do_the_login(request.form['uname'], request.form['pwd'])
    else:
        return show_the_login_form()
        
def show_the_login_form():
    return render_template('login.html',page=url_for('login'))

def do_the_login(u,p):
    con = sqlite3.connect('registered_users.db')
    cur = con.cursor();
    cur.execute("SELECT count(*) FROM users WHERE name=? AND pwd=?;", (u, p)) #fetching username and password and see if it matches
    x = cur.fetchone()
    if(x[0])>0:
        session['username'] = u
        #return redirect (url_for('store'))
        return render_template('success.html')
    else:
        return render_template('unauthorised.html')
    #if x is not None:
        #print('in login details')
        #title = str(x[1])
        #name = str(x[2])
        #logged_in(title,name)
        #, title=title,name=name) 
    

def logged_in(t,n): #not used
    con = sqlite3.connect('logged_in.db')
    try:
        con.execute('CREATE TABLE auth (title TEXT, name TEXT)')
        print ('Table created successfully');
    except:
        pass

    con.close()  
    con = sqlite3.connect('logged_in.db')
    con.execute("INSERT INTO auth values(?,?);", (t,n))
    con.commit()
    con.close()  


@app.route('/stock') #route to see book stock levels
def stocklevel(): 
    
    con = sqlite3.connect('products.db') #connection to database
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from products")
    rows = cur.fetchall()
    con.close()
    return render_template("stock.html",rows = rows) #prints out all of the books that are in stock

@app.route('/stock/addnew', methods=['GET', 'POST'])
def updatenewstock(): #gets book attributes from html form and transfers them to the insertNewStock function
    if request.method == 'POST':
        return insertNewStock(request.form['aiidd'], request.form['bname'], request.form['ccode'], request.form['iidir'], request.form['aprice'], request.form['ddscr'], request.form['ddate'], request.form['tprice'], request.form['quant'], request.form['aauth'])
    else:
        return showstockupd();
    
def showstockupd():
    return render_template('addstock.html') #rendering the html form to input values

def insertNewStock(a, n, c, i, p, d, w, t, q, z): #grabs values that were put in by the user from the html form and then inserts it into the products sql database
    con = sqlite3.connect('products.db')
    con.execute("INSERT INTO products values(?,?,?,?,?,?,?,?,?,?);", (a, n, c, i, p, d, w, t, q, z))
    con.commit()
    con.close()  

    return showstockupd()


@app.route('/add', methods=['POST']) #code from week 5 lab task with minor changes
def add_product_to_cart():
    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        
        if _quantity and _code and request.method == 'POST':
            con = sqlite3.connect('products.db')
            cur = con.cursor();
            cur.execute("SELECT * FROM products WHERE code=?;", [_code])
            row = cur.fetchone()
            itemArray = { row[2] : {'name' : row[1], 'code' : row[2], 'quantity' : _quantity, 'price' : row[4], 'image' : row[3], 'total_price': _quantity * row[4]}}
            print('itemArray is', itemArray)
            
            all_total_price = 0
            all_total_quantity = 0
            
            session.modified = True
            
            if 'cart_item' in session:
                print('in session')
                if row[2] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if row[2] == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row[4]
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)
                    
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row[4]
                
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            #code from week 6 lab task below
            checksumstr = "pid={pid:s}&sid={sid:s}&amount={all_total_price:.1f}&token={secret:s}"
            #print('checksumstr is', checksumstr)
            checksum = md5(checksumstr.encode('utf-8')).hexdigest()
            session['checksum'] = checksum
            #print(checksum is, checksum)
            session['sid'] = sid
            session['pid'] = pid
            #until this point the rest week 4
            return redirect(url_for('.products'))
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
		
@app.route('/store') #mainly code from week 4 lab task
def products(): 
    if session['username'] == 'admin': #check function to see if the user that logged in is an admin
        con = sqlite3.connect('products.db')
        cur = con.cursor();
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return render_template('adminproducts.html', products=rows) #concept is main store page divided into 2, for admin and for user, this one loads up the admin store page, contains stock levels button.
    else:
        try: #alternatively if the if statement above is false it just goes there
            con = sqlite3.connect('products.db')
            cur = con.cursor();
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            return render_template('products.html', products=rows)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            con.close()
        

@app.route('/empty') #code from week 4 lab task
def empty_cart():
	try:
		session.pop('cart_item', None) #suggested fix by Luke SID 10107753
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>') #code from week 4 lab task
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None) #suggested fix by Luke SID 10107753
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		
		if all_total_quantity == 0:
			session.pop('cart_item', None) #suggested fix by Luke SID 10107753
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		
if __name__ == "__main__":
    app.run()