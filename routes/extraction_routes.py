from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

from config import Config
from utils.pdf_processor import extract_text_from_pdf
from services.llm_service import extract_sites_with_llm
from utils.coordinate_parser import parse_coordinate_string

extraction_bp = Blueprint('extraction', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def post_process_coordinates(extracted_data):
    """Post-process extracted data to ensure coordinates are in decimal format"""
    sites = extracted_data.get('sites', [])
    
    for site in sites:
        coords = site.get('coordinates', {})
        raw_text = coords.get('raw_text')
        
        if raw_text:
            lat, lon = parse_coordinate_string(raw_text)
            
            if lat is not None and lon is not None:
                coords['latitude'] = lat
                coords['longitude'] = lon
                coords['has_explicit_coordinates'] = True
            else:
                print(f"WARNING: Could not parse coordinates: '{raw_text}'")
    
    return extracted_data

@extraction_bp.route('/extract', methods=['POST'])
def extract():
    """Handle PDF upload and extraction"""
    
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        temp_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        paper_text = extract_text_from_pdf(temp_path)
        
        extracted_data = extract_sites_with_llm(paper_text)
        
        extracted_data = post_process_coordinates(extracted_data)
        
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'data': extracted_data
        })
        
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify({
            'error': f'Processing error: {str(e)}'
        }), 500