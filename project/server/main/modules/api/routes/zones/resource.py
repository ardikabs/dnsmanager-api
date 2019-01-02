
from flask_restplus import Resource

from . import api
from .schema import *
from .serializer import *
from .parameter import *

from ...decorators import *
from ...parser import pagination

@api.route("/")
@api.response(code=401, description="Unauthorized Access", model="HTTPError401")
@api.response(code=403, description="Forbidden Access", model="HTTPError403")
@api.response(code=404, description="Record Not Found", model="HTTPError404")
class ZoneCollection(Resource):
    
    @api.marshal_with(zone_response_plural, code=200)
    @api.expect(pagination, validate=True)
    def get(self):
        """ Display All Available DNS Zone """
        parameter = pagination.parse_args()
        limit = parameter["limit"]
        offset = parameter["offset"]

        query = ZoneModel.query
        queryset = query.order_by(ZoneModel.created_at).limit(limit).offset(limit*offset)
        zones = queryset.all()
        return ZoneSchema(many=True)\
            .response_dump(zones, query=query, queryset=queryset, parameter=parameter)

    @api.marshal_with(zone_response_singular, code=201)
    @api.expect(base_field, validate=True)
    def post(self):
        """ Add new DNS Zone """
        zone, err = ZoneSchema().load(api.payload)
        if err:
            raise BadRequestError(err)
        return ZoneSchema().response_dump(zone), 201

@api.route("/<string:zone_name>/")
@api.response(code=401, description="Unauthorized Access", model="HTTPError401")
@api.response(code=403, description="Forbidden Access", model="HTTPError403")
@api.response(code=404, description="Record Not Found", model="HTTPError404")
class ZoneDetail(Resource):

    @api.marshal_with(zone_response_singular, code=200)
    def get(self, zone_name):
        """ Show Detail DNSZone by selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        return ZoneSchema().response_dump(zone)

    @api.response(code=204, description="DNS Zone Updated")
    @api.expect(base_field)
    def put(self, zone_name):
        """ Update DNS Zone Information by selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        zone.update(**api.payload)
        return None, 204

    @api.response(code=204, description="DNS Zone Deleted")
    def delete(self, zone_name):
        """ Delete DNS Zone by selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        zone.delete()
        return None, 204
        
@api.route("/<string:zone_name>/records/")
@api.response(code=401, description="Unauthorized Access", model="HTTPError401")
@api.response(code=403, description="Forbidden Access", model="HTTPError403")
@api.response(code=404, description="Record Not Found", model="HTTPError404")
class ZoneRecordCollection(Resource):

    @api.marshal_with(zone_with_record_response_plural, code=200)
    @api.expect(record_in_zone_parameter, validate=True)
    def get(self, zone_name):
        """ Display All DNS Records by by selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        filterset = dict(zone=zone)

        parameter = record_in_zone_parameter.parse_args()
        limit = parameter["limit"]
        offset = parameter["offset"]
        record_type = parameter["record_type"]
        record_name = parameter["record_name"]

        if record_type:
            rtype = RecordTypeModel.get(record_type)
            if not rtype:
                raise NoResultFoundError(RecordTypeModel.__modelname__, record_type)
            filterset.update(dict(rtype=rtype))
        if record_name:
            filterset.update(dict(name=record_name))

        query = RecordModel.query.filter_by(**filterset)
        queryset = query.order_by(RecordModel.created_at).limit(limit).offset(limit*offset)
        records = queryset.all()
        return RecordZoneSchema(many=True)\
            .response_dump(records, query=query, queryset=queryset, parameter=parameter)

    @api.marshal_with(zone_with_record_response_singular, code=201)
    @api.expect(base_record_field, validate=True)
    def post(self, zone_name):
        """ Add new DNS Record to selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)

        record, err = RecordZoneSchema().load(api.payload)
        if err:
            raise BadRequestError(err)
        return RecordZoneSchema().response_dump(record), 201

@api.route("/<string:zone_name>/records/<string:record_uuid>/")
@api.response(code=401, description="Unauthorized Access", model="HTTPError401")
@api.response(code=403, description="Forbidden Access", model="HTTPError403")
@api.response(code=404, description="Record Not Found", model="HTTPError404")
class ZoneRecordInfo(Resource):

    @api.marshal_with(zone_with_record_response_singular, code=200)
    def get(self, zone_name, record_uuid):
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        
        record = RecordModel.query.filter_by(uuid=record_uuid,zone=zone).first()
        if not record:
            raise NoResultFoundError(RecordModel.__modelname__, record_uuid)
        """ Show DNS Records by UUID on selected DNS Zone """
        return RecordZoneSchema().response_dump(record)

    @api.response(code=204, description="DNS Record Updated")
    @api.expect(base_record_field)
    def put(self, zone_name, record_uuid):
        """ Update DNS Records Information by UUID on selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        
        record = RecordModel.query.filter_by(uuid=record_uuid,zone=zone).first()
        if not record:
            raise NoResultFoundError(RecordModel.__modelname__, record_uuid)
        
        record.update(**api.payload)
        return None, 204

    @api.response(code=204, description="DNS Record Deleted")
    def delete(self, zone_name, record_uuid):
        """ Delete DNS Records by UUID on selected DNS Zone """
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        
        record = RecordModel.query.filter_by(uuid=record_uuid,zone=zone).first()
        if not record:
            raise NoResultFoundError(RecordModel.__modelname__, record_uuid)
        
        record.delete()
        return None, 204