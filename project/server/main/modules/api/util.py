
from flask_restplus import fields
from server.app import ma
from . import api_v1


pagination_model = api_v1.model("Pagination", {
    "item_per_page": fields.Integer(description="Number of item in a page"),
    "page": fields.Integer(description="Current Page"),
    "total_page": fields.Integer(description="Total Available Page"),
    "total_item": fields.Integer(description="Total Available Items")
})
