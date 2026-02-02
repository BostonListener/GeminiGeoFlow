import os
import tempfile
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Using system environment variables.")

class Config:
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    UPLOAD_FOLDER = tempfile.gettempdir()
    ALLOWED_EXTENSIONS = {'pdf'}
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    GEE_PROJECT_ID = os.getenv('GEE_PROJECT_ID')
    GEE_SERVICE_ACCOUNT_PATH = Path(__file__).parent / 'gee_service_account.json'
    
    GEE_CONFIG = {
        'project': GEE_PROJECT_ID,
        'cell_size_km': 1.0,
        'pixels_per_km': 100,
        'sentinel2': {
            'collection': 'COPERNICUS/S2_SR_HARMONIZED',
            'bands': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12'],
            'date_start': '2020-01-01',
            'date_end': '2024-12-31',
            'cloud_cover_max': 20,
            'scale': 10
        },
        'dem': {
            'collection': 'USGS/SRTMGL1_003'
        }
    }