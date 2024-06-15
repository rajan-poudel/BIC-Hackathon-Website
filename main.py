from flask import Flask , render_template , request , flash ,redirect ,session
import requests
from flask_mail import Mail
import random

#Database
import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["boston-web"]
collection = db["users-data"] 


app=Flask(__name__)
app.secret_key="supersecretkeydkdjd"
app.config.update(
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT = 465,
MAIL_USE_SSL = True,
MAIL_USERNAME = '',
MAIL_PASSWORD = ''
)
mail = Mail(app)

def email_exists(email):
    result = collection.find_one({"email": email})
    if result is not None:
        return True
    else:
        return False


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        result = collection.find_one({"email": email})
        if result is not None:
            if password == result["password"]:
                session["email"] = email
                flash("You have successfully logged in", "success")
                return redirect("/home")
            else:
                flash("Incorrect password", "danger")
                return redirect("/login")
        else:
            flash("Email does not exist", "danger")
            return redirect("/login")
    else:
        return redirect("/login")

@app.route("/signup",methods=['GET','POST'])
def signup():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        p
        assword = request.form.get('password')

        url = """ """+email
        res = requests.get(url)
        result = res.json()


        smtp_check_value = result['smtp_check']

        if(smtp_check_value==True):
            if (email_exists(email)==False):
                otp = random.randint(1000, 9999)
                message=f"OTP:{otp} - By MediNep"
                session["otp_success"]='success'
                session["otp"] = otp
                session["name"] = name
                session["email"] = email
                session["password"] = password
                mail.send_message('New message from ' + name ,sender="",recipients=[f"{email}"],body=message)
                return render_template("otp-verify.html")
            else:
                flash("Email is already used :(","danger")
                return redirect("/login")
        else:
            flash("Invalid Email :(","danger")
            return redirect("/login")
        
    flash("Some error occured :(","danger")
    return redirect("/login")

@app.route("/otp-proceed",methods=['GET','POST'])
def otp_verify():
    if 'otp_success' in session and session['otp_success']:
        if(request.method=='POST'):
                    otp_1 = request.form.get("num1")
                    otp_2 = request.form.get("num2")
                    otp_3 = request.form.get("num3")
                    otp_4 = request.form.get("num4")
                    got_otp = int(otp_1+otp_2+otp_3+otp_4)
                    if got_otp == session["otp"]:
                        user_data = {
    "name": session["name"],
    "email": session["email"],
    "password":session["password"]
}
                        result = collection.insert_one(user_data)
                        return redirect("/home")
                    else:
                        flash("Invalid OPT","danger")
                        return render_template("otp-verify.html")
        else :
            return redirect("/login")
    return redirect("/login")

@app.route("/home",methods=['GET','POST'])
def home():
    if 'email' in session and session['email']:
        return render_template("home.html")
    return redirect("/")

@app.route("/registration",methods=['GET','POST'])
def registration():
    if 'email' in session and session['email']:
        return render_template("disease.html")
    return redirect("/")

@app.route("/payment",methods=['GET','POST'])
def payment():
    if 'email' in session and session['email']:
        return render_template("payment.html")
    return redirect("/")

@app.route("/doctor",methods=['GET','POST'])
def doctor():
    if 'email' in session and session['email']:
        return render_template("doctor.html")
    return redirect("/")

@app.route("/doctor-signup",methods=['GET','POST'])
def doctor_signup():
    return render_template("doctor_signup.html")

@app.route("/doctor-signup-procced",methods=['GET','POST'])
def doctor_signup_procced():
    return render_template("doctor-signup-procced.html")

@app.route("/doctor-dashboard",methods=['GET','POST'])
def doctor_dashboard():
    return render_template("doctor-dashboard.html")

@app.route("/medicine",methods=['GET','POST'])
def medicine():
    if 'email' in session and session['email']:
        return render_template("medicine.html")
    return redirect("/")

@app.route("/hotline",methods=['GET','POST'])
def hotline():
    if 'email' in session and session['email']:
        return render_template("hotline.html")
    return redirect("/")

@app.route("/medicine-payment",methods=['GET','POST'])
def medicine_payment():
    if 'email' in session and session['email']:
        return render_template("medicine-payment.html")
    return redirect("/")

@app.route("/order-placed",methods=['GET','POST'])
def order_placed():
    if 'email' in session and session['email']:
        return render_template("order-placed.html")
    return redirect("/")

@app.route("/searching-ambulance",methods=['GET','POST'])
def searching_ambulance():
    if 'email' in session and session['email']:
        return render_template("/searching-ambulance.html")
    return redirect("/")

@app.route("/call-ambulance",methods=['GET','POST'])
def call_ambulance():
    if 'email' in session and session['email']:
        return render_template("call-ambulance.html")
    return redirect("/")

@app.route("/courses",methods=['GET','POST'])
def courses():
    if 'email' in session and session['email']:
        return render_template("courses.html")
    return redirect("/")

@app.route("/turn-tracker",methods=['GET','POST'])
def turn_tracker():
    if 'email' in session and session['email']:
        return render_template("turn-tracker.html")
    return redirect("/")

@app.route("/setting",methods=['GET','POST'])
def setting():
    if 'email' in session and session['email']:
        return render_template("setting.html")
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop('email')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
