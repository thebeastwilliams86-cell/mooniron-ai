"""
Mythic-themed logging system for the Sentinel
"""

import os
import logging
from datetime import datetime

class SentinelLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"sentinel_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("Sentinel")
        
        self.mythic_messages = {
            "SCAN": [
                "The Sentinel's gaze sweeps across {target}",
                "Ancient eyes perceive {target}",
                "The watch continues over {target}"
            ],
            "CLEANUP": [
                "The Archive is purged. {size} of echoes fade into void.",
                "Dust settles. {size} reclaimed from the forgotten.",
                "The cleansing is complete. {size} returned to the aether."
            ],
            "DEFRAG": [
                "The Blade is reforged. Fragmentation reduced.",
                "Order restored. The Blade sings once more.",
                "Chaos yields to harmony. The Blade gleams."
            ],
            "ORGANIZE": [
                "Files find their place in the grand tapestry.",
                "{count} souls returned to their rightful halls.",
                "The Archive breathes easier. {count} items sorted."
            ],
            "ERROR": [
                "The Sentinel stumbles: {error}",
                "A shadow crosses the path: {error}",
                "Darkness whispers: {error}"
            ],
            "SYSTEM": [
                "{message}"
            ]
        }
    
    def log_event(self, message, event_type="SYSTEM", **kwargs):
        if event_type in self.mythic_messages:
            templates = self.mythic_messages[event_type]
            if kwargs:
                formatted = templates[0].format(**kwargs)
            else:
                formatted = templates[0].replace("{message}", message)
        else:
            formatted = message
        
        if event_type == "ERROR":
            self.logger.error(formatted)
        else:
            self.logger.info(f"[{event_type}] {formatted}")
        
        return formatted
    
    def get_recent_logs(self, lines=50):
        log_file = os.path.join(self.log_dir, f"sentinel_{datetime.now().strftime('%Y%m%d')}.log")
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                return f.readlines()[-lines:]
        return []
