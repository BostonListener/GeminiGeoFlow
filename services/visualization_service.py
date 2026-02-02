import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tempfile
import zipfile
import os
import json

def create_overview_visualization(channels, site_name, output_path):
    """Create 2x3 grid visualization of all channels"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f'Site: {site_name}', fontsize=16)
    
    r = channels['B4']
    g = channels['B3']
    b = channels['B2']
    rgb = np.stack([r, g, b], axis=-1)
    
    p2, p98 = np.percentile(rgb, [2, 98])
    rgb_norm = np.clip((rgb - p2) / (p98 - p2), 0, 1)
    
    axes[0, 0].imshow(rgb_norm)
    axes[0, 0].set_title('RGB Composite (B4-B3-B2)')
    axes[0, 0].axis('off')
    
    ndvi = channels['NDVI']
    im1 = axes[0, 1].imshow(ndvi, cmap='RdYlGn', vmin=-0.5, vmax=0.8)
    axes[0, 1].set_title('NDVI')
    axes[0, 1].axis('off')
    plt.colorbar(im1, ax=axes[0, 1], fraction=0.046)
    
    ndwi = channels['NDWI']
    im2 = axes[0, 2].imshow(ndwi, cmap='Blues', vmin=-0.5, vmax=0.5)
    axes[0, 2].set_title('NDWI')
    axes[0, 2].axis('off')
    plt.colorbar(im2, ax=axes[0, 2], fraction=0.046)
    
    bsi = channels['BSI']
    im3 = axes[1, 0].imshow(bsi, cmap='YlOrBr', vmin=-0.5, vmax=0.5)
    axes[1, 0].set_title('BSI')
    axes[1, 0].axis('off')
    plt.colorbar(im3, ax=axes[1, 0], fraction=0.046)
    
    dem = channels['DEM']
    im4 = axes[1, 1].imshow(dem, cmap='terrain')
    axes[1, 1].set_title('DEM (Elevation)')
    axes[1, 1].axis('off')
    plt.colorbar(im4, ax=axes[1, 1], fraction=0.046)
    
    slope = channels['Slope']
    im5 = axes[1, 2].imshow(slope, cmap='plasma')
    axes[1, 2].set_title('Slope')
    axes[1, 2].axis('off')
    plt.colorbar(im5, ax=axes[1, 2], fraction=0.046)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def package_data_as_zip(data, site_name, output_path):
    """Package extracted data as a ZIP file"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for channel_name, array in data['channels'].items():
            temp_npy = tempfile.NamedTemporaryFile(delete=False, suffix='.npy')
            np.save(temp_npy.name, array)
            temp_npy.close()
            
            zipf.write(temp_npy.name, 
                      f"{site_name}/channels/{channel_name}.npy")
            
            os.unlink(temp_npy.name)
        
        temp_png = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_png.close()
        
        try:
            create_overview_visualization(
                data['channels'], 
                site_name, 
                temp_png.name
            )
            
            zipf.write(temp_png.name, 
                      f"{site_name}/visualizations/overview.png")
            
            os.unlink(temp_png.name)
        except Exception as e:
            print(f"ERROR: Failed to create visualization - {str(e)}")
            try:
                os.unlink(temp_png.name)
            except:
                pass
        
        metadata_str = json.dumps(data['metadata'], indent=2)
        zipf.writestr(f"{site_name}/metadata.json", metadata_str)