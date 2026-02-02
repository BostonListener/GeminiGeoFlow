def create_contextual_enrichment_prompt(site_data):
    """Create prompt for contextual enrichment with search grounding"""
    
    site_name = site_data.get('site_name', 'Unknown Site')
    location = site_data.get('location_description', '')
    admin_location = site_data.get('administrative_location', {})
    country = admin_location.get('country', '')
    state = admin_location.get('state_province', '')
    
    temporal = site_data.get('temporal', {})
    dating = temporal.get('dating', '')
    cultural_period = temporal.get('cultural_period', '')
    
    characteristics = site_data.get('characteristics', {})
    site_type = characteristics.get('site_type', '')
    
    prompt = f"""# Archaeological Site Contextual Research

    ## CRITICAL RULES - CITATIONS REQUIRED

    1. **ONLY use information from search results**
    2. **EVERY factual claim MUST include a source URL**
    3. **If no information found, explicitly state "No information available"**
    4. **Never make up URLs or sources**
    5. **Prioritize academic papers, official archaeological databases, government heritage sites**
    6. **Flag when sources are low quality or general**

    ## CRITICAL SOURCE FORMATTING RULES

    **EVERY source object MUST have BOTH url AND title fields:**
    - If you have the page title from search results, use it
    - If title is unavailable, use the domain name (e.g., "iphan.gov.br", "unesco.org")
    - If domain extraction fails, use "Source"
    - **NEVER leave title as null, undefined, or empty string**
    - **NEVER use "undefined" as a title**

    Example valid sources:
    {{"url": "https://iphan.gov.br/...", "title": "IPHAN - National Heritage Institute"}}
    {{"url": "https://unesco.org/...", "title": "UNESCO World Heritage Centre"}}
    {{"url": "https://unknown-site.com/...", "title": "unknown-site.com"}}

    ## Site Information to Research

    - **Site Name**: {site_name}
    - **Location**: {location}
    - **Country**: {country}
    - **State/Region**: {state}
    - **Dating**: {dating}
    - **Cultural Period**: {cultural_period}
    - **Site Type**: {site_type}

    ## Research Tasks

    Search for and synthesize information about:

    1. **Cultural Context** (if culture/period mentioned)
    - Characteristics of {cultural_period} culture during {dating}
    - What was happening in this region during this period?
    - Typical material culture, settlement patterns

    2. **Comparative Context**
    - Similar {site_type} sites in {country} or {state}
    - How does this site type compare regionally?
    - Typical features and characteristics

    3. **Regional Archaeology**
    - Recent archaeological research in {state} or nearby regions
    - Known archaeological sites in the area
    - Current excavation projects

    4. **Conservation Status** (if applicable)
    - Is this site or region protected?
    - Any known threats (development, looting, deforestation)?
    - Heritage registration status

    ## Output Format

    Return a JSON object with this EXACT structure:

    {{
    "cultural_context": {{
        "summary": "2-3 sentence summary OR 'No information available'",
        "details": [
        {{
            "fact": "specific factual statement",
            "source_url": "https://exact-url-from-search",
            "source_title": "MUST BE POPULATED - never null/undefined",
            "source_type": "academic|database|news|general"
        }}
        ],
        "confidence": "high|medium|low|none"
    }},

    "comparative_context": {{
        "similar_sites": [
        {{
            "name": "site name",
            "location": "where it is",
            "similarity": "why it's similar",
            "source_url": "https://...",
            "source_title": "MUST BE POPULATED - never null/undefined"
        }}
        ],
        "regional_patterns": "synthesis based on sources OR 'No information available'",
        "sources": [
        {{"url": "https://...", "title": "MUST BE POPULATED - never null/undefined"}}
        ]
    }},

    "recent_research": {{
        "findings": [
        {{
            "summary": "research finding or project",
            "source_url": "https://...",
            "source_title": "MUST BE POPULATED - never null/undefined",
            "year": "YYYY or null"
        }}
        ],
        "gaps": "what information is lacking"
    }},

    "conservation_status": {{
        "status": "description OR 'No information available'",
        "threats": ["list of threats or empty array"],
        "sources": [
        {{"url": "https://...", "title": "MUST BE POPULATED - use page title, domain name, or 'Source' as fallback"}}
        ]
    }},

    "source_quality_assessment": {{
        "total_sources": 0,
        "academic_sources": 0,
        "database_sources": 0,
        "general_sources": 0,
        "reliability": "high|medium|low",
        "note": "Brief assessment of source quality"
    }}
    }}

    ## Important Notes

    - **CRITICAL**: Every "title" field in sources must be a non-empty string
    - If you cannot find specific information about this site, search for the broader region/culture
    - Be explicit when extrapolating from regional data vs site-specific data
    - Never fabricate source URLs
    - If all sources are general/unreliable, note this clearly
    - Return empty arrays/null for sections with no data, don't omit them
    - **Double-check all source objects have valid title strings before returning**

    Return ONLY the JSON, no markdown formatting, no additional text.
    """
    
    return prompt