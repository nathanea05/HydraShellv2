# Contains exceptions related to core objects

# Library Imports


# Local Imports


class RegistrationError(Exception):
    """Raised when an error occurs during command registration (init)"""


class NotImplementedError(Exception):
    """Raised when a command has not been implemented"""


class ContextImplementationError(Exception):
    """Raised when a heads context has not been properly implemented"""