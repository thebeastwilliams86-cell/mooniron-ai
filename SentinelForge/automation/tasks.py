"""
Task automation for defrag, cleanup, and file archiving
"""

import os
import shutil
import platform
from datetime import datetime, timedelta

class AutomationTasks:
    """Handles automated system maintenance tasks"""
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.is_windows = platform.system() == "Windows"
    
    def cleanup_temp_files(self, folder_path, age_days=30, dry_run=True):
        """
        Clean up temporary and old files
        
        Args:
            folder_path: Path to clean
            age_days: Remove files older than this
            dry_run: If True, only report what would be deleted
        
        Returns:
            dict: Results of cleanup operation
        """
        if not os.path.exists(folder_path):
            return {"error": "Path does not exist"}
        
        results = {
            "files_removed": 0,
            "space_freed_mb": 0,
            "files_to_remove": [],
            "errors": []
        }
        
        temp_extensions = self.config.get("archive_extensions", [".tmp", ".bak", ".old", ".cache"])
        cutoff_date = datetime.now() - timedelta(days=age_days)
        
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        stat = os.stat(file_path)
                        mod_time = datetime.fromtimestamp(stat.st_mtime)
                        size_mb = stat.st_size / (1024 * 1024)
                        
                        # Check if file is old or has temp extension
                        is_old = mod_time < cutoff_date
                        is_temp = any(file.endswith(ext) for ext in temp_extensions)
                        
                        if is_old or is_temp:
                            results["files_to_remove"].append({
                                "path": file_path,
                                "size_mb": size_mb,
                                "age_days": (datetime.now() - mod_time).days,
                                "reason": "old" if is_old else "temp"
                            })
                            
                            if not dry_run:
                                os.remove(file_path)
                                results["files_removed"] += 1
                                results["space_freed_mb"] += size_mb
                    
                    except Exception as e:
                        results["errors"].append(str(e))
            
            if not dry_run and results["files_removed"] > 0:
                self.logger.log_event(
                    f"Cleanup complete",
                    "CLEANUP",
                    size=f"{results['space_freed_mb']:.2f} MB"
                )
        
        except Exception as e:
            results["errors"].append(str(e))
            self.logger.log_event(str(e), "ERROR", error=str(e))
        
        return results
    
    def defragment_disk(self, drive="C:", dry_run=True):
        """
        Defragment disk (Windows only)
        
        Args:
            drive: Drive letter to defragment
            dry_run: If True, only analyze
        
        Returns:
            dict: Results of defragmentation
        """
        if not self.is_windows:
            return {
                "error": "Defragmentation only supported on Windows",
                "platform": platform.system()
            }
        
        try:
            import subprocess
            
            if dry_run:
                command = ['defrag', drive, '/A']
                action = "analyzed"
            else:
                command = ['defrag', drive, '/O']
                action = "defragmented"
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if not dry_run:
                self.logger.log_event("The Blade is reforged", "DEFRAG")
            
            return {
                "drive": drive,
                "action": action,
                "output": result.stdout,
                "success": result.returncode == 0
            }
        
        except Exception as e:
            self.logger.log_event(str(e), "ERROR", error=str(e))
            return {"error": str(e)}
    
    def archive_files(self, files_to_archive, archive_folder, dry_run=True):
        """
        Move files to an archive folder
        
        Args:
            files_to_archive: List of file paths
            archive_folder: Destination folder
            dry_run: If True, only report what would be archived
        
        Returns:
            dict: Results of archiving operation
        """
        results = {
            "files_archived": 0,
            "total_size_mb": 0,
            "errors": []
        }
        
        if not dry_run:
            os.makedirs(archive_folder, exist_ok=True)
        
        for file_path in files_to_archive:
            if not os.path.exists(file_path):
                results["errors"].append(f"File not found: {file_path}")
                continue
            
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                results["total_size_mb"] += size_mb
                
                if not dry_run:
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(archive_folder, filename)
                    
                    # Handle duplicate names
                    counter = 1
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(filename)
                        dest_path = os.path.join(archive_folder, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    shutil.move(file_path, dest_path)
                    results["files_archived"] += 1
            
            except Exception as e:
                results["errors"].append(str(e))
        
        if not dry_run and results["files_archived"] > 0:
            self.logger.log_event(
                "Files archived",
                "ORGANIZE",
                count=results["files_archived"]
            )
        
        return results
    
    def organize_by_type(self, source_folder, dry_run=True):
        """
        Organize files into subfolders by type
        
        Args:
            source_folder: Folder to organize
            dry_run: If True, only report what would be done
        
        Returns:
            dict: Results of organization
        """
        if not os.path.exists(source_folder):
            return {"error": "Folder does not exist"}
        
        results = {
            "files_organized": 0,
            "folders_created": [],
            "errors": []
        }
        
        # Define type categories
        type_categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c"],
            "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"]
        }
        
        try:
            for file in os.listdir(source_folder):
                file_path = os.path.join(source_folder, file)
                
                if not os.path.isfile(file_path):
                    continue
                
                ext = os.path.splitext(file)[1].lower()
                
                # Find category
                category = "Other"
                for cat, extensions in type_categories.items():
                    if ext in extensions:
                        category = cat
                        break
                
                # Create category folder
                category_path = os.path.join(source_folder, category)
                
                if not dry_run:
                    if not os.path.exists(category_path):
                        os.makedirs(category_path)
                        results["folders_created"].append(category)
                    
                    dest_path = os.path.join(category_path, file)
                    shutil.move(file_path, dest_path)
                
                results["files_organized"] += 1
        
        except Exception as e:
            results["errors"].append(str(e))
            self.logger.log_event(str(e), "ERROR", error=str(e))
        
        if not dry_run and results["files_organized"] > 0:
            self.logger.log_event(
                "Files organized",
                "ORGANIZE",
                count=results["files_organized"]
            )
        
        return results
