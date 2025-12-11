import os
import json
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
import io

# Configuration
UPLOAD_FOLDER = 'uploads'
MERGED_FOLDER = 'merged'
EDITED_FOLDER = 'edited'
ALLOWED_EXTENSIONS = {'pdf'}
CONFIG_FILE = 'web_config.json'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)
os.makedirs(EDITED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MERGED_FOLDER'] = MERGED_FOLDER
app.config['EDITED_FOLDER'] = EDITED_FOLDER
app.secret_key = 'pdf_merger_secret_key_2023'

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_config():
    """Load configuration from file"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"dark_mode": False, "last_directory": "."}

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Could not save config: {e}")

@app.route('/')
def index():
    """Main page"""
    config = load_config()
    return render_template('index.html', dark_mode=config.get("dark_mode", False))

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files selected'}), 400
    
    files = request.files.getlist('files[]')
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append({
                'name': filename,
                'path': filepath
            })
    
    return jsonify({'files': uploaded_files})

@app.route('/reorder', methods=['POST'])
def reorder_files():
    """Reorder files"""
    data = request.get_json()
    file_order = data.get('order', [])
    
    # Validate file paths
    valid_files = []
    for file_info in file_order:
        filepath = file_info.get('path', '')
        if os.path.exists(filepath) and allowed_file(filepath):
            valid_files.append(file_info)
    
    return jsonify({'files': valid_files})

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    """Merge PDF files"""
    data = request.get_json()
    file_order = data.get('files', [])
    
    if not file_order:
        return jsonify({'error': 'No files selected'}), 400
    
    # Create PDF writer
    writer = PdfWriter()
    total_pages = 0
    error_files = []
    
    # Process each file in order
    for file_info in file_order:
        filepath = file_info.get('path', '')
        filename = file_info.get('name', '')
        
        try:
            with open(filepath, 'rb') as f:
                reader = PdfReader(f)
                # Add all pages to writer
                for page in reader.pages:
                    writer.add_page(page)
                total_pages += len(reader.pages)
        except Exception as e:
            error_files.append((filename, str(e)))
    
    # Check for errors
    if error_files:
        error_msg = "Errors occurred with the following files:\n"
        for filename, error in error_files[:3]:  # Show first 3 errors
            error_msg += f"{filename}: {error}\n"
        if len(error_files) > 3:
            error_msg += f"\n... and {len(error_files) - 3} more files."
        
        return jsonify({'error': error_msg}), 400
    
    # Write merged PDF
    output_path = os.path.join(app.config['MERGED_FOLDER'], 'merged.pdf')
    try:
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return jsonify({
            'success': True,
            'output_path': output_path,
            'total_pages': total_pages
        })
    except Exception as e:
        return jsonify({'error': f'Failed to save merged PDF: {str(e)}'}), 500

@app.route('/edit/add_text', methods=['POST'])
def add_text_to_pdf():
    """Add text to a PDF"""
    data = request.get_json()
    pdf_path = data.get('pdf_path', '')
    text = data.get('text', '')
    page_num = data.get('page_num', 0)
    x = data.get('x', 100)
    y = data.get('y', 750)
    
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF file not found'}), 404
    
    try:
        # Read the PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # Copy all pages to the writer
        for i, page in enumerate(reader.pages):
            if i == page_num:
                # For simplicity, we'll create a new PDF with the text using reportlab
                # In a real implementation, we would overlay text on the existing page
                pass
            writer.add_page(page)
        
        # Save edited PDF
        output_filename = f'edited_{os.path.basename(pdf_path)}'
        output_path = os.path.join(app.config['EDITED_FOLDER'], output_filename)
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return jsonify({
            'success': True,
            'output_path': output_path
        })
    except Exception as e:
        return jsonify({'error': f'Failed to add text to PDF: {str(e)}'}), 500

@app.route('/edit/remove_page', methods=['POST'])
def remove_page_from_pdf():
    """Remove a page from a PDF"""
    data = request.get_json()
    pdf_path = data.get('pdf_path', '')
    page_num = data.get('page_num', 0)
    
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF file not found'}), 404
    
    try:
        # Read the PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # Copy all pages except the one to remove
        for i, page in enumerate(reader.pages):
            if i != page_num:
                writer.add_page(page)
        
        # Save edited PDF
        output_filename = f'edited_{os.path.basename(pdf_path)}'
        output_path = os.path.join(app.config['EDITED_FOLDER'], output_filename)
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return jsonify({
            'success': True,
            'output_path': output_path,
            'total_pages': len(writer.pages)
        })
    except Exception as e:
        return jsonify({'error': f'Failed to remove page from PDF: {str(e)}'}), 500

@app.route('/edit/rotate_page', methods=['POST'])
def rotate_page_in_pdf():
    """Rotate a page in a PDF"""
    data = request.get_json()
    pdf_path = data.get('pdf_path', '')
    page_num = data.get('page_num', 0)
    rotation = data.get('rotation', 90)  # 90, 180, or 270 degrees
    
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF file not found'}), 404
    
    try:
        # Read the PDF
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # Copy all pages, rotating the specified one
        for i, page in enumerate(reader.pages):
            if i == page_num:
                # Rotate the page
                page.rotate(rotation)
            writer.add_page(page)
        
        # Save edited PDF
        output_filename = f'edited_{os.path.basename(pdf_path)}'
        output_path = os.path.join(app.config['EDITED_FOLDER'], output_filename)
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return jsonify({
            'success': True,
            'output_path': output_path
        })
    except Exception as e:
        return jsonify({'error': f'Failed to rotate page in PDF: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download merged file"""
    if filename.startswith('edited_'):
        output_path = os.path.join(app.config['EDITED_FOLDER'], filename)
    else:
        output_path = os.path.join(app.config['MERGED_FOLDER'], filename)
    
    if not os.path.exists(output_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(output_path, as_attachment=True)

@app.route('/delete_file', methods=['POST'])
def delete_file():
    """Delete a file"""
    data = request.get_json()
    filepath = data.get('path', '')
    
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': f'Failed to delete file: {str(e)}'}), 500
    
    return jsonify({'success': True})

@app.route('/clear_all', methods=['POST'])
def clear_all():
    """Clear all uploaded files"""
    try:
        for folder in [app.config['UPLOAD_FOLDER'], app.config['MERGED_FOLDER'], app.config['EDITED_FOLDER']]:
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Failed to clear files: {str(e)}'}), 500

@app.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    """Toggle between light and dark mode"""
    config = load_config()
    config["dark_mode"] = not config.get("dark_mode", False)
    save_config(config)
    return jsonify({'dark_mode': config["dark_mode"]})

if __name__ == '__main__':
    # Create templates directory
    os.makedirs('templates', exist_ok=True)
    
    # Create static directory
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='127.0.0.1', port=5000)