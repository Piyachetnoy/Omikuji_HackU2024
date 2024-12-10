from flask import Flask, request, jsonify,render_template
import random
import os
from imageprocessing import PreProcessImage, ModelApply

app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Define the upload folder
UPLOAD_FOLDER = './static/upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set the upload folder in the app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_random_image():
    upload_folder = os.path.join(app.root_path, 'static', 'upload') # Get the list of files in the 'upload' folder
    image_files = os.listdir(upload_folder) # Choose a random image from the list
    return random.choice(image_files)

# Set the template of html file (put htmls in templates folder)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showcase')
def showcase():
    random_image = get_random_image()
    return render_template('showcase.html', random_image=random_image) # Return the 'showcase.html' template and pass the random image filename

@app.route('/random_image')
def random_image():
    random_image = get_random_image()
    return jsonify({'random_image': random_image}) # Return the filename of the random image

@app.route('/process-upload', methods=['POST'])
def process_upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # Retrieve the uploaded file
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the /upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Instantiate ModelApply and process the image
    model = PreProcessImage(file_path)
    org_file_path, processed_file_path = model.CannyProcess()

    model2 = ModelApply(org_file_path, processed_file_path)
    detected_file_path, kuji_result = model2.NumberDetect()

    return render_template("result.html", name=detected_file_path, number = kuji_result)


if __name__ == '__main__':
    app.run(debug=True)