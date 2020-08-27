def get_dto_history_sensor():
    return [
        "history_id",
        "alarm_status",
        "loc_name",
        "device_name",
        "date_reading",
        "alarm_type"
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


def get_live_metrics():
    return[
        "current_time",
        "metrics"
    ]
