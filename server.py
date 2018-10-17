from jinja2 import StrictUndefined

import requests

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Recipe, Favorite

import os
import random

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
    caution = request.args["intolerances"]

    recipes = get_recipes(cuisine, limit, caution)['results']
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
                            caution=caution)


@app.route('/save', methods=['POST'])
def favorite_recipe():
    """Add a recipe to our database"""

    spoonacular_id = request.form.get("recipeId")
    recipe_title = request.form.get("recipeTitle")
    recipe_url = request.form.get("recipeUrl")
    # print("in save*****************")

    # query the recipe table by id to see if this recipe
    # is already in the database.
    recipe = Recipe.query.get(spoonacular_id)
    recipe = Recipe.query.get(spoonacular_id)

    if not recipe:
        new_recipe = Recipe(spoonacular_id=spoonacular_id, 
                            title=recipe_title,
                            url=recipe_url)
        db.session.add(new_recipe)
        db.session.commit()


    fav_recipe = Favorite.query.filter_by(user_id=session["user_id"],
                                spoonacular_id=spoonacular_id).first()

    if not fav_recipe:    
    # next, add to the favorite table.
        fav_recipe = Favorite(user_id=session["user_id"],
                               spoonacular_id=spoonacular_id)
        db.session.add(fav_recipe)
        db.session.commit()

    results = {"message": "Your recipe saved.", "recipe_id": spoonacular_id}

    return jsonify(results) 


@app.route('/favorites')
def saved_recipes():
    favorites = Favorite.query.filter_by(user_id=session["user_id"])
    return render_template("favorites.html", favorites=favorites)


@app.route("/favorites/<int:spoonacular_id>") #here, the id should be spoonacular_id
def show_recipe(spoonacular_id):
    
    # Use the id to call get_recipe_by_id function
    # render a favorite.html template to show the recipe info
    recipe_result = get_recipe_by_id(spoonacular_id)

    return render_template("favorite.html", details=recipe_result)


@app.route("/remove", methods=["POST"])
def remove_recipe():

    spoonacular_id = request.form.get("recipeId")

    # Query the Favorite table to see if there us a record
    # with the user_id from the session and this spoonacular_id
    # If there is a record with this information, delete it.

    take_out_recipe = Favorite.query.filter_by(user_id=session["user_id"],
                                               spoonacular_id=spoonacular_id).first()

    if take_out_recipe:
         
        db.session.delete(take_out_recipe)
        db.session.commit()

    return "Recipe removed"


def get_recipes(cuisine, limit, intolerances):
    payload = {
        "number": 5,
        "diet": limit,
        "cuisine": cuisine,
        "intolerances":intolerances,
        "offset":random.randint(0, 10)
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
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
