import os
import logging
import tensorflow as tf
from tensorflow.keras.models import Sequential
from ultralytics import YOLO
from PIL import Image, ImageOps
import io

logger = logging.getLogger(__name__)

def load_YOLO(name: str, path: str) -> YOLO:
    '''
    Load YOLO model

    Args:
        name: name of the model
        path: path to the model weights

    Returns: 
        YOLO model
    '''

    model_path = os.path.join(path, name)
    if os.path.exists(model_path):
        model = YOLO(model_path)
        logger.info(f'Loaded YOLO model from {model_path}')
        return model
    else:
        logger.error(f'Model {name} not found at {path}')
        return None
    
def load_CNN(name: str, path: str) -> Sequential:
    '''
    Load the CNN model we deployed

    Args:
        name: name of the model
        path: path to the model weights
    
    Returns:
        CNN model
    '''
    model_path = os.path.join(path, name)
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        logger.info(f'Loaded CNN model from {model_path}')
        return model
    else:
        logger.error(f'Model {name} not found at {path}')
        return None
    
def read_image(bytes: bytes) -> Image.Image:
    '''
    Read image from bytes

    Args:
        bytes: image data in bytes
    Returns:
        PIL Image
    '''
    image = Image.open(io.BytesIO(bytes)).convert('RGB')
    image = ImageOps.exif_transpose(image)

    return image