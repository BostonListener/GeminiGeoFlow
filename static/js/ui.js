function showError(message) {
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorSection').style.display = 'block';
}

function displayResults(data) {
    const summary = data.extraction_summary || {};
    const summaryHTML = `
        <p><strong>Total Sites Found:</strong> ${summary.total_sites_found || 0}</p>
        <p><strong>Sites with Coordinates:</strong> ${summary.sites_with_explicit_coordinates || 0}</p>
        <p><strong>Sites with Descriptions Only:</strong> ${summary.sites_with_descriptions_only || 0}</p>
    `;
    document.getElementById('summaryContent').innerHTML = summaryHTML;

    const sites = data.sites || [];
    let sitesHTML = '';

    if (sites.length === 0) {
        sitesHTML = '<p>No sites found in the document.</p>';
    } else {
        sites.forEach((site, index) => {
            sitesHTML += createSiteCard(site, index);
        });
    }

    document.getElementById('sitesContent').innerHTML = sitesHTML;
    document.getElementById('resultsSection').style.display = 'block';

    attachButtonListeners();
}

function createSiteCard(site, index) {
    const hasCoordinates = site.coordinates?.has_explicit_coordinates || false;
    const coordinatesRaw = site.coordinates?.raw_text || '';
    const siteName = site.site_name || 'Unnamed Site';
    const lat = site.coordinates?.latitude || '';
    const lon = site.coordinates?.longitude || '';
    
    const aiButtonText = hasCoordinates ? '🤖 AI Analysis & Research' : '🔍 AI Research';
    const aiButtonTitle = hasCoordinates 
        ? 'Satellite imagery analysis + contextual web research' 
        : 'Contextual web research and comparative analysis';
    
    let html = `
        <div class="site-card" id="site-${index}">
            <div class="site-header">
                <h4>Site ${index + 1}: ${siteName}</h4>
                <div class="button-group">
                    <button class="ai-analysis-btn" 
                            data-site-index="${index}"
                            data-site-name="${siteName}"
                            data-coordinates="${coordinatesRaw}"
                            data-lat="${lat}"
                            data-lon="${lon}"
                            title="${aiButtonTitle}">
                        ${aiButtonText}
                    </button>
                    
                    ${hasCoordinates ? `
                        <button class="preview-btn" 
                                data-site-name="${siteName}"
                                data-coordinates="${coordinatesRaw}"
                                data-lat="${lat}"
                                data-lon="${lon}"
                                data-index="${index}">
                            🛰️ Preview Imagery
                        </button>
                        <button class="maps-btn" 
                                data-site-name="${siteName}"
                                data-coordinates="${coordinatesRaw}"
                                data-lat="${lat}"
                                data-lon="${lon}"
                                data-index="${index}">
                            🗺️ View on Map
                        </button>
                        <button class="gee-download-btn" 
                                data-site-name="${siteName}"
                                data-coordinates="${coordinatesRaw}"
                                data-lat="${lat}"
                                data-lon="${lon}"
                                data-index="${index}">
                            📥 Download GEE Data
                        </button>
                    ` : ''}
                </div>
            </div>
            
            ${site.site_code ? `<p><strong>Code:</strong> ${site.site_code}</p>` : ''}
            
            ${hasCoordinates ? `
                <div class="coordinates">
                    <strong>Coordinates:</strong> ${coordinatesRaw}
                    ${site.coordinates.format ? ` (${site.coordinates.format})` : ''}
                    ${site.coordinates.datum ? ` [${site.coordinates.datum}]` : ''}
                </div>
            ` : ''}
            
            ${site.location_description ? `
                <p><strong>Location:</strong> ${site.location_description}</p>
            ` : ''}
            
            ${site.administrative_location?.country ? `
                <p><strong>Country:</strong> ${site.administrative_location.country}</p>
            ` : ''}
            
            ${site.temporal?.dating ? `
                <p><strong>Dating:</strong> ${site.temporal.dating}</p>
            ` : ''}
            
            ${site.characteristics?.site_type ? `
                <p><strong>Type:</strong> ${site.characteristics.site_type}</p>
            ` : ''}
            
            ${site.metadata?.confidence_level ? `
                <p class="confidence"><strong>Confidence:</strong> ${site.metadata.confidence_level}</p>
            ` : ''}
            
            <div class="ai-analysis-section" id="ai-analysis-${index}">
                <h4>🤖 AI-Powered Analysis</h4>
                <div id="ai-analysis-content-${index}"></div>
            </div>
            
            <div class="preview-section" id="preview-${index}">
                <h4>Satellite Imagery</h4>
                <div id="preview-content-${index}"></div>
            </div>
        </div>
    `;
    
    return html;
}

function displayAIAnalysis(data, contentElement) {
    let html = '';
    
    if (data.visual_analysis) {
        const va = data.visual_analysis;
        const metadata = va.satellite_metadata || {};
        
        html += `
            <div class="visual-analysis-section">
                <h5>🛰️ Satellite Imagery Analysis</h5>
                
                ${va.preview_image ? `
                    <img src="data:image/png;base64,${va.preview_image}" 
                        alt="Satellite Analysis" 
                        class="ai-preview-image">
                ` : ''}
                
                <div class="analysis-metadata">
                    <p><strong>Image Date:</strong> ${metadata.acquisition_date ? new Date(metadata.acquisition_date).toLocaleDateString() : 'N/A'}</p>
                    <p><strong>Cloud Cover:</strong> ${metadata.cloud_cover !== null ? metadata.cloud_cover.toFixed(1) + '%' : 'N/A'}</p>
                </div>
                
                ${va.overall_assessment ? `
                    <div class="assessment-summary">
                        <h6>Overall Assessment</h6>
                        <p>${va.overall_assessment.summary}</p>
                        <p><strong>Archaeological Potential:</strong> 
                        <span class="potential-${va.overall_assessment.archaeological_potential}">
                            ${va.overall_assessment.archaeological_potential?.toUpperCase()}
                        </span>
                        </p>
                    </div>
                ` : ''}
                
                ${va.visual_features && va.visual_features.length > 0 ? `
                    <div class="visual-features">
                        <h6>Identified Features</h6>
                        ${va.visual_features.map(feature => `
                            <div class="feature-item confidence-${feature.confidence}">
                                <strong>${feature.feature_type}</strong> 
                                <span class="confidence-badge">${feature.confidence} confidence</span>
                                <p>${feature.description}</p>
                                <p class="feature-location">📍 ${feature.location}</p>
                                <p class="feature-reasoning"><em>Reasoning: ${feature.reasoning}</em></p>
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${va.archaeological_indicators && va.archaeological_indicators.length > 0 ? `
                    <div class="archaeological-indicators">
                        <h6>Archaeological Indicators</h6>
                        <ul>
                            ${va.archaeological_indicators.map(ind => `
                                <li>
                                    <strong>${ind.indicator}:</strong> ${ind.evidence}
                                    <br><em>${ind.significance}</em>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${va.overall_assessment?.recommendations && va.overall_assessment.recommendations.length > 0 ? `
                    <div class="recommendations">
                        <h6>Recommendations</h6>
                        <ul>
                            ${va.overall_assessment.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${va.caveats && va.caveats.length > 0 ? `
                    <div class="caveats">
                        <h6>⚠️ Caveats</h6>
                        <ul>
                            ${va.caveats.map(caveat => `<li>${caveat}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    if (data.contextual_enrichment) {
        const ce = data.contextual_enrichment;
        
        html += `
            <div class="contextual-enrichment-section">
                <h5>🔍 Contextual Research</h5>
                
                ${ce.cultural_context && ce.cultural_context.summary !== 'No information available' ? `
                    <div class="cultural-context">
                        <h6>Cultural Context</h6>
                        <p>${ce.cultural_context.summary}</p>
                        ${ce.cultural_context.details && ce.cultural_context.details.length > 0 ? `
                            <ul class="sourced-facts">
                                ${ce.cultural_context.details.map(detail => `
                                    <li>
                                        ${detail.fact}
                                        <a href="${detail.source_url}" target="_blank" class="source-link" title="${detail.source_title}">
                                            [${detail.source_type || 'Source'}]
                                        </a>
                                    </li>
                                `).join('')}
                            </ul>
                        ` : ''}
                    </div>
                ` : ''}
                
                ${ce.comparative_context && ce.comparative_context.similar_sites && ce.comparative_context.similar_sites.length > 0 ? `
                    <div class="comparative-context">
                        <h6>Similar Sites</h6>
                        <ul class="similar-sites-list">
                            ${ce.comparative_context.similar_sites.map(site => `
                                <li>
                                    <strong>${site.name}</strong> ${site.location ? `(${site.location})` : ''}
                                    <br>${site.similarity}
                                    <a href="${site.source_url}" target="_blank" class="source-link" title="${site.source_title}">
                                        [Source]
                                    </a>
                                </li>
                            `).join('')}
                        </ul>
                        ${ce.comparative_context.regional_patterns && ce.comparative_context.regional_patterns !== 'No information available' ? `
                            <p><strong>Regional Patterns:</strong> ${ce.comparative_context.regional_patterns}</p>
                        ` : ''}
                    </div>
                ` : ''}
                
                ${ce.recent_research && ce.recent_research.findings && ce.recent_research.findings.length > 0 ? `
                    <div class="recent-research">
                        <h6>Recent Research</h6>
                        <ul class="research-list">
                            ${ce.recent_research.findings.map(finding => `
                                <li>
                                    ${finding.summary}
                                    ${finding.year ? `<span class="research-year">(${finding.year})</span>` : ''}
                                    <a href="${finding.source_url}" target="_blank" class="source-link" title="${finding.source_title}">
                                        [Source]
                                    </a>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                ${ce.conservation_status && ce.conservation_status.status !== 'No information available' ? `
                    <div class="conservation-status">
                        <h6>Conservation Status</h6>
                        <p>${ce.conservation_status.status}</p>
                        ${ce.conservation_status.threats && ce.conservation_status.threats.length > 0 ? `
                            <p><strong>Threats:</strong> ${ce.conservation_status.threats.join(', ')}</p>
                        ` : ''}
                        ${ce.conservation_status.sources && ce.conservation_status.sources.length > 0 ? `
                            <p class="sources-list">
                                Sources: ${ce.conservation_status.sources.map(s => 
                                    `<a href="${s.url}" target="_blank" class="source-link">${s.title}</a>`
                                ).join(', ')}
                            </p>
                        ` : ''}
                    </div>
                ` : ''}
                
                ${ce.source_quality_assessment ? `
                    <div class="source-quality">
                        <h6>ℹ️ Source Quality Assessment</h6>
                        <p>
                            <strong>Total Sources:</strong> ${ce.source_quality_assessment.total_sources} 
                            (${ce.source_quality_assessment.academic_sources} academic, 
                            ${ce.source_quality_assessment.database_sources} database, 
                            ${ce.source_quality_assessment.general_sources} general)
                        </p>
                        <p><strong>Reliability:</strong> ${ce.source_quality_assessment.reliability?.toUpperCase()}</p>
                        <p>${ce.source_quality_assessment.note}</p>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    if (data.errors && data.errors.length > 0) {
        html += `
            <div class="ai-warnings">
                <h6>⚠️ Warnings</h6>
                <ul>
                    ${data.errors.map(err => `<li>${err}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    contentElement.innerHTML = html;
}