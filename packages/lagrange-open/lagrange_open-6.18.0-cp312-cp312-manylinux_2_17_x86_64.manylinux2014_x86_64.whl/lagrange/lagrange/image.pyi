from typing import Any, Optional, overload, Typing, Sequence
from enum import Enum
import lagrange.image

class ImageChannel:
    """
    <attribute '__doc__' of 'lagrange.image.ImageChannel' objects>
    """

    @entries: dict
    
    def __init__(*args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """
        ...
    
    four: ImageChannel
    
    one: ImageChannel
    
    three: ImageChannel
    
    unknown: ImageChannel
    
class ImagePrecision:
    """
    <attribute '__doc__' of 'lagrange.image.ImagePrecision' objects>
    """

    @entries: dict
    
    def __init__(*args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """
        ...
    
    float16: ImagePrecision
    
    float32: ImagePrecision
    
    float64: ImagePrecision
    
    int32: ImagePrecision
    
    int8: ImagePrecision
    
    uint32: ImagePrecision
    
    uint8: ImagePrecision
    
    unknown: ImagePrecision
    
class ImageStorage:

    def __init__(self, arg0: int, arg1: int, arg2: int, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    
    @property
    def (self) -> int:
        ...
    
    @property
    def (self) -> int:
        ...
    
    @property
    def (self) -> int:
        ...
    
