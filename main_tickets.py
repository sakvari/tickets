from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask.ext.mysql import MySQL

# it's neccesary install "pip install flask-mysql"
# App config.
#this it's the first version from table  i'll be change it  create table ticket (id_ticket INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(40) NOT NULL, email VARCHAR(50) NOT NULL, extension VARCHAR(8), description TEXT,criticality VARCHAR(7) ,red_date TIMESTAMP);
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



class ReusableForm(Form):
    
    name = TextField('Name:', validators=[validators.required()])
    extension = TextField('Extension:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required()]) 
    comp_select = TextField('comp_select:', validators=[validators.required()]) 
    report = TextField('Report:', validators=[validators.required(), validators.Length(min=2, max=35)])
 
@app.route("/", methods=['GET', 'POST'])
def add_ticket():
    form = ReusableForm(request.form)
    conn = mysql.connect() # let's create the MySQL connection:
    cursor = conn.cursor() # let's create cursor 

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
        
            #flash('Listo, Estamos listos para empezar a trabajar... ' + name + email + extension + report + comp_select)
        else:
            flash('Error: Llena bien los datos por favor')
 
    return render_template('add_ticket.html', form=form, data=[{'criticality':'Normal'}, {'criticality':'Baja'}, {'criticality':'Alta'}])

@app.route("/MySQL")
def test_mysql():
    try:
        c, conn = connection()
        return("okay")
    except Exception as e:
        return(str(e))
if __name__ == "__main__":
    app.run()
