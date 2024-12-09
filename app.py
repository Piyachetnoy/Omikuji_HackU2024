from flask import Flask, request, jsonify,render_template
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = './static/upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set the upload folder in the app configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the template of html file (put htmls in templates folder)
@app.route('/')
def index():
    return render_template('index.html')

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

    # return jsonify({"success": True, "filePath": file_path}), 200
    return render_template("result.html", name = file_path)

if __name__ == '__main__':
    app.run(debug=True)