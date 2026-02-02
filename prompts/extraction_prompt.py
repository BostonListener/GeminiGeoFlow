def create_extraction_prompt(paper_text):
    """Create the extraction prompt with the paper text"""
    
    prompt = """# Archaeological Site Information Extraction

    ## Task
    Extract information about archaeological sites from the provided academic paper. Your role is to act as a precise data extractor, NOT an interpreter or estimator.

    ## CRITICAL RULES - READ CAREFULLY

    1. **ONLY extract information explicitly stated in the paper**
    - If coordinates are not given, leave the coordinates field empty
    - If a site name is not mentioned, do not invent one
    - If information is ambiguous or unclear, mark it as such

    2. **NEVER:**
    - Guess or estimate coordinates from place names
    - Invent precision that doesn't exist in the source
    - Convert between coordinate systems unless explicitly shown in the paper
    - Fill in missing information based on general knowledge
    - Assume information from context alone

    3. **ALWAYS:**
    - Preserve the exact format of coordinates as written in the paper
    - Note when information is approximate, estimated, or uncertain
    - Include the specific page or section where information was found
    - Flag when coordinates are withheld or stated as "not disclosed"

    ## Information to Extract

    For each archaeological site mentioned in the paper, extract the following:

    ### Site Identification
    - **site_name**: The exact name(s) used in the paper
    - **site_code**: Any alphanumeric codes or identifiers (e.g., "PA-KU-29")
    - **alternative_names**: Other names mentioned for the same site

    ### Location Information
    - **coordinates_explicit**: ONLY if coordinates are explicitly provided
    - Extract the exact text as written (e.g., "5.23°S, 60.12°W")
    - Note the format: decimal_degrees, DMS, UTM, etc.
    - Note the datum if specified (WGS84, SAD69, etc.)
    - Mark precision level: "exact", "approximate", "rounded"
    
    - **location_description**: Textual descriptions of location
    - Examples: "near the confluence of Xingu and Amazon rivers"
    - "15 km north of modern-day Santarém"
    - "in the Upper Tapajós basin"
    
    - **administrative_location**: Modern political boundaries mentioned
    - Country, state/province, municipality, etc.

    - **location_withheld**: Boolean - true if paper explicitly states location is not disclosed

    ### Temporal Information
    - **dating**: Dates or date ranges mentioned (e.g., "1200-1400 CE", "Late Pre-Columbian")
    - **cultural_period**: Cultural phases or periods named
    - **dating_method**: If specified (radiocarbon, thermoluminescence, etc.)
    - **dating_uncertainty**: Any caveats about dating

    ### Site Characteristics
    - **site_type**: Settlement, mound, ceremonial center, earthwork, etc.
    - **site_features**: Specific features mentioned (e.g., "circular plaza", "defensive ditch")
    - **site_size**: Dimensions if provided (area, diameter, length)
    - **site_condition**: Preservation state if mentioned

    ### Context
    - **study_type**: Is this a site being actively studied or just mentioned for comparison?
    - **source_location**: Page number(s) or section where this information appears
    - **confidence_level**: Your assessment - "high" (explicit coordinates + clear description), "medium" (clear description but no coordinates), "low" (vague or passing mention)
    - **extraction_notes**: Any important caveats, ambiguities, or clarifications

    ## Output Format

    Return a JSON object with this structure:

    {
    "paper_metadata": {
        "title": "extracted from paper",
        "authors": ["list", "of", "authors"],
        "year": "publication year",
        "doi": "if available"
    },
    "extraction_summary": {
        "total_sites_found": 0,
        "sites_with_explicit_coordinates": 0,
        "sites_with_descriptions_only": 0,
        "extraction_date": "YYYY-MM-DD"
    },
    "sites": [
        {
        "site_name": "string or null",
        "site_code": "string or null",
        "alternative_names": [],
        "coordinates": {
            "has_explicit_coordinates": false,
            "raw_text": null,
            "format": null,
            "latitude": null,
            "longitude": null,
            "datum": null,
            "precision_level": null
        },
        "location_description": null,
        "administrative_location": {
            "country": null,
            "state_province": null,
            "other": null
        },
        "location_withheld": false,
        "temporal": {
            "dating": null,
            "cultural_period": null,
            "dating_method": null,
            "uncertainty": null
        },
        "characteristics": {
            "site_type": null,
            "features": [],
            "size": null,
            "condition": null
        },
        "metadata": {
            "study_type": null,
            "source_location": null,
            "confidence_level": null,
            "extraction_notes": null
        }
        }
    ]
    }

    ## Your Task

    Extract all archaeological site information from the following paper:

    """
    
    return prompt + "\n" + paper_text + "\n\nReturn ONLY the JSON output, no additional commentary."