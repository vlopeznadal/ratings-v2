"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def homepage():
    """show my homepage"""

    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """show all movies"""

    movies = crud.get_all_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_specific_movie(movie_id):
    """show the movie with the given ID"""
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    """show all users"""

    users = crud.get_all_users()

    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("This account already exists, try again")
    else:
        crud.create_user(email, password)
        flash ("Your account was created! Log in now")

    return redirect ("/")
        

@app.route("/users/<user_id>")
def show_specific_user(user_id):
    """show the user with the given ID"""
    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def user_login():
    """Login a user"""
    login_email = request.form.get("login-email")
    login_password = request.form.get("login-password")

    login_user = crud.get_user_by_email(login_email)

    if login_user.password == login_password:
        session["user"] = login_user.user_id
        flash("Logged in!")

    else:
        flash("Incorrect password")
    
    return redirect("/")


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
