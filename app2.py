from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
import os
from collections import Counter
import math

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

# CAN RESULT IN OVERFLOW:
# def color_distance(c1, c2):
#     """Calculate the Euclidean distance between two colors."""
#     return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

# Explicitly cast the color values to np.int32 before performing 
# the subtraction to avoid overflow issue:
def color_distance(c1, c2):
    """Calculate the Euclidean distance between two colors, avoiding overflow."""
    # Convert color values to int32 to avoid overflow issues
    return math.sqrt(sum((int(a) - int(b)) ** 2 for a, b in zip(c1, c2)))

# ALTERNATE IMPLEMENTATION - color_distance:
# Avoid the overflow issue by ensuring we are always dealing with positive 
# differences (which avoids the overflow from negative squared values): 
# def color_distance(c1, c2):
#     """Calculate the Euclidean distance between two colors with absolute differences."""
#     return math.sqrt(sum((abs(a - b)) ** 2 for a, b in zip(c1, c2)))

def group_similar_colors(pixel_counts, delta):
    """Group similar colors based on a delta threshold."""
    grouped_colors = []
    for color, count in pixel_counts.items():
        found_group = False
        for group in grouped_colors:
            # Compare this color to the group's representative color
            if color_distance(group['color'], color) < delta:
                group['count'] += count
                found_group = True
                break
        if not found_group:
            # Add a new group with this color as the representative
            grouped_colors.append({'color': color, 'count': count})
    return grouped_colors

def process_image(image_path, delta, top_n_colors):
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

    # Group similar colors
    grouped_colors = group_similar_colors(pixel_counts, delta)

    # Sort by pixel count and get the top N colors
    grouped_colors.sort(key=lambda x: x['count'], reverse=True)
    top_colors = grouped_colors[:top_n_colors]

    # Prepare color information
    color_info = []
    for group in top_colors:
        color = group['color']
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        percentage = (group['count'] / total_pixels) * 100
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

            # Get custom color count and delta from the form
            top_n_colors = int(request.form.get('color_count', 10))
            delta = int(request.form.get('delta', 30))  # Default delta of 30

            # Process the image
            color_info = process_image(filepath, delta, top_n_colors)

            # Render the result template
            return render_template('result2.html', image_url=filepath, colors=color_info)
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)

