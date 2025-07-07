class NotFoundError(Exception):
    """Error raised when a db asset does not exist in the db."""


class SameUserError(Exception):
    """Error raised when a user is attempting to perform a forbidden action on itself."""
