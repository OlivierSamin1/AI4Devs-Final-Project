# Import directly, but don't re-export to avoid duplicate module paths
# Assets and Files will be accessed through the parent models.py or directly

# Change from 
# from .asset import Asset
# from .files import File
# 
# __all__ = [
#     Asset,
#     File,
# ]

# To a simple comment explaining the structure
"""
Transportation models package.

This package contains the models for the transportation app:
- asset.py: Asset model
- files.py: File model

These models should be imported directly from their modules or
through the parent models.py file.
"""