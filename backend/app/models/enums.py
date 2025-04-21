import enum

class UserRole(str, enum.Enum):
    """
    Defines the possible roles for a user.
    Inherits from str to be easily serializable.
    """
    ADMIN = "admin"
    USER = "user"