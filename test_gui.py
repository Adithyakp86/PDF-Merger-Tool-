import tkinter as tk
from tkinter import ttk
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_merger import PDFMergerGUI

def test_gui_creation():
    """Test that the GUI can be created without errors"""
    print("Testing GUI creation...")
    
    try:
        # Create a root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create the PDF merger GUI
        app = PDFMergerGUI(root)
        
        # Check that essential components exist
        assert hasattr(app, 'file_listbox'), "File listbox not created"
        assert hasattr(app, 'progress'), "Progress bar not created"
        assert hasattr(app, 'status_label'), "Status label not created"
        
        print("GUI creation test PASSED")
        return True
        
    except Exception as e:
        print(f"GUI creation test FAILED: {e}")
        return False

def test_config_functions():
    """Test configuration loading and saving"""
    print("Testing configuration functions...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        app = PDFMergerGUI(root)
        
        # Test saving config
        app.save_config()
        
        # Test loading config
        config = app.load_config()
        
        # Check that config has expected keys
        assert isinstance(config, dict), "Config should be a dictionary"
        
        print("Configuration functions test PASSED")
        return True
        
    except Exception as e:
        print(f"Configuration functions test FAILED: {e}")
        return False

def test_theme_functions():
    """Test theme switching functionality"""
    print("Testing theme functions...")
    
    try:
        root = tk.Tk()
        root.withdraw()
        app = PDFMergerGUI(root)
        
        # Test toggling theme
        original_mode = app.dark_mode
        app.toggle_theme()
        assert app.dark_mode != original_mode, "Theme should have toggled"
        
        # Toggle back
        app.toggle_theme()
        assert app.dark_mode == original_mode, "Theme should have toggled back"
        
        print("Theme functions test PASSED")
        return True
        
    except Exception as e:
        print(f"Theme functions test FAILED: {e}")
        return False

if __name__ == "__main__":
    print("Running GUI tests...\n")
    
    tests = [
        test_gui_creation,
        test_config_functions,
        test_theme_functions
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("ALL GUI TESTS PASSED!")
    else:
        print("Some tests failed.")