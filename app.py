from flask import Flask, render_template, url_for, redirect, request
from forms import Form_update, Form_add, Form_registration, Form_login
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import random
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gigi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Citation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), index = True, unique = False)
    surname = db.Column(db.String(20), index = True, unique = False)
    quote = db.Column(db.String(200), index = True, unique = True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String(), index = True, unique = True)
    bio = db.Column(db.String(), index = True, unique = False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), index = True, unique = True)
    email = db.Column(db.String(60), index = True, unique = True)
    password_hash = db.Column(db.String(200), index = True, unique = True)
    joined_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

@app.route("/")
def home():
    random_quote = random.choice(Citation.query.all())
    random_image = random.choice(Image.query.all())
    citations = Citation.query.group_by(Citation.surname)
    return render_template("home.html", template_citations = citations, template_quote = random_quote, template_image = random_image)

@app.route("/authors")
def authors():
    return render_template("authors.html")

@app.route("/archive")
def archive():
    citations = Citation.query.all()
    return render_template("archive.html", template_citations = citations)

@app.route("/update", methods=["GET", "POST"])
@login_required
def update():  
    form = Form_update(csrf_enabled=False)
    if form.validate_on_submit():
        citation = Citation(name = form.name.data, surname = form.surname.data, quote = form.quote.data) 
        db.session.add(citation) 
        db.session.commit()
        return redirect(url_for("archive"))
    return render_template("update.html", template_form = form)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = Form_add(csrf_enabled=False)
    if form.validate_on_submit() and form.image.data[-4:] == ".jpg":
        image = Image(image = form.image.data, bio = form.bio.data)
        db.session.add(image)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", template_form = form)

@app.route("/authors/<string:writer_surname>/<string:writer_name>")
def writer(writer_surname, writer_name):
    quotes_for_writer = Citation.query.filter_by(surname = writer_surname)
    return render_template("writer.html", template_quotes = quotes_for_writer, template_surname = writer_surname, template_name = writer_name)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = Form_login(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html", template_form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = Form_registration(csrf_enabled=False)
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data, password_hash = generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html", template_form = form)

