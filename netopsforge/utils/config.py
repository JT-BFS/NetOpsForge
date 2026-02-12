"""
Configuration management for NetOpsForge
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """NetOpsForge configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent
    CMDB_PATH = BASE_DIR / os.getenv("CMDB_PATH", "cmdb/devices.yml")
    PACKS_PATH = BASE_DIR / os.getenv("PACKS_PATH", "packs")
    RECIPES_PATH = BASE_DIR / os.getenv("RECIPES_PATH", "recipes")
    LOGS_DIR = BASE_DIR / "logs"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = BASE_DIR / os.getenv("LOG_FILE", "logs/netopsforge.log")
    
    # Linear Integration
    LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
    LINEAR_TEAM_ID = os.getenv("LINEAR_TEAM_ID")
    
    # ServiceNow Integration
    SERVICENOW_INSTANCE = os.getenv("SERVICENOW_INSTANCE")
    SERVICENOW_USERNAME = os.getenv("SERVICENOW_USERNAME")
    SERVICENOW_PASSWORD = os.getenv("SERVICENOW_PASSWORD")
    
    # Connection defaults
    DEFAULT_SSH_PORT = 22
    DEFAULT_TELNET_PORT = 23
    DEFAULT_CONNECTION_TIMEOUT = 30
    DEFAULT_COMMAND_TIMEOUT = 60
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist"""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        
    @classmethod
    def get_pack_path(cls, pack_name: str) -> Path:
        """Get full path to a pack file"""
        return cls.PACKS_PATH / f"{pack_name}.yml"
    
    @classmethod
    def get_recipe_path(cls, recipe_name: str) -> Path:
        """Get full path to a recipe file"""
        return cls.RECIPES_PATH / f"{recipe_name}.yml"

