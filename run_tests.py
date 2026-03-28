#!/usr/bin/env python3
"""
Test runner script for the inventory management system
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import pytest
    
    # Run pytest with verbose output
    exit_code = pytest.main(['test_app.py', '-v'])
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ Tests failed with exit code: {exit_code}")
    
    sys.exit(exit_code)
    
except ImportError:
    print("❌ pytest not found. Please install it with:")
    print("pip install pytest")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error running tests: {e}")
    sys.exit(1)
