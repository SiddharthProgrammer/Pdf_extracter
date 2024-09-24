from flask import Flask, render_template, request, redirect, url_for, flash
import pdfplumber
import os

app = Flask(__name__)
app.secret_key = "secret_key_for_flashing"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        try:
            with pdfplumber.open(file_path) as pdf:
                extracted_text = ''
                for page in pdf.pages:
                    extracted_text += page.extract_text()
            
            return render_template('index.html', extracted_text=extracted_text)
        except Exception as e:
            flash('Error extracting text from PDF')
            return redirect(url_for('index'))

    flash('Invalid file type. Please upload a PDF file.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
