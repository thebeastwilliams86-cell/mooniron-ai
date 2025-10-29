"""
Folder monitoring system using watchdog
"""

import os
import time
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderAnalyzer:
    """Analyzes folder contents for cleanup opportunities"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def analyze_folder(self, folder_path, max_files=1000):
        """Analyze folder for file organization opportunities"""
        if not os.path.exists(folder_path):
            return None
        
        analysis = {
            "path": folder_path,
            "total_files": 0,
            "total_size_mb": 0,
            "old_files": [],
            "large_files": [],
            "duplicates": [],
            "by_extension": {},
            "suggestions": []
        }
        
        try:
            file_count = 0
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file_count >= max_files:
                        break
                    
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        size_mb = stat.st_size / (1024 * 1024)
                        mod_time = datetime.fromtimestamp(stat.st_mtime)
                        age_days = (datetime.now() - mod_time).days
                        
                        analysis["total_files"] += 1
                        analysis["total_size_mb"] += size_mb
                        
                        # Track by extension
                        ext = os.path.splitext(file)[1].lower()
                        if ext not in analysis["by_extension"]:
                            analysis["by_extension"][ext] = {"count": 0, "size_mb": 0}
                        analysis["by_extension"][ext]["count"] += 1
                        analysis["by_extension"][ext]["size_mb"] += size_mb
                        
                        # Track old files (>30 days)
                        if age_days > 30:
                            analysis["old_files"].append({
                                "path": file_path,
                                "age_days": age_days,
                                "size_mb": size_mb
                            })
                        
                        # Track large files (>100MB)
                        if size_mb > 100:
                            analysis["large_files"].append({
                                "path": file_path,
                                "size_mb": size_mb
                            })
                        
                        file_count += 1
                    except Exception as e:
                        continue
                
                if file_count >= max_files:
                    break
            
            # Generate suggestions
            analysis["suggestions"] = self._generate_suggestions(analysis)
            
        except Exception as e:
            self.logger.log_event(f"Error analyzing {folder_path}: {str(e)}", "ERROR")
        
        return analysis
    
    def _generate_suggestions(self, analysis):
        """Generate cleanup suggestions based on analysis"""
        suggestions = []
        
        # Suggest cleanup of old files
        if len(analysis["old_files"]) > 10:
            total_old_size = sum(f["size_mb"] for f in analysis["old_files"])
            suggestions.append({
                "type": "cleanup_old",
                "message": f"Archive or remove {len(analysis['old_files'])} files older than 30 days ({total_old_size:.1f} MB)",
                "files": analysis["old_files"]
            })
        
        # Suggest organizing by extension
        if len(analysis["by_extension"]) > 5:
            suggestions.append({
                "type": "organize_by_type",
                "message": f"Organize {analysis['total_files']} files into {len(analysis['by_extension'])} type-based folders",
                "extensions": analysis["by_extension"]
            })
        
        # Suggest compression for large files
        if len(analysis["large_files"]) > 0:
            total_large_size = sum(f["size_mb"] for f in analysis["large_files"])
            suggestions.append({
                "type": "compress_large",
                "message": f"Consider compressing {len(analysis['large_files'])} large files ({total_large_size:.1f} MB)",
                "files": analysis["large_files"]
            })
        
        return suggestions


class SentinelEventHandler(FileSystemEventHandler):
    """Handles file system events for monitored folders"""
    
    def __init__(self, logger, callback=None):
        super().__init__()
        self.logger = logger
        self.callback = callback
    
    def on_created(self, event):
        if not event.is_directory:
            self.logger.log_event(f"New file detected: {event.src_path}", "SCAN")
            if self.callback:
                self.callback("created", event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            if self.callback:
                self.callback("modified", event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.logger.log_event(f"File removed: {event.src_path}", "SCAN")
            if self.callback:
                self.callback("deleted", event.src_path)


class FolderWatcher:
    """Main folder watching service"""
    
    def __init__(self, logger, folders=None):
        self.logger = logger
        self.folders = folders or []
        self.observers = []
        self.analyzer = FolderAnalyzer(logger)
    
    def add_folder(self, folder_path):
        """Add a folder to watch"""
        if folder_path not in self.folders:
            self.folders.append(folder_path)
    
    def start_watching(self, callback=None):
        """Start monitoring all configured folders"""
        for folder in self.folders:
            if os.path.exists(folder):
                event_handler = SentinelEventHandler(self.logger, callback)
                observer = Observer()
                observer.schedule(event_handler, folder, recursive=True)
                observer.start()
                self.observers.append(observer)
                self.logger.log_event(f"Watch begins over {folder}", "SCAN")
    
    def stop_watching(self):
        """Stop all folder monitoring"""
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.observers = []
        self.logger.log_event("The watch ends.", "SYSTEM")
