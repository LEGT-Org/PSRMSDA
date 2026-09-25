from enum import StrEnum


class ServiceRequestStatus(StrEnum):

    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FOR_FURTHER_INSPECTION = "For Further Inspection"
    UNSUCCESSFUL = "Unsuccessful"