def create_satellite_analysis_prompt(site_name, metadata):
    """Create prompt for satellite imagery analysis"""
    
    prompt = f"""# Archaeological Satellite Imagery Analysis

    You are analyzing satellite imagery for an archaeological site.

    ## Site Information
    - Name: {site_name}
    - Coordinates: {metadata.get('latitude', 'N/A')}, {metadata.get('longitude', 'N/A')}
    - Grid Size: {metadata.get('cell_size_km', 1)} km × {metadata.get('cell_size_km', 1)} km

    ## Images Provided
    You are viewing a 6-panel satellite analysis:
    1. RGB Composite (natural color)
    2. NDVI (vegetation index: -1 to +1, higher = more vegetation)
    3. NDWI (water index: -1 to +1, higher = more water)
    4. BSI (bare soil index: -1 to +1, higher = more exposed soil)
    5. DEM (elevation in meters)
    6. Slope (terrain slope in degrees)

    ## Your Task

    Analyze these images for archaeological features and return a JSON object:

    {{
    "visual_features": [
        {{
        "feature_type": "type of feature (e.g., 'circular earthwork', 'linear feature', 'mound')",
        "description": "detailed description",
        "location": "location within image (e.g., 'center', 'northeast quadrant')",
        "confidence": "high|medium|low",
        "reasoning": "why you identified this feature"
        }}
    ],
    "landscape_context": {{
        "terrain": "description of terrain type",
        "elevation_pattern": "description of elevation patterns",
        "vegetation_pattern": "description from NDVI",
        "water_presence": "description from NDWI",
        "soil_exposure": "description from BSI"
    }},
    "archaeological_indicators": [
        {{
        "indicator": "what suggests human activity",
        "evidence": "which imagery shows this",
        "significance": "what this might mean archaeologically"
        }}
    ],
    "overall_assessment": {{
        "summary": "2-3 sentence summary of what you see",
        "archaeological_potential": "high|medium|low",
        "recommendations": ["list of recommendations for researchers"]
    }},
    "caveats": [
        "list any limitations or uncertainties in the analysis"
    ]
    }}

    ## Guidelines
    - Look for geometric patterns (circles, squares, lines)
    - Unusual vegetation patterns can indicate buried structures
    - Elevated areas in flat terrain may be mounds
    - Darker soils (terra preta) indicate human occupation
    - Linear features may be old roads or earthworks
    - Be conservative - note uncertainty when features are ambiguous
    - Consider natural features vs human-made

    Return ONLY the JSON, no additional text.
    """
    
    return prompt