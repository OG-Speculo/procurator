from flask import render_template, request, redirect, session, url_for, flash, g, send_from_directory, Flask
from forms import RegisterForm, LoginForm, DonorDetailsForm
from datetime import timedelta
import pyrebase
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SECRET_KEY'] = "c6e803cd18a8c528c161eb9fcf013245248506ffb540ff70"
csrf = CSRFProtect(app)

firebaseConfig = {
  'apiKey': "AIzaSyCxaKkYIhjVEuX8T1i7F-l_oNW4z7diiuc",
  'authDomain': "nmims-gdsc-speculo.firebaseapp.com",
  'databaseURL': "https://nmims-gdsc-speculo-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "nmims-gdsc-speculo",
  'storageBucket': "nmims-gdsc-speculo.appspot.com",
  'messagingSenderId': "30446673290",
  'appId': "1:30446673290:web:957e8dc493327e835b3c73",
  'measurementId': "G-SR9Y7THH6E"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


# def get_individual_donor_list(email):
#     email = email.replace("~", "@").replace("`", ".")
#     c = 1
#     res = list()
#     data_file = db.child("Data").get()
#     if(data_file.val() != None):
#         for details in data_file.each():
#             if details.val()["Donor mail"] == email:
#                 res.append([details.val(), c])
#                 c += 1
#     return res
#
#
# def get_complete_donor_list():
#     c = 1
#     res = list()
#     data_file = db.child("Data").get()
#     if(data_file.val() != None):
#         for details in data_file.each():
#             if details.val()["Distributor mail"] == "Not claimed":
#                 res.append([details.val(), details.key(), c])
#                 c += 1
#     return res
#
#
# def get_individual_distributor_list(email):
#     email = email.replace("~", "@").replace("`", ".")
#     c = 1
#     res = list()
#     data_file = db.child("Data").get()
#     if(data_file.val() != None):
#         for details in data_file.each():
#             if details.val()["Distributor mail"] == email:
#                 res.append([details.val(), c])
#                 c += 1
#     return res

def get_individual_employee_details(email):
    c = 1
    res = list()
    data_file = db.child("Data-2").get()
    if(data_file.val() != None):
        for details in data_file.each():
            if details.val()["Employee mail"] == email:
                res.append([details.val(), c])
                c += 1
    return res

def get_complete_employee_list():
    c = 1
    res = list()
    data_file = db.child("Data-2").get()
    if(data_file.val() != None):
        for details in data_file.each():
            if details.val()["Approval"] == "Not approved":
                res.append([details.val(), details.key(), c])
                c += 1
    return res

def get_individual_manager_list():
    c = 1
    res = list()
    data_file = db.child("Data-1").get()
    if(data_file.val() != None):
        for details in data_file.each():
            res.append([details.val(), c])
            c += 1
    return res

def get_name(email):
    data_file = db.child("Data-1").get()
    if (data_file.val() != None):
        for details in data_file.each():
            if details.val()["Employee mail"] == email:
                return details.val()["Employee name"]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        if g.user is not None:
            return redirect(url_for('account_page'))
    message = ""
    sumessage = ""
    passerror = ""
    login_form = LoginForm()
    session.pop('logged_in', None)
    if login_form.validate_on_submit():
        email = str(login_form.email.data)
        password = str(login_form.password.data)
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            session['logged_in'] = True
            session['name'] = get_name(email)
            sumessage = "Successfully logged in"
            return redirect(url_for("account_page"))
        except:
            message = "Invalid email or password.Try again"
    return render_template("login.html", form=login_form, ermessage=message, sumessage=sumessage, pass_error=passerror)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'GET':
        if g.user is not None:
            return redirect(url_for('account_page'))
    message = ""
    ermessage = ""
    register_form = RegisterForm()
    session.pop('logged_in', None)
    if register_form.validate_on_submit():
        try:
            data = dict()
            email = register_form.email_address.data
            data["Employee mail"] = email
            password = register_form.email_address.data
            name = register_form.name.data
            data["Employee name"] = name
            data["No of hours"] = 0
            category = register_form.radio_btn.data
            auth.create_user_with_email_and_password(email, password)
            session['logged_in'] = True
            session['email'] = email
            session['name'] = name
            message = "Successfully Registered"
            username = email.replace("@", "~").replace(".", "`")
            db.child("Category").update({username: category})
            db.child("Data-1").push(data)
            return redirect(url_for("account_page"))
        except Exception as e:
            ermessage = e
    return render_template("register.html", form=register_form, regermessage=ermessage, regmessage=message)


@app.route("/account", methods=["POST", "GET"])
def account_page():
    if g.user is None:
        return redirect(url_for('login'))
    category = None
    key_email = session["email"].replace("@", "~").replace(".", "`")
    data_file = db.child("Category").get()
    for details in data_file.each():
        if details.key() == key_email:
            category = details.val()
    donor_form = DonorDetailsForm()
    if request.method == "POST":
        if category == "Employee":
            if donor_form.validate_on_submit():
                info = dict()  # must include getting all the info and adding to the database
                # info["Employee name"] = donor_form.name.data
                # info["Designation"] = donor_form.designation.data
                # info["Contact details"] = donor_form.contact.data
                info["Work Done"] = donor_form.work.data
                info["No of hours"] = donor_form.hours.data
                info["Employee mail"] = session['email']
                info["Manager mail"] = "manager@gmail.com"
                info["Approval"] = "Not approved"
                db.child("Data-2").push(info)
        else:
            key = request.form["key"]
            db.child("Data-2").child(key).update({"Approval": "Approved"})
        return redirect(url_for('account_page'))

    if category == "Employee":
        l = get_individual_employee_details(session['email'])
        return render_template("employee.html",user=session['email'], data=l, form=donor_form)
    else:
        donor_list = get_complete_employee_list()
        distributor_list = get_individual_manager_list()
        return render_template("manager.html", user=session['email'] ,donor_list=donor_list, distributor_list=distributor_list)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route("/reset-pass", methods=["POST", "GET"])
def reset_pass():
    if g.user is None:
        return redirect(url_for('login'))
    auth.send_password_reset_email(session['email'])
    return redirect(url_for('logout'))


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=3)
    g.user = None
    if 'logged_in' in session:
        g.user = session['logged_in']

if __name__ == "__main__":
    app.run()
