
from marshmallow import pre_dump, pre_load, post_dump, post_load, fields as base_fields
from server.app import ma
from server.main.models import (
    ZoneModel,
    RecordModel,
    RecordTypeModel
)
from ...http_exceptions import *
from server.main.services.dns_service import DNSService

class BaseSchema(ma.ModelSchema):
    def response_dump(self, obj, query=None, queryset=None, parameter=None):
        response_json = {"success": True}
        data, err = self.dump(obj)
        if err: 
            raise InternalError(err)
        response_json["data"] = data        

        if query and queryset and parameter:
            import math
            offset = parameter["offset"]
            limit = parameter["limit"]
            total_item = query.count()

            page = (limit*offset/limit)
            items = queryset.count()
            total_page = math.ceil(total_item/limit) - 1

            paging = {}
            paging["item_per_page"] = items
            paging["page"] = page
            paging["total_item"] = total_item 
            paging["total_page"] = total_page
            response_json["pagination"] = paging
        
        return response_json
        
class RecordSchema(BaseSchema):
    rtype_obj = ma.Field(load_only=True)
    zone_obj = ma.Field(load_only=True)

    rtype = base_fields.Method("rtype_solver", dump_only=True)
    zone = base_fields.Method("zone_solver", dump_only=True)

    def rtype_solver(self, obj): return obj.rtype.name
    def zone_solver(self, obj): return obj.zone.name

    class Meta:
        model = RecordModel
        dump_only = (
            RecordModel.uuid.key,
            RecordModel.created_at.key,
            RecordModel.modified_at.key,
        )
    
    @pre_load
    def pre_process(self, in_data):
        zone_name = in_data.pop("zone")
        zone = ZoneModel.get_name(zone_name)
        if not zone:
            raise NoResultFoundError(ZoneModel.__modelname__, zone_name)
        
        rtype_name = in_data.pop("rtype")
        rtype = RecordTypeModel.get(rtype_name)
        if not rtype:
            raise NoResultFoundError(RecordTypeModel.__modelname__, rtype_name)

        in_data["zone_obj"] = zone
        in_data["rtype_obj"] = rtype
        return in_data


    @post_load
    def make_instance(self, data):
        zone = data.pop("zone_obj")
        rtype = data.pop("rtype_obj")

        record = RecordModel.query.filter_by(
            name=data.get("name"),
            zone=zone
        ).first()
        if record:
            raise UnprocessableError(RecordModel.__modelname__, record.name)

        try:
            record = RecordModel(
                name=data.get("name"),
                content=data.get("content"),
                ttl=data.get("ttl"),
                rtype=rtype,
                zone=zone
            )
            record.new()
        except ValueError as e:
            raise InternalError(str(e))
        else:
            return record