from flask_restplus import reqparse

pagination = reqparse.RequestParser()
pagination.add_argument("offset", type=int, default=0, help="A number of item page")
pagination.add_argument("limit", type=int, default=20, help="A number of limit items")

jwt_parser = reqparse.RequestParser()
jwt_parser.add_argument(
    "Authorization", 
    type=str,
    required=True,
    location="headers",
    help="Bearer Access Token")

jwt_refresh_parser = reqparse.RequestParser()
jwt_refresh_parser.add_argument(
    "Authorization", 
    type=str,
    required=True,
    location="headers",
    help="Bearer Refresh Token")