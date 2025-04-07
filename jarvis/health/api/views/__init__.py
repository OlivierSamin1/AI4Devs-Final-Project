"""
Views initialization file.
"""

from .product_views import ProductViewSet
from .symptom_views import SymptomViewSet
from .bill_views import BillViewSet
from .file_views import (
    FileViewSet,
    FileBillViewSet,
    FileProductViewSet,
    FileSymptomViewSet
)

__all__ = [
    'ProductViewSet',
    'SymptomViewSet',
    'BillViewSet',
    'FileViewSet',
    'FileBillViewSet',
    'FileProductViewSet',
    'FileSymptomViewSet',
] 