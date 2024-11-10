from flask import current_app
import os
from PIL import Image, ImageOps
import numpy as np
from keras.models import load_model


def Test(picture):
    np.set_printoptions(suppress=True)

    # Construct paths relative to the Flask app's root
    model_path = os.path.join(current_app.root_path, 'static', 'converted_keras', 'keras_Model.h5')
    labels_path = os.path.join(current_app.root_path, 'static', 'converted_keras', 'labels.txt')

    model = load_model(model_path, compile=False)
    class_names = open(labels_path, "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    size = (224, 224)
    image = Image.fromarray(picture.astype('uint8')).convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    class_name = class_name.strip()

    return class_name[2:]




'''
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

from app.common import shared_variable

def Test(pecture):
    np.set_printoptions(suppress=True)
    model = load_model("../static/converted_keras/keras_Model.h5", compile=False)
    class_names = open("../static/converted_keras/labels.txt", "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(pecture).convert("RGB")
    #image = Image.fromarray(pecture.astype('uint8'), 'RGB')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name[2:]



result = Test(shared_variable)
print(result)
'''