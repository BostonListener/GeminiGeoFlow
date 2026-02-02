async function extractSites(formData) {
    const response = await fetch('/extract', {
        method: 'POST',
        body: formData
    });
    return await response.json();
}

async function previewGEEData(siteName, coordinatesRaw, lat, lon) {
    const response = await fetch('/preview_gee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            site_name: siteName,
            coordinates_raw: coordinatesRaw,
            latitude: lat,
            longitude: lon
        })
    });

    const result = await response.json();

    if (!response.ok || result.error) {
        throw new Error(result.error || 'Preview generation failed');
    }

    return result;
}

async function downloadGEEData(siteName, coordinatesRaw, lat, lon) {
    const response = await fetch('/download_gee', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            site_name: siteName,
            coordinates_raw: coordinatesRaw,
            latitude: lat,
            longitude: lon
        })
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Download failed');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    const contentDisposition = response.headers.get('Content-Disposition');
    let filename = `${siteName.replace(/[^a-z0-9]/gi, '_')}_gee_data.zip`;
    
    if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
        if (filenameMatch) {
            filename = filenameMatch[1];
        }
    }
    
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

async function performAIAnalysis(siteIndex, siteName, coordinatesRaw, lat, lon) {
    const siteData = extractedData.sites[siteIndex];
    
    const response = await fetch('/ai_analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            site_data: siteData,
            coordinates_raw: coordinatesRaw,
            latitude: lat,
            longitude: lon
        })
    });

    const result = await response.json();

    if (!response.ok || result.error) {
        throw new Error(result.error || 'AI analysis failed');
    }

    return result;
}