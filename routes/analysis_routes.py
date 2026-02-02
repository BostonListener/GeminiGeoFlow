from flask import Blueprint, request, jsonify
import tempfile
import os
import base64

from services.gee_service import extract_gee_data, initialize_gee
from services.visualization_service import create_overview_visualization
from services.llm_service import analyze_satellite_imagery, enrich_site_context
from utils.coordinate_parser import parse_coordinate_string

analysis_bp = Blueprint('analysis', __name__)

GEE_INITIALIZED = initialize_gee()

@analysis_bp.route('/ai_analysis', methods=['POST'])
def ai_analysis():
    """Perform AI analysis: satellite imagery analysis + contextual enrichment"""
    
    try:
        data = request.get_json()
        site_data = data.get('site_data', {})
        site_name = site_data.get('site_name', 'Unknown Site')
        
        lat = data.get('latitude')
        lon = data.get('longitude')
        coordinates_raw = data.get('coordinates_raw', '')
        
        has_coordinates = lat is not None and lon is not None
        
        result = {
            'site_name': site_name,
            'has_coordinates': has_coordinates,
            'visual_analysis': None,
            'contextual_enrichment': None,
            'errors': []
        }
        
        if has_coordinates and GEE_INITIALIZED:
            try:
                if lat is None or lon is None:
                    lat, lon = parse_coordinate_string(coordinates_raw)
                
                if lat is None or lon is None:
                    result['errors'].append('Could not parse coordinates')
                elif not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    result['errors'].append(f'Invalid coordinates: lat={lat}, lon={lon}')
                else:
                    gee_data = extract_gee_data(lat, lon, site_name)
                    
                    temp_png = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                    temp_png.close()
                    
                    create_overview_visualization(
                        gee_data['channels'],
                        site_name,
                        temp_png.name
                    )
                    
                    with open(temp_png.name, 'rb') as f:
                        image_bytes = f.read()
                        image_data = base64.b64encode(image_bytes).decode('utf-8')
                    
                    os.unlink(temp_png.name)
                    
                    visual_analysis = analyze_satellite_imagery(
                        site_name, 
                        gee_data['metadata'],
                        image_data
                    )
                    
                    visual_analysis['satellite_metadata'] = gee_data['metadata']
                    visual_analysis['preview_image'] = image_data
                    
                    result['visual_analysis'] = visual_analysis
                    
            except Exception as e:
                error_msg = f"Satellite analysis error: {str(e)}"
                print(f"ERROR: {error_msg}")
                import traceback
                traceback.print_exc()
                result['errors'].append(error_msg)
        
        try:
            contextual_enrichment = enrich_site_context(site_data)
            
            result['contextual_enrichment'] = contextual_enrichment
            
        except Exception as e:
            error_msg = f"Contextual enrichment error: {str(e)}"
            print(f"ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            result['errors'].append(error_msg)
        
        if result['visual_analysis'] or result['contextual_enrichment']:
            return jsonify({
                'success': True,
                'data': result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Analysis failed: ' + '; '.join(result['errors'])
            }), 500
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'AI analysis error: {str(e)}'
        }), 500