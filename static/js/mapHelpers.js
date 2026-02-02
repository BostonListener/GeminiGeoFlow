function openGoogleMaps(siteName, coordinatesRaw, lat, lon, buttonElement) {
    const originalText = buttonElement.textContent;
    buttonElement.disabled = true;
    buttonElement.textContent = '🗺️ Opening...';
    
    let mapsUrl;
    
    if (!isNaN(lat) && !isNaN(lon) && lat !== 0 && lon !== 0) {
        const coordString = `${lat},${lon}`;
        mapsUrl = `https://www.google.com/maps/place/${encodeURIComponent(coordString)}/@${coordString},500m`;
    } else if (coordinatesRaw) {
        mapsUrl = `https://www.google.com/maps/place/${encodeURIComponent(coordinatesRaw)}`;
    } else {
        buttonElement.textContent = '❌ No Coordinates';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 2000);
        return;
    }
    
    window.open(mapsUrl, '_blank');
    
    buttonElement.textContent = '✅ Opened!';
    setTimeout(() => {
        buttonElement.textContent = originalText;
        buttonElement.disabled = false;
    }, 2000);
}