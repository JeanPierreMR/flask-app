from flask import Flask, render_template, url_for, request, session, redirect, render_template_string, send_file, \
    send_from_directory, make_response
from app import db_manager
from app import app
from app.db_manager import insert_house
from app.forms import LoginForm, CreateAccountForm, VentaForm, CompraForm
from io import BytesIO

# -- calling the create function each time
db_manager.create()


# -- mapping for home page(root)
# -- using decorator function
@app.route("/", methods=["POST", "GET"])
@app.route("/index.html", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
@app.route("/forms", methods=["POST", "GET"])
def home():
    compra_form = CompraForm(request.form)
    # Session control
    if not session.get('logged_in'):
        return redirect("/login")
    elif request.method == 'POST':
        # select (zone, typehome, roomsnumber, roomsbath, 5, page_number-1,)
        page = request.args.get('page', 1, type=int)
        zone = request.form['zone']
        typehome = request.form['typehome']
        roomsnumber = request.form['roomsnumber']
        roomsbath = request.form['roomsbath']

        houses_info = db_manager.get_houses(zone, typehome, roomsnumber, roomsbath, page)
        resp = make_response(
            render_template("ui-avatars.html", pagination_page=page, houses_info=houses_info, compra_form=compra_form))
        resp.set_cookie('zone', zone)
        resp.set_cookie('typehome', typehome)
        resp.set_cookie('roomsnumber', roomsnumber)
        resp.set_cookie('roomsbath', roomsbath)
        return resp
    else:
        # page = request.args.get('page', 1, type=int)
        page = request.args.get('page', 1, type=int)
        zone = request.cookies.get('zone', default=9)
        typehome = request.cookies.get('typehome', default='Casa')
        roomsnumber = request.cookies.get('roomsnumber', default=1)
        roomsbath = request.cookies.get('roomsbath', default=1)
        houses_info = db_manager.get_houses(int(zone), typehome, int(roomsnumber), int(roomsbath), page)
        resp = make_response(
            render_template("ui-avatars.html", pagination_page=page, houses_info=houses_info, compra_form=compra_form))
        resp.set_cookie('zone', str(zone))
        resp.set_cookie('typehome', typehome)
        resp.set_cookie('roomsnumber', str(roomsnumber))
        resp.set_cookie('roomsbath', str(roomsbath))
        return resp


# -- Form ventas page
@app.route("/form-venta", methods=["POST", "GET"])
def form_venta1():
    compra_form = CompraForm(request.form)
    venta_form = VentaForm(request.form)
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return redirect('/register')
    elif request.method == 'POST':
        print(dict(request.form))
        name1 = request.form['name1']
        name2 = request.form['name2']
        lastname1 = request.form['lastname1']
        lastname2 = request.form['lastname2']
        dpi = request.form['dpi']
        email1 = request.form['email1']
        phone = request.form['phone']
        address = request.form['address']
        typehome = request.form['typehome']
        zone = request.form['zone']
        roomsnumber = request.form['roomsnumber']
        roomsbath = request.form['roomsbath']
        pricedol = request.form['pricedol']
        pricequet = request.form['pricequet']
        meters = request.form['meters']
        comments = request.form['comments']
        user_id = session['user_id']
        images = request.files.getlist('images')
        insert_house(user_id, name1, name2, lastname1, lastname2, dpi, email1, phone, address, typehome, zone,
                     roomsnumber, roomsbath, pricedol, pricequet, meters, comments, images)
        return render_template('form_venta.html',
                               msg='Su formulario fue enviado',
                               success=True,
                               form=venta_form, compra_form=compra_form)
    # elif not session.get('logged_in'):
    #     return redirect('/register')
    else:
        return render_template("form_venta.html", form=venta_form, compra_form=compra_form)


@app.route('/imgs')
def img_house():
    num_image = request.args.get('num_image', -1, type=int)
    house_id = request.args.get('house_id', 0, type=int)
    print(f'{num_image}, {house_id}')
    try:
        file = db_manager.get_house_images(house_id, num_image)
        return send_file(BytesIO(file[0]), mimetype='image/jpeg')
    except Exception as e:
        # print('sending blank')
        return send_from_directory(directory='static/img', filename='img.png', as_attachment=True)


@app.route("/form-cita")
def form_cita():
    return render_template("form_cita.html")


# -------- User control -------#

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
                db_manager.insert_user(username, email, password)
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
        return redirect('/')


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
            session['user_id'] = db_manager.get_userid(username)
            return redirect('/')
        # Something (user or pass) is not ok
        return render_template('accounts/login.html', msg='Wrong email or password', form=login_form)

    elif not session.get('logged_in'):
        return render_template('accounts/login.html',
                               form=login_form)
    else:
        return redirect('/')


@app.route("/full", methods=["POST", "GET"])
def full_output():
    compra_form = CompraForm(request.form)
    # Session control
    if not session.get('logged_in'):
        return redirect("/login")
    elif request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        houses_info = db_manager.get_all_houses(page)
        resp = make_response(
            render_template("ui-avatars-full.html", pagination_page=page,
                            houses_info=houses_info, compra_form=compra_form)
        )
        return resp
    else:

        page = request.args.get('page', 1, type=int)
        houses_info = db_manager.get_all_houses(page)
        resp = make_response(
            render_template("ui-avatars-full.html", pagination_page=page,
                            houses_info=houses_info, compra_form=compra_form))
        return resp


if __name__ == "__main__":
    # -- run the app in debug mode
    app.run(debug=True)
