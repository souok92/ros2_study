"""
AI module for model inference.

This module contains:
- config.py: AI model parameters and constants
- model_wrapper.py: Model loading and inference logic
"""

from .config import MODEL_CONFIG, INFERENCE_CONFIG, IMAGENET_CLASSES, FILE_PATHS
from .model_wrapper import MobileNetInference

__all__ = ['MODEL_CONFIG', 'INFERENCE_CONFIG', 'IMAGENET_CLASSES', 'FILE_PATHS', 'MobileNetInference']
