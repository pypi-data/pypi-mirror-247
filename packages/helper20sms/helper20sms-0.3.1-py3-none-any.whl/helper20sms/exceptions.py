class HelperSMSException(Exception):
    pass


class OtherApiException(HelperSMSException):
    pass


class ValidationException(HelperSMSException):
    pass


class NoApiKeyProvidedException(HelperSMSException):
    pass


class BadApiKeyProvidedException(HelperSMSException):
    pass


class ForbiddenAccessException(HelperSMSException):
    pass


class BadCountryIdException(HelperSMSException):
    pass


class BadServiceIdException(HelperSMSException):
    pass


class WrongOperatorCodeException(HelperSMSException):
    pass


class InternalErrorException(HelperSMSException):
    pass


class NoNumbersException(HelperSMSException):
    pass


class BlockedUserException(HelperSMSException):
    pass


class InsufficientFundsException(HelperSMSException):
    pass


class CannotBuyMailRuServicesException(HelperSMSException):
    pass


class NoNumbersWithMaxPriceException(HelperSMSException):
    pass


class TooFastOperationException(HelperSMSException):
    pass


class OrderStatusChangeException(HelperSMSException):
    pass


class TooEarlyCancellationException(HelperSMSException):
    pass


class OrderProcessingException(HelperSMSException):
    pass


class UnsupportedOrderTypeException(HelperSMSException):
    pass


class TechnicalWorksException(HelperSMSException):
    pass


class RentTimeNotAvailableException(HelperSMSException):
    pass


class InvalidServiceCountException(HelperSMSException):
    pass
