from pydantic import BaseModel

class PictureMetaCls(BaseModel):
    filename: str
    type: str|None
    image_size: float|None
    image_x: int|None
    image_y: int|None
    dpi: int|None
    center_coordinate: tuple[float, float]|None
    favorite: str|None
    continent: str|None
    bit_color: int|None
    alpha: str|None
    hockey_team: str|None
    user_tags: str|None

class Point(BaseModel):
    x: float
    y: float

str_props = ['filename', 'type', 'favorite', 'continent', 'alpha', 'hockey_team', 'user_tags']

value_props = ['image_x', 'image_y', 'dpi', 'bit_color']
