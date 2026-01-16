"""
ROS2 node for image classification using MobileNetV2.

This node demonstrates how to:
1. Load a pretrained PyTorch model from package data files
2. Subscribe to image paths and run AI inference
3. Publish classification results to another topic
4. Use GPU (CUDA) when available, fallback to CPU
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ament_index_python.packages import get_package_share_directory
import os

import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple, List


# ImageNet class labels (dogs and cats only)
IMAGENET_CLASSES = {
    # Cats
    281: 'tabby, tabby cat',
    282: 'tiger cat',
    283: 'Persian cat',
    284: 'Siamese cat, Siamese',
    285: 'Egyptian cat',

    # Dogs
    151: 'Chihuahua',
    152: 'Japanese spaniel',
    153: 'Maltese dog, Maltese terrier, Maltese',
    154: 'Pekinese, Pekingese, Peke',
    155: 'Shih-Tzu',
    156: 'Blenheim spaniel',
    157: 'papillon',
    158: 'toy terrier',
    159: 'Rhodesian ridgeback',
    160: 'Afghan hound, Afghan',
    161: 'basset, basset hound',
    162: 'beagle',
    163: 'bloodhound, sleuthhound',
    164: 'bluetick',
    165: 'black-and-tan coonhound',
    166: 'Walker hound, Walker foxhound',
    167: 'English foxhound',
    168: 'redbone',
    169: 'borzoi, Russian wolfhound',
    170: 'Irish wolfhound',
    171: 'Italian greyhound',
    172: 'whippet',
    173: 'Ibizan hound, Ibizan Podenco',
    174: 'Norwegian elkhound, elkhound',
    175: 'otterhound, otter hound',
    176: 'Saluki, gazelle hound',
    177: 'Scottish deerhound, deerhound',
    178: 'Weimaraner',
    179: 'Staffordshire bullterrier, Staffordshire bull terrier',
    180: 'American Staffordshire terrier, Staffordshire terrier, American pit bull terrier, pit bull terrier',
    181: 'Bedlington terrier',
    182: 'Border terrier',
    183: 'Kerry blue terrier',
    184: 'Irish terrier',
    185: 'Norfolk terrier',
    186: 'Norwich terrier',
    187: 'Yorkshire terrier',
    188: 'wire-haired fox terrier',
    189: 'Lakeland terrier',
    190: 'Sealyham terrier, Sealyham',
    191: 'Airedale, Airedale terrier',
    192: 'cairn, cairn terrier',
    193: 'Australian terrier',
    194: 'Dandie Dinmont, Dandie Dinmont terrier',
    195: 'Boston bull, Boston terrier',
    196: 'miniature schnauzer',
    197: 'giant schnauzer',
    198: 'standard schnauzer',
    199: 'Scotch terrier, Scottish terrier, Scottie',
    200: 'Tibetan terrier, chrysanthemum dog',
    201: 'silky terrier, Sydney silky',
    202: 'soft-coated wheaten terrier',
    203: 'West Highland white terrier',
    204: 'Lhasa, Lhasa apso',
    205: 'flat-coated retriever',
    206: 'curly-coated retriever',
    207: 'golden retriever',
    208: 'Labrador retriever',
    209: 'Chesapeake Bay retriever',
    210: 'German short-haired pointer',
    211: 'vizsla, Hungarian pointer',
    212: 'English setter',
    213: 'Irish setter, red setter',
    214: 'Gordon setter',
    215: 'Brittany spaniel',
    216: 'clumber, clumber spaniel',
    217: 'English springer, English springer spaniel',
    218: 'Welsh springer spaniel',
    219: 'cocker spaniel, English cocker spaniel, cocker',
    220: 'Sussex spaniel',
    221: 'Irish water spaniel',
    222: 'kuvasz',
    223: 'schipperke',
    224: 'groenendael',
    225: 'malinois',
    226: 'briard',
    227: 'kelpie',
    228: 'komondor',
    229: 'Old English sheepdog, bobtail',
    230: 'Shetland sheepdog, Shetland sheep dog, Shetland',
    231: 'collie',
    232: 'Border collie',
    233: 'Bouvier des Flandres, Bouviers des Flandres',
    234: 'Rottweiler',
    235: 'German shepherd, German shepherd dog, German police dog, alsatian',
    236: 'Doberman, Doberman pinscher',
    237: 'miniature pinscher',
    238: 'Greater Swiss Mountain dog',
    239: 'Bernese mountain dog',
    240: 'Appenzeller',
    241: 'EntleBucher',
    242: 'boxer',
    243: 'bull mastiff',
    244: 'Tibetan mastiff',
    245: 'French bulldog',
    246: 'Great Dane',
    247: 'Saint Bernard, St Bernard',
    248: 'Eskimo dog, husky',
    249: 'malamute, malemute, Alaskan malamute',
    250: 'Siberian husky',
    251: 'dalmatian, coach dog, carriage dog',
    252: 'affenpinscher, monkey pinscher, monkey dog',
    253: 'basenji',
    254: 'pug, pug-dog',
    255: 'Leonberg',
    256: 'Newfoundland, Newfoundland dog',
    257: 'Great Pyrenees',
    258: 'Samoyed, Samoyede',
    259: 'Pomeranian',
    260: 'chow, chow chow',
    261: 'keeshond',
    262: 'Brabancon griffon',
    263: 'Pembroke, Pembroke Welsh corgi',
    264: 'Cardigan, Cardigan Welsh corgi',
    265: 'toy poodle',
    266: 'miniature poodle',
    267: 'standard poodle',
    268: 'Mexican hairless',
    269: 'timber wolf, grey wolf, gray wolf, Canis lupus',
    270: 'white wolf, Arctic wolf, Canis lupus tundrarum',
    271: 'red wolf, maned wolf, Canis rufus, Canis niger',
    272: 'coyote, prairie wolf, brush wolf, Canis latrans',
    273: 'dingo, warrigal, warragal, Canis dingo',
    274: 'dhole, Cuon alpinus',
    275: 'African hunting dog, hyena dog, Cape hunting dog, Lycaon pictus',
}


class InferenceNode(Node):
    """
    ROS2 node that performs image classification using MobileNetV2.

    Subscribes to: /image_path (String) - path to image file
    Publishes to: /inference_result (String) - formatted classification results
    """

    def __init__(self):
        super().__init__('inference_node')

        # Get package share directory
        pkg_dir = get_package_share_directory('template_python_step_5_include_data')
        model_path = os.path.join(pkg_dir, 'models/mobilenet_v2.pth')

        self.get_logger().info(f'Loading model from: {model_path}')

        # Determine device (GPU if available, otherwise CPU)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.get_logger().info(f'Using device: {self.device}')

        # Load model
        # Note: weights_only=False is needed for full model loading
        # Only use this with trusted model files!
        self.model = torch.load(model_path, map_location=self.device, weights_only=False)
        self.model.eval()  # Set to evaluation mode

        # Inference configuration
        self.top_k = 5
        self.confidence_threshold = 0.01

        # Create image preprocessing pipeline
        # These are standard ImageNet preprocessing steps
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],  # ImageNet mean
                std=[0.229, 0.224, 0.225]     # ImageNet std
            )
        ])

        self.get_logger().info('Model loaded successfully!')

        # Create subscriber for image paths
        self.subscription = self.create_subscription(
            String,
            'image_path',
            self.image_path_callback,
            10
        )

        # Create publisher for inference results
        self.publisher = self.create_publisher(String, 'inference_result', 10)

        # Counter for tracking inferences
        self.inference_count = 0

        self.get_logger().info('InferenceNode ready! Waiting for image paths...')

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

    def image_path_callback(self, msg):
        """
        Callback function that runs inference on received image path.

        Args:
            msg: String message containing the image path
        """
        image_path = msg.data
        image_name = os.path.basename(image_path)

        self.get_logger().info(f'Running inference on: {image_name}')

        try:
            # Run inference
            class_indices, probabilities, class_names = self.predict(image_path)

            if not class_indices:
                self.get_logger().warn('No predictions above confidence threshold')
                return

            # Format and publish results
            result_msg = String()
            result_lines = [
                f'Image: {image_name}',
                f'Predictions:'
            ]

            for i, (idx, prob, name) in enumerate(zip(class_indices, probabilities, class_names)):
                result_lines.append(f'  {i+1}. {name} (confidence: {prob:.2%})')

            result_msg.data = '\n'.join(result_lines)

            self.publisher.publish(result_msg)
            self.get_logger().info(f'Published inference result #{self.inference_count}')

            self.inference_count += 1

        except Exception as e:
            self.get_logger().error(f'Inference failed: {e}')


def main(args=None):
    rclpy.init(args=args)

    try:
        node = InferenceNode()
        rclpy.spin(node)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
