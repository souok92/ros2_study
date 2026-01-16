"""
Model wrapper for MobileNetV2 inference.

This module handles:
- Loading the pretrained model
- Image preprocessing
- Running inference
- Postprocessing results
"""

import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple, List

from .config import MODEL_CONFIG, INFERENCE_CONFIG, IMAGENET_CLASSES


class MobileNetInference:
    """
    Wrapper class for MobileNetV2 model inference.

    This class encapsulates all model-related logic, making it easy to
    use in ROS2 nodes or standalone scripts.
    """

    def __init__(self, model_path: str):
        """
        Initialize the model and preprocessing pipeline.

        Args:
            model_path: Path to the .pth model file
        """
        # Determine device
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() and INFERENCE_CONFIG['device'] == 'cuda'
            else 'cpu'
        )
        print("Using device:", self.device)

        # Load model
        # Note: weights_only=False is needed for full model loading
        # Only use this with trusted model files!
        self.model = torch.load(model_path, map_location=self.device, weights_only=False)
        self.model.eval()  # Set to evaluation mode

        # Store config
        self.top_k = INFERENCE_CONFIG['top_k']
        self.confidence_threshold = INFERENCE_CONFIG['confidence_threshold']

        # Create preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(MODEL_CONFIG['input_size']),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=MODEL_CONFIG['mean'],
                std=MODEL_CONFIG['std']
            )
        ])

        print(f"Model loaded successfully on {self.device}")

    def predict(self, image_path: str) -> Tuple[List[int], List[float], List[str]]:
        """
        Run inference on an image.

        Args:
            image_path: Path to the image file

        Returns:
            Tuple of (class_indices, probabilities, class_names)
        """
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        # Run inference
        with torch.no_grad():
            output = self.model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)

        # Get top-k predictions
        top_prob, top_idx = torch.topk(probabilities, self.top_k)

        # Convert to lists
        class_indices = top_idx.cpu().tolist()
        class_probs = top_prob.cpu().tolist()

        # Get class names
        class_names = [
            IMAGENET_CLASSES.get(idx, f'Unknown class {idx}')
            for idx in class_indices
        ]

        # Filter by confidence threshold
        filtered_results = [
            (idx, prob, name)
            for idx, prob, name in zip(class_indices, class_probs, class_names)
            if prob >= self.confidence_threshold
        ]

        if not filtered_results:
            return [], [], []

        indices, probs, names = zip(*filtered_results)
        return list(indices), list(probs), list(names)

    def predict_batch(self, image_paths: List[str]) -> List[Tuple[List[int], List[float], List[str]]]:
        """
        Run inference on multiple images.

        Args:
            image_paths: List of paths to image files

        Returns:
            List of (class_indices, probabilities, class_names) tuples
        """
        results = []
        for img_path in image_paths:
            results.append(self.predict(img_path))
        return results
