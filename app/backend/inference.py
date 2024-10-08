import logging
from tensorflow.keras.models import Sequential
from ultralytics import YOLO
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

# LABELS = {
#     0:'alb_id', 
#     1:'aze_passport', 
#     2:'esp_id', 
#     3:'est_id', 
#     4:'fin_id', 
#     5:'grc_passport', 
#     6:'lva_passport', 
#     7:'rus_internalpassport', 
#     8:'srb_passport', 
#     9:'svk_id'
# }

LABELS = {
    0:'ID Card of Albania', 
    1:'Passport of Azerbaijan', 
    2:'ID Card of Spain', 
    3:'ID Card of Estonia', 
    4:'ID Card of Finland', 
    5:'Passport of Greece', 
    6:'Passport of Latvia', 
    7:'Internal passport of Russia', 
    8:'Passport of Serbia', 
    9:'ID Card of Slovakia'
}

def segment(model: YOLO, image: Image.Image) -> Image.Image:
    '''
    Segment the ID/Passport using YOLO model

    Args:
        model: YOLO model
        image: input image to segment

    Returns: 
        cropped ID/Passport
    '''

    results = model.predict(image)
    try:
        bounds = results[0].boxes.xyxy[0].tolist()
        cropped_image = image.crop((bounds[0], bounds[1], bounds[2], bounds[3]))

    except IndexError:
        logger.warning('No bounding box detected in the image')
        return image

    logger.info('ID/Passport segmented')

    return cropped_image

def predict(model: Sequential, image: Image.Image) -> str:
    '''
    Predict the country using CNN model

    Args:
        model: CNN model
        image: input image

    Returns: 
        predicted country
    '''

    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    label = np.argmax(predictions, axis=1)[0]

    logger.info(f'Predicted country: {LABELS[label]}')

    return LABELS[label]