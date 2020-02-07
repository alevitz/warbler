"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app
import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            # id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()
        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """Does repr work?"""

        u = User(
            # id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(
            u.__repr__(), f"<User #{u.id}: {u.username}, {u.email}>")

    def test_is_following(self):
        """Does is_following work?"""

        u1 = User(
            email="one@test.com",
            username="testuserone",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="two@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(u1, u2)
        db.session.commit()

        u1.following.append(u2)
        db.session.add(u1)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), True) 

    def test_is_not_following(self):
        """Does is_following work when false?"""

        u1 = User(
            email="one@test.com",
            username="testuserone",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="two@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(u1, u2)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), False) 

    def test_is_followed_by(self):
        """Does is_following work?"""

        u1 = User(
            email="one@test.com",
            username="testuserone",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="two@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(u1, u2)
        db.session.commit()

        u1.following.append(u2)
        db.session.add(u1)
        db.session.commit()

        self.assertEqual(u2.is_followed_by(u1), True) 

    def test_is_not_followed_by(self):
        """Does is_following work when false?"""

        u1 = User(
            email="one@test.com",
            username="testuserone",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="two@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        
        db.session.add(u1, u2)
        db.session.commit()

        self.assertEqual(u2.is_followed_by(u1), False) 

    def test_create_user(self):
        """Does create a new user work given valid credentials?"""

        u1 = User(
            email="one@test.com",
            username="testuserone",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()

        user = User.query.get(u1.id)
        user_id = user.id
        user_email = user.email
        user_username = user.username

        self.assertEqual(user_id, u1.id)
        self.assertEqual(user_email, f"{u1.email}")
        self.assertEqual(user_username, f"{u1.username}")

    # def test_do_not_create_user(self):
    #     """Does create a new user fail given invalid credentials?"""

    #     u1 = User.signup("testuserone", "one@test.com", "HASHED_PASSWORD", "/static/image.png")

    #     u2 = User.signup("testusertwo", "onetwo@test.com", "HASHED_PASSWORD", "/static/image.png")

    #     db.session.add(u1, u2)
    #     db.session.commit()

    #     # result = db.session.query("SELECT * FROM users WHERE id = " u2.id).one()

    #     self.assertEqual(u1.email, 'one@test.com')
