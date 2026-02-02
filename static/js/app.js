let extractedData = null;

// ==================== PDF FILE INPUT ====================
document.getElementById('pdfFile').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name || 'Choose PDF file...';
    document.getElementById('fileLabel').textContent = fileName;
});

// ==================== PDF FORM SUBMISSION ====================
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('pdfFile');
    if (!fileInput.files[0]) {
        alert('Please select a PDF file');
        return;
    }

    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('statusSection').style.display = 'block';
    document.getElementById('submitBtn').disabled = true;

    const formData = new FormData();
    formData.append('pdf_file', fileInput.files[0]);

    try {
        const result = await extractSites(formData);

        document.getElementById('statusSection').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;

        if (result.error) {
            showError(result.error);
        } else {
            extractedData = result.data;
            displayResults(result.data);
        }

    } catch (error) {
        document.getElementById('statusSection').style.display = 'none';
        document.getElementById('submitBtn').disabled = false;
        showError('Network error: ' + error.message);
    }
});

// ==================== INPUT MODE SWITCHING ====================
document.querySelectorAll('input[name="inputMode"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const uploadSection = document.getElementById('uploadSection');
        const manualSection = document.getElementById('manualSection');
        
        // Clear any previous errors/results when switching modes
        document.getElementById('errorSection').style.display = 'none';
        document.getElementById('resultsSection').style.display = 'none';
        
        if (e.target.value === 'pdf') {
            uploadSection.style.display = 'block';
            manualSection.style.display = 'none';
        } else {
            uploadSection.style.display = 'none';
            manualSection.style.display = 'block';
        }
    });
});

// ==================== COORDINATE FORMAT SWITCHING ====================
document.querySelectorAll('input[name="coordFormat"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
        const decimalInputs = document.getElementById('decimalInputs');
        const dmsInputs = document.getElementById('dmsInputs');
        
        if (e.target.value === 'decimal') {
            decimalInputs.style.display = 'block';
            dmsInputs.style.display = 'none';
        } else {
            decimalInputs.style.display = 'none';
            dmsInputs.style.display = 'block';
        }
    });
});

// ==================== VALIDATION FUNCTIONS ====================
function validateDecimalCoordinates(lat, lon) {
    if (isNaN(lat) || isNaN(lon)) {
        return { valid: false, message: 'Please enter valid numeric coordinates' };
    }
    
    if (lat < -90 || lat > 90) {
        return { valid: false, message: 'Latitude must be between -90 and 90' };
    }
    
    if (lon < -180 || lon > 180) {
        return { valid: false, message: 'Longitude must be between -180 and 180' };
    }
    
    return { valid: true };
}

function validateDMSCoordinates(latDeg, latMin, latSec, lonDeg, lonMin, lonSec) {
    // Check if all values are numbers
    if (isNaN(latDeg) || isNaN(latMin) || isNaN(latSec) ||
        isNaN(lonDeg) || isNaN(lonMin) || isNaN(lonSec)) {
        return { valid: false, message: 'Please fill all DMS fields with valid numbers' };
    }
    
    // Validate degrees
    if (latDeg < 0 || latDeg > 90) {
        return { valid: false, message: 'Latitude degrees must be between 0 and 90' };
    }
    
    if (lonDeg < 0 || lonDeg > 180) {
        return { valid: false, message: 'Longitude degrees must be between 0 and 180' };
    }
    
    // Validate minutes
    if (latMin < 0 || latMin >= 60) {
        return { valid: false, message: 'Minutes must be between 0 and 59' };
    }
    
    if (lonMin < 0 || lonMin >= 60) {
        return { valid: false, message: 'Minutes must be between 0 and 59' };
    }
    
    // Validate seconds
    if (latSec < 0 || latSec >= 60) {
        return { valid: false, message: 'Seconds must be between 0 and 59.999' };
    }
    
    if (lonSec < 0 || lonSec >= 60) {
        return { valid: false, message: 'Seconds must be between 0 and 59.999' };
    }
    
    return { valid: true };
}

function dmsToDecimal(degrees, minutes, seconds, direction) {
    let decimal = Math.abs(degrees) + minutes / 60 + seconds / 3600;
    
    // Apply direction
    if (direction === 'S' || direction === 'W') {
        decimal = -decimal;
    }
    
    return decimal;
}

function formatDMSString(degrees, minutes, seconds, direction) {
    return `${degrees}° ${minutes}' ${seconds.toFixed(3)}" ${direction}`;
}

// ==================== MANUAL COORDINATE SUBMISSION ====================
document.getElementById('manualSubmitBtn').addEventListener('click', async function() {
    // Clear previous errors
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    
    // Get site name
    const siteName = document.getElementById('siteName').value.trim();
    
    if (!siteName) {
        alert('Please enter a site name');
        document.getElementById('siteName').focus();
        return;
    }
    
    // Get coordinate format
    const coordFormat = document.querySelector('input[name="coordFormat"]:checked').value;
    
    let lat, lon, rawText;
    
    if (coordFormat === 'decimal') {
        // ===== DECIMAL FORMAT =====
        const latInput = document.getElementById('latDecimal').value.trim();
        const lonInput = document.getElementById('lonDecimal').value.trim();
        
        if (!latInput || !lonInput) {
            alert('Please enter both latitude and longitude');
            return;
        }
        
        lat = parseFloat(latInput);
        lon = parseFloat(lonInput);
        
        // Validate
        const validation = validateDecimalCoordinates(lat, lon);
        if (!validation.valid) {
            alert(validation.message);
            return;
        }
        
        rawText = `${lat}, ${lon}`;
        
    } else {
        // ===== DMS FORMAT =====
        const latDegInput = document.getElementById('latDeg').value.trim();
        const latMinInput = document.getElementById('latMin').value.trim();
        const latSecInput = document.getElementById('latSec').value.trim();
        const latDir = document.getElementById('latDir').value;
        
        const lonDegInput = document.getElementById('lonDeg').value.trim();
        const lonMinInput = document.getElementById('lonMin').value.trim();
        const lonSecInput = document.getElementById('lonSec').value.trim();
        const lonDir = document.getElementById('lonDir').value;
        
        // Check if any field is empty
        if (!latDegInput || !latMinInput || !latSecInput ||
            !lonDegInput || !lonMinInput || !lonSecInput) {
            alert('Please fill all DMS fields (degrees, minutes, seconds)');
            return;
        }
        
        const latDeg = parseInt(latDegInput);
        const latMin = parseInt(latMinInput);
        const latSec = parseFloat(latSecInput);
        
        const lonDeg = parseInt(lonDegInput);
        const lonMin = parseInt(lonMinInput);
        const lonSec = parseFloat(lonSecInput);
        
        // Validate
        const validation = validateDMSCoordinates(latDeg, latMin, latSec, lonDeg, lonMin, lonSec);
        if (!validation.valid) {
            alert(validation.message);
            return;
        }
        
        // Convert to decimal
        lat = dmsToDecimal(latDeg, latMin, latSec, latDir);
        lon = dmsToDecimal(lonDeg, lonMin, lonSec, lonDir);
        
        // Create raw text in DMS format
        const latDMS = formatDMSString(latDeg, latMin, latSec, latDir);
        const lonDMS = formatDMSString(lonDeg, lonMin, lonSec, lonDir);
        rawText = `${latDMS}, ${lonDMS}`;
    }
    
    // Construct data structure matching PDF extraction format
    extractedData = {
        sites: [{
            site_name: siteName,
            coordinates: {
                raw_text: rawText,
                latitude: lat,
                longitude: lon,
                has_explicit_coordinates: true
            },
            temporal: {
                dating: null,
                cultural_period: null
            },
            characteristics: {
                site_type: null,
                features: [],
                size: null
            },
            metadata: {
                source: "Manual Input",
                input_format: coordFormat,
                confidence: "high"
            }
        }],
        metadata: {
            source_type: "manual_input",
            extraction_method: coordFormat,
            sites_found: 1,
            timestamp: new Date().toISOString()
        }
    };
    
    // Display results using existing function
    displayResults(extractedData);
});

// ==================== DOWNLOAD JSON BUTTON ====================
document.getElementById('downloadBtn').addEventListener('click', function() {
    if (!extractedData) return;

    const dataStr = JSON.stringify(extractedData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    
    // Use site name in filename if available
    const siteName = extractedData.sites?.[0]?.site_name || 'sites';
    const safeFileName = siteName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    link.download = `${safeFileName}_extracted.json`;
    
    link.click();
    URL.revokeObjectURL(url);
});