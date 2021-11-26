from flask import request, abort, make_response
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from flask.wrappers import Response
from sqlalchemy.sql.expression import delete


from biblioteca.models import Livro, Autor
from biblioteca.schema import LivroSchema, AutorSchema
from biblioteca.service import LivroService


ns = Namespace("Biblioteca", description="Back-end Sistema de biblioteca")


@ns.route("/obras/")
class BibliotecaResource(Resource):
    def get(self) -> Response:
        livro_service = LivroService()
        return Response(response=livro_service.get_all(), status=200)

    # @accepts(schema=BibliotecaSchema,api=ns)
    def post(self) -> Response:
        data = request.json
        livro_service = LivroService()
        return Response(response=livro_service.create(data_atributte=data), status=201)


@ns.route("/obras/<int:id>")
class BibliotecaIdResource(Resource):
    def delete(self, id):
        livro = LivroService().find_id_livro(id)

        if livro is not None:
            autores = LivroService().find_id_autor(livro.id)
            LivroService().delete_by_id(livro, autores)
            return make_response(f"Livro {id} deleted", 200)
        else:
            abort(404, f"Livro not found for Id: {id}")
