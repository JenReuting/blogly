"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):

    """ User """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        """Show user id, first_name, last_name"""
        return f"""<User 
                id={self.id} first_
                name={self.first_name} 
                last_name={self.last_name}>"""

    # @classmethod
    # def create_user():
    #     db.session.add()
