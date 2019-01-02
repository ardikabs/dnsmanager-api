from ...parser import pagination

record_parameter = pagination.copy()
record_parameter.add_argument("record_name", type=str, help="A record name")
record_parameter.add_argument("record_type", type=str, help="A record type")