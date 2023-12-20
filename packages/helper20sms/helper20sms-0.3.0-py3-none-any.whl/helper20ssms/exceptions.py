class OtherApiException(Exception):
    pass


class ValidationException(Exception):
    pass


class NoApiKeyProvidedException(Exception):
    pass


class BadApiKeyProvidedException(Exception):
    pass


class ForbiddenAccessException(Exception):
    pass


class BadCountryIdException(Exception):
    pass


class BadServiceIdException(Exception):
    pass


class WrongOperatorCodeException(Exception):
    pass


class InternalErrorException(Exception):
    pass


class NoNumbersException(Exception):
    pass


class BlockedUserException(Exception):
    pass


class InsufficientFundsException(Exception):
    pass


class CannotBuyMailRuServicesException(Exception):
    pass


class NoNumbersWithMaxPriceException(Exception):
    pass


class TooFastOperationException(Exception):
    pass


class OrderStatusChangeException(Exception):
    pass


class TooEarlyCancellationException(Exception):
    pass


class OrderProcessingException(Exception):
    pass


class UnsupportedOrderTypeException(Exception):
    pass


class TechnicalWorksException(Exception):
    pass


class RentTimeNotAvailableException(Exception):
    pass


class InvalidServiceCountException(Exception):
    pass
