import unittest
import numpy as np
from cs107_project.visualization_interactive import viz_tool_interactive

class TestInteractiveVisualization(unittest.TestCase):

    def test_interactive_spectral_initialization(self):
        wavelen = np.random.normal(size=100) * 100
        flux = wavelen ** 2 + np.random.normal(size=100) * 200
        tool = viz_tool_interactive()

        # Check if the method initializes without errors
        try:
            tool.interactive_spectral(wavelen, flux, "test")
            initialization_success = True
        except Exception as e:
            initialization_success = False

        self.assertTrue(initialization_success, "The interactive_spectral method failed to initialize")

    def test_widget_creation(self):
        wavelen = np.random.normal(size=100) * 100
        flux = wavelen ** 2 + np.random.normal(size=100) * 200
        tool = viz_tool_interactive()

        # Check if the widget is created
        try:
            tool.interactive_spectral(wavelen, flux, "test")
            widget_created = True
        except Exception as e:
            widget_created = False

        self.assertTrue(widget_created, "Widgets for interactive visualization were not created")
