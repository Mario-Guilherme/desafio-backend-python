from flask_restx import Namespace, Resource

from models import Biblioteca
from schema import BibliotecaSchema
from service import BibliotecaService
from interface import BibliotecaInterface


api = Namespace("Biblioteca", description="Back-end Sistema de biblioteca")


@api.route("/obras")
class BibliotecaResource(Resource):
    pass
