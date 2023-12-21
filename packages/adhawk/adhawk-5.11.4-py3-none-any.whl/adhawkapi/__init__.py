'''This module defines all of the APIs to Adhawk's embedded devices'''

from .error import CommunicationError, Error
from .publicapi import (
    REQUEST_TIMEOUT,
    AckCodes,
    APIRequestError,
    BlobType,
    BlobVersion,
    CameraResolution,
    CameraType,
    EventControlBit,
    Events,
    EyeMask,
    LogMode,
    MarkerSequenceMode,
    PacketType,
    ProcedureType,
    PropertyType,
    StreamControlBit,
    StreamRates,
    SystemInfo,
    CameraUserSettings,
    errormsg
)
