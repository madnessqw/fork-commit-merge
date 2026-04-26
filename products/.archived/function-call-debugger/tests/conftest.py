"""
Shared test fixtures and configuration for Function Call Debugger tests.
"""
import pytest
import json
import os
from unittest.mock import patch, MagicMock

@pytest.fixture
def api_process():
    """Load the process.js API handler"""
    return require_js('api/process.js')

@pytest.fixture
def api_health():
    """Load the health.js API handler"""
    return require_js('api/health.js')

@pytest.fixture
def api_webhook():
    """Load the webhook.js API handler"""
    return require_js('api/webhook.js')

@pytest.fixture
def mock_res():
    """Create a mock Vercel serverless response object"""
    res = MagicMock()
    res.status_code = 200
    res.json_data = None
    res.headers = {}
    res.status.return_value = res
    res.json.side_effect = lambda data: setattr(res, 'json_data', data)
    res.end.return_value = res
    def set_header(key, value):
        res.headers[key] = value
    res.setHeader.side_effect = set_header
    return res

@pytest.fixture
def mock_req():
    """Create a mock Vercel serverless request object"""
    req = MagicMock()
    req.method = 'POST'
    req.body = {}
    req.headers = {}
    return req

@pytest.fixture
def sample_js_code():
    """Sample JavaScript code for testing"""
    return 'return 2 + 2;'

@pytest.fixture
def sample_function():
    """Sample function definition for testing"""
    return 'function add(a, b) { return a + b; } add(3, 4);'

def require_js(module_path):
    """Helper to load Node.js modules for testing"""
    import subprocess
    import tempfile

    # Create a test script that loads and exposes the module
    test_script = f'''
    const mod = require('./{module_path}');
    console.log(JSON.stringify({{loaded: typeof mod === 'function'}}));
    '''

    try:
        result = subprocess.run(
            ['node', '-e', test_script],
            capture_output=True,
            text=True,
            cwd='/home/gokhan/UniverseCreator/products/function-call-debugger',
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False
