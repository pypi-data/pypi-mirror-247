from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import cv2
import pkg_resources

def get_model_path():
  return pkg_resources.resource_filename(__name__, "model.h5")


import gdown
file_id = '12MeKZg6KY_aQH2Dd4c25y2HpiEQqJTiY'
output_file = 'model.h5'
url = f'https://drive.google.com/uc?id={file_id}'
gdown.download(url, output_file, quiet=False)





img_size = (145, 145)

def preprocess_image(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img_array = img_array / 255
    resized_array = cv2.resize(img_array, (145, 145))
    return resized_array.reshape(-1, 145, 145, 3)

def Face_Mash(img_path,model_path):
     model = load_model(model_path)
     img_array = preprocess_image(img_path)
     predictions = model.predict(img_array)
     prediction_class = np.argmax(predictions, axis=1)
     class_labels = ["yawn", "no_yawn", "Closed", "Open"]
     predicted_class_label = class_labels[prediction_class[0]]
     return predicted_class_label

