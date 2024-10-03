# BEFORE RUNNING THE FILES EXECUTE THE FOLLOWING IN THE TERMINAL FROM THE WORKING FOLDER:
pip install -r requirements.txt

## BASIC IMPLEMENTATION - app.py, templates/index.html

The application allows the user to upload an image, calculate the top 10 colors using Flask and NumPy,
and returns it as a JSON.

### KEY COMPONENTS:

Frontend (HTML/Bootstrap): The user can upload an image using a form. Upon submission, the image file is sent to the Flask backend for processing.

Backend (Flask): The image is processed using Pillow to extract pixel data and NumPy to manipulate it. The top 10 most common colors are calculated, converted to hexadecimal format, and the percentage of pixels with that color is calculated.

Top Colors Calculation: We use collections.Counter to count the frequency of each unique RGB color in the image, then convert the most frequent colors to hexadecimal and percentage of total pixels.

### RUNNING THE APP:

Run app.py and access the app at http://127.0.0.1:5000/

## DETAILED IMPLEMENTATION - app1.py, templates/index1.html, result1.html

### KEY COMPONENTS:

The application will:

Allow users to upload an image.
Display the uploaded image.
Show the top 10 colors in the image, their hex codes, and the percentage of pixels for each color.

We'll use:

Front-end: HTML, CSS, Bootstrap
Back-end: Python, Flask, NumPy, Pillow (PIL)

### HOW IT WORKS:

Front-End:

index1.html: A simple page with a file upload form styled using Bootstrap.
result1.html: Displays the uploaded image and a table of the top 10 colors.

Back-End:

File Upload Handling: The index route handles both GET and POST requests. On POST, it processes the uploaded image.
Image Processing:
Pillow (PIL): Opens the image and converts it to RGB format.
NumPy: Converts the image to a NumPy array for efficient processing.
Color Counting: Flattens the array to a list of pixels and counts occurrences of each color.
Color Information: Extracts the top 10 colors, converts them to hex codes, and calculates their percentage of the total pixels.

### TESTING THE APPLICATION:

Upload an Image: On the home page, click "Choose File" and select an image from your local system.
View Results: After submitting, you'll see the uploaded image and a table of the top 10 colors.

### NOTES:

Image Size: Large images may slow down processing. You can resize images before processing if necessary.
Color Similarity: This method counts exact pixel values. Similar colors (e.g., shades of blue) are counted separately. For better grouping, consider using color quantization algorithms like K-Means clustering.
Error Handling: The provided code has basic error handling. For a production app, you should add more robust checks and user feedback.
Security: Always be cautious with file uploads. Validate and sanitize inputs to prevent security vulnerabilities.

## DETAILED IMPLEMENTATION 2 - app2.py, templates/index2.html, result2.html

### ENHANCEMENTS OVERVIEW:

Color Grouping: We introduce a "color similarity delta" which allows grouping similar colors (e.g., shades of blue). The user can specify the delta, which ranges from 1 to 255. Lower values mean stricter color matching, while higher values group similar colors.

Custom Color Count: We allow users to specify how many top colors they want to see (up to a maximum, e.g., 20).

Visualization: We add a simple bar chart to visualize the color distribution using Bootstrap for layout and inline styles.

### app2.py Updates:

Added:

A helper function to calculate color differences.
A delta parameter for grouping similar colors.
A form input for selecting the number of colors to display.

### templates/index2.html Updates:

Added two form inputs:

One to specify the number of colors.
Another for the color similarity delta.

### templates/result2.html Updates:

Added visualization in the form of a bar chart to display the color percentages. 
It is placed below the image and color list.

### HOW IT WORKS:

Color Grouping:

The function group_similar_colors compares each pixel's color to the representative color of existing groups using the Euclidean distance in RGB space.
The user-specified delta controls how strict the grouping is. A lower delta (e.g., 10) means only very similar colors are grouped, while a higher delta (e.g., 100) groups a wider range of similar colors together.

Custom Color Count:

The user can select how many top colors to display (from 1 to 20) via an input form.

Visualization:

The color bar chart displays each color's percentage of the total pixels as a horizontal bar. The width of each bar is proportional to the color’s percentage.

### NOTES:

Color Grouping: The grouping uses RGB space. For better perceptual grouping, you might consider converting to a different color space like LAB or HSV.

Performance: Large images with a high number of unique colors may slow down processing. You can resize the image before analysis for better performance.

Bar Chart Styling: You can further enhance the bar chart by adding labels or custom animations.

