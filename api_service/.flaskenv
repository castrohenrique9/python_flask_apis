FLASK_ENV=development
FLASK_APP=app:create_app
SECRET_KEY=yoursecretkey
DATABASE_URI=sqlite:///api_service.sqlite3

URL_EXTERNAL_STOCK=http://127.0.0.1:5000/api/v1/stock/?q={}
QUERY_ROW_LIMIT_DEFAULT=5
