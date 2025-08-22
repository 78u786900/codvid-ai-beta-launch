"""
Configuration settings for CodVid.AI Instagram Analytics Platform
"""

import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # API Configuration - Updated to match notebook environments
    API_BASE_URLS = {
        "development": "https://codvid-ai-backend-development.up.railway.app",
        "production": "https://codvid-ai-backend-production.up.railway.app", 
        "local": "http://localhost:8080",
        # Added to match demo notebooks
        "betamale": "https://codvid-ai-backend-betamale.up.railway.app"
    }
    
    # Default environment - can be changed via environment variable
    DEFAULT_ENV = "development"
    
    # Streamlit Configuration
    STREAMLIT_CONFIG = {
        "page_title": "CodVid.AI - Instagram Analytics",
        "page_icon": "📊",  # Will be updated to CodVid.AI logo
        "layout": "wide",
        "initial_sidebar_state": "collapsed"
    }
    
    # Mobile Optimization
    MOBILE_CONFIG = {
        "button_height": "3rem",
        "button_font_size": "1rem",
        "border_radius": "10px"
    }
    
    # Chart Configuration
    CHART_CONFIG = {
        "height": 400,
        "use_container_width": True,
        "showlegend": False
    }
    
    # Scraping Intervals
    SCRAPE_INTERVALS = {
        "min_days": 0.5,
        "max_days": 30.0,
        "default_days": 2.0
    }
    
    # Pagination
    PAGINATION = {
        "posts_per_page": 10,
        "max_posts_display": 50
    }
    
    # Sentiment Analysis Configuration
    SENTIMENT_CONFIG = {
        "max_bar_width": 30,
        "emoji_map": {
            "positive": "😊",
            "negative": "😞", 
            "neutral": "😐"
        }
    }
    
    # CodVid.AI Branding
    BRANDING = {
        "company_name": "CodVid.AI",
        "app_name": "Instagram Analytics Platform",
        "tagline": "Premium Instagram Analytics & AI Insights",
        "primary_color": "#1E40AF",  # Blue
        "secondary_color": "#6B7280",  # Gray
        "accent_color": "#10B981",  # Green
        "background_color": "#F9FAFB",  # Light gray
        "text_color": "#111827"  # Dark gray
    }
    
    @classmethod
    def get_api_url(cls, environment: str = None) -> str:
        """Get API base URL for specified environment"""
        env = environment or cls.get_environment()
        return cls.API_BASE_URLS.get(env, cls.API_BASE_URLS[cls.DEFAULT_ENV])
    
    @classmethod
    def get_environment(cls) -> str:
        """Get current environment from environment variable"""
        return os.getenv("APP_ENV", cls.DEFAULT_ENV)
    
    @classmethod
    def set_environment(cls, env: str):
        """Set the environment"""
        if env in cls.API_BASE_URLS:
            os.environ["APP_ENV"] = env
            return True
        return False
    
    @classmethod
    def get_all_config(cls) -> Dict[str, Any]:
        """Get all configuration settings"""
        return {
            "api_base_url": cls.get_api_url(cls.get_environment()),
            "environment": cls.get_environment(),
            "streamlit_config": cls.STREAMLIT_CONFIG,
            "mobile_config": cls.MOBILE_CONFIG,
            "chart_config": cls.CHART_CONFIG,
            "scrape_intervals": cls.SCRAPE_INTERVALS,
            "pagination": cls.PAGINATION,
            "sentiment_config": cls.SENTIMENT_CONFIG,
            "branding": cls.BRANDING
        } 