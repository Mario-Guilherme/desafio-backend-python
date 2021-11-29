from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config_by_name
from biblioteca.controller import ns
from database import init_db, db_session


app = Flask(__name__)
app.config.from_object(config_by_name["development"])
api = Api(app, title="API Biblioteca", version="0.1.0")
app.wsgi_app = ProxyFix(app.wsgi_app)

api.add_namespace(ns, path="/biblioteca")
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    # Remover sessões ao final de cada request
    db_session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
