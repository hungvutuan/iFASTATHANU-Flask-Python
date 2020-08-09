# from datetime import datetime
# from pydantic import BaseModel
#
#
# class DtoHistory(BaseModel):
#     history_id: int
#     device_id: int
#     temp_reading: int
#     smoke_reading: int
#     gas_reading: int
#     date_reading: datetime
#     temp_id: int
#     smoke_id: int
#     gas_id: int


def get_dto_history_sensor():
    return [
        "history_id",
        "device_id",
        "temp_reading",
        "smoke_reading",
        "gas_reading",
        "date_reading",
        "temp_id",
        "smoke_id",
        "gas_id"
    ]


def get_dto_gas_sensor():
    return [
        "gas_id",
        "gas_name",
        "loc_id"
    ]


def get_dto_sensor_loc():
    return [
        "loc_id",
        "loc_name"
    ]


def get_dto_device():
    return [
        "device_id",
        "device_name",
        "device_type",
        "device_loc_id",
        "smoke_id",
        "gas_id",
        "temp_id"
    ]


def get_dto_smoke_sensor():
    return [
        "smoke_id",
        "smoke_name",
        "loc_id"
    ]


def get_dto_temp_sensor():
    return [
        "temp_id",
        "temp_name",
        "loc_id"
    ]


def get_dto_message():
    return [
        "message"
    ]
