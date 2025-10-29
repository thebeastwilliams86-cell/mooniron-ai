"""
Moon-Iron System Sentinel
An AI-powered desktop system monitor and automation tool
"""

import tkinter as tk
from gui.main_window import SentinelGUI
from utils.config import Config
from utils.logger import SentinelLogger
import sys

def main():
    logger = SentinelLogger()
    logger.log_event("System Sentinel awakens...", "SYSTEM")
    
    try:
        config = Config()
        
        root = tk.Tk()
        app = SentinelGUI(root, config, logger)
        
        logger.log_event("The Sentinel stands watch.", "SYSTEM")
        root.mainloop()
        
    except Exception as e:
        logger.log_event(f"The Sentinel falters: {str(e)}", "ERROR")
        sys.exit(1)
    finally:
        logger.log_event("The Sentinel rests.", "SYSTEM")

if __name__ == "__main__":
    main()
