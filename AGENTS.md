# AGENTS.md - 3D-Agent.md Project Context

This folder is home. Treat it that way.

## Project: 3D-Agent.md (#54)

### Identity
- **Name**: 3D-Agent.md
- **License**: GPL-3.0
- **Org**: avasis-ai
- **PyPI**: 3d-agent-md
- **Version**: 0.1.0
- **Tagline**: Autonomous agents that model, rig, and animate directly in Blender

### What It Does
Connecting an LLM directly to Blender's Python API via a specialized SKILL.md, users can create complex 3D scenes with natural language prompts. The agent sequentially executes Python commands to generate geometry and materials natively in Blender.

### Inspired By
- Blender Python API
- MCP (Multi-Agent Collaboration Protocol)
- Multimodal + 3D generation technologies

### Core Components

#### `/blender-plugin/`
- Core Blender integration layer
- Script execution engine
- Context management

#### `/agent-core/`
- Procedural generation library
- Material system
- Geometry generators
- CLI interface

#### `/docs/`
- API documentation
- Tutorials
- Best practices

### Technical Architecture

**Key Dependencies:**
- `pyyaml>=6.0` - Configuration parsing (Trust score: 7.4)
- `click>=8.0` - CLI framework (Trust score: 8.8)

**Core Modules:**
1. `blender_client.py` - Blender API client
2. `procedural.py` - Procedural generation library
3. `cli.py` - Command-line interface

### AI Coding Agent Guidelines

#### When Contributing:

1. **Understand the moat**: An exhaustive, highly tuned library of procedural generation scripts mapped to semantic intents bypasses the LLM's inability to understand complex 3D spatial geometry natively.

2. **Respect the Blender API**: All operations must be valid Blender Python code. Test thoroughly.

3. **Use Context7**: Check trust scores for new libraries before adding dependencies.

4. **Type safety**: Always use type hints and docstrings.

#### What to Remember:

- **Procedural generation is key**: Don't try to make LLMs understand 3D space. Map semantic intents to pre-built procedural functions.
- **Materials matter**: Wood, metal, fabric materials are pre-configured with realistic properties.
- **Geometry primitives**: Cube, cylinder, cone are the building blocks for complex structures.
- **Mock support**: Tests use mocked Blender context for reliable CI/CD.

#### Common Patterns:

**Creating Geometry:**
```python
from 3d_agent_md.procedural import ProceduralLibrary

library = ProceduralLibrary(bpy.context)
walls = library.generate_walls(width=10, height=5, material_name="stone")
```

**Using Materials:**
```python
wood_mat = library.materials.create_wood_material("my_wood")
wall.materials.append(wood_mat)
```

**CLI Usage:**
```bash
3d-agent-md generate --config tavern.yaml --output tavern.blend
```

### Project Status

- ✅ Initial implementation complete
- ✅ CLI interface functional
- ✅ Procedural library with geometry & materials
- ✅ Comprehensive test suite
- ⚠️ Full SKILL.md integration pending
- ⚠️ LLM prompt mapping in progress

### How to Work with This Project

1. **Read `SOUL.md`** - Understand who you are
2. **Read `USER.md`** - Know who you're helping
3. **Check `memory/YYYY-MM-DD.md`** - Recent context
4. **Read `MEMORY.md`** - Long-term decisions (main session only)
5. **Execute**: Code → Test → Commit

### Red Lines

- **No stubs or TODOs**: Every function must have real implementation
- **Type hints required**: All function signatures must include types
- **Docstrings mandatory**: Explain what, why, and how
- **Test coverage**: New features need tests
- **Blender compatibility**: All code must work with Blender 3.0+

### Development Workflow

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/
isort src/ tests/

# Check syntax
python -m py_compile src/3d_agent_md/*.py

# Commit
git add -A && git commit -m "feat: add procedural generation"
```

### Key Files to Understand

- `src/3d_agent_md/blender_client.py` - How we talk to Blender
- `src/3d_agent_md/procedural.py` - Core generation logic
- `src/3d_agent_md/cli.py` - CLI interface
- `pyproject.toml` - Project metadata and dependencies

### Security Considerations

- All processing is local - no external API calls
- Trust model: Personal assistant (one trusted operator boundary)
- Dependencies verified via Context7

### Next Steps

1. Complete the SKILL.md integration layer
2. Build LLM prompt-to-procedural mapping
3. Add more geometry types (arches, stairs, windows)
4. Implement animation system
5. Create sample generation scripts

---

**This file should evolve as you learn more about the project.**
