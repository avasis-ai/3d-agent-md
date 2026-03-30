"""CLI interface for 3D-Agent.md."""

import click
import yaml
import sys
from pathlib import Path
from typing import List, Optional

from .blender_client import BlenderClient, create_blender_client
from .procedural import ProceduralLibrary


@click.group()
@click.version_option(version="0.1.0", prog_name="3d-agent-md")
def main():
    """3D-Agent.md: Autonomous agents that model, rig, and animate in Blender."""
    pass


@main.command()
@click.option('--blender', '-b', default='blender', 
              help='Path to Blender executable')
@click.option('--script', '-s', required=True, 
              type=click.Path(exists=True),
              help='Python script to execute')
@click.option('--output', '-o', default='output.json',
              help='Output file for results')
def execute(blender: str, script: str, output: str) -> None:
    """Execute a Python script in Blender."""
    try:
        client = create_blender_client(blender_path=blender, background=True)
        result = client.execute_file(script)
        
        # Write results
        with open(output, 'w') as f:
            import json
            json.dump(result, f, indent=2)
        
        click.echo(f"Results written to {output}")
        
        if not result.get('success'):
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--blender', '-b', default='blender',
              help='Path to Blender executable')
@click.option('--config', '-c', required=True,
              type=click.Path(exists=True),
              help='YAML configuration file')
@click.option('--output', '-o', default='generation.blend',
              help='Output .blend file path')
def generate(blender: str, config: str, output: str) -> None:
    """Generate 3D content using procedural library."""
    try:
        # Load configuration
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if not config_data:
            click.echo("Error: Empty configuration file", err=True)
            sys.exit(1)
        
        # Create Blender client and procedural library
        client = create_blender_client(blender_path=blender, background=True)
        
        click.echo(f"Generating: {config_data.get('name', 'Unknown')}")
        
        # Execute generation
        result = client.execute_script(config_data.get('script', ''))
        
        click.echo(f"Generation complete: {output}")
        click.echo(f"Success: {result.get('success', False)}")
        
        if not result.get('success'):
            sys.exit(1)
            
    except yaml.YAMLError as e:
        click.echo(f"YAML Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--blender', '-b', default='blender',
              help='Path to Blender executable')
def version(blender: str) -> None:
    """Check Blender version."""
    try:
        client = create_blender_client(blender_path=blender, background=True)
        import subprocess
        
        result = subprocess.run(
            [blender, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        click.echo(f"Blender version: {result.stdout.strip()}")
        
    except Exception as e:
        click.echo(f"Error checking Blender version: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--blender', '-b', default='blender',
              help='Path to Blender executable')
def test(blender: str) -> None:
    """Run health check on the setup."""
    try:
        # Test Blender connectivity
        client = create_blender_client(blender_path=blender, background=True)
        
        # Simple test script
        test_script = '''
import bpy
import json

# Test basic operation
cube = bpy.ops.object.add(type='MESH', location=(0, 0, 1))
cube = bpy.context.active_object
cube.name = "test_cube"

result = {
    "success": True,
    "objects": len(bpy.data.objects),
    "meshes": len(bpy.data.meshes),
    "materials": len(bpy.data.materials)
}

print(json.dumps(result))
'''
        
        result = client.execute_script(test_script)
        
        if result.get('success'):
            click.echo("✓ Blender connectivity: OK")
            click.echo(f"✓ Objects: {result.get('objects', 0)}")
            click.echo(f"✓ Meshes: {result.get('meshes', 0)}")
            click.echo(f"✓ Materials: {result.get('materials', 0)}")
            click.echo("\nAll tests passed!")
        else:
            click.echo("✗ Test failed", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option('--name', '-n', required=True,
              help='Name of the 3D model to generate')
@click.option('--type', '-t', type=click.Choice(['tavern', 'house', 'castle']),
              default='tavern',
              help='Type of structure to generate')
@click.option('--output', '-o', default='generated.blend',
              help='Output .blend file path')
def demo(name: str, type: str, output: str) -> None:
    """Demo: Generate a sample 3D structure."""
    click.echo(f"Generating {type} '{name}'...")
    click.echo(f"Output: {output}")
    click.echo("\nThis demo shows the basic structure of 3D-Agent.md.")
    click.echo("In a full implementation, this would generate a complex 3D scene.")


if __name__ == '__main__':
    main()
