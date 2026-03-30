"""Tests for the CLI interface."""

import pytest
import sys
import os
import json
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from 3d_agent_md.cli import main, execute, generate, version, test, demo


class TestCLI:
    """Tests for CLI commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    @patch('subprocess.run')
    def test_version_command(self, mock_run):
        """Test version command."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Blender 4.0"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.runner.invoke(version, ['--blender', 'test_blender'])
        
        assert result.exit_code == 0
        assert "Blender version:" in result.output
    
    @patch('subprocess.run')
    def test_test_command_success(self, mock_run):
        """Test test command with success."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "success": True,
            "objects": 1,
            "meshes": 1,
            "materials": 0
        })
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.runner.invoke(test, ['--blender', 'test_blender'])
        
        assert result.exit_code == 0
        assert "All tests passed!" in result.output
    
    @patch('subprocess.run')
    def test_test_command_failure(self, mock_run):
        """Test test command with failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = json.dumps({"success": False})
        mock_result.stderr = "Error"
        mock_run.return_value = mock_result
        
        result = self.runner.invoke(test, ['--blender', 'test_blender'])
        
        assert result.exit_code != 0
        assert "Test failed" in result.output
    
    @patch('builtins.open', new_callable=MagicMock)
    @patch('subprocess.run')
    def test_generate_command(self, mock_run, mock_open):
        """Test generate command."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({"success": True, "message": "Generated"})
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        # Mock file reading
        mock_open.return_value.__enter__ = lambda s: s
        mock_open.return_value.__exit__ = MagicMock()
        mock_open.return_value.read.return_value = json.dumps({
            "name": "test",
            "script": "print('test')"
        })
        
        result = self.runner.invoke(generate, [
            '--blender', 'test_blender',
            '--config', 'test_config.yaml',
            '--output', 'test_output.blend'
        ])
        
        assert result.exit_code == 0
        assert "Generation complete" in result.output
    
    def test_demo_command(self):
        """Test demo command."""
        result = self.runner.invoke(demo, [
            '--name', 'test_tavern',
            '--type', 'tavern',
            '--output', 'test.blend'
        ])
        
        assert result.exit_code == 0
        assert "Generating tavern" in result.output
    
    def test_help_command(self):
        """Test help output."""
        result = self.runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "3D-Agent.md" in result.output


class TestCLIEdgeCases:
    """Edge case tests for CLI."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    @patch('builtins.open', new_callable=MagicMock)
    def test_generate_empty_config(self, mock_open):
        """Test generate with empty config."""
        mock_open.return_value.__enter__ = lambda s: s
        mock_open.return_value.__exit__ = MagicMock()
        mock_open.return_value.read.return_value = ""
        
        result = self.runner.invoke(generate, [
            '--blender', 'test_blender',
            '--config', 'empty.yaml',
            '--output', 'output.blend'
        ])
        
        assert result.exit_code != 0
        assert "Empty configuration file" in result.output
    
    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        """Test execute command with success."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({"success": True})
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.runner.invoke(execute, [
            '--blender', 'test_blender',
            '--script', 'test_script.py'
        ])
        
        assert result.exit_code == 0
        assert "Results written to" in result.output
