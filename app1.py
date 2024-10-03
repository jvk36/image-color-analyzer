from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import os
from collections import Counter

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    # Open the image and convert to RGB
    image = Image.open(image_path).convert('RGB')
    # Convert image to numpy array
    np_image = np.array(image)
    # Reshape the array to a list of RGB pixels
    pixels = np_image.reshape(-1, 3)
    # Convert pixels to tuples so they can be counted
    pixels = [tuple(pixel) for pixel in pixels]

    # Count the pixels
    pixel_counts = Counter(pixels)
    total_pixels = sum(pixel_counts.values())

    # Get the top 10 colors
    top_colors = pixel_counts.most_common(10)

    # Prepare color information
    color_info = []
    for color, count in top_colors:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        percentage = (count / total_pixels) * 100
        color_info.append({
            'color': hex_color,
            'percentage': round(percentage, 2)
        })

    return color_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an image was uploaded
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Save the image
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the image
            color_info = process_image(filepath)

            # Render the result template
            return render_template('result1.html', image_url=filepath, colors=color_info)
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
