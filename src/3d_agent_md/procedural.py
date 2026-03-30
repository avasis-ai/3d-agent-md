"""Procedural generation library for Blender 3D modeling."""

from typing import Dict, Any, List, Optional, Callable, TypeVar
import bpy
import bmesh
from mathutils import Vector, Matrix, Color


T = TypeVar('T')


class ProceduralGenerator:
    """Base class for procedural 3D generation operations."""
    
    def __init__(self, context: bpy.types.Context):
        """Initialize the procedural generator.
        
        Args:
            context: Blender's context object for scene manipulation
        """
        self.context = context
        self.ob = context.object if hasattr(context, 'object') else None
        self.scene = context.scene if hasattr(context, 'scene') else bpy.context.scene
    
    def get_or_create_material(self, name: str) -> bpy.types.Material:
        """Create or retrieve a material by name.
        
        Args:
            name: Material name
            
        Returns:
            Existing or newly created material
        """
        if name in bpy.data.materials:
            return bpy.data.materials[name]
        
        material = bpy.data.materials.new(name=name)
        material.use_nodes = True
        
        # Setup Principled BSDF node
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            return material
        
        # Create material nodes
        tree = material.node_tree
        tree.nodes.clear()
        
        bsdf = tree.nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)
        
        output = tree.nodes.new('ShaderNodeOutputMaterial')
        output.location = (200, 0)
        
        tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        
        return material
    
    def create_mesh_from_data(self, mesh_data: Dict[str, Any]) -> bpy.types.Mesh:
        """Create a mesh from dictionary data.
        
        Args:
            mesh_data: Dictionary with vertices, edges, faces
            
        Returns:
            Created mesh object
        """
        mesh = bpy.data.meshes.new(name=mesh_data.get('name', 'ProceduralMesh'))
        
        vertices = mesh_data.get('vertices', [])
        edges = mesh_data.get('edges', [])
        faces = mesh_data.get('faces', [])
        
        mesh.from_pydata(vertices, edges, faces)
        mesh.update()
        
        # Assign materials if provided
        if 'materials' in mesh_data:
            for i, mat_data in enumerate(mesh_data['materials']):
                material = self.get_or_create_material(mat_data['name'])
                if i < len(mesh.materials):
                    mesh.materials[i] = material
                else:
                    mesh.materials.append(material)
        
        return mesh
    
    def position_object(self, 
                       obj: bpy.types.Object, 
                       location: List[float],
                       rotation: Optional[List[float]] = None,
                       scale: Optional[List[float]] = None) -> bpy.types.Object:
        """Position an object in 3D space.
        
        Args:
            obj: Object to position
            location: [x, y, z] position
            rotation: [x, y, z] rotation in degrees (optional)
            scale: [x, y, z] scale (optional)
            
        Returns:
            Positioned object
        """
        obj.location = Vector(location)
        
        if rotation:
            obj.rotation_euler = [r * 3.14159265359 / 180 for r in rotation]
        
        if scale:
            obj.scale = Vector(scale)
        
        return obj


class GeometryGenerator(ProceduralGenerator):
    """Generator for creating basic 3D geometry."""
    
    def create_cube(self, 
                   name: str,
                   size: float = 1.0,
                   location: List[float] = [0, 0, 0]) -> bpy.types.Object:
        """Create a cube mesh.
        
        Args:
            name: Object name
            size: Side length
            location: [x, y, z] position
            
        Returns:
            Cube mesh object
        """
        mesh_data = {'name': name, 'vertices': [], 'edges': [], 'faces': []}
        
        # Define cube vertices
        s = size / 2
        vertices = [
            (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),
            (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)
        ]
        
        # Define faces (each face has 4 vertex indices)
        faces = [
            (0, 1, 2, 3),  # bottom
            (5, 4, 7, 6),  # top
            (4, 0, 3, 7),  # left
            (6, 2, 1, 5),  # right
            (3, 2, 6, 7),  # front
            (4, 5, 1, 0)   # back
        ]
        
        mesh_data['vertices'] = vertices
        mesh_data['faces'] = faces
        
        mesh = self.create_mesh_from_data(mesh_data)
        obj = bpy.data.objects.new(name, mesh)
        self.scene.collection.objects.link(obj)
        
        return self.position_object(obj, location)
    
    def create_cylinder(self,
                       name: str,
                       radius: float = 1.0,
                       depth: float = 1.0,
                       locations: List[float] = [0, 0, 0]) -> bpy.types.Object:
        """Create a cylinder mesh.
        
        Args:
            name: Object name
            radius: Cylinder radius
            depth: Cylinder height
            location: [x, y, z] position
            
        Returns:
            Cylinder mesh object
        """
        import math
        
        mesh_data = {'name': name, 'vertices': [], 'edges': [], 'faces': []}
        
        # Create side vertices
        sides = 32
        angle_step = 2 * math.pi / sides
        
        vertices = []
        
        # Top ring
        for i in range(sides):
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y, depth / 2))
        
        # Bottom ring
        for i in range(sides):
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y, -depth / 2))
        
        mesh_data['vertices'] = vertices
        
        # Create faces
        faces = []
        
        # Side faces
        for i in range(sides):
            next_i = (i + 1) % sides
            faces.append([i, next_i, next_i + sides, i + sides])
        
        # Top face (using center vertex)
        center_top = len(vertices)
        vertices.append((0, 0, depth / 2))
        for i in range(sides):
            faces.append([i, (i + 1) % sides, center_top])
        
        # Bottom face (using center vertex)
        center_bottom = len(vertices)
        vertices.append((0, 0, -depth / 2))
        for i in range(sides):
            faces.append([i + sides, (i + 1) % sides + sides, center_bottom])
        
        mesh_data['vertices'] = vertices
        mesh_data['faces'] = faces
        
        mesh = self.create_mesh_from_data(mesh_data)
        obj = bpy.data.objects.new(name, mesh)
        self.scene.collection.objects.link(obj)
        
        return self.position_object(obj, locations)
    
    def create_cone(self,
                   name: str,
                   radius: float = 1.0,
                   depth: float = 2.0,
                   location: List[float] = [0, 0, 0]) -> bpy.types.Object:
        """Create a cone mesh.
        
        Args:
            name: Object name
            radius: Base radius
            depth: Cone height
            location: [x, y, z] position
            
        Returns:
            Cone mesh object
        """
        import math
        
        mesh_data = {'name': name, 'vertices': [], 'edges': [], 'faces': []}
        
        # Create base vertices
        sides = 32
        angle_step = 2 * math.pi / sides
        vertices = []
        
        for i in range(sides):
            angle = i * angle_step
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y, -depth / 2))
        
        # Add apex
        vertices.append((0, 0, depth / 2))
        
        mesh_data['vertices'] = vertices
        
        # Create faces
        faces = []
        apex = len(vertices) - 1
        
        # Side faces
        for i in range(sides):
            next_i = (i + 1) % sides
            faces.append([i, next_i, apex])
        
        # Base face
        for i in range(sides):
            next_i = (i + 1) % sides
            faces.append([i, apex, next_i])
        
        mesh_data['faces'] = faces
        
        mesh = self.create_mesh_from_data(mesh_data)
        obj = bpy.data.objects.new(name, mesh)
        self.scene.collection.objects.link(obj)
        
        return self.position_object(obj, location)


class MaterialGenerator(ProceduralGenerator):
    """Generator for creating and configuring materials."""
    
    def create_wood_material(self, 
                           name: str,
                           color: List[float] = [0.8, 0.6, 0.4]) -> bpy.types.Material:
        """Create a wood-like material.
        
        Args:
            name: Material name
            color: [r, g, b] color values (0-1)
            
        Returns:
            Created wood material
        """
        material = self.get_or_create_material(f"{name}_wood")
        
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = Color(color)
            bsdf.inputs["Roughness"].default_value = 0.7
            bsdf.inputs["Metallic"].default_value = 0.0
        
        return material
    
    def create_metal_material(self,
                             name: str,
                             color: List[float] = [0.8, 0.8, 0.8]) -> bpy.types.Material:
        """Create a metal-like material.
        
        Args:
            name: Material name
            color: [r, g, b] color values (0-1)
            
        Returns:
            Created metal material
        """
        material = self.get_or_create_material(f"{name}_metal")
        
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = Color(color)
            bsdf.inputs["Roughness"].default_value = 0.3
            bsdf.inputs["Metallic"].default_value = 1.0
        
        return material
    
    def create_fabric_material(self,
                              name: str,
                              color: List[float] = [1.0, 0.5, 0.5]) -> bpy.types.Material:
        """Create a fabric-like material.
        
        Args:
            name: Material name
            color: [r, g, b] color values (0-1)
            
        Returns:
            Created fabric material
        """
        material = self.get_or_create_material(f"{name}_fabric")
        
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = Color(color)
            bsdf.inputs["Roughness"].default_value = 0.9
            bsdf.inputs["Metallic"].default_value = 0.0
        
        return material


class ProceduralLibrary:
    """Comprehensive library of procedural generation scripts."""
    
    def __init__(self, context: bpy.types.Context):
        """Initialize the procedural library.
        
        Args:
            context: Blender's context object
        """
        self.context = context
        self.geometry = GeometryGenerator(context)
        self.materials = MaterialGenerator(context)
    
    def generate_walls(self,
                      width: float = 10.0,
                      height: float = 5.0,
                      depth: float = 0.5,
                      location: List[float] = [0, 0, 2.5],
                      material_name: str = "wall_stone") -> List[bpy.types.Object]:
        """Generate wall structure.
        
        Args:
            width: Wall width
            height: Wall height
            depth: Wall thickness
            location: [x, y, z] position
            material_name: Material name
            
        Returns:
            List of wall objects
        """
        material = self.materials.get_or_create_material(material_name)
        
        cube = self.geometry.create_cube(
            name=f"wall_{width}x{height}",
            size=width,
            location=[0, -depth/2, location[2]]
        )
        
        cube.data.materials.append(material)
        cube.dimensions = Vector([width, depth, height])
        
        return [cube]
    
    def generate_floor(self,
                      width: float = 10.0,
                      depth: float = 10.0,
                      location: List[float] = [0, 0, 0],
                      material_name: str = "floor_wood") -> List[bpy.types.Object]:
        """Generate floor structure.
        
        Args:
            width: Floor width
            depth: Floor depth
            location: [x, y, z] position
            material_name: Material name
            
        Returns:
            List of floor objects
        """
        material = self.materials.get_or_create_material(material_name)
        
        floor = self.geometry.create_cube(
            name=f"floor_{width}x{depth}",
            size=max(width, depth),
            location=[0, 0, 0.05]
        )
        
        floor.data.materials.append(material)
        floor.dimensions = Vector([width, depth, 0.1])
        
        return [floor]
    
    def generate_roof(self,
                     width: float = 10.0,
                     depth: float = 10.0,
                     height: float = 3.0,
                     location: List[float] = [0, 0, 5.0],
                     material_name: str = "roof_tile") -> List[bpy.types.Object]:
        """Generate roof structure.
        
        Args:
            width: Roof width
            depth: Roof depth
            height: Roof height
            location: [x, y, z] position
            material_name: Material name
            
        Returns:
            List of roof objects
        """
        material = self.materials.get_or_create_material(material_name)
        
        cube = self.geometry.create_cube(
            name=f"roof_{width}x{height}",
            size=width,
            location=[0, -depth/2, location[2]]
        )
        
        cube.data.materials.append(material)
        cube.dimensions = Vector([width, depth, height])
        
        return [cube]
