from flask import *
from flask_mail import Mail, Message
from . import __init__
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user, login_required
from .models import User #importing User class from models.py
from . import db #importing db object from __init__.py
from datetime import datetime
import secrets #for generating random otp
from . import password2 #contains password of the email

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "bethelmv2@gmail.com"
app.config['MAIL_PASSWORD'] = password2.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
auth = Blueprint('auth', __name__)
mail=Mail(app)
def generateOTP(): #function to generate an OTP (6 digit number)
    num = str(secrets.randbelow(999999))
    return num

@auth.route('/login') #for loading the login page for first time
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #To handle form data
    email = request.form['email']
    password = request.form['password']
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    # To check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # Reload page if invalid credentials/user doesn't exist

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=["POST"])
def signup_post():
    #handling form data
    name = request.form['Name']
    dob = request.form['dob']
    #converting date into datetime
    y,m,d = dob.split('-')
    dob = datetime(int(y), int(m), int(d))
    gender =  request.form['gender']
    phone =  request.form['phone']
    email =  request.form['email']
    state =  request.form['stt']
    city =  request.form['city']
    password =  request.form['password']
    session['email']=request.form['email']
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again with another email
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    #OTP generation
    otp = generateOTP()
    list_email=[]
    list_email.append(email)
    session['response'] = str(otp) #storing the generated otp in session
    msg = Message('CoviSafe - OTP',sender = 'bethelmv2@gmail.com',recipients=list_email) #subject, sender's email and receipient email
    msg.body = "Thank you for creating an account. To complete your registration, enter this OTP. " +str(otp) #body of the message
    mail.send(msg)
    new_user=User(name=name, dob=dob, gender=gender, phone=phone, email=email, state=state, city=city, password=generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    flash('Enter the otp received in your email')
    return render_template('otp.html')

    #OTP Validation
@auth.route('/otp',methods=['POST'])
def validateOTP():
    email=session['email']
    str(email)
    otp = request.form['otp']
    if 'response' in session:
        s = session['response'] #retrieving the generated otp
        session.pop('response',None)
        if s==otp: #checking the form-entered otp with retrieved otp
            flash("Account created successfully, you can now login")
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid otp entered!")
            user = User.query.filter_by(email=email).first()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('auth.signup'))
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
