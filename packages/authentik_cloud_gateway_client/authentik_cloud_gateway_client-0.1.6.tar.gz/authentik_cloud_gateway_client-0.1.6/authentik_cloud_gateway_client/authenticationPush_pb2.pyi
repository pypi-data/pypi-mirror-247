from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthenticationResponseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[AuthenticationResponseStatus]
    SENT: _ClassVar[AuthenticationResponseStatus]
    FAILED: _ClassVar[AuthenticationResponseStatus]
    ANSWERED: _ClassVar[AuthenticationResponseStatus]

UNKNOWN: AuthenticationResponseStatus
SENT: AuthenticationResponseStatus
FAILED: AuthenticationResponseStatus
ANSWERED: AuthenticationResponseStatus

class AuthenticationRequest(_message.Message):
    __slots__ = ("device_token", "title", "body", "tx_id", "mode", "items")
    DEVICE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    device_token: str
    title: str
    body: str
    tx_id: str
    mode: str
    items: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        device_token: _Optional[str] = ...,
        title: _Optional[str] = ...,
        body: _Optional[str] = ...,
        tx_id: _Optional[str] = ...,
        mode: _Optional[str] = ...,
        items: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class AuthenticationCheckRequest(_message.Message):
    __slots__ = ("tx_id", "attempts")
    TX_ID_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    tx_id: str
    attempts: int
    def __init__(self, tx_id: _Optional[str] = ..., attempts: _Optional[int] = ...) -> None: ...

class AuthenticationResponse(_message.Message):
    __slots__ = ("status", "decided_item")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DECIDED_ITEM_FIELD_NUMBER: _ClassVar[int]
    status: AuthenticationResponseStatus
    decided_item: str
    def __init__(
        self, status: _Optional[_Union[AuthenticationResponseStatus, str]] = ..., decided_item: _Optional[str] = ...
    ) -> None: ...
