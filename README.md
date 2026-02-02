# Gemini GeoFlow: AI-Powered Archaeological Site Extraction

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![Domain](https://img.shields.io/badge/domain-Archaeology-8B4513.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285f4.svg)
![Google Earth Engine](https://img.shields.io/badge/Google-Earth%20Engine-4285f4.svg)
![Google Maps](https://img.shields.io/badge/Google-Maps-4285f4.svg)
![Sentinel-2](https://img.shields.io/badge/Sentinel--2-Satellite%20Imagery-5B9BD5.svg)
![SRTM](https://img.shields.io/badge/SRTM-DEM%20Data-70AD47.svg)
![Multimodal AI](https://img.shields.io/badge/AI-Multimodal-FF6B6B.svg)

An intelligent web application that combines **Gemini 3 Flash**, **Google Earth Engine**, and **Google Maps** to automate archaeological site extraction from academic papers and provide comprehensive satellite-based analysis.

---

## 🎯 What It Does

Upload an archaeological research paper (PDF), and the system:

1. **Extracts site information** using Gemini 3's multimodal capabilities
2. **Analyzes satellite imagery** with Gemini 3 Vision to identify archaeological features
3. **Performs contextual research** using Gemini 3 with search grounding to find related sites and recent findings
4. **Downloads satellite data** from Google Earth Engine for further analysis

All powered by **Gemini 3 Flash** with advanced reasoning, multimodal understanding, and real-time search capabilities.

---

## 🚀 Gemini 3 Integration

### Core Features Used

**1. Multimodal Input Processing**
- **PDF Analysis**: Gemini 3 processes entire research papers to extract structured archaeological data
- **Satellite Image Analysis**: Vision capabilities analyze 6-panel satellite composites (RGB, NDVI, NDWI, BSI, DEM, Slope)
- **Text + Image Reasoning**: Combined modalities for comprehensive site assessment

**2. Search Grounding**
- Real-time web search integration for contextual enrichment
- Finds similar archaeological sites globally
- Retrieves recent research and conservation status
- All responses include verified source citations

**3. Structured Outputs**
- Complex JSON schema extraction from unstructured PDFs
- Nested archaeological metadata (coordinates, dating, site characteristics)
- Satellite analysis results with confidence levels and recommendations

**4. Advanced Reasoning**
- Coordinate format recognition and conversion (DMS, decimal degrees)
- Archaeological feature identification in satellite imagery
- Cross-referencing site data with regional archaeological patterns

### Why Gemini 3 Flash?

- **Speed**: Sub-second response for PDF extraction and image analysis
- **Multimodal**: Seamlessly handles text, images, and search results
- **Structured**: Native JSON output with complex nested schemas
- **Grounded**: Search integration ensures factual accuracy with citations
- **Cost-effective**: Flash model provides enterprise-grade intelligence at scale

---

## 🛠️ Architecture
```
PDF Upload → Gemini 3 (Text) → Structured Site Data
                ↓
    Site Coordinates → Google Earth Engine → Satellite Data
                ↓
    Satellite Images → Gemini 3 (Vision) → Archaeological Analysis
                ↓
    Site Metadata → Gemini 3 (Search) → Contextual Research
                ↓
    Integrated Results → Google Maps Visualization
```

### Google Ecosystem Integration

- **Gemini 3 Flash**: All AI processing (extraction, analysis, research)
- **Google Earth Engine**: Sentinel-2 imagery, SRTM DEM, spectral indices
- **Google Maps**: Interactive site visualization and navigation
- **Google Cloud**: Service account authentication for GEE

---

## 📋 Example Workflow

**Input**: Upload "Archaeological Survey of Brazilian Amazon.pdf"

**Gemini 3 Extraction Output**:
```json
{
  "sites": [
    {
      "site_name": "Fazenda Colorada",
      "coordinates": {
        "raw_text": "9°57'38.96\"S, 67°29'51.39\"W",
        "latitude": -9.960822,
        "longitude": -67.497608
      },
      "temporal": {
        "dating": "1200-1400 CE",
        "cultural_period": "Late Pre-Columbian"
      },
      "characteristics": {
        "site_type": "Settlement mound",
        "features": ["circular plaza", "defensive earthworks"]
      }
    }
  ]
}
```

**Gemini 3 Vision Analysis** (on satellite imagery):
```json
{
  "visual_features": [
    {
      "feature_type": "Circular earthwork",
      "confidence": "high",
      "location": "Center-west quadrant",
      "reasoning": "Distinct circular pattern in NDVI suggests buried structure with altered vegetation"
    }
  ],
  "archaeological_potential": "high",
  "recommendations": [
    "Ground-penetrating radar survey recommended",
    "Darker soils in BSI indicate possible terra preta (anthropogenic soil)"
  ]
}
```

**Gemini 3 Search Grounding** (contextual research):
```json
{
  "similar_sites": [
    {
      "name": "Acre geoglyphs",
      "location": "Acre, Brazil",
      "similarity": "Geometric earthworks from same cultural period",
      "source_url": "https://www.nature.com/articles/...",
      "source_title": "Nature - Ancient Amazonian earthworks"
    }
  ],
  "recent_research": [
    {
      "summary": "LiDAR reveals extensive pre-Columbian settlements in Amazon",
      "year": "2024",
      "source_url": "https://science.org/..."
    }
  ]
}
```

---

## 🎨 Key Capabilities Demonstrated

### 1. Advanced Document Understanding
- Extracts precise coordinates from various formats (DMS, decimal, UTM)
- Identifies ambiguous or withheld location data
- Preserves confidence levels and source references

### 2. Multimodal Reasoning
- Analyzes 6 different satellite data products simultaneously
- Correlates vegetation patterns (NDVI) with terrain (DEM/Slope)
- Identifies archaeological indicators invisible to single-sensor analysis

### 3. Grounded Research
- Every factual claim includes source URL and title
- Distinguishes between academic, database, and general sources
- Provides reliability assessment of information quality

### 4. Practical Intelligence
- Converts academic text to actionable GIS data
- Generates researcher-focused recommendations
- Flags uncertainties and data quality issues

---

## 🔧 Setup & Deployment

### Prerequisites

1. **Gemini API Key**
   - Get from: https://aistudio.google.com/apikey

2. **Google Earth Engine Service Account**
   - Create GCP project: https://console.cloud.google.com/
   - Enable Earth Engine API
   - Create service account with JSON key
   - Register at: https://code.earthengine.google.com/

### Environment Configuration

Create `.env` file:
```bash
GEMINI_API_KEY=your-gemini-api-key
GEE_PROJECT_ID=your-gcp-project-id
```

Place GEE service account JSON:
```bash
# Rename to gee_service_account.json in project root
mv ~/Downloads/your-project-xxxxx.json ./gee_service_account.json
```

### Docker Deployment
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8088
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

---

## 📁 Project Structure
```
gemini-geoflow/
│
├── app.py                              # Flask application entry point
├── config.py                           # Configuration and GEE settings
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Container configuration
├── docker-compose.yml                  # Docker orchestration    
│
├── prompts/                            # Gemini 3 prompt templates
│   ├── extraction_prompt.py            # PDF site extraction instructions
│   ├── satellite_analysis_prompt.py    # Vision analysis guidelines
│   └── contextual_enrichment_prompt.py # Search grounding prompts
│
├── services/                           # Core business logic
│   ├── llm_service.py                  # Gemini 3 API integration
│   ├── gee_service.py                  # Earth Engine data extraction
│   └── visualization_service.py        # Satellite image rendering
│
├── routes/                             # Flask API endpoints
│   ├── extraction_routes.py            # /extract - PDF processing
│   ├── gee_routes.py                   # /preview_gee, /download_gee
│   └── analysis_routes.py              # /ai_analysis - Gemini vision + search
│
├── utils/                              # Utility functions
│   ├── coordinate_parser.py            # DMS/decimal conversion
│   └── pdf_processor.py                # PDF text extraction
│
├── templates/                          # Frontend HTML
│   └── index.html                      # Web interface
│
└── static/                             # Frontend assets
    ├── css/
    │   └── style.css                   # Application styling
    └── js/
        ├── app.js                      # Application initialization
        ├── api.js                      # Backend communication
        ├── ui.js                       # UI rendering
        ├── eventHandlers.js            # User interactions
        └── mapHelpers.js               # Google Maps integration
```

---

## 🔐 Security Notes

**Never commit these files:**
- `.env` (contains API keys)
- `gee_service_account.json` (GCP credentials)

Use `.gitignore` to exclude sensitive data.

---