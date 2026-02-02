from flask import Blueprint, request, jsonify, send_file
import tempfile
import os
import base64

from services.gee_service import extract_gee_data, initialize_gee
from services.visualization_service import create_overview_visualization, package_data_as_zip
from utils.coordinate_parser import parse_coordinate_string

gee_bp = Blueprint('gee', __name__)

GEE_INITIALIZED = initialize_gee()

@gee_bp.route('/download_gee', methods=['POST'])
def download_gee():
    """Handle GEE data extraction and download"""
    
    if not GEE_INITIALIZED:
        return jsonify({
            'error': 'Google Earth Engine not initialized. Please configure service account.'
        }), 500
    
    try:
        data = request.get_json()
        
        site_name = data.get('site_name', 'unknown_site')
        coordinates_raw = data.get('coordinates_raw', '')
        
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            lat, lon = parse_coordinate_string(coordinates_raw)
        
        if lat is None or lon is None:
            return jsonify({
                'error': f'Could not parse coordinates from: {coordinates_raw}'
            }), 400
        
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return jsonify({
                'error': f'Invalid coordinates: lat={lat}, lon={lon}'
            }), 400
        
        gee_data = extract_gee_data(lat, lon, site_name)
        
        safe_site_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' 
                                for c in site_name)
        zip_filename = f"{safe_site_name}_{lat:.4f}_{lon:.4f}.zip"
        
        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        temp_zip.close()
        
        package_data_as_zip(gee_data, safe_site_name, temp_zip.name)
        
        response = send_file(
            temp_zip.name,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
        @response.call_on_close
        def cleanup():
            try:
                os.unlink(temp_zip.name)
            except:
                pass
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'GEE extraction error: {str(e)}'
        }), 500

@gee_bp.route('/preview_gee', methods=['POST'])
def preview_gee():
    """Handle GEE data extraction and return preview image"""
    
    if not GEE_INITIALIZED:
        return jsonify({
            'error': 'Google Earth Engine not initialized. Please configure service account.'
        }), 500
    
    try:
        data = request.get_json()
        
        site_name = data.get('site_name', 'unknown_site')
        coordinates_raw = data.get('coordinates_raw', '')
        
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            lat, lon = parse_coordinate_string(coordinates_raw)
        
        if lat is None or lon is None:
            return jsonify({
                'error': f'Could not parse coordinates from: {coordinates_raw}'
            }), 400
        
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return jsonify({
                'error': f'Invalid coordinates: lat={lat}, lon={lon}'
            }), 400
        
        gee_data = extract_gee_data(lat, lon, site_name)
        
        temp_png = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_png.close()
        
        create_overview_visualization(
            gee_data['channels'], 
            site_name, 
            temp_png.name
        )
        
        with open(temp_png.name, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        os.unlink(temp_png.name)
        
        return jsonify({
            'success': True,
            'image': image_data,
            'metadata': gee_data['metadata']
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Preview generation error: {str(e)}'
        }), 500