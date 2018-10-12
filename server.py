from jinja2 import StrictUndefined

import requests

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Recipe, Favorite

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

spoonacular_base_endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com"


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Process user registration"""

    # take user input from register_form.html
    email = request.form["email"]
    password = request.form["password"]

    # query users table in database, retrieve user instance that matches email.
    user = User.query.filter(User.email == email).first()

    #if there is a user in database that matches email
    if user:
        flash("Account already exists. Please login.")
        return redirect("/login")

    # if email is not already in database, create new instance of User class.
    new_user = User(email=email, password=password)
    # add new user instance to users table in database.
    db.session.add(new_user)
    db.session.commit()

    flash("User account created. Please login.")
    return redirect("/login")

     
@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login',methods=['POST'])
def login_process():
    """Process login."""

    # Get from variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if password==user.password:
        session["user_id"] = user.user_id

        flash("Logged in")
        return redirect("/search")
    else:
        flash("Incorrect password")
        return redirect("/login")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/search')
def user_info():
    """User information"""

    return render_template("/search.html")


@app.route('/results', methods=["GET"]) #change to GET (and also change form)
def display_results():
    """displays recipes"""

    cuisine = request.args["cuisine_type"]
    limit = request.args["diet_restrictions"]
    time = request.args["cooking_time"]

    recipes = get_recipes(cuisine, limit, time)['results']
    print(recipes)

    recipe_dict = {}

    for recipe in recipes:
        recipe_id = recipe['id']
        details = get_recipe_by_id(recipe_id)
        if details['instructions'] is None:
            continue
        recipe_dict[recipe_id]= details

        if len(recipe_dict) == 2:
            break

    r_id = list(recipe_dict.keys())[0]
    print(list(recipe_dict[r_id].keys()))

    return render_template("/recipe.html",
                            recipes=recipe_dict,
                            cuisine=cuisine,
                            restrictions=limit,
                            cook_time=time)


@app.route('/recipe')
def favorite_recipe():
    favorite = []
    request.args["cuisine_type"]
    favorite_recipe_dict = 
    favorite_recipe_dict[]


def get_recipes(cuisine, limit, time):
    payload = {
        "number": 5,
        "diet": limit,
        "cuisine": cuisine,
        # add time restruction later
    }

    response = requests.get(
        spoonacular_base_endpoint + "/recipes/search",
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_KEY"],
            "X-Mashape-Host": os.environ["SPOONACULAR_HOST"]
        },
        params=payload
    )
    return response.json()

 
def get_recipe_by_id(id):

    # /recipes/id/information

    response = requests.get(
        spoonacular_base_endpoint + "/recipes/{}/information".format(id),
        headers={
            "X-Mashape-Key": os.environ["SPOONACULAR_KEY"],
            "X-Mashape-Host": os.environ["SPOONACULAR_HOST"]
        }
    )

    return response.json()





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
