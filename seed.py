from app import create_app
from app.extensions import db
from app.models import User

app = create_app()
with app.app_context():
    if not User.query.first():
        users = [
            User(name='Alice', api_key='alice_key'),
            User(name='Bob', api_key='bob_key'),
            User(name='Charlie', api_key='charlie_key')
        ]
        db.session.add_all(users)
        db.session.commit()
        print('Demo users created.')
    else:
        print('Users already exist.')
