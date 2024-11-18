from fastapi import HTTPException


class InvalidSessionError(ValueError):
    def __init__(self):
        super().__init__("Invalid session ID")


class InvalidCredentialsError(ValueError):
    def __init__(self):
        super().__init__("Invalid credentials")


class UsernameInUseError(ValueError):
    def __init__(self):
        super().__init__("The username is already taken")


class EmailInUseError(ValueError):
    def __init__(self):
        super().__init__("The email is already taken")


class UserNotFoundError(ValueError):
    def __init__(self):
        super().__init__("User not found")


class UnexpectedError(ValueError):
    def __init__(self, operation: str):
        super().__init__(f"Unexpected error while operation: {operation}")


class InvalidTagException(ValueError):
    def __init__(self, tag: str):
        super().__init__(f"Tag '{tag}' is not a valid tag")


class PassNotSetException(ValueError):
    def __init__(self):
        super().__init__('There is no password set for this account. Please set your password in settings')


class UserNotAllowedError(ValueError):
    def __init__(self: str):
        super().__init__("This operation is not allowed for user")


class TokenNotFoundError(ValueError):
    def __init__(self):
        super().__init__("Token not found.")


class TokenAlreadyExistsError(ValueError):
    def __init__(self):
        super().__init__("A token with this ticker already exists.")


class InvalidTokenOperationError(ValueError):
    def __init__(self):
        super().__init__("Invalid operation on token.")


class UserAssetsNotFoundError(ValueError):
    def __init__(self):
        super().__init__("User assets not found.")


class InvalidUserAssetsOperationError(ValueError):
    def __init__(self):
        super().__init__("Invalid operation on user assets.")


class InvalidTradeTypeError(ValueError):
    def __init__(self):
        super().__init__("Invalid Trade Type Error.")


class InsufficientTokenSupplyError(ValueError):
    def __init__(self):
        super().__init__("Insufficient Token Supply Error.")


exceptions_list = (UserNotFoundError,
                   EmailInUseError,
                   UsernameInUseError,
                   InvalidCredentialsError,
                   InvalidSessionError,
                   UnexpectedError,
                   InvalidTagException,
                   PassNotSetException,
                   UserNotAllowedError,
                   TokenNotFoundError,
                   TokenAlreadyExistsError,
                   InvalidTokenOperationError,
                   UserAssetsNotFoundError,
                   InvalidUserAssetsOperationError,
                   InvalidTradeTypeError,
                   InsufficientTokenSupplyError,
                   )
