from flask import Flask, request, jsonify, render_template
import random
import os
from imageprocessing import PreProcessImage, ModelApply

app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Define the upload folder
UPLOAD_FOLDER = './static/upload'
DETECTED_FOLDER = './static/images/detected'
PROCESSED_FOLDER = './static/images/processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECTED_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

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
    model.resize_with_aspect_ratio(width=500)
    org_file_path, processed_file_path = model.CannyProcess()

    model2 = ModelApply(org_file_path, processed_file_path)
    detected_file_path, kuji_result = model2.NumberDetect()

    return render_template("result.html", name=detected_file_path, number = kuji_result)

@app.route('/manage_uploads')
def manage_uploads():
    upload_folder = os.path.join(app.root_path, 'static', 'upload')
    images = os.listdir(upload_folder)
    return render_template('manage_uploads.html', images=images)

@app.route('/delete_image', methods=['POST'])
def delete_image():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({"error": "Filename not provided"}), 400

    try:
        # Delete file from upload folder
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(upload_path):
            os.remove(upload_path)

        # Delete file from detected folder
        detected_path = os.path.join(DETECTED_FOLDER, filename)
        if os.path.exists(detected_path):
            os.remove(detected_path)

        # Delete file from processed folder
        processed_path = os.path.join(PROCESSED_FOLDER, filename)
        if os.path.exists(processed_path):
            os.remove(processed_path)

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)