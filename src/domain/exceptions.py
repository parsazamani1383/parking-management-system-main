class DomainError(Exception):
    """Base class for all domain-related errors."""
    pass


class ValidationError(DomainError):
    """Raised when business rules are violated."""
    pass


class EntityNotFoundError(DomainError):
    pass


class ParkingSpotUnavailableError(DomainError):
    pass


class SessionAlreadyClosedError(DomainError):
    pass


class InvalidSessionStateError(DomainError):
    pass


class TariffNotFoundError(DomainError):
    pass
