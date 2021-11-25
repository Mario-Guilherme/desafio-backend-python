from flask import Flask
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from flask.wrappers import Response

from models import Biblioteca
from schema import BibliotecaSchema
from service import BibliotecaService
from interface import BibliotecaInterface

app = Flask(__name__)

api = Namespace("Biblioteca", description="Back-end Sistema de biblioteca")


@api.route("/obras/")
class BibliotecaResource(Resource):
    @accepts(schema=BibliotecaSchema, api=api)
    @responds(schema=BibliotecaSchema)
    def get(self) -> Response:
        return Response(response=BibliotecaService.get_all(), status=200)


if __name__ == "main":
    app.run(port=5000, debug=False)
