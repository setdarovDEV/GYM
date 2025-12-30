class BotException(Exception):
    pass


class UserNotFoundException(BotException):
    pass


class ProductNotFoundException(BotException):
    pass


class OrderNotFoundException(BotException):
    pass


class InsufficientStockException(BotException):
    pass


class ValidationException(BotException):
    pass