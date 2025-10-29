"""
Configuration management for the Sentinel
"""

import json
import os

class Config:
    def __init__(self, config_file="sentinel_config.json"):
        self.config_file = config_file
        self.default_config = {
            "monitored_folders": [],
            "scan_interval": 300,
            "auto_cleanup_threshold_gb": 5.0,
            "auto_defrag_threshold": 15,
            "enable_auto_actions": False,
            "openai_model": "gpt-4o-mini",
            "max_file_analysis_batch": 50,
            "mythic_theme": True,
            "archive_extensions": [".tmp", ".bak", ".old", ".cache"],
            "cleanup_age_days": 30
        }
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    return {**self.default_config, **loaded}
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.default_config
        else:
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config=None):
        if config:
            self.config = config
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()
    
    def add_monitored_folder(self, folder_path):
        if folder_path not in self.config["monitored_folders"]:
            self.config["monitored_folders"].append(folder_path)
            self.save_config()
    
    def remove_monitored_folder(self, folder_path):
        if folder_path in self.config["monitored_folders"]:
            self.config["monitored_folders"].remove(folder_path)
            self.save_config()
