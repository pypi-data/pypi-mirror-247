import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Status(str, Enum):
    """
    Enum representing the status of a data request.
    """

    pending = "pending"
    acknowledged = "acknowledged"
    rejected = "rejected"
    failed = "failed"
    completed = "completed"


class BaseDataRequestModel(BaseModel):
    """
    Base model for a DataRequest.

    Attributes:
        id (UUID): Unique identifier for the data request.
        status (Status): The current status of the data request.
        composition (dict): Data composition.
        score (Optional[float]): Score associated with the data request.
        sample_label (Optional[str]): Sample label.
        analysis (Optional[dict]): Analysis data.
    """

    status: Status
    composition: dict
    score: Optional[float]
    parameters: Optional[dict] = None
    sample_label: Optional[str]
    analysis: Optional[dict]


class ReadDataRequest(BaseDataRequestModel):
    """
    Model for reading DataRequests.
    Used to differentiate the models if any additional fields are required for reading.
    """

    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime


class CreateDataRequestModel(BaseModel):
    """
    Model for creating DataRequests.
    """

    composition: dict[str, float] = Field(..., examples=[{"Fe": 0.5, "Ni": 0.5}])
    score: Optional[float] = None
    parameters: Optional[dict] = None
    sample_label: Optional[str] = None
    analysis: Optional[dict] = Field(default=None)


class UpdateDataRequestModel(BaseModel):
    """
    Model for updating DataRequests.

    Attributes:
        id (UUID): Unique identifier for the data request.
        sample_label (Optional[str]): Updated sample label.
        score (Optional[float]): Updated score.
        composition (Optional[dict]): Updated composition.
    """

    id: UUID
    sample_label: Optional[str] = None
    score: Optional[float] = None
    parameters: Optional[dict] = None
    composition: Optional[dict] = None
