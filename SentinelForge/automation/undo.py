"""
Undo System - Complete change history with rollback capability
"""

import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

class UndoSystem:
    """
    Tracks all file operations and enables complete rollback
    """
    
    def __init__(self, logger, backup_dir=".sentinel_backups"):
        self.logger = logger
        self.backup_dir = backup_dir
        self.history_file = os.path.join(backup_dir, "history.json")
        self.history = []
        
        os.makedirs(backup_dir, exist_ok=True)
        self.load_history()
    
    def load_history(self):
        """Load operation history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def save_history(self):
        """Save operation history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)
    
    def create_checkpoint(self, operation_type, description, files_affected):
        """
        Create a checkpoint before making changes
        
        Args:
            operation_type: Type of operation (cleanup, organize, etc.)
            description: Human-readable description
            files_affected: List of file paths that will be modified
        
        Returns:
            checkpoint_id: ID for this checkpoint
        """
        checkpoint_id = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_dir = os.path.join(self.backup_dir, checkpoint_id)
        os.makedirs(checkpoint_dir, exist_ok=True)
        
        # Backup affected files
        backed_up_files = []
        
        for file_path in files_affected:
            if os.path.exists(file_path):
                try:
                    # Create relative path structure in backup
                    rel_path = os.path.relpath(file_path)
                    backup_path = os.path.join(checkpoint_dir, rel_path)
                    
                    # Create directories as needed
                    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(file_path, backup_path)
                    
                    backed_up_files.append({
                        "original_path": file_path,
                        "backup_path": backup_path,
                        "size_mb": os.path.getsize(file_path) / (1024 * 1024)
                    })
                except Exception as e:
                    self.logger.log_event(f"Backup failed for {file_path}: {str(e)}", "ERROR")
        
        # Record checkpoint
        checkpoint = {
            "id": checkpoint_id,
            "timestamp": datetime.now().isoformat(),
            "operation": operation_type,
            "description": description,
            "files_count": len(backed_up_files),
            "total_size_mb": sum(f["size_mb"] for f in backed_up_files),
            "files": backed_up_files,
            "checkpoint_dir": checkpoint_dir,
            "can_undo": True
        }
        
        self.history.append(checkpoint)
        self.save_history()
        
        self.logger.log_event(f"Checkpoint created: {checkpoint_id}", "SYSTEM")
        
        return checkpoint_id
    
    def record_operation(self, checkpoint_id, operation_details):
        """
        Record the actual operation that was performed
        
        Args:
            checkpoint_id: The checkpoint ID
            operation_details: Dict with details of what was done
        """
        for checkpoint in self.history:
            if checkpoint["id"] == checkpoint_id:
                checkpoint["operation_details"] = operation_details
                checkpoint["completed"] = True
                checkpoint["completed_at"] = datetime.now().isoformat()
                self.save_history()
                break
    
    def undo_last(self):
        """
        Undo the last operation
        
        Returns:
            Result of undo operation
        """
        # Find last undoable operation
        for checkpoint in reversed(self.history):
            if checkpoint.get("can_undo", False) and not checkpoint.get("undone", False):
                return self.undo_checkpoint(checkpoint["id"])
        
        return {
            "success": False,
            "error": "No operations to undo"
        }
    
    def undo_checkpoint(self, checkpoint_id):
        """
        Undo a specific checkpoint
        
        Args:
            checkpoint_id: ID of checkpoint to undo
        
        Returns:
            Result of undo operation
        """
        checkpoint = None
        for cp in self.history:
            if cp["id"] == checkpoint_id:
                checkpoint = cp
                break
        
        if not checkpoint:
            return {
                "success": False,
                "error": "Checkpoint not found"
            }
        
        if checkpoint.get("undone", False):
            return {
                "success": False,
                "error": "Already undone"
            }
        
        restored_count = 0
        errors = []
        
        # Restore files from backup
        for file_info in checkpoint.get("files", []):
            backup_path = file_info["backup_path"]
            original_path = file_info["original_path"]
            
            try:
                if os.path.exists(backup_path):
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(original_path), exist_ok=True)
                    
                    # Restore file
                    shutil.copy2(backup_path, original_path)
                    restored_count += 1
                else:
                    errors.append(f"Backup not found: {backup_path}")
            
            except Exception as e:
                errors.append(f"Failed to restore {original_path}: {str(e)}")
        
        # Mark as undone
        checkpoint["undone"] = True
        checkpoint["undone_at"] = datetime.now().isoformat()
        checkpoint["restore_count"] = restored_count
        checkpoint["restore_errors"] = errors
        
        self.save_history()
        
        self.logger.log_event(f"Undone: {checkpoint_id} ({restored_count} files restored)", "SYSTEM")
        
        return {
            "success": True,
            "checkpoint_id": checkpoint_id,
            "files_restored": restored_count,
            "errors": errors
        }
    
    def get_history(self, limit=20):
        """Get recent operation history"""
        return list(reversed(self.history[-limit:]))
    
    def get_undo_candidates(self):
        """Get operations that can be undone"""
        candidates = []
        
        for checkpoint in reversed(self.history):
            if checkpoint.get("can_undo", False) and not checkpoint.get("undone", False):
                candidates.append({
                    "id": checkpoint["id"],
                    "operation": checkpoint["operation"],
                    "description": checkpoint["description"],
                    "timestamp": checkpoint["timestamp"],
                    "files_count": checkpoint["files_count"]
                })
        
        return candidates
    
    def cleanup_old_backups(self, keep_days=30):
        """Remove old backups to save space"""
        cutoff = datetime.now() - timedelta(days=keep_days)
        removed_count = 0
        
        for checkpoint in self.history:
            checkpoint_time = datetime.fromisoformat(checkpoint["timestamp"])
            
            if checkpoint_time < cutoff:
                checkpoint_dir = checkpoint.get("checkpoint_dir")
                if checkpoint_dir and os.path.exists(checkpoint_dir):
                    try:
                        shutil.rmtree(checkpoint_dir)
                        checkpoint["backup_removed"] = True
                        removed_count += 1
                    except Exception as e:
                        self.logger.log_event(f"Failed to remove backup: {str(e)}", "ERROR")
        
        if removed_count > 0:
            self.save_history()
            self.logger.log_event(f"Cleaned up {removed_count} old backups", "SYSTEM")
        
        return removed_count
