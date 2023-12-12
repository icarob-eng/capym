from attrs import define


@define(frozen=True)
class Limits:
    x: tuple[float, float]
    y: tuple[float, float]
