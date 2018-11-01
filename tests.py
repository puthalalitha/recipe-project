from unittest import TestCase
from server import app
from model import connect_to_db, db
from seed import example_data
from flask import session



class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_Homepage(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(b"Welcome to World Wide Recipes", result.data)


    def test_register_form(self):
        result = self.client.get("/register")
        self.assertIn(b"Register New User", result.data)


    def test_logout(self):
        result = self.client.get("/logout", follow_redirects=True)

        self.assertIn(b"logout", result.data)





class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
         

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "fluffy@gmail.com", "password": "111"},
                                  follow_redirects=True)
        self.assertIn(b"Login", result.data)


    def test_search(self):
        result = self.client.get("/search", follow_redirects=True)

        self.assertIn(b"Recipe Search Information", result.data)


    def test_register_process(self):
        result = self.client.post("/register",
                                  data={"email": "reddy@recipe.com",
                                        "password": "345"},
                                        follow_redirects=True)

        self.assertIn(b"Login", result.data)


    def test_recipe_by_name(self):
        result = self.client.get("/recipe-by-name", follow_redirects=True)

        self.assertIn(b"", result.data)

      


if __name__ == "__main__":
    import unittest
    unittest.main()
