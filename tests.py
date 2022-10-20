from unittest import TestCase

from app import app, db
from models import User
# from models import DEFAULT_IMAGE_URL, User

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)


    def test_root_redirect(self):
        """Check if we get a redirect"""
        with self.client as c:
            resp = c.get('/')
            self.assertEqual(resp.location, "/users")
            self.assertEqual(resp.status_code, 302)


    def test_users_route(self):
        """Check the users list page"""
        with self.client as c:
            resp = c.get('/', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("user list  DO NOT CHANGE, FOR TESTING", html)

    def test_add_user(self):
        """Verify that add user works correctly"""
        with self.client as c:
            resp = c.post('/users/new',
                data={"first-name": 'Jennifer',
                    "last-name": 'Gates',
                    "image-url": 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/fb-master-template-2-47-1659701917.jpg'},
                    follow_redirects=True)

            # test that user is in the html
            html = resp.get_data(as_text=True)
            self.assertIn("Jennifer Gates", html)
            # test that this newly created user is in the db
            users = User.query.filter_by(first_name = "Jennifer").all()
            self.assertEqual(len(users), 1)
            # test that this newly created user is not in the db
            users = User.query.filter_by(first_name = "Jenniferzdadsasf").all()
            self.assertNotEqual(len(users), 1)
            # test thatt some random user does not exist in the db
            fake_users = User.query.filter_by(first_name = "Elon").all()
            self.assertNotEqual(len(fake_users), 1)


    def test_edit_user(self):
        """Test the edit user route"""
        with self.client as c:
            c.post('/users/new',
                data={"first-name": 'Chris',
                    "last-name": 'Lim',
                    "image-url": 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/fb-master-template-2-47-1659701917.jpg'},
                    follow_redirects=True)

            users = User.query.filter_by(first_name = "Chris").all()
            user = users[0]
            user_id = user.id

            # check that get redirect to /users
            # check that edited user is in the /users
            resp = c.post(f'/users/{user_id}/edit', 
                        data={"first-name": "CHRIS", "last-name": "LIM"}, 
                        follow_redirects=True)
            users_list_html = resp.get_data(as_text=True)
            self.assertIn("CHRIS LIM", users_list_html)
            self.assertNotIn('Chris Lim', users_list_html)

            # check that edited user page is updated
            user_detail_resp = c.get(f'/users/{user_id}')
            user_detail_html = user_detail_resp.get_data(as_text=True)
            self.assertIn('CHRIS LIM', user_detail_html)
            self.assertNotIn('Chris Lim', user_detail_html)

    def test_delete_user(self):
        """Test the delete user route"""
        with self.client as c:

            users = User.query.filter_by(first_name = "test_first").all()
            test_user = users[0]
            test_user_id = test_user.id

            c.post(f'/users/{test_user_id}/delete', follow_redirects=True)

            # check user not in db
            users = User.query.filter_by(first_name = "test_first").all()
            self.assertEqual(len(users), 0)

            # check the deleted user detail page
            resp = c.get(f'/users/{test_user_id}')
            self.assertEqual(resp.status_code, 404)
            

            






