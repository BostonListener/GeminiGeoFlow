#!/usr/bin/env python3
"""
Flask web interface for Archaeological Site Extraction with GEE Integration
"""

from flask import Flask, render_template
import sys
import os
import logging

from config import Config
from services.gee_service import initialize_gee
from routes.extraction_routes import extraction_bp
from routes.gee_routes import gee_bp
from routes.analysis_routes import analysis_bp

app = Flask(__name__)
app.config.from_object(Config)

# Suppress Flask request logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Register blueprints
app.register_blueprint(extraction_bp)
app.register_blueprint(gee_bp)
app.register_blueprint(analysis_bp)

# Initialize GEE on startup
GEE_INITIALIZED = initialize_gee()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment.")
        print("Create a .env file with: GEMINI_API_KEY=your-key-here")
        sys.exit(1)
    
    if not GEE_INITIALIZED:
        print("\nWARNING: Google Earth Engine not initialized!")
        print("GEE download features will not work.")
        print("Please configure gee_service_account.json")
    
    app.run(debug=False, host='0.0.0.0', port=8088)