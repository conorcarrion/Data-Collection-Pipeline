from dataclasses import dataclass

@dataclass(repr=True)
class Spirit:

    """Dataclass for detailing attributes of a Spirit."""

    name: str = ''
    subname: str = ''                    
    product_id: str = ''
    product_uuid: str = ''
    contents_liquid_volume: str = '0cl'
    alcohol_by_volume: str = '0%'
    price: float = 0
    description: str = 'tasteless'
    facts: dict = None
    flavour_style: dict = None
    flavour_character: list = None
    image_url: str = ''
    filepath: str = ''
    brand_name = str = ''