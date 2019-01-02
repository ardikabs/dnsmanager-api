from flask_restplus import fields
from . import api_v1
from copy import deepcopy

class BaseException(Exception):
    def __init__(self, message):
        self.message = message

class BadRequestError(BaseException): 
    title = "Bad Request"
    code = 400
    def __init__(self, message):
        self.message = message

class NoResultFoundError(BaseException):
    title = "Resource Not Found"
    code = 404
    def __init__(self, model_name, id):
        super().__init__(f"{model_name} <{id}> not found")    

class UnauthorizedError(BaseException):
    title = "Unauthorized Access"
    code = 401
    def __init__(self, message):
        super().__init__(message)

class ForbiddenError(BaseException):
    title = "Forbidden Access"
    code = 403
    def __init__(self, message):
        super().__init__(message)

class UnprocessableError(BaseException):
    title = "Unprocessable Entity (Conflict)"
    code = 422
    def __init__(self, model_name, identifier, message=None):
        if not message:
            message = f"{model_name} <{identifier}> already exist"
        else:
            message = f"{model_name}<{identifier}> {message}"
        super().__init__(message)

class InternalError(BaseException):
    title = "Server Internal Error"
    code = 500
    def __init__(self, message):
        super().__init__(message)


base_error_schema = {
    "success": fields.Boolean(description="Response Success Flag"),
    "title": fields.String(description="Error Title"),
    "message": fields.String(description="Error Message")
}

bad_request_field = api_v1.model("HTTPError400", deepcopy(base_error_schema))
unauthorized_field = api_v1.model("HTTPError401", deepcopy(base_error_schema))
forbidden_field = api_v1.model("HTTPError403", deepcopy(base_error_schema))
no_result_field = api_v1.model("HTTPError404", deepcopy(base_error_schema))
unprocessable_entity_field = api_v1.model("HTTPError422", deepcopy(base_error_schema))
internal_error_field = api_v1.model("HTTPError500", deepcopy(base_error_schema))

@api_v1.errorhandler(BadRequestError)
@api_v1.marshal_with(bad_request_field, code=400)
def handle_bad_request(error):
    return {"success": False, "title": error.title, "message": error.message}, error.code

@api_v1.errorhandler(UnauthorizedError)
@api_v1.marshal_with(unauthorized_field, code=401)
def handle_unauthorized_access(error):
    return {"success": False, "title": error.title, "message": error.message}, error.code

@api_v1.errorhandler(ForbiddenError)
@api_v1.marshal_with(forbidden_field, code=403)
def handle_forbidden_access(error):
    return {"success": False, "title": error.title, "message": error.message}, error.code

@api_v1.errorhandler(NoResultFoundError)
@api_v1.marshal_with(no_result_field, code=404)
def handle_no_result_found(error):
    return {"success": False, "title": error.title, "message": error.message}, error.code

@api_v1.errorhandler(UnprocessableError)
@api_v1.marshal_with(unprocessable_entity_field, code=422)
def handle_unprocessable_entity(error):
    return {"success": False, "title": error.title, "message": error.message}, error.code

@api_v1.errorhandler(InternalError)
@api_v1.marshal_with(internal_error_field, code=500)
def handle_internal_error(error):
    return {"success": False, "title": error.title, "message": error.message}, error.code
