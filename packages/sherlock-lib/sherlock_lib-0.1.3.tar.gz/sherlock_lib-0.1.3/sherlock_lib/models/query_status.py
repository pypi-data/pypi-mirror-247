from enum import Enum


class QueryStatus(Enum):
    """Query Status Enumeration.

    Describes status of query about a given username.
    """
    CLAIMED   = "Claimed"   # Username Detected
    AVAILABLE = "Available" # Username Not Detected
    UNKNOWN   = "Unknown"   # Error Occurred While Trying To Detect Username
    ILLEGAL   = "Illegal"   # Username Not Allowable For This Site

    def __str__(self):
        """Convert Object To String.

        Keyword Arguments:
        self                   -- This object.

        Return Value:
        Nicely formatted string to get information about this object.
        """
        return self.value