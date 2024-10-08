# model/Dockerfile

FROM busybox

# create directory to store the models
RUN mkdir /model

# copy model files to container
COPY cnn.keras /model/cnn.keras
COPY yolo_seg.pt /model/yolo_seg.pt

CMD [ "true" ]