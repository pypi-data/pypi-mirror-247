from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os
import cv2
import pkg_resources

def get_model_path():
  """Returns the absolute path to the model.h5 file using pkg_resources"""
  return pkg_resources.resource_filename(__name__, "model.h5")

model = load_model(get_model_path())



img_size = (145, 145)

def preprocess_image(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img_array = img_array / 255
    resized_array = cv2.resize(img_array, (145, 145))
    return resized_array.reshape(-1, 145, 145, 3)

def Face_Mash(img_path):
     img_array = preprocess_image(img_path)
     predictions = model.predict(img_array)
     prediction_class = np.argmax(predictions, axis=1)
     class_labels = ["yawn", "no_yawn", "Closed", "Open"]
     predicted_class_label = class_labels[prediction_class[0]]
     return predicted_class_label

