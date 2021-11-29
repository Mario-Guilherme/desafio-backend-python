import json

from flask import request, abort, redirect, flash, jsonify
from flask_restx import Namespace, Resource
from flask.wrappers import Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from biblioteca.models import Livro, Autor
from biblioteca.schema import LivroSchema, AutorSchema
from biblioteca.service import LivroService
from biblioteca.task import send_email

import os


ns = Namespace("Biblioteca", description="Back-end Sistema de biblioteca")

upload_parser = ns.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


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


@ns.route("/obras/<int:id>/")
class BibliotecaIdResource(Resource):
    def put(self, id: int) -> Response:
        livro_service = LivroService()
        livro = livro_service.find_id_livro(id)
        data = request.json

        if livro is None:
            abort(404, f"Livro not found for Id: {id}")
        else:
            autores = livro_service.find_id_autor(livro.id)
            livro_service.update_livro(
                livro, data["titulo"], data["editora"], data["foto"]
            )
            livro_service.update_autor(autores, data["autores"], livro.id)

        return Response(response=json(data), status=200)

    def delete(self, id):
        livro = LivroService().find_id_livro(id)

        if livro is not None:
            autores = LivroService().find_id_autor(livro.id)
            LivroService().delete_by_id(livro, autores)
            return Response(response=f"Livro {id} deleted", status=200)
        else:
            abort(404, f"Livro not found for Id: {id}")


@ns.route("/upload-obras")
@ns.expect(upload_parser)
class ObrasCsv(Resource):
    def post(self) -> None:

        args = upload_parser.parse_args()

        if "file" not in args:
            flash("No file part")
            return redirect(args.url)
        uploaded_file = args["file"]

        if uploaded_file.filename == "":
            flash("No Selected file")
            return redirect(args.url)
        if uploaded_file and LivroService().allowed_file(uploaded_file.filename):
            file_name = secure_filename(uploaded_file.filename)
            LivroService().spawn_dict_temp()
            path = os.path.join(os.getcwd() + "/uploads", file_name)

            uploaded_file.save(path)

            LivroService().save_data_csv_db(path)

            LivroService().delete_csv(path)

            return Response(status=200)


@ns.route("/file-obras/<string:email>")
class BibliotecaNotify(Resource):
    def post(self, email: str) -> Response:

        send_email.delay(email)

        return Response(status=202)
