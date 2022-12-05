
from flask import *
from fileinput import filename
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import sqlite3


 
UPLOAD_FOLDER = 'Desktop/JustInCase/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 

@app.route('/index.html')
def index():
    return render_template('index.html')
    
@app.route('/about.html')
def about():
    return render_template('about.html')
    
@app.route('/services.html')
def services():
    return render_template('services.html')
    
@app.route('/contact.html')
def contact():
    return render_template('contact.html')
    
@app.route('/checkout.html', methods =["GET", "POST"])
def checkout():
    if request.method == "POST":
       full_name = request.form["fname"]
       email = request.form["email"]
       phone = request.form["pnum"]
       raddy = request.form["addy"]
       rfull_name = request.form["rfname"]
       remail = request.form["remail"]
       deliverymonth = request.form["month"]
       deliveryday = request.form["day"]
       
       letterfile = request.files['Letter']
       idfile = request.files['Official ID']
       
       letter = letterfile.filename
       id = idfile.filename
       if letterfile.filename == '':
        print('No selected file')
        return redirect(request.url)
       if idfile.filename == '':
        print('No selected file')
        return redirect(request.url)
       if letterfile and allowed_file(letterfile.filename):
        letterfilename = secure_filename(letterfile.filename)
        letterfile.save(letterfilename)
       if idfile and allowed_file(idfile.filename):
        idfilename = secure_filename(idfile.filename)
        idfile.save(idfilename)
       
       
      
       return redirect(url_for('payment', full_name=full_name, email=email, phone=phone, raddy=raddy, rfull_name=rfull_name, remail=remail, deliverymonth=deliverymonth, deliveryday=deliveryday, letter=letter, id=id))

    else:
        return render_template('checkout.html')
    
@app.route('/confirmation.html')
def confirmation():
    return render_template('confirmation.html')
    
@app.route('/modal-oops.html')
def modal():
    return render_template('modal-oops.html')
    
@app.route('/payment.html', methods =["GET", "POST"])
def payment():
    if request.method == "POST":
       payname = request.form["fullname"]
       
       cemail = request.form["email"]
       addy = request.form["address"]
       city = request.form["city"]
       state = request.form["state"]
       zip = request.form["zip"]
       
       cname = request.form["cardname"]
       ccnum = request.form["cardnumber"]
       expmonth = request.form["expmonth"]
       expyear = request.form["expyear"]
       cvv = request.form["cvv"]
       
       
       full_name=request.args['full_name']
       email=request.args['email']
       phone=request.args['phone']
       raddy=request.args['raddy']
       rfull_name=request.args['rfull_name']
       remail=request.args['remail']
       deliverymonth=request.args['deliverymonth']
       deliveryday=request.args['deliveryday']
       letter=request.args['letter']
       id=request.args['id']
       
      
       create_table()
       with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('''SELECT COUNT(*) FROM transactions''')
            uid = cur.fetchall()
            uid=uid[0][0]+1
            print(uid)
            cur.execute('''INSERT INTO transactions (userId,user_name, user_email, user_phone, receiver_address, receiver_name, reciever_email, delivery_month, delivery_day, letterfile, idfile, billing_name, billing_email, billing_address, billing_city, billing_state, billing_zip, cardname, cardnumber, expmonth, expyear, cvv) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (uid, full_name, email, phone, raddy, rfull_name, remail, deliverymonth, deliveryday,letter, id,payname, cemail, addy, city, state, zip, cname, ccnum, expmonth, expyear, cvv))
              
            conn.commit()
            
            msg= "added successfully"
        except Exception as e:
            msg= "error occured"
            print(e)
            
            conn.rollback()
        
        print(msg)
       
       
        return redirect(url_for('confirmation'))
        conn.close()
    else:
        return render_template('payment.html')
    
 
if __name__=='__main__':
   app.run()
   
   
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_table():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions
  (userId INTEGER PRIMARY KEY,
  user_name TEXT,
  user_email TEXT,
  user_phone INTEGER,
  receiver_address TEXT,
  receiver_name TEXT,
  reciever_email TEXT,
  delivery_month INTEGER,
  delivery_day INTEGER,
  letterfile TEXT,
  idfile TEXT,
  billing_name TEXT,
  billing_email TEXT,
  billing_address TEXT,
  billing_city TEXT,
  billing_state TEXT,
  billing_zip INTEGER,
  cardname TEXT,
  cardnumber INTEGER,
  expmonth INTEGER,
  expyear INTEGER,
  cvv INTEGER
  )''')
    print("Table created")
    conn.close()

