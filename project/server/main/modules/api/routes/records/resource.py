
from server.app import ma
from flask_restplus import Resource

from . import api
from .schema import *
from .serializer import *
from .parameter import *


from ...http_exceptions import *
from ...parser import *


@api.route("/")
@api.response(code=401, description="Unauthorized Access", model="HTTPError401")
@api.response(code=403, description="Forbidden Access", model="HTTPError403")
@api.response(code=404, description="Record Not Found", model="HTTPError404")
class RecordCollection(Resource):

    @api.marshal_with(record_response_plural, code=200)
    @api.expect(record_parameter, validate=True)
    def get(self):
        """ Display All Available Records """
        parameter = record_parameter.parse_args()
        limit = parameter["limit"]
        offset = parameter["offset"]
        record_type = parameter["record_type"]
        record_name = parameter["record_name"]

        filterset = {}
        if record_name:
            filterset.update(dict(name=record_name))
        if record_type:
            rtype = RecordTypeModel.get(record_type)
            if not rtype:
                raise NoResultFoundError(RecordTypeModel.__modelname__, record_type)
            filterset.update(dict(rtype=rtype))


        query = RecordModel.query.filter_by(**filterset)
        queryset = query.order_by(RecordModel.created_at).limit(limit).offset(limit*offset)
        records = queryset.all()
        return RecordSchema(many=True)\
            .response_dump(records, query=query, queryset=queryset, parameter=parameter)

    @api.marshal_with(record_response_singular, code=201)
    @api.expect(record_field, validate=True)
    def post(self):
        """ Display All Available Records """
        record, err = RecordSchema().load(api.payload)
        if err:
            raise BadRequestError(err)
        return RecordSchema().response_dump(record), 201

@api.route("/<string:uuid>/")
@api.response(code=401, description="Unauthorized Access", model="HTTPError401")
@api.response(code=403, description="Forbidden Access", model="HTTPError403")
@api.response(code=404, description="Record Not Found", model="HTTPError404")
class RecordItem(Resource):

    @api.marshal_with(record_response_singular, code=200)
    def get(self, uuid):
        """ Show Record Detail by Selected Record """
        record = RecordModel.get(uuid)
        if not record:
            raise NoResultFoundError(RecordModel.__modelname__, uuid)
        return RecordSchema().response_dump(record)

    @api.response(code=204, description="DNS Record Updated")
    @api.expect(base_field)
    def put(self, uuid):
        """ Update Information of Record by Selected Record """
        record = RecordModel.get(uuid)
        if not record:
            raise NoResultFoundError(RecordModel.__modelname__, uuid)
        record.update(**api.payload)
        return None, 204

    @api.response(code=204, description="DNS Record Deleted")
    def delete(self, uuid):
        """ Delete Selected Record """
        record = RecordModel.get(uuid)
        if not record:
            raise NoResultFoundError(RecordModel.__modelname__, uuid)
        record.delete()
        return None, 204