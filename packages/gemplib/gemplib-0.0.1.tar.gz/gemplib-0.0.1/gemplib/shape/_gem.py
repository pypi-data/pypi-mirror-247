
from gemplib.misc import *

__all__ = [
    "Geometry"
]

class Geometry:
    def __init__(
        self,
        gem_type:str,
        **kwargs
    ):
        """_summary_

        Args:
            gem_type (str): _description_
        """
        self.gem_type = gem_type
        
    