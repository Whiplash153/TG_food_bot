class AppError(Exception):
    """Base application error."""

class ValidationError(AppError):
    """Raised when user input is invalid."""

class NotFoundError(AppError):
    """Raised when requested data was not found."""

class NotificationError(AppError):
    """Raised when notification delivery failed."""

class ApplicationError(AppError):
    """Raised when application processing fails."""