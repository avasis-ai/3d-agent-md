# README.md - 3D-Agent.md

## Autonomy Agents that Model, Rig, and Animate Directly in Blender

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/3d-agent-md.svg)](https://pypi.org/project/3d-agent-md/)

**3D-Agent.md** is a revolutionary tool that connects LLMs directly to Blender's Python API, enabling autonomous agents to create complex 3D scenes through natural language prompts.

## 🎯 What It Does

With 3D-Agent.md, you can:

- **Create 3D scenes** with natural language commands
- **Generate procedural geometry** (walls, floors, roofs, shapes)
- **Apply materials** (wood, metal, fabric) with realistic properties
- **Model, rig, and animate** directly in Blender
- **Bridge AI and digital art** by democratizing 3D creation

### Example Use Case

```python
# Create a low-poly medieval tavern
from 3d_agent_md.procedural import ProceduralLibrary

# Generate a complete tavern structure
library = ProceduralLibrary(bpy.context)
walls = library.generate_walls(width=20, height=8)
floor = library.generate_floor(width=20, depth=15)
roof = library.generate_roof(width=20, depth=15, height=5)

# Apply materials
wall_mat = library.materials.create_wood_material("tavern_wood")
```

## 🚀 Features

- **Procedural Generation Library**: Comprehensive collection of 3D generation scripts
- **Blender API Integration**: Seamless communication with Blender's Python API
- **CLI Tools**: Command-line interface for executing generation scripts
- **Material Library**: Pre-configured materials for wood, metal, fabric, and more
- **Geometry Primitives**: Cube, cylinder, cone generators with full customization
- **Mock Support**: Testable with mocked Blender context

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Blender 3.0+ (optional, for execution)
- Git (optional, for development)

### Install from PyPI

```bash
pip install 3d-agent-md
```

### Install from Source

```bash
git clone https://github.com/avasis-ai/3d-agent-md.git
cd 3d-agent-md
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
pip install pytest pytest-mock black isort
```

## 🔧 Usage

### Command-Line Interface

```bash
# Check Blender version
3d-agent-md version

# Run health check
3d-agent-md test

# Generate a sample structure
3d-agent-md demo --name "my_tavern" --type tavern

# Execute a Python script in Blender
3d-agent-md execute --script my_script.py

# Generate 3D content from YAML config
3d-agent-md generate --config generation.yaml --output scene.blend
```

### Programmatic Usage

```python
from 3d_agent_md.procedural import ProceduralLibrary

# Initialize with Blender context
library = ProceduralLibrary(bpy.context)

# Generate walls
walls = library.generate_walls(
    width=10.0,
    height=5.0,
    depth=0.5,
    location=[0, 0, 2.5],
    material_name="stone_wall"
)

# Generate floor
floor = library.generate_floor(
    width=10.0,
    depth=10.0,
    material_name="wood_floor"
)

# Generate roof
roof = library.generate_roof(
    width=10.0,
    height=3.0,
    material_name="tile_roof"
)
```

### Blender Client API

```python
from 3d_agent_md.blender_client import create_blender_client

# Create client
client = create_blender_client(
    blender_path='/path/to/blender',
    background=True
)

# Execute script
result = client.execute_script('''
import bpy
# Your Blender Python code here
cube = bpy.ops.object.add(type='MESH', location=(0, 0, 1))
''')

print(f"Success: {result['success']}")
print(f"Objects created: {result.get('objects', 0)}")
```

## 📚 API Reference

### ProceduralLibrary

Main entry point for procedural generation.

#### `generate_walls(width, height, depth, location, material_name)`

Generate wall structure.

**Parameters:**
- `width` (float): Wall width
- `height` (float): Wall height  
- `depth` (float): Wall thickness
- `location` (list): [x, y, z] position
- `material_name` (str): Material name

**Returns:** List of wall objects

#### `generate_floor(width, depth, location, material_name)`

Generate floor structure.

#### `generate_roof(width, depth, height, location, material_name)`

Generate roof structure.

### GeometryGenerator

Create basic 3D geometry.

#### `create_cube(name, size, location)`

Create a cube mesh.

#### `create_cylinder(name, radius, depth, location)`

Create a cylinder mesh.

#### `create_cone(name, radius, depth, location)`

Create a cone mesh.

### MaterialGenerator

Create and configure materials.

#### `create_wood_material(name, color)`

Create wood-like material.

#### `create_metal_material(name, color)`

Create metal-like material.

#### `create_fabric_material(name, color)`

Create fabric-like material.

## 🧪 Testing

Run tests with pytest:

```bash
python -m pytest tests/ -v
```

## 📁 Project Structure

```
3d-agent-md/
├── README.md
├── pyproject.toml
├── src/
│   └── 3d_agent_md/
│       ├── __init__.py
│       ├── blender_client.py
│       ├── cli.py
│       └── procedural.py
├── tests/
│   ├── test_procedural.py
│   ├── test_blender_client.py
│   └── test_cli.py
└── .github/
    └── ISSUE_TEMPLATE/
        └── bug_report.md
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `python -m pytest tests/ -v`
5. **Submit a pull request**

### Development Setup

```bash
git clone https://github.com/avasis-ai/3d-agent-md.git
cd 3d-agent-md
pip install -e ".[dev]"
pre-commit install  # Optional, for automatic formatting
```

## 📝 License

This project is licensed under the **GNU General Public License v3.0** (GPL-3.0). See [LICENSE](LICENSE) for details.

## 🎯 Vision

3D-Agent.md democratizes 3D creation by:

- **Reducing the learning curve**: No need to master Blender's complex interface
- **Bridging AI and art**: Connect LLM reasoning with visual creation
- **Enabling rapid prototyping**: Generate scenes in seconds, not hours
- **Empowering artists**: Focus on creativity, not technical details

## 🌟 Viral Potential

This tool is extremely visual and highly shareable. Watch AI generate:

- Medieval taverns with detailed wood and stone
- Futuristic cities with metal and glass
- Fantasy castles with realistic materials
- Abstract art installations with procedural geometry

## 🛡️ Security & Trust

- **High-trust dependencies**: Click (8.8), PyYAML (7.4) - [Context7 verified](https://context7.com)
- **GPL-3.0 license**: Open source, community-driven
- **No external API calls**: All processing local

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/avasis-ai/3d-agent-md/wiki)
- **Issues**: [GitHub Issues](https://github.com/avasis-ai/3d-agent-md/issues)
- **Discord**: [Join our community](https://discord.gg/3d-agent-md)

## 🙏 Acknowledgments

- **Blender Foundation** for the incredible Blender API
- **MCP** for the multi-agent collaboration inspiration
- **The 3D community** for shared knowledge and techniques

---

**Made with ❤️ by [Avasis AI](https://avasis.ai)**

*The future of 3D creation is autonomous.*
