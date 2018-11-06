from unittest import TestCase
from server import app
from model import connect_to_db, db, User, Favorite, Recipe
from seed import example_data
from flask import session
import server
import tests


# Make mock for get recipes
def _mock_get_recipes(cuisine, limit, caution):
    return [
            {'id': 716275,
             'title': 'Native Jollof Rice - Iwuk Edesi',
             'readyInMinutes': 45, 'servings': 3,
             'image': 'native-jollof-rice-iwuk-edesi-716275.jpg',
             'imageUrls': ['native-jollof-rice-iwuk-edesi-716275.jpg']}
            ]


def _mock_get_recipes_by_name(recipe_name):
    return [
    {"number": 5,
        "query": 'Jollof Rice' 
     }]
         


# Make mock for get recipe by id
def _mock_get_recipe_by_id(details_id=716275):
    results = {
        716275: 
        {'vegetarian': False, 
         'vegan': False, 
         'glutenFree': True, 
         'dairyFree': True, 
         'veryHealthy': True, 
         'cheap': False, 
         'veryPopular': False, 
         'sustainable': False, 
         'weightWatcherSmartPoints': 14, 
         'gaps': 'no', 
         'lowFodmap': False, 
         'ketogenic': False, 
         'whole30': False, 
         'sourceUrl': 'http://www.afrolems.com/2013/07/19/native-jollof-rice-iwuk-edesi/',
         'spoonacularSourceUrl': 'https://spoonacular.com/native-jollof-rice-iwuk-edesi-716275',
         'aggregateLikes': 239,
         'spoonacularScore': 99.0, 
         'healthScore': 85.0,
         'creditText': 'Afrolems',
         'license': 'CC BY 4.0',
         'sourceName': 'Afrolems',
         'pricePerServing': 242.78,
         'extendedIngredients': [
            {
            'id': 2004, 
            'aisle': 'Spices and Seasonings', 
            'image': 'bay-leaves.jpg',
            'consitency': 'solid', 
            'name': 'bay leaves', 
            'original': 'A handful of chopped scent leaves',
            'originalString': 'A handful of chopped scent leaves', 
            'originalName': None, 
            'amount': 1.0, 
            'unit': 'handful',
            'meta': ['chopped'], 
            'metaInformation': ['chopped'], 
            'measures': {'us': {'amount': 1.0, 'unitShort': 'handful', 'unitLong': 'handful'},
            'metric': {'amount': 1.0, 'unitShort': 'handful', 'unitLong': 'handful'}}
            }, 
            {'id': 10115261, 'aisle': 'Seafood', 'image': 'fish-fillet.jpg', 'consitency': 'solid', 'name': 'fish', 'original': '1 medium sized Smoked Fish (optional)', 'originalString': '1 medium sized Smoked Fish (optional)', 'originalName': None, 'amount': 1.0, 'unit': '', 'meta': ['smoked', 'medium sized'], 'metaInformation': ['smoked', 'medium sized'], 'measures': {'us': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}}}, 
            {'id': 11282, 'aisle': 'Produce', 'image': 'brown-onion.jpg', 'consitency': 'solid', 'name': 'onions', 'original': '1 Medium bulb of Onions', 'originalString': '1 Medium bulb of Onions', 'originalName': None, 'amount': 1.0, 'unit': '', 'meta': ['medium'], 'metaInformation': ['medium'], 'measures': {'us': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}}},
            {'id': 4055, 'aisle': 'Ethnic Foods', 'image': 'vegetable-oil.jpg', 'consitency': 'liquid', 'name': 'palm oil', 'original': '2 cooking spoons of Palm oil (Moderate if you are watching your weight)', 'originalString': '2 cooking spoons of Palm oil (Moderate if you are watching your weight)', 'originalName': None, 'amount': 2.0, 'unit': '', 'meta': ['(Moderate if you are watching your weight)'], 'metaInformation': ['(Moderate if you are watching your weight)'], 'measures': {'us': {'amount': 2.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 2.0, 'unitShort': '', 'unitLong': ''}}},
            {'id': 11821, 'aisle': 'Produce', 'image': 'red-bell-pepper.png', 'consitency': 'solid', 'name': 'red bell pepper', 'original': '1 red bell pepper', 'originalString': '1 red bell pepper', 'originalName': None, 'amount': 1.0, 'unit': '', 'meta': ['red'], 'metaInformation': ['red'], 'measures': {'us': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 1.0, 'unitShort': '', 'unitLong': ''}}},
            {'id': 20444, 'aisle': 'Pasta and Rice', 'image': 'rice-white-uncooked.jpg', 'consitency': 'solid', 'name': 'rice', 'original': '2 cups Rice', 'originalString': '2 cups Rice', 'originalName': None, 'amount': 2.0, 'unit': 'cups', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 2.0, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 473.176, 'unitShort': 'g', 'unitLong': 'grams'}}},
            {'id': 2047, 'aisle': 'Spices and Seasonings', 'image': 'salt.jpg', 'consitency': 'solid', 'name': 'salt', 'original': 'Salt', 'originalString': 'Salt', 'originalName': None, 'amount': 3.0, 'unit': 'servings', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 3.0, 'unitShort': 'servings', 'unitLong': 'servings'}, 'metric': {'amount': 3.0, 'unitShort': 'servings', 'unitLong': 'servings'}}},
            {'id': 10011819, 'aisle': 'Produce;Ethnic Foods', 'image': 'habanero-pepper.jpg', 'consitency': 'solid', 'name': 'scotch bonnet chili peppers', 'original': '2 scotch bonnet peppers', 'originalString': '2 scotch bonnet peppers', 'originalName': None, 'amount': 2.0, 'unit': '', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 2.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 2.0, 'unitShort': '', 'unitLong': ''}}},
            {'id': 1042027, 'aisle': None, 'image': 'spices.png', 'consitency': 'solid', 'name': 'seasoning', 'original': 'Seasoning', 'originalString': 'Seasoning', 'originalName': None, 'amount': 3.0, 'unit': 'servings', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 3.0, 'unitShort': 'servings', 'unitLong': 'servings'}, 'metric': {'amount': 3.0, 'unitShort': 'servings', 'unitLong': 'servings'}}},
            {'id': 15152, 'aisle': 'Seafood', 'image': 'shrimp.jpg', 'consitency': 'liquid', 'name': 'shrimp', 'original': '1 cup Dried Shrimp (optional) / 1 tablespoon of crayfish powder', 'originalString': '1 cup Dried Shrimp (optional) / 1 tablespoon of crayfish powder', 'originalName': None, 'amount': 1.0, 'unit': 'cup', 'meta': ['dried'], 'metaInformation': ['dried'], 'measures': {'us': {'amount': 1.0, 'unitShort': 'cup', 'unitLong': 'cup'}, 'metric': {'amount': 236.588, 'unitShort': 'g', 'unitLong': 'grams'}}},
            {'id': 10011457, 'aisle': 'Produce', 'image': 'spinach.jpg', 'consitency': 'solid', 'name': 'spinach', 'original': '1/2 small bunch of spinach', 'originalString': '1/2 small bunch of spinach', 'originalName': None, 'amount': 0.5, 'unit': 'bunch', 'meta': ['small'], 'metaInformation': ['small'], 'measures': {'us': {'amount': 0.5, 'unitShort': 'bunch', 'unitLong': 'bunches'}, 'metric': {'amount': 0.5, 'unitShort': 'bunch', 'unitLong': 'bunches'}}},
            {'id': 11529, 'aisle': 'Produce', 'image': 'tomato.jpg', 'consitency': 'solid', 'name': 'tomatoes', 'original': '2 medium tomatoes', 'originalString': '2 medium tomatoes', 'originalName': None, 'amount': 2.0, 'unit': '', 'meta': ['medium'], 'metaInformation': ['medium'], 'measures': {'us': {'amount': 2.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 2.0, 'unitShort': '', 'unitLong': ''}}}
        ],
        'id': 716275,
        'title': 'Native Jollof Rice - Iwuk Edesi',
        'readyInMinutes': 45,
        'servings': 3,
        'image': 'https://spoonacular.com/recipeImages/716275-556x370.jpg',
        'imageType': 'jpg',
        'cuisines': ['african'],
        'dishTypes': ['lunch', 'main course', 'main dish', 'dinner'],
        'diets': ['gluten free', 'dairy free', 'pescatarian'],
        'occasions': [],
        'winePairing': {'pairedWines': ['pinotage', 'chenin blanc', 'riesling'],
        'pairingText': "Jollof Rice on the menu? Try pairing with Pinotage, Chenin Blanc, and Riesling. The best wine for African dishes will depend on the dish, but a fruity, aromatic white wine is a safe bet for spicy dishes while pinotage would be a traditional match for South African cuisine. The L'Ecole 41 Chenin Blanc with a 4.4 out of 5 star rating seems like a good match. It costs about 18 dollars per bottle.",
        'productMatches': [{'id': 437316, 'title': "L'Ecole 41 Chenin Blanc", 'description': 'This fresh and vibrant Chenin Blanc shows abundant expressive aromatics of jasmine, passion fruit, and orange blossom with flavors of star fruit and apple on a balanced, crisp mineral finish.', 'price': '$17.99', 'imageUrl': 'https://spoonacular.com/productImages/437316-312x231.jpg', 'averageRating': 0.8800000000000001, 'ratingCount': 6.0, 'score': 0.8273684210526318, 'link': 'https://click.linksynergy.com/deeplink?id=*QCiIS6t4gA&mid=2025&murl=https%3A%2F%2Fwww.wine.com%2Fproduct%2Flecole-41-chenin-blanc-2013%2F132051'}]},
        'instructions': 'Wash the rice and parboil. (This means boil for a short time and it shouldn’t be completely soft)Blend your tomatoes and peppers and boil to remove excess water.Chop your onions and vegetables and set aside.Heat up the palm oil and fry the onions and blended pepper mix.Season with salt and any seasoning of your choice. You could also use leftover stock to season it if you have.Add your rice to the pot and stir. Reduce the burner to very low heat so the rice can cook properly. if you need to add a little water, you should but make sure it is very little so the rice isn’t soaking in water.Wash the smoked fish and add to the pot of rice as it’s cooking along with the dried shrimps if you have or crayfish powder.Once the rice is soft, increase the heat and add the chopped vegetables. Stir in and allow to simmer for one minute.This dish is best served slightly warm not hot so the flavours really come out. Let me know if you try it out.',
        'analyzedInstructions': [{'name': '', 'steps': [{'number': 1, 'step': 'Wash the rice and parboil. (This means boil for a short time and it shouldn’t be completely soft)Blend your tomatoes and peppers and boil to remove excess water.Chop your onions and vegetables and set aside.', 'ingredients': [{'id': 11529, 'name': 'tomato', 'image': 'tomato.jpg'}, {'id': 11282, 'name': 'onion', 'image': 'brown-onion.jpg'}, {'id': 20444, 'name': 'rice', 'image': 'rice-white-uncooked.jpg'}], 'equipment': []}, {'number': 2, 'step': 'Heat up the palm oil and fry the onions and blended pepper mix.Season with salt and any seasoning of your choice. You could also use leftover stock to season it if you have.', 'ingredients': [{'id': 1042027, 'name': 'seasoning', 'image': 'spices.png'}, {'id': 4055, 'name': 'palm oil', 'image': 'vegetable-oil.jpg'}, {'id': 11282, 'name': 'onion', 'image': 'brown-onion.jpg'}, {'id': 2047, 'name': 'salt', 'image': 'salt.jpg'}], 'equipment': []}, {'number': 3, 'step': 'Add your rice to the pot and stir. Reduce the burner to very low heat so the rice can cook properly. if you need to add a little water, you should but make sure it is very little so the rice isn’t soaking in water.Wash the smoked fish and add to the pot of rice as it’s cooking along with the dried shrimps if you have or crayfish powder.Once the rice is soft, increase the heat and add the chopped vegetables. Stir in and allow to simmer for one minute.This dish is best served slightly warm not hot so the flavours really come out.', 'ingredients': [{'id': 15152, 'name': 'shrimp', 'image': 'shrimp.jpg'}, {'id': 20444, 'name': 'rice', 'image': 'rice-white-uncooked.jpg'}], 'equipment': [{'id': 404752, 'name': 'pot', 'image': 'stock-pot.jpg'}]}, {'number': 4, 'step': 'Let me know if you try it out.', 'ingredients': [], 'equipment': []}]}],
        'creditsText': 'Afrolems'}
    }
    return results[details_id]


class MockFlaskTests(TestCase):
    """Flask tests that show off mocking."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        # User 1 is logged in
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        server.get_recipes = _mock_get_recipes
       
        server.get_recipe_by_id = _mock_get_recipe_by_id

    
    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        


    def test_results(self):        
        result = self.client.get("/results?cuisine_type=african&diet_restrictions=pescetarian&intolerances=gluten")

        self.assertIn(b"Native Jollof Rice - Iwuk Edesi", result.data)
        self.assertIn(b"button", result.data)
        self.assertIn(b"<h2>Servings:&nbsp;3</h2>", result.data)
        self.assertIn(b"<h2>Cooking Time In Minutes:&nbsp;45</h2>", result.data)
        self.assertIn(b"https://spoonacular.com/recipeImages/716275-556x370.jpg", result.data)        
        

    def test_save(self):


        results = self.client.post("/save", 
                            data={
                                "recipeId":"716275",
                                "recipeTitle": "Native Jollof Rice - Iwuk Edesi",
                                "recipeUrl":"http://www.afrolems.com/2013/07/19/native-jollof-rice-iwuk-edesi/"
                            },
                            follow_redirects=False)

        fav_recipe = Favorite.query.filter_by(user_id=1,
                                              spoonacular_id=716275).first()

        self.assertIsNotNone(fav_recipe)

        #also test to see that correct json was returned


    def test_favorites(self):
        results = self.client.get("/favorites/716275")
        
        self.assertIn(b"Native Jollof Rice - Iwuk Edesi", results.data)

    def test_remove(self):
        results = self.client.post("/remove", data={"recipe_id": "716275"}, follow_redirects=False)

        take_out_recipe = Favorite.query.filter_by(user_id=1, spoonacular_id="716275").first()
        
        self.assertIsNone(take_out_recipe)
  
    
    def test_recipe_by_name(self):
        results = self.client.get("/recipe-by-name")
        recipe_name = Recipe.query.filter_by(title="Native Jollof Rice - Iwuk Edesi", spoonacular_id="716275").first()

        self.assertIsNone(recipe_name)


         

if __name__ == "__main__":
    import unittest

    unittest.main()
