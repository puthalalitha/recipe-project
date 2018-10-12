from model import User, Recipe, Favorite, connect_to_db, db

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()

    lalitha = User(email="lalitha@recipe.com", password="evil")
     
    dall = Recipe(title="dall")
    lalitha_fav = Favorite(user=lalitha, recipe=dall)
    db.session.add_all([lalitha, dall])

    mushroom_curry = Recipe(title="mushroom curry")
    db.session.add(mushroom_curry)

    sambar = Recipe(title="sambar")
    db.session.add(sambar)


    jessica = User(email="jessica@recipe.com", password="123")
    jessica_fav = Favorite(user=jessica, recipe=sambar)
    db.session.add(jessica)
    
    db.session.commit()

