"""Tests for the procedural generation library."""

import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock bpy before importing procedural module
sys.modules['bpy'] = MagicMock()
sys.modules['bpy.types'] = MagicMock()
sys.modules['bpy.data'] = MagicMock()
sys.modules['bpy.context'] = MagicMock()

from 3d_agent_md.procedural import (
    ProceduralGenerator,
    GeometryGenerator,
    MaterialGenerator,
    ProceduralLibrary
)
from mathutils import Vector, Color


class TestProceduralGenerator:
    """Tests for ProceduralGenerator base class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        mock_context = MagicMock()
        mock_context.object = MagicMock()
        mock_context.scene = MagicMock()
        
        self.generator = ProceduralGenerator(mock_context)
    
    def test_get_or_create_material_existing(self):
        """Test getting an existing material."""
        mock_mat = MagicMock(name="test_material")
        mock_context = self.generator.context
        mock_context.scene.collection.objects.link = MagicMock()
        
        # Mock bpy.data.materials
        import bpy
        bpy.data.materials = {'test_material': mock_mat}
        
        result = self.generator.get_or_create_material("test_material")
        assert result == mock_mat
    
    def test_get_or_create_material_new(self):
        """Test creating a new material."""
        import bpy
        bpy.data.materials = {}
        
        result = self.generator.get_or_create_material("new_material")
        assert result is not None
        assert result.name == "new_material"
        assert result.use_nodes is True
    
    def test_position_object(self):
        """Test positioning an object."""
        mock_obj = MagicMock()
        
        result = self.generator.position_object(
            mock_obj,
            location=[1, 2, 3],
            rotation=[90, 0, 0],
            scale=[2, 2, 2]
        )
        
        assert result == mock_obj
        mock_obj.location = Vector([1, 2, 3])
        assert mock_obj.scale == Vector([2, 2, 2])


class TestGeometryGenerator:
    """Tests for GeometryGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        mock_context = MagicMock()
        mock_context.object = MagicMock()
        mock_context.scene = MagicMock()
        mock_context.scene.collection = MagicMock()
        mock_context.scene.collection.objects = MagicMock()
        mock_context.scene.collection.objects.link = MagicMock()
        
        self.generator = GeometryGenerator(mock_context)
    
    def test_create_cube(self):
        """Test cube creation."""
        import bpy
        bpy.data.meshes = {}
        bpy.data.objects = {}
        
        obj = self.generator.create_cube(
            name="test_cube",
            size=2.0,
            location=[1, 2, 3]
        )
        
        assert obj is not None
        assert obj.name == "test_cube"
        assert obj.location == Vector([1, 2, 3])
    
    def test_create_cylinder(self):
        """Test cylinder creation."""
        import bpy
        bpy.data.meshes = {}
        bpy.data.objects = {}
        
        obj = self.generator.create_cylinder(
            name="test_cylinder",
            radius=1.0,
            depth=2.0,
            location=[0, 0, 1]
        )
        
        assert obj is not None
        assert obj.name == "test_cylinder"
        assert obj.location == Vector([0, 0, 1])
    
    def test_create_cone(self):
        """Test cone creation."""
        import bpy
        bpy.data.meshes = {}
        bpy.data.objects = {}
        
        obj = self.generator.create_cone(
            name="test_cone",
            radius=1.0,
            depth=2.0,
            location=[0, 0, 1]
        )
        
        assert obj is not None
        assert obj.name == "test_cone"
        assert obj.location == Vector([0, 0, 1])


class TestMaterialGenerator:
    """Tests for MaterialGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        mock_context = MagicMock()
        mock_context.object = MagicMock()
        mock_context.scene = MagicMock()
        
        self.generator = MaterialGenerator(mock_context)
    
    def test_create_wood_material(self):
        """Test wood material creation."""
        import bpy
        bpy.data.materials = {}
        
        material = self.generator.create_wood_material(
            name="test_wood",
            color=[0.8, 0.6, 0.4]
        )
        
        assert material is not None
        assert "wood" in material.name
        assert material.use_nodes is True
    
    def test_create_metal_material(self):
        """Test metal material creation."""
        import bpy
        bpy.data.materials = {}
        
        material = self.generator.create_metal_material(
            name="test_metal",
            color=[0.8, 0.8, 0.8]
        )
        
        assert material is not None
        assert "metal" in material.name
        assert material.use_nodes is True
    
    def test_create_fabric_material(self):
        """Test fabric material creation."""
        import bpy
        bpy.data.materials = {}
        
        material = self.generator.create_fabric_material(
            name="test_fabric",
            color=[1.0, 0.5, 0.5]
        )
        
        assert material is not None
        assert "fabric" in material.name
        assert material.use_nodes is True


class TestProceduralLibrary:
    """Tests for ProceduralLibrary."""
    
    def setup_method(self):
        """Set up test fixtures."""
        mock_context = MagicMock()
        mock_context.object = MagicMock()
        mock_context.scene = MagicMock()
        mock_context.scene.collection.objects.link = MagicMock()
        
        self.library = ProceduralLibrary(mock_context)
    
    def test_initialization(self):
        """Test library initialization."""
        assert self.library.geometry is not None
        assert self.library.materials is not None
    
    def test_generate_walls(self):
        """Test wall generation."""
        import bpy
        bpy.data.materials = {}
        bpy.data.objects = {}
        
        walls = self.library.generate_walls(
            width=10.0,
            height=5.0,
            depth=0.5,
            location=[0, 0, 2.5],
            material_name="test_wall"
        )
        
        assert len(walls) > 0
        assert all(isinstance(obj, type(bpy.context.active_object) if hasattr(bpy.context, 'active_object') else MagicMock()) for obj in walls)


class TestIntegration:
    """Integration tests for the procedural module."""
    
    def test_complete_workflow(self):
        """Test complete generation workflow."""
        mock_context = MagicMock()
        mock_context.object = MagicMock()
        mock_context.scene = MagicMock()
        mock_context.scene.collection.objects.link = MagicMock()
        
        import bpy
        bpy.data.materials = {}
        bpy.data.objects = {}
        
        library = ProceduralLibrary(mock_context)
        
        # Generate floor
        floor = library.generate_floor(
            width=10.0,
            depth=10.0,
            material_name="test_floor"
        )
        
        assert len(floor) > 0
        
        # Generate walls
        walls = library.generate_walls(
            width=10.0,
            height=5.0,
            material_name="test_wall"
        )
        
        assert len(walls) > 0
        
        # Generate roof
        roof = library.generate_roof(
            width=10.0,
            height=3.0,
            material_name="test_roof"
        )
        
        assert len(roof) > 0
