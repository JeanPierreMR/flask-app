from flask import Flask, render_template, url_for, request, session, redirect
from app import db_manager
from app import app
from app.forms import LoginForm, CreateAccountForm
# -- calling the create function each time
db_manager.create()


# -- mapping for home page(root)
# -- using decorator function
@app.route("/")
@app.route("/index.html")
@app.route("/home")
def home():
    #Session control
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("ui-avatars.html")





#-------- User control -------#

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect("/login")


# -- mapping for register_success page
# -- the registery page uses post method to send data to server
@app.route("/register", methods=["POST", "GET"])
def register():
    create_account_form = CreateAccountForm(request.form)
    if request.method == 'POST':
        # read form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if db_manager.check_data(email):
            if db_manager.check_username(username):
                db_manager.insert(username, email, password)
                return render_template('accounts/register.html',
                                       msg='User created please <a href="/login">login</a>',
                                       success=True,
                                       form=create_account_form)
            else:
                return render_template('accounts/register.html',
                                       msg='Username already registered',
                                       success=False,
                                       form=create_account_form)
        else:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
    elif not session.get('logged_in'):
        return render_template('accounts/register.html', form=create_account_form)
    else:
        return render_template("ui-avatars.html")


# -- Login page
@app.route("/login", methods=["POST", "GET"])
def login_fun():
    login_form = LoginForm(request.form)
    if request.method == 'POST':
        # read form data
        username = request.form['username']
        password = request.form['password']
        if db_manager.check_login_data(username, password):
            session['logged_in'] = True
            session['username'] = username
            session['email'] = db_manager.get_email(username)
            return render_template("ui-avatars.html")
        # Something (user or pass) is not ok
        return render_template('accounts/login.html', msg='Wrong email or password', form=login_form)

    elif not session.get('logged_in'):
        return render_template('accounts/login.html',
                               form=login_form)
    else:
        return render_template("ui-avatars.html")




if __name__ == "__main__":
    # -- run the app in debug mode
    app.run(debug=True)
