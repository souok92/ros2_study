import torch
from torchvision import models
from torchvision.models import MobileNet_V2_Weights

model = models.mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)