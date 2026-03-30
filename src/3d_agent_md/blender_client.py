"""Blender client for executing Python commands via Blender's Python API."""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import time


class BlenderClient:
    """Client for interacting with Blender's Python API."""
    
    def __init__(self, blender_path: str = "blender", background: bool = True):
        """
        Initialize the Blender client.
        
        Args:
            blender_path: Path to the Blender executable
            background: Run Blender in background/headless mode
        """
        self.blender_path = blender_path
        self.background = background
        self._check_blender_available()
    
    def _check_blender_available(self) -> None:
        """Check if Blender is available in the system."""
        try:
            result = subprocess.run(
                [self.blender_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise RuntimeError(f"Blender version check failed: {result.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "Blender not found. Please install Blender and ensure it's in your PATH, "
                "or specify the path via the blender_path parameter."
            )
    
    def execute_script(
        self,
        script: str,
        blend_file: Optional[str] = None,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Execute a Python script in Blender.
        
        Args:
            script: Python code to execute in Blender
            blend_file: Optional .blend file to load before executing
            output_format: Output format ("json" or "text")
            
        Returns:
            Result dictionary with success status and output data
        """
        # Create a temporary script file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            script_path = f.name
        
        try:
            # Build Blender command
            cmd = [self.blender_path]
            if self.background:
                cmd.append('--background')
            if blend_file:
                cmd.extend(['--', blend_file])
            else:
                cmd.extend(['--', '--python', script_path])
            
            # Execute
            result = subprocess.run(
                cmd + ['--python', script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for complex operations
            )
            
            # Parse output
            if output_format == "json":
                # Try to parse JSON from stdout
                try:
                    return json.loads(result.stdout.strip())
                except json.JSONDecodeError:
                    # If no valid JSON, return raw output
                    return {
                        "success": result.returncode == 0,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
            else:
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(script_path)
            except OSError:
                pass
    
    def execute_file(self, file_path: str, blend_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a Python script file in Blender.
        
        Args:
            file_path: Path to the Python script file
            blend_file: Optional .blend file to load before executing
            
        Returns:
            Result dictionary with success status and output data
        """
        with open(file_path, 'r') as f:
            script = f.read()
        return self.execute_script(script, blend_file)
    
    def spawn_editor_session(self, blend_file: Optional[str] = None) -> int:
        """
        Spawn an interactive Blender editor session.
        
        Args:
            blend_file: Optional .blend file to open
            
        Returns:
            Process ID of the spawned Blender process
        """
        cmd = [self.blender_path]
        if blend_file:
            cmd.append(blend_file)
        
        process = subprocess.Popen(cmd)
        return process.pid


def create_blender_client(
    blender_path: str = "blender",
    background: bool = True
) -> BlenderClient:
    """
    Factory function to create a BlenderClient instance.
    
    Args:
        blender_path: Path to the Blender executable
        background: Run Blender in background/headless mode
        
    Returns:
        Configured BlenderClient instance
    """
    return BlenderClient(blender_path=blender_path, background=background)
