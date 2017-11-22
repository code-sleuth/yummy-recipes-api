import os
from app import set_app

# create an object pp
from app.models import db
app = set_app(config_name=os.getenv('APP_SETTINGS'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5005)
