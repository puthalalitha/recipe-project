"""Models and database functions for Find_Recipes project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##########################################################

class User(db.Model):
    """User of Find_Recipes website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

    favorites = db.relationship("Favorite")
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"

class Recipe(db.Model):
    """Find_Recipes website."""

    __tablename__ = "recipes"

    recipe_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(200))

    favorites = db.relationship("Favorite")
    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Recipe user_id={self.user_id} title={self.title}>"

class Favorite(db.Model):
    """User of favorites website."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False )
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    
    user = db.relationship("User")
    recipe = db.relationship("Recipe")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Favorite recipe={self.recipe_id} user_id={self.user_id}>"


# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///recipes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    #from server import app
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
