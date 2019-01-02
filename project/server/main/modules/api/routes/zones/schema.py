
from marshmallow import pre_dump, pre_load, post_dump, post_load, fields as base_fields
from server.app import ma
from server.main.models import (
    ZoneModel,
    RecordModel,
    RecordTypeModel
)
from server.extensions.celery.tasks import dns as dns_task
from ...http_exceptions import *
from ..records.schema import RecordSchema

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

class ZoneSchema(BaseSchema):

    class Meta:
        model = ZoneModel
        dump_only = (
            ZoneModel.uuid.key,
            ZoneModel.created_at.key,
            ZoneModel.modified_at.key,
        )
    
    @post_load
    def make_instance(self, data):
        
        zone = ZoneModel.get_name(data.get("name"))

        if zone:
            raise UnprocessableError(ZoneModel.__modelname__, zone.name)
        
        zone = ZoneModel(**data)
        zone.new()
        dns_task.import_record.delay(zone_uuid=zone.uuid)
        return zone
    
class RecordZoneSchema(RecordSchema):
    rtype_obj = ma.Field(load_only=True, required=True)
    zone_obj = ma.Field(load_only=True, required=True)

    zone = ma.Nested(ZoneSchema, dump_only=True, exclude=("created_at", "modified_at", "keyring_name", "keyring_value"))
    class Meta(RecordSchema.Meta):
        pass
    
    @post_dump
    def bundler(self, data):
        zone = data.pop("zone")
        dict_ = {"zone": zone, "record": data}
        return dict_
    
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

        record = RecordModel(
            name=data.get("name"),
            content=data.get("content"),
            ttl=data.get("ttl"),
            rtype=rtype,
            zone=zone
        )
        record.new()
        return record