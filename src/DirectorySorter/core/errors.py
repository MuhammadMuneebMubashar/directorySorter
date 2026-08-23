class OrganizerError(Exception):
    """Base exception for organizer errors."""
    pass

class InvalidDirectoryError(OrganizerError):
    """Raised when directory is invalid."""
    pass

class FileOperationError(OrganizerError):
    """Raised when file operation fails."""
    pass