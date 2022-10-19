"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get("/")
def go_home():
    "Home page that displays all users"

    return redirect("/users")

@app.get('/users')
def get_users():
    """Get list of users"""

    users = User.query.all()

    return render_template('users_list.html', users=users)

@app.get('/users/new')
def show_new_user_form():
    """Get the add new user form"""

    return render_template("create_user.html")

@app.post('/users/new')
def add_user_to_db():
    """Add the user to the database"""
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def get_user_detail(user_id):
    """User detail page"""

    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)

@app.get('/users/<int:user_id>/edit')
def get_user_edit(user_id):
    """User Edit page"""

    user = User.query.get_or_404(user_id)

    # cancel button --> returns to user_detail.html
    # save button --> updates user
    return render_template("user_edit.html", user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Process user data changes"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form.get('first-name')
    user.last_name = request.form.get('last-name')
    user.image_url = request.form.get('image-url')

    db.session.commit()

    return redirect('/users')