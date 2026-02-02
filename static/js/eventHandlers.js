function attachButtonListeners() {
    const aiAnalysisButtons = document.querySelectorAll('.ai-analysis-btn');
    aiAnalysisButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const siteIndex = parseInt(this.getAttribute('data-site-index'));
            const siteName = this.getAttribute('data-site-name');
            const coordinatesRaw = this.getAttribute('data-coordinates');
            const lat = parseFloat(this.getAttribute('data-lat')) || null;
            const lon = parseFloat(this.getAttribute('data-lon')) || null;
            
            await handleAIAnalysis(siteIndex, siteName, coordinatesRaw, lat, lon, this);
        });
    });
    
    const previewButtons = document.querySelectorAll('.preview-btn');
    previewButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const siteName = this.getAttribute('data-site-name');
            const coordinatesRaw = this.getAttribute('data-coordinates');
            const index = this.getAttribute('data-index');
            const lat = parseFloat(this.getAttribute('data-lat')) || null;
            const lon = parseFloat(this.getAttribute('data-lon')) || null;
            
            await handlePreview(siteName, coordinatesRaw, index, lat, lon, this);
        });
    });

    const mapsButtons = document.querySelectorAll('.maps-btn');
    mapsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const siteName = this.getAttribute('data-site-name');
            const coordinatesRaw = this.getAttribute('data-coordinates');
            const lat = parseFloat(this.getAttribute('data-lat'));
            const lon = parseFloat(this.getAttribute('data-lon'));
            
            openGoogleMaps(siteName, coordinatesRaw, lat, lon, this);
        });
    });

    const downloadButtons = document.querySelectorAll('.gee-download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const siteName = this.getAttribute('data-site-name');
            const coordinatesRaw = this.getAttribute('data-coordinates');
            const lat = parseFloat(this.getAttribute('data-lat')) || null;
            const lon = parseFloat(this.getAttribute('data-lon')) || null;
            
            await handleDownload(siteName, coordinatesRaw, lat, lon, this);
        });
    });
}

async function handleAIAnalysis(siteIndex, siteName, coordinatesRaw, lat, lon, buttonElement) {
    const analysisSection = document.getElementById(`ai-analysis-${siteIndex}`);
    const analysisContent = document.getElementById(`ai-analysis-content-${siteIndex}`);
    
    if (analysisSection.classList.contains('visible')) {
        analysisSection.classList.remove('visible');
        return;
    }
    
    analysisSection.classList.add('visible');
    analysisContent.innerHTML = '<div class="ai-loading">⏳ Running AI analysis (satellite imagery + web research)... This may take 30-60 seconds...</div>';
    
    const originalText = buttonElement.textContent;
    buttonElement.disabled = true;
    buttonElement.textContent = '⏳ Analyzing...';
    
    try {
        const result = await performAIAnalysis(siteIndex, siteName, coordinatesRaw, lat, lon);

        displayAIAnalysis(result.data, analysisContent);

        buttonElement.textContent = '✅ Analysis Complete!';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 2000);

    } catch (error) {
        console.error('AI analysis error:', error);
        analysisContent.innerHTML = `
            <div class="ai-error">
                <strong>⚠️ Error:</strong> ${error.message}
            </div>
        `;
        
        buttonElement.textContent = '❌ Failed';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 3000);
    }
}

async function handlePreview(siteName, coordinatesRaw, index, lat, lon, buttonElement) {
    const previewSection = document.getElementById(`preview-${index}`);
    const previewContent = document.getElementById(`preview-content-${index}`);
    
    if (previewSection.classList.contains('visible')) {
        previewSection.classList.remove('visible');
        return;
    }
    
    previewSection.classList.add('visible');
    previewContent.innerHTML = '<div class="preview-loading">⏳ Extracting satellite imagery from Google Earth Engine...</div>';
    
    const originalText = buttonElement.textContent;
    buttonElement.disabled = true;
    buttonElement.textContent = '⏳ Loading...';
    
    try {
        const result = await previewGEEData(siteName, coordinatesRaw, lat, lon);

        const metadata = result.metadata || {};
        const imageDate = metadata.acquisition_date ? new Date(metadata.acquisition_date).toLocaleDateString() : 'N/A';
        const cloudCover = metadata.cloud_cover !== null ? metadata.cloud_cover.toFixed(1) + '%' : 'N/A';
        
        previewContent.innerHTML = `
            <img src="data:image/png;base64,${result.image}" alt="Satellite Imagery" class="preview-image">
            <div class="preview-metadata">
                <p><strong>Image Date:</strong> ${imageDate}</p>
                <p><strong>Cloud Cover:</strong> ${cloudCover}</p>
                <p><strong>Coordinates:</strong> ${metadata.latitude?.toFixed(4)}, ${metadata.longitude?.toFixed(4)}</p>
                <p><strong>Grid Size:</strong> ${metadata.cell_size_km} km × ${metadata.cell_size_km} km</p>
            </div>
        `;

        buttonElement.textContent = '✅ Loaded!';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 2000);

    } catch (error) {
        console.error('Preview error:', error);
        previewContent.innerHTML = `
            <div class="preview-error">
                <strong>⚠️ Error:</strong> ${error.message}
            </div>
        `;
        
        buttonElement.textContent = '❌ Failed';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 3000);
    }
}

async function handleDownload(siteName, coordinatesRaw, lat, lon, buttonElement) {
    const originalText = buttonElement.textContent;
    buttonElement.disabled = true;
    buttonElement.textContent = '⏳ Extracting...';
    
    try {
        await downloadGEEData(siteName, coordinatesRaw, lat, lon);

        buttonElement.textContent = '✅ Downloaded!';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 3000);

    } catch (error) {
        console.error('GEE download error:', error);
        alert('Failed to download GEE data: ' + error.message);
        
        buttonElement.textContent = '❌ Failed';
        setTimeout(() => {
            buttonElement.textContent = originalText;
            buttonElement.disabled = false;
        }, 3000);
    }
}