"""Tests for the Blender client."""

import pytest
import sys
import os
import json
from unittest.mock import MagicMock, patch, mock_open

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from 3d_agent_md.blender_client import BlenderClient, create_blender_client


class TestBlenderClient:
    """Tests for BlenderClient."""
    
    @pytest.fixture
    def mock_context(self):
        """Create a mock context."""
        return MagicMock()
    
    @patch('subprocess.run')
    def test_check_blender_available(self, mock_run, tmp_path):
        """Test that Blender availability check works."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        client = BlenderClient(blender_path=str(tmp_path / "blender"), background=True)
        assert client is not None
    
    @patch('subprocess.run')
    def test_check_blender_not_found(self, mock_run):
        """Test error handling when Blender is not found."""
        mock_run.side_effect = FileNotFoundError("Blender not found")
        
        with pytest.raises(RuntimeError):
            BlenderClient(blender_path="nonexistent_blender_binary", background=True)
    
    @patch('subprocess.run')
    def test_execute_script(self, mock_run, mock_context):
        """Test script execution."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"success": true}'
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        client = BlenderClient(background=True)
        
        result = client.execute_script("print('hello')")
        
        assert result.get('success') is True
        assert 'stdout' in result
    
    @patch('subprocess.run')
    def test_execute_script_failure(self, mock_run):
        """Test script execution with failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error occurred"
        mock_run.return_value = mock_result
        
        client = BlenderClient(background=True)
        
        result = client.execute_script("invalid_python_code()")
        
        assert result.get('success') is False
        assert 'stderr' in result
        assert 'Error occurred' in result.get('stderr', '')


class TestFactoryFunction:
    """Tests for create_blender_client factory function."""
    
    @patch('subprocess.run')
    def test_create_client_default(self, mock_run):
        """Test factory function with default parameters."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        client = create_blender_client()
        
        assert client is not None
        assert client.background is True


class TestBlenderIntegration:
    """Integration tests for Blender client."""
    
    @patch('subprocess.run')
    def test_execute_with_json_output(self, mock_run, mock_context):
        """Test execution returning JSON."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            "success": True,
            "objects": 5,
            "meshes": 3
        })
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        client = BlenderClient(background=True)
        
        result = client.execute_script("test_script", output_format="json")
        
        assert result['success'] is True
        assert 'objects' in result
        assert result['objects'] == 5
    
    @patch('subprocess.run')
    def test_execute_with_text_output(self, mock_run, mock_context):
        """Test execution returning text."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Output text here"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        client = BlenderClient(background=True)
        
        result = client.execute_script("test_script", output_format="text")
        
        assert result['success'] is True
        assert 'stdout' in result
        assert 'Output text here' in result['stdout']
