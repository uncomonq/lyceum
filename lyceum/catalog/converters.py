def positive_int_converter(value: str) -> int | None:
    if value.isdigit() and int(value) > 0:
        return int(value)
    return None
