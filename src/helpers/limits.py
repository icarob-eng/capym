from attrs import define


@define(frozen=True, slots=False)
class Limits:
    x: tuple[float, float]
    y: tuple[float, float]
