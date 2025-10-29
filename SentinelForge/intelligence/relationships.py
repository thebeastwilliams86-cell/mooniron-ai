"""
File Relationship Detection - Finds related files
"""

import os
import re
from collections import defaultdict
from datetime import datetime, timedelta

class RelationshipDetector:
    """
    Detects relationships between files:
    - Project folders
    - Document series
    - Related media
    - Backup/original pairs
    """
    
    def __init__(self, logger):
        self.logger = logger
    
    def detect_all_relationships(self, file_info):
        """
        Comprehensive relationship detection
        
        Args:
            file_info: List of file information dicts
        
        Returns:
            Dict of detected relationships
        """
        relationships = {
            "projects": self.detect_project_folders(file_info),
            "series": self.detect_file_series(file_info),
            "pairs": self.detect_backup_pairs(file_info),
            "related_media": self.detect_related_media(file_info),
            "temporal_groups": self.detect_temporal_groups(file_info)
        }
        
        return relationships
    
    def detect_project_folders(self, file_info):
        """
        Detect project-like folder structures
        (code repos, work projects, etc.)
        """
        projects = []
        
        # Group files by directory
        by_directory = defaultdict(list)
        for file in file_info:
            dir_path = os.path.dirname(file.get('path', ''))
            by_directory[dir_path].append(file)
        
        for dir_path, files in by_directory.items():
            project_indicators = {
                "code_files": 0,
                "config_files": 0,
                "docs": 0,
                "has_readme": False,
                "has_gitignore": False,
                "has_package_json": False
            }
            
            for file in files:
                ext = file.get('extension', '').lower()
                name = file.get('name', '').lower()
                
                # Check for code files
                if ext in ['.py', '.js', '.java', '.cpp', '.c', '.go', '.rs', '.ts']:
                    project_indicators["code_files"] += 1
                
                # Check for config files
                if ext in ['.json', '.yaml', '.toml', '.ini', '.xml']:
                    project_indicators["config_files"] += 1
                
                # Check for docs
                if ext in ['.md', '.txt', '.rst']:
                    project_indicators["docs"] += 1
                
                # Check for specific files
                if 'readme' in name:
                    project_indicators["has_readme"] = True
                if '.gitignore' in name or 'gitignore' in name:
                    project_indicators["has_gitignore"] = True
                if 'package.json' in name:
                    project_indicators["has_package_json"] = True
            
            # Determine if this is a project
            is_project = False
            project_type = "unknown"
            confidence = 0
            
            if project_indicators["code_files"] >= 3:
                is_project = True
                project_type = "code_project"
                confidence = min(95, 50 + (project_indicators["code_files"] * 5))
                
                if project_indicators["has_readme"]:
                    confidence += 10
                if project_indicators["has_gitignore"]:
                    confidence += 10
            
            if is_project:
                projects.append({
                    "path": dir_path,
                    "type": project_type,
                    "confidence": confidence,
                    "file_count": len(files),
                    "indicators": project_indicators
                })
        
        return projects
    
    def detect_file_series(self, file_info):
        """
        Detect numbered file series (photo_1, photo_2, etc.)
        """
        series = defaultdict(list)
        
        for file in file_info:
            name = file.get('name', '')
            
            # Remove numbers to get base pattern
            base_pattern = re.sub(r'\d+', '#', name)
            
            series[base_pattern].append(file)
        
        # Filter to only series with 3+ files
        detected_series = []
        for pattern, files in series.items():
            if len(files) >= 3 and '#' in pattern:
                # Extract the numbering pattern
                numbers = []
                for file in files:
                    match = re.search(r'\d+', file.get('name', ''))
                    if match:
                        numbers.append(int(match.group()))
                
                # Check if sequential
                numbers.sort()
                is_sequential = all(
                    numbers[i+1] - numbers[i] == 1
                    for i in range(len(numbers)-1)
                )
                
                detected_series.append({
                    "pattern": pattern,
                    "files": files,
                    "count": len(files),
                    "is_sequential": is_sequential,
                    "range": f"{min(numbers)}-{max(numbers)}" if numbers else "unknown"
                })
        
        return detected_series
    
    def detect_backup_pairs(self, file_info):
        """
        Detect backup/original file pairs
        """
        pairs = []
        
        # Group by base name
        by_base_name = defaultdict(list)
        
        for file in file_info:
            name = file.get('name', '')
            
            # Remove common backup suffixes
            base = re.sub(r'(?i)\s*[-_]?\s*(copy|backup|old|bak|\(\d+\))$', '', name)
            by_base_name[base].append(file)
        
        # Find pairs
        for base, files in by_base_name.items():
            if len(files) > 1:
                # Sort by modification time
                files_sorted = sorted(
                    files,
                    key=lambda f: f.get('modified_time', datetime.min),
                    reverse=True
                )
                
                pairs.append({
                    "base_name": base,
                    "original": files_sorted[0],
                    "backups": files_sorted[1:],
                    "count": len(files)
                })
        
        return pairs
    
    def detect_related_media(self, file_info):
        """
        Detect related media files (same event/project)
        """
        related_groups = []
        
        # Group by creation date (within 1 hour)
        image_files = [f for f in file_info if f.get('extension', '').lower() in ['.jpg', '.png', '.gif']]
        video_files = [f for f in file_info if f.get('extension', '').lower() in ['.mp4', '.mov', '.avi']]
        
        # Group images by time
        time_groups = defaultdict(list)
        
        for file in image_files:
            if 'modified_time' in file:
                # Round to nearest hour
                time_key = file['modified_time'].replace(minute=0, second=0, microsecond=0)
                time_groups[time_key].append(file)
        
        # Find groups with multiple files
        for time_key, files in time_groups.items():
            if len(files) >= 5:  # At least 5 images in the same hour
                related_groups.append({
                    "type": "photo_batch",
                    "timestamp": time_key,
                    "files": files,
                    "count": len(files)
                })
        
        return related_groups
    
    def detect_temporal_groups(self, file_info):
        """
        Group files by creation/modification time period
        """
        groups = defaultdict(list)
        
        for file in file_info:
            if 'modified_time' in file:
                # Group by month
                month_key = file['modified_time'].strftime('%Y-%m')
                groups[month_key].append(file)
        
        temporal_groups = []
        for period, files in groups.items():
            if len(files) >= 10:  # Significant group
                temporal_groups.append({
                    "period": period,
                    "files": files,
                    "count": len(files),
                    "total_size_mb": sum(f.get('size_mb', 0) for f in files)
                })
        
        return sorted(temporal_groups, key=lambda x: x['period'], reverse=True)
    
    def generate_relationship_report(self, relationships):
        """Generate human-readable relationship report"""
        report = ["🔗 FILE RELATIONSHIP ANALYSIS 🔗\n"]
        
        # Projects
        projects = relationships.get("projects", [])
        if projects:
            report.append(f"📁 DETECTED PROJECTS: {len(projects)}")
            for proj in projects[:5]:
                report.append(f"   • {os.path.basename(proj['path'])}: {proj['file_count']} files ({proj['confidence']}% confidence)")
        
        # Series
        series = relationships.get("series", [])
        if series:
            report.append(f"\n📊 FILE SERIES: {len(series)}")
            for s in series[:5]:
                seq = "sequential" if s['is_sequential'] else "non-sequential"
                report.append(f"   • {s['pattern']}: {s['count']} files ({seq})")
        
        # Backup pairs
        pairs = relationships.get("pairs", [])
        if pairs:
            report.append(f"\n💾 BACKUP PAIRS: {len(pairs)}")
            for pair in pairs[:5]:
                report.append(f"   • {pair['base_name']}: 1 original + {len(pair['backups'])} backup(s)")
        
        # Related media
        media = relationships.get("related_media", [])
        if media:
            report.append(f"\n📸 RELATED MEDIA: {len(media)} groups")
            for group in media[:3]:
                report.append(f"   • {group['timestamp']}: {group['count']} photos")
        
        # Temporal groups
        temporal = relationships.get("temporal_groups", [])
        if temporal:
            report.append(f"\n📅 TEMPORAL GROUPS:")
            for group in temporal[:5]:
                report.append(f"   • {group['period']}: {group['count']} files ({group['total_size_mb']:.1f} MB)")
        
        return "\n".join(report)
