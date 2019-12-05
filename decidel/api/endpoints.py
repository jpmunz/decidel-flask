import jsonschema

from flask import abort, request, Blueprint
from flask_restplus import Api, Resource

from .models import DecidelModel

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    doc="/docs",
    title="Decidel API",
    version="1.0",
    description="API for interacting with Decidels",
)

decidel = api.namespace("decidels", description="Core interactions with Decidels")
decidel_schema_model = decidel.schema_model("Decidel", DecidelModel.schema)


class DecidelResource(Resource):
    @staticmethod
    def validate_request(value):
        try:
            jsonschema.validate(request.json, DecidelModel.schema)
        except jsonschema.ValidationError as e:
            abort(400, e.message)


@decidel.route("/")
class DecidelList(DecidelResource):
    @decidel.expect(decidel_schema_model)
    @decidel.response(201, "Created", decidel_schema_model)
    @decidel.response(400, description="Invalid Decidel")
    def post(self):
        """
        Creates a new Decidel
        """

        self.validate_request(request.json)
        decidel = DecidelModel.create(request.json)

        return decidel.as_json(), 201


@decidel.route("/<string:id>")
class Decidel(DecidelResource):
    @decidel.response(200, "Success", decidel_schema_model)
    @decidel.response(404, description="Not Found")
    def get(self, id):
        """
        Gets a Decidel
        """

        decidel = DecidelModel.get_or_404(id)

        return decidel.as_json()

    @decidel.expect(decidel_schema_model)
    @decidel.response(200, "Success", decidel_schema_model)
    @decidel.response(400, description="Invalid Decidel")
    @decidel.response(404, description="Not Found")
    def put(self, id):
        """
        Updates a Decidel
        """

        decidel = DecidelModel.get_or_404(id)

        self.validate_request(request.json)
        decidel.update(request.json)

        return decidel.as_json()
