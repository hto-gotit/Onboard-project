class CategoryDNE(Exception):
    code = 404
    message = 'Category not found'


class ItemDNE(Exception):
    code = 404
    message = 'Item not found'


class ItemNameDuplicate(Exception):
    code = 400
    message = 'Item name already exists in destination category'


class InvalidCredentials(Exception):
    code = 400
    message = 'Invalid username or password'


class UsernameAlreadyExists(Exception):
    code = 400
    message = 'Username already exists'


class UserForbidden(Exception):
    code = 403
    message = 'User is forbidden to perform this action ' \
              '(user is not item creator)'


# handle custom errors
def handle_custom_errors(e):
    return {'message': e.message}, e.code


# Handle other HTTP Exceptions
def handle_http_exception(e):
    return {'message': e.description}, e.code


# Handle all Exceptions
def default_handler():
    return {'message': 'Internal Server Error'}, 500
