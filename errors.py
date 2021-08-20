class ParentException(Exception):
    pass


class CategoryDoesNotExist(ParentException):
    code = 404
    message = 'Category not found'


class ItemDoesNotExist(ParentException):
    code = 404
    message = 'Item not found'


class ItemNameDuplicate(ParentException):
    code = 400
    message = 'Item name already exists in destination category'


class InvalidCredentials(ParentException):
    code = 400
    message = 'Invalid username or password'


class UsernameAlreadyExists(ParentException):
    code = 400
    message = 'Username already exists'


class UserForbidden(ParentException):
    code = 403
    message = 'User is forbidden to perform this action ' \
              '(user is not item creator)'


class ValidateSchemaError(ParentException):
    code = 400
    message = 'Something is wrong in the request'


# handle custom errors
def handle_custom_errors(e):
    return {'message': e.message}, e.code


# Handle other HTTP Exceptions
def handle_http_exception(e):
    return {'message': e.description}, e.code


# Handle jwt error where jwt header is missing
def handle_missing_jwt(e):
    return {'message': 'You are not logged in'}, 401


# Handle all Exceptions
def default_handler(*args, **kwargs):
    return {'message': 'Internal Server Error'}, 500
