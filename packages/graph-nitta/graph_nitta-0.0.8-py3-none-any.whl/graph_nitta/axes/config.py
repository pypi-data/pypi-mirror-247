from pydantic import BaseModel


class SpineConfig(BaseModel):
    label: str = ""
    scale: str = "linear"
    lim: tuple[float, float] | None = None
    step: float | None = None
    pow: int = 0
    visible: bool = True
    invert: bool = False


class AxConfig(BaseModel):
    x: SpineConfig = SpineConfig()
    y: SpineConfig = SpineConfig()
    is_visible_legend: bool = True
    legends_loc: str = "upper left"
    bbox_to_anchor: tuple[float, float] | None = (1.0, 1.0)
