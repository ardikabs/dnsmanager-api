from ...parser import pagination

record_in_zone_parameter = pagination.copy()
record_in_zone_parameter.add_argument("record_name", type=str, help="A record name")
record_in_zone_parameter.add_argument("record_type", type=str, help="A record type")