import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import numpy as np
from collections import Counter

app = Flask(__name__)

# Path to save uploaded files
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_top_colors(image_path, top_n=10):
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Convert image to numpy array and reshape it to be a list of pixels
    np_image = np.array(image)
    pixels = np_image.reshape((-1, 3))
    # print(f"pixels length = {len(pixels)}")
    
    # Count the frequency of each unique color
    counter = Counter(map(tuple, pixels))
    total_pixels = np_image.shape[0] * np_image.shape[1]
    # print(f"total_pixels length = {total_pixels}")
    
    # Get the top N colors
    top_colors = counter.most_common(top_n)
    
    # Prepare the color info
    color_info = []
    for color, count in top_colors:
        hex_color = '#%02x%02x%02x' % color
        percentage = (count / total_pixels) * 100
        color_info.append({
            'hex': hex_color,
            'percentage': round(percentage, 2)
        })
    
    return color_info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['imageFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Get top 10 colors
        top_colors = get_top_colors(file_path)

        return jsonify({
            'file_url': f'/{file_path}',
            'colors': top_colors
        })

# @app.route('/<path:filename>')
# def send_uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
