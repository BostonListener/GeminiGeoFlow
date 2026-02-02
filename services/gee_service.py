import ee
import numpy as np
from google.oauth2 import service_account
from scipy.ndimage import zoom
from config import Config

def initialize_gee():
    """Initialize Google Earth Engine with service account"""
    try:
        if not Config.GEE_SERVICE_ACCOUNT_PATH.exists():
            print(f"ERROR: Service account file not found: {Config.GEE_SERVICE_ACCOUNT_PATH}")
            return False
        
        credentials = service_account.Credentials.from_service_account_file(
            str(Config.GEE_SERVICE_ACCOUNT_PATH),
            scopes=['https://www.googleapis.com/auth/earthengine']
        )
        
        ee.Initialize(credentials=credentials, project=Config.GEE_CONFIG['project'])
        return True
        
    except Exception as e:
        print(f"ERROR initializing GEE: {str(e)}")
        return False

def create_grid_bbox(lat, lon, cell_size_km):
    """Create bounding box for extraction"""
    half_size_deg = (cell_size_km / 2) / 111.32
    
    min_lon = lon - half_size_deg
    max_lon = lon + half_size_deg
    min_lat = lat - half_size_deg
    max_lat = lat + half_size_deg
    
    return ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

def get_sentinel2_image(roi):
    """Get least cloudy Sentinel-2 image for region"""
    config = Config.GEE_CONFIG['sentinel2']
    
    collection = (
        ee.ImageCollection(config['collection'])
        .filterBounds(roi)
        .filterDate(config['date_start'], config['date_end'])
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', config['cloud_cover_max']))
        .sort('CLOUDY_PIXEL_PERCENTAGE')
    )
    
    return ee.Image(collection.first())

def get_dem_data(roi):
    """Get SRTM DEM elevation data"""
    dem = ee.Image('USGS/SRTMGL1_003')
    return dem

def calculate_slope(dem_image):
    """Calculate slope from DEM"""
    return ee.Terrain.slope(dem_image)

def extract_band_array(image, band, roi, pixels):
    """Extract a single band as numpy array"""
    band_image = image.select(band)
    
    array = band_image.sampleRectangle(region=roi, defaultValue=0)
    data = array.get(band).getInfo()
    arr = np.array(data, dtype=np.float32)
    
    if np.all(arr == 0):
        print(f"WARNING: Band {band} is all zeros!")
    if np.isnan(arr).any():
        print(f"WARNING: Band {band} contains NaN values!")
    
    if arr.shape != (pixels, pixels):
        zoom_factors = (pixels / arr.shape[0], pixels / arr.shape[1])
        arr = zoom(arr, zoom_factors, order=1)
    
    return arr

def calculate_ndvi(b8, b4):
    """Calculate NDVI"""
    numerator = b8 - b4
    denominator = b8 + b4
    ndvi = np.divide(numerator, denominator, 
                    out=np.zeros_like(numerator), 
                    where=denominator!=0)
    return ndvi.astype(np.float32)

def calculate_ndwi(b3, b8):
    """Calculate NDWI"""
    numerator = b3 - b8
    denominator = b3 + b8
    ndwi = np.divide(numerator, denominator,
                    out=np.zeros_like(numerator),
                    where=denominator!=0)
    return ndwi.astype(np.float32)

def calculate_bsi(b11, b4, b8, b2):
    """Calculate BSI"""
    numerator = (b11 + b4) - (b8 + b2)
    denominator = (b11 + b4) + (b8 + b2)
    bsi = np.divide(numerator, denominator,
                   out=np.zeros_like(numerator),
                   where=denominator!=0)
    return bsi.astype(np.float32)

def extract_gee_data(lat, lon, site_name="site"):
    """Extract all GEE data for a location"""
    cell_size_km = Config.GEE_CONFIG['cell_size_km']
    pixels = Config.GEE_CONFIG['pixels_per_km']
    
    roi = create_grid_bbox(lat, lon, cell_size_km)
    
    s2_image = get_sentinel2_image(roi)
    dem_image = get_dem_data(roi)
    slope_image = calculate_slope(dem_image)
    
    dem_band = 'elevation'
    
    channels = {}
    
    for band in Config.GEE_CONFIG['sentinel2']['bands']:
        channels[band] = extract_band_array(s2_image, band, roi, pixels)
    
    channels['DEM'] = extract_band_array(dem_image, dem_band, roi, pixels)
    channels['Slope'] = extract_band_array(slope_image, 'slope', roi, pixels)
    
    channels['NDVI'] = calculate_ndvi(channels['B8'], channels['B4'])
    channels['NDWI'] = calculate_ndwi(channels['B3'], channels['B8'])
    channels['BSI'] = calculate_bsi(channels['B11'], channels['B4'], 
                                     channels['B8'], channels['B2'])
    
    image_info = s2_image.getInfo()
    metadata = {
        'site_name': site_name,
        'latitude': lat,
        'longitude': lon,
        'cell_size_km': cell_size_km,
        'image_id': image_info['id'] if image_info else None,
        'cloud_cover': image_info['properties'].get('CLOUDY_PIXEL_PERCENTAGE') if image_info else None,
        'acquisition_date': image_info['properties'].get('GENERATION_TIME') if image_info else None
    }
    
    return {'channels': channels, 'metadata': metadata}