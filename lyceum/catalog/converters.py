class PositiveIntWithLeadingZerosConverter:
    regex = r"0*[1-9][0-9]*"

    def to_python(self, value: str) -> int:
        return int(value)

    def to_url(self, value: int) -> str:
        return str(value)
