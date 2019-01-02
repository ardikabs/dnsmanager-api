
from flask_restplus import fields
from . import api
from ...util import pagination_model

base_field = api.model("DNSRecord_0", {
    "uuid": fields.String(readonly=True, description="DNS Record UUID"),
    "name": fields.String(required=True, description="DNS Record Name"),
    "rtype": fields.String(required=True, description="DNS Record Type"),
    "content": fields.String(required=True, description="DNS Record Content"),
    "ttl": fields.Integer(required=True, default=300, description="DNS Record TTL Value"),
    "created_at": fields.DateTime(readonly=True, description="Created Timestamp"),
    "modified_at": fields.DateTime(readonly=True, description="Modified Timestamp")
})

record_field = api.inherit("DNSRecord_1", base_field, {
    "zone": fields.String(required=True, description="DNS Zone Name")
})

record_response_singular = api.model("ResponseDNSRecordSingular", {
    "success": fields.Boolean(description="Response Success Flag"),
    "data": fields.Nested(record_field,skip_none=True)
})

record_response_plural = api.model("ResponseDNSRecordPlural", {
    "success": fields.Boolean(description="Response Success Flag"),
    "data": fields.Nested(record_field,skip_none=True),
    "pagination": fields.Nested(pagination_model,skip_none=True)
})