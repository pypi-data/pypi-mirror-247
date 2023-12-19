from pydantic import BaseModel
from enum import Enum


class Trip(BaseModel):
    trip_id: str
    start_time: str
    start_date: str

    class Config:
        from_attributes = True


class Position(BaseModel):
    latitude: float
    longitude: float
    bearing: float

    class Config:
        from_attributes = True


class VehicleID(BaseModel):
    id: str

    class Config:
        from_attributes = True


class OccupancyStatus(Enum):
    EMPTY = 0
    MANY_SEATS_AVAILABLE = 1
    FEW_SEATS_AVAILABLE = 2
    STANDING_ROOM_ONLY = 3
    CRUSHED_STANDING_ROOM_ONLY = 4
    FULL = 5
    NOT_ACCEPTING_PASSENGERS = 6
    NO_DATA_AVAILABLE = 7
    NOT_BOARDABLE = 8


class Vehicle(BaseModel):
    trip: Trip
    position: Position
    timestamp: int
    vehicle: VehicleID
    occupancy_status: OccupancyStatus = OccupancyStatus.NO_DATA_AVAILABLE

    class Config:
        from_attributes = True


class VehiclePosition(BaseModel):
    id: str
    vehicle: Vehicle

    class Config:
        from_attributes = True


class TrainPositions(BaseModel):
    vehicle_positions: list[VehiclePosition]


class TramPositions(BaseModel):
    vehicle_positions: list[VehiclePosition]


class Timestamp(BaseModel):
    time: int

    class Config:
        from_attributes = True


class StopTimeUpdate(BaseModel):
    stop_sequence: int
    arrival: Timestamp
    departure: Timestamp

    class Config:
        from_attributes = True


class StopTimeUpdates(BaseModel):
    lst: list[StopTimeUpdate]

    class Config:
        from_attributes = True


class TripUpdate(BaseModel):
    trip: Trip
    stop_time_update: list[StopTimeUpdate]

    class Config:
        from_attributes = True


class TransportUpdate(BaseModel):
    id: str
    trip_update: TripUpdate

    class Config:
        from_attributes = True


class Translation(BaseModel):
    text: str
    language: str

    class Config:
        from_attributes = True


class TranslatedString(BaseModel):
    translation: list[Translation]

    class Config:
        from_attributes = True


class EntitySelector(BaseModel):
    agency_id: str | None = None
    route_id: str | None = None
    route_type: int | None = None
    direction_id: int | None = None
    trip: Trip | None = None
    stop_id: str | None = None

    class Config:
        from_attributes = True


class ServiceEffect(Enum):
    NO_SERVICE = 1
    REDUCED_SERVICE = 2
    SIGNIFICANT_DELAYS = 3
    DETOUR = 4
    ADDITIONAL_SERVICE = 5
    MODIFIED_SERVICE = 6
    OTHER_EFFECT = 7
    UNKNOWN_EFFECT = 8
    STOP_MOVED = 9


class Alert(BaseModel):
    informed_entity: EntitySelector
    effect: ServiceEffect
    header_text: TranslatedString
    description_text: TranslatedString

    class Config:
        from_attributes = True


class ServiceAlert(BaseModel):
    id: str
    alert: Alert

    class Config:
        from_attributes = True
