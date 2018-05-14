from flask import Flask, render_template, flash, request, Response, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask.ext.mysql import MySQL

# it's neccesary install "pip install flask-mysql"
# App config.
# pip install flask-login
# I had  create a database called ticket_et
# after i had create this table: create table ticket (id_ticket INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(40) NOT NULL, email VARCHAR(50) NOT NULL, extension VARCHAR(8), description TEXT,criticality VARCHAR(7) ,red_date TIMESTAMP, red_date_end TIMESTAMP, assignto VARCHAR(25), status VARCHAR(15) DEFAULT 'open');
# this it's the  users table
# create table users (id_ticket INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,name VARCHAR(35),username VARCHAR(25),password VARCHAR(35), email VARCHAR(40))
# insert INTO users (name,username,password,email) VALUES ("arnoldo magana","maganaa","nocturna","maganaa@e-telecomm.com.mx");
# 
# 
DEBUG = True
app = Flask(__name__)
#mysql connection
mysql=MySQL()
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='ticket_et'
app.config['MYSQL_DATABASE_host']='127.0.0.1:3306'
mysql.init_app(app)
conn = mysql.connect() # let's create the MySQL connection:
cursor = conn.cursor() # let's create cursor 

#end mysql cnnection

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




    
@app.route("/", methods=['GET', 'POST'])
def add_ticket():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        extension=request.form['extension']
        comp_select=request.form['comp_select']
        report=request.form['report']
        #print name, " ", email, " ", report, " ", extension, " "
 
        if form.validate():
            # Save the comment here.
            cursor.execute('''INSERT INTO ticket (name, email, extension, description, criticality) VALUES (%s, %s, %s, %s, %s)''', (name,email,extension,report,comp_select))
            conn.commit()
            flash('Listo, Estamos listos para empezar a trabajar... ' )
        else:
            flash('Error: Llena bien los datos por favor')
 
    return render_template('add_ticket.html', form=form, data=[{'criticality':'Normal'}, {'criticality':'Baja'}, {'criticality':'Alta'}])


@app.route("/login", methods=['GET','POST'])
def login():
    form = ReusableFormLogin(request.form)
    if request.method == 'POST':
        username=request.form['user']
        password=request.form['password']
        cursor.execute("SELECT name FROM users WHERE username ='"+username+"' AND password ='"+password+"'")
        name = cursor.fetchone()
        if name and len(name) is  1:
             flash('Datos validos Hola ' + name[0])
             cursor.execute("SELECT * from ticket where status = 'open'")
             return  render_template('display_ticket.html', name=name[0],plop=cursor.fetchone() )
        else:
            flash('Error: Acceso incorrecto')
            
    return render_template('login.html', form=form)


@app.route("/MySQL")
def test_mysql():
    try:
        c, conn = connection()
        return("okay")
    except Exception as e:
        return(str(e))



### REusable forms

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    extension = TextField('Extension:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required()]) 
    comp_select = TextField('comp_select:', validators=[validators.required()]) 
    report = TextField('Report:', validators=[validators.required(), validators.Length(min=2, max=35)])
    
class ReusableFormLogin(Form):
    user = TextField('User:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required()])
    
    
if __name__ == "__main__":
    app.run()

