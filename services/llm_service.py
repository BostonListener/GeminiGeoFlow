import os
import json
import warnings
from google import genai
from google.genai import types
from prompts.extraction_prompt import create_extraction_prompt
from prompts.satellite_analysis_prompt import create_satellite_analysis_prompt
from prompts.contextual_enrichment_prompt import create_contextual_enrichment_prompt
warnings.filterwarnings('ignore', module='google.genai')

def get_gemini_client():
    """Get initialized Gemini client"""
    return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_sites_with_llm(paper_text):
    """Use Gemini to extract site information"""
    client = get_gemini_client()
    prompt = create_extraction_prompt(paper_text)
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    
    response_text = response.text
    
    try:
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        extracted_data = json.loads(response_text)
        return extracted_data
    except json.JSONDecodeError as e:
        return {"raw_response": response_text, "parse_error": str(e)}

def analyze_satellite_imagery(site_name, metadata, image_data):
    """Analyze satellite imagery with Gemini Vision"""
    client = get_gemini_client()
    prompt = create_satellite_analysis_prompt(site_name, metadata)
    
    import base64
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=base64.b64decode(image_data),
                mime_type="image/png"
            )
        ]
    )
    
    response_text = response.text
    if response_text.startswith("```json"):
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif response_text.startswith("```"):
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    return json.loads(response_text)

def enrich_site_context(site_data):
    """Perform contextual enrichment with search grounding"""
    client = get_gemini_client()
    
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    config = types.GenerateContentConfig(
        tools=[grounding_tool],
        response_modalities=["TEXT"]
    )
    
    prompt = create_contextual_enrichment_prompt(site_data)
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=config
    )
    
    response_text = response.text
    if response_text.startswith("```json"):
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif response_text.startswith("```"):
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    return json.loads(response_text)