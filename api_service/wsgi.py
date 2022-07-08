from api_service.app import create_app
from api_service.extensions import db

app = create_app()

@app.before_first_request
def create_database():
    db.create_all()
