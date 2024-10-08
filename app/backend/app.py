import os
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from inference import segment, predict
from utils import load_YOLO, load_CNN, read_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend-ui:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load models
MODEL_DIR = os.getenv('MODEL_DIR', '/model')
# MODEL_DIR = '../model'
yolo_model = load_YOLO('yolo_seg.pt', MODEL_DIR)
cnn_model = load_CNN('cnn.keras', MODEL_DIR)

@app.get('/')
def read_root():
    return {'message': 'status: healthy'}

@app.post('/inference')
async def inference(image: UploadFile = File(...)):
    logger.info('inference requested')

    try:
        # read image
        img_bytes = await image.read()
        image = read_image(img_bytes)

        # crop the ID/Passport out
        cropped_image = segment(yolo_model, image)

        # predict the country
        pred = predict(cnn_model, cropped_image)

        return JSONResponse(content={"prediction": pred})
    
    except Exception as e:
        logger.error(f'Error during inference: {str(e)}')
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)