from typing import Any, Optional, overload, Typing, Sequence
from enum import Enum
import lagrange.scene

class Animation:

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
class Camera:
    """
    Camera
    """

    class Type:
        """
        <attribute '__doc__' of 'Type' objects>
        """
    
        @entries: dict
        
        Orthographic: Type
        
        Perspective: Type
        
        def __init__(*args, **kwargs):
            """
            Initialize self.  See help(type(self)) for accurate signature.
            """
            ...
        
    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @aspect_ratio.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @far_plane.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    
    @property
    def (self) -> float:
        ...
    @horizontal_fov.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @look_at.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @near_plane.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @orthographic_width.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @position.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.Camera.Type:
        ...
    @type.setter
    def (self, arg: lagrange.scene.Camera.Type, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @up.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
class FacetAllocationStrategy:
    """
    <attribute '__doc__' of 'FacetAllocationStrategy' objects>
    """

    @entries: dict
    
    EvenSplit: FacetAllocationStrategy
    
    RelativeToMeshArea: FacetAllocationStrategy
    
    RelativeToNumFacets: FacetAllocationStrategy
    
    Synchronized: FacetAllocationStrategy
    
    def __init__(*args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """
        ...
    
class ImageLegacy:

    class Type:
        """
        <attribute '__doc__' of 'Type' objects>
        """
    
        @entries: dict
        
        Bmp: Type
        
        Gif: Type
        
        Jpeg: Type
        
        Png: Type
        
        Unknown: Type
        
        def __init__(*args, **kwargs):
            """
            Initialize self.  See help(type(self)) for accurate signature.
            """
            ...
        
    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> lagrange.image.ImageChannel:
        ...
    @channel.setter
    def (self, arg: lagrange.image.ImageChannel, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.image.ImageStorage:
        ...
    @data.setter
    def (self, arg: lagrange.image.ImageStorage, /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    
    @property
    def (self) -> int:
        ...
    @height.setter
    def (self, arg: int, /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    
    @property
    def (self) -> lagrange.image.ImagePrecision:
        ...
    @precision.setter
    def (self, arg: lagrange.image.ImagePrecision, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.ImageLegacy.Type:
        ...
    @type.setter
    def (self, arg: lagrange.scene.ImageLegacy.Type, /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @uri.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @width.setter
    def (self, arg: int, /) -> None:
        ...
    
class Light:
    """
    Light
    """

    class Type:
        """
        <attribute '__doc__' of 'Type' objects>
        """
    
        @entries: dict
        
        Ambient: Type
        
        Area: Type
        
        Directional: Type
        
        Point: Type
        
        Spot: Type
        
        Undefined: Type
        
        def __init__(*args, **kwargs):
            """
            Initialize self.  See help(type(self)) for accurate signature.
            """
            ...
        
    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @angle_inner_cone.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @angle_outer_cone.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @attenuation_constant.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @attenuation_cubic.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @attenuation_linear.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @attenuation_quadratic.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @color_ambient.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @color_diffuse.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @color_specular.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @direction.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @intensity.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @position.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @range.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @size.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.Light.Type:
        ...
    @type.setter
    def (self, arg: lagrange.scene.Light.Type, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @up.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
class Material:

    class AlphaMode:
        """
        <attribute '__doc__' of 'AlphaMode' objects>
        """
    
        @entries: dict
        
        Blend: AlphaMode
        
        Mask: AlphaMode
        
        Opaque: AlphaMode
        
        def __init__(*args, **kwargs):
            """
            Initialize self.  See help(type(self)) for accurate signature.
            """
            ...
        
    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @alpha_cutoff.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.Material.AlphaMode:
        ...
    @alpha_mode.setter
    def (self, arg: lagrange.scene.Material.AlphaMode, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.TextureInfo:
        ...
    @base_color_texture.setter
    def (self, arg: lagrange.scene.TextureInfo, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @base_color_value.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> bool:
        ...
    @double_sided.setter
    def (self, arg: bool, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.TextureInfo:
        ...
    @emissive_texture.setter
    def (self, arg: lagrange.scene.TextureInfo, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @emissive_value.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.TextureInfo:
        ...
    @metallic_roughness_texture.setter
    def (self, arg: lagrange.scene.TextureInfo, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @metallic_value.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @normal_scale.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.TextureInfo:
        ...
    @normal_texture.setter
    def (self, arg: lagrange.scene.TextureInfo, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @occlusion_strength.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.TextureInfo:
        ...
    @occlusion_texture.setter
    def (self, arg: lagrange.scene.TextureInfo, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @roughness_value.setter
    def (self, arg: float, /) -> None:
        ...
    
class MeshInstance3D:
    """
    A single mesh instance in a scene
    """

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @mesh_index.setter
    def (self, arg: int, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @transform.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
class Node:

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> list[int]:
        ...
    @cameras.setter
    def (self, arg: list[int], /) -> None:
        ...
    
    @property
    def (self) -> list[int]:
        ...
    @children.setter
    def (self, arg: list[int], /) -> None:
        ...
    
    @property
    def (self) -> list[int]:
        ...
    @lights.setter
    def (self, arg: list[int], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.SceneMeshInstance]:
        ...
    @meshes.setter
    def (self, arg: list[lagrange.scene.SceneMeshInstance], /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @parent.setter
    def (self, arg: int, /) -> None:
        ...
    
    @property
    def (self) -> list[list[float]]:
        ...
    @transform.setter
    def (self, arg: list[list[float]], /) -> None:
        ...
    
class RemeshingOptions:

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.FacetAllocationStrategy:
        ...
    @facet_allocation_strategy.setter
    def (self, arg: lagrange.scene.FacetAllocationStrategy, /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @min_facets.setter
    def (self, arg: int, /) -> None:
        ...
    
class Scene:
    """
    A 3D scene
    """

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Animation]:
        ...
    @animations.setter
    def (self, arg: list[lagrange.scene.Animation], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Camera]:
        ...
    @cameras.setter
    def (self, arg: list[lagrange.scene.Camera], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.ImageLegacy]:
        ...
    @images.setter
    def (self, arg: list[lagrange.scene.ImageLegacy], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Light]:
        ...
    @lights.setter
    def (self, arg: list[lagrange.scene.Light], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Material]:
        ...
    @materials.setter
    def (self, arg: list[lagrange.scene.Material], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.core.SurfaceMesh]:
        ...
    @meshes.setter
    def (self, arg: list[lagrange.core.SurfaceMesh], /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Node]:
        ...
    @nodes.setter
    def (self, arg: list[lagrange.scene.Node], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Skeleton]:
        ...
    @skeletons.setter
    def (self, arg: list[lagrange.scene.Skeleton], /) -> None:
        ...
    
    @property
    def (self) -> list[lagrange.scene.Texture]:
        ...
    @textures.setter
    def (self, arg: list[lagrange.scene.Texture], /) -> None:
        ...
    
class SceneMeshInstance:
    """
    Mesh and material index of a node
    """

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> list[int]:
        ...
    @materials.setter
    def (self, arg: list[int], /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @mesh.setter
    def (self, arg: int, /) -> None:
        ...
    
class SimpleScene3D:
    """
    Simple scene container for instanced meshes
    """

    def __init__(self) -> None:
        ...
    
    def add_instance(self, instance: lagrange.scene.MeshInstance3D) -> int:
        ...
    
    def add_mesh(self, mesh: lagrange.core.SurfaceMesh) -> int:
        ...
    
    def get_instance(self, mesh_index: int, instance_index: int) -> lagrange.scene.MeshInstance3D:
        ...
    
    def get_mesh(self, mesh_index: int) -> lagrange.core.SurfaceMesh:
        ...
    
    def num_instances(self, mesh_index: int) -> int:
        ...
    
    @property
    def (self) -> int:
        """
        Number of meshes in the scene
        """
        ...
    
    def ref_mesh(self, mesh_index: int) -> lagrange.core.SurfaceMesh:
        ...
    
    def reserve_instances(self, mesh_index: int, num_instances: int) -> None:
        ...
    
    def reserve_meshes(self, num_meshes: int) -> None:
        ...
    
    @property
    def (self) -> int:
        """
        Total number of instances for all meshes in the scene
        """
        ...
    
class Skeleton:

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> list[int]:
        ...
    @meshes.setter
    def (self, arg: list[int], /) -> None:
        ...
    
class Texture:
    """
    Texture
    """

    class WrapMode:
        """
        <attribute '__doc__' of 'WrapMode' objects>
        """
    
        @entries: dict
        
        Clamp: WrapMode
        
        Decal: WrapMode
        
        Mirror: WrapMode
        
        Wrap: WrapMode
        
        def __init__(*args, **kwargs):
            """
            Initialize self.  See help(type(self)) for accurate signature.
            """
            ...
        
    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @image.setter
    def (self, arg: int, /) -> None:
        ...
    
    @property
    def (self) -> lagrange::scene::Texture::TextureFilter:
        ...
    @mag_filter.setter
    def (self, arg: lagrange::scene::Texture::TextureFilter, /) -> None:
        ...
    
    @property
    def (self) -> lagrange::scene::Texture::TextureFilter:
        ...
    @min_filter.setter
    def (self, arg: lagrange::scene::Texture::TextureFilter, /) -> None:
        ...
    
    @property
    def (self) -> str:
        ...
    @name.setter
    def (self, arg: str, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @offset.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> float:
        ...
    @rotation.setter
    def (self, arg: float, /) -> None:
        ...
    
    @property
    def (self) -> numpy.typing.NDArray:
        ...
    @scale.setter
    def (self, arg: numpy.typing.NDArray, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.Texture.WrapMode:
        ...
    @wrap_u.setter
    def (self, arg: lagrange.scene.Texture.WrapMode, /) -> None:
        ...
    
    @property
    def (self) -> lagrange.scene.Texture.WrapMode:
        ...
    @wrap_v.setter
    def (self, arg: lagrange.scene.Texture.WrapMode, /) -> None:
        ...
    
class TextureInfo:

    def __init__(self) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @index.setter
    def (self, arg: int, /) -> None:
        ...
    
    @property
    def (self) -> int:
        ...
    @texcoord.setter
    def (self, arg: int, /) -> None:
        ...
    
def add_child(arg0: lagrange.scene.Scene, arg1: lagrange.scene.Node, arg2: lagrange.scene.Node, /) -> int:
    ...

def add_mesh(arg0: lagrange.scene.Scene, arg1: lagrange.core.SurfaceMesh, /) -> int:
    ...

def compute_global_node_transform(arg0: lagrange.scene.Scene, arg1: int, /) -> list[list[float]]:
    ...

