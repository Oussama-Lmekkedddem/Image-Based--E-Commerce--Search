from flask import Blueprint, render_template, url_for, request, jsonify, session, redirect
import os
import random
from PIL import Image
from io import BytesIO
import base64
import numpy as np

from .test import Test
main_bp = Blueprint('main', __name__)


all_folders = ['earphone', 'furniture', 'laptop', 'mouse', 'pants', 'perfume', 'phone', 'sac', 'shirt', 'shoes', 'tv', 'watch']

@main_bp.route('/')
def index():
    max_images_per_folder = 6
    max_total_images = 40
    selected_images = []

    for folder_name in all_folders:
        folder_path = os.path.join('app/static/images', folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            images = [os.path.join(folder_name, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
            images = random.sample(images, min(max_images_per_folder, len(images)))
            selected_images.extend(images)

        if len(selected_images) >= max_total_images:
            break

    random.shuffle(selected_images)

    num_columns = max(1, min(3, len(selected_images)))  # Ensure num_columns is at least 1

    static_folder_path = url_for('static', filename='images/')
    return render_template('index.html', folder_name='Best Product', num_columns=num_columns, images=selected_images, static_folder_path=static_folder_path)

@main_bp.route('/products/<folder_name>')
def fashion_section(folder_name):
    folder_path = os.path.join('app/static/images', folder_name)
    images = []

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    num_columns = max(1, min(3, len(images)))  # Ensure num_columns is at least 1

    static_folder_path = url_for('static', filename=f'images/{folder_name}/')
    return render_template('index.html', folder_name=folder_name, num_columns=num_columns, images=images, static_folder_path=static_folder_path)


@main_bp.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data.get('imageData', '')
    image_data = image_data.split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_matrix = np.array(image)
    result = Test(image_matrix)
    new_url = f'/products/{result}'
    print(f"Redirect URL: {new_url}")

    # Return the redirect URL as part of the JSON response
    return jsonify({'redirect_url': new_url})


'''

@main_bp.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data.get('imageData', '')
    image_data = image_data.split(',')[1]

    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_matrix = np.array(image)

    result_class = Test(image_matrix)
    print(result_class)

    return jsonify(result=result_class)
    
@main_bp.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_data = data.get('imageData', '')
    image_data = image_data.split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image_matrix = np.array(image)
    result = Test(image_matrix)

    return jsonify({'status': 'success'})
'''
