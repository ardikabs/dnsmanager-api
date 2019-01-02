
from flask_restplus import fields
from . import api
from ..records.serializer import (
    base_field as base_record_field,
    record_field as record_field
)
from ...util import pagination_model

base_field = api.model("DNSZone", {
    "uuid": fields.String(readonly=True, description="DNS Zone UUID"),
    "name": fields.String(required=True, description="DNS Zone Name"),
    "server_name": fields.String(required=True, description="DNS Server Name of the DNS Zone"),
    "server_address": fields.String(required=True, description="DNS Server IPv4 Address of the DNS Zone"),
    "keyring_name": fields.String(required=True, description="DNS Zone Keyring Name"),
    "keyring_value": fields.String(required=True, description="DNS Zone Keyring Value")
})

zone_response_plural = api.model("ResponseDNSZone_0", {
    "success": fields.Boolean(description="Response Success Flag"),
    "data": fields.Nested(base_field,skip_none=True),
    "pagination": fields.Nested(pagination_model, skip_none=True)
})

zone_response_singular = api.model("ResponseDNSZone_1", {
    "success": fields.Boolean(description="Response Success Flag"),
    "data": fields.Nested(base_field,skip_none=True)
})


zone_with_record_field = api.model("DNSZonewithDNSRecord", {
    "zone": fields.Nested(base_field, skip_none=True),
    "record": fields.Nested(record_field, skip_none=True)
})

zone_with_record_response_plural = api.clone("ResponseDNSZonewithDNSRecord_0", zone_response_plural, {
    "data": fields.Nested(zone_with_record_field)
})

zone_with_record_response_singular = api.clone("ResponseDNSZonewithDNSRecord_1", zone_response_singular, {
    "data": fields.Nested(zone_with_record_field)
})