"""
COVID-19 EMD Analysis Package

Python package for analyzing COVID-19 spread data using Empirical Mode Decomposition (EMD)
"""

__version__ = "1.0.0"
__author__ = "randong"

from .emd_analyzer import EMDAnalyzer
from .data_loader import DataLoader
from .visualization import EMDVisualizer

__all__ = [
    'EMDAnalyzer', 
    'DataLoader', 
    'EMDVisualizer'
] 