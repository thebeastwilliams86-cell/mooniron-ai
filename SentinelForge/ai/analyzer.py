"""
Sentinel Intelligence Engine - Self-Contained AI Analysis
No external APIs required - runs completely on your machine
"""

import os
import re
from datetime import datetime
from collections import defaultdict

class AIFileAnalyzer:
    """
    Sentinel Intelligence Engine
    Self-contained AI using advanced pattern recognition and semantic analysis
    """
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self._initialize_intelligence()
    
    def _initialize_intelligence(self):
        """Initialize the Sentinel's intelligence patterns"""
        self.logger.log_event("Sentinel Intelligence Engine activated - Self-contained AI ready", "SYSTEM")
        
        # Knowledge base of file patterns
        self.file_categories = {
            'images': {
                'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff', '.heic'],
                'keywords': ['photo', 'image', 'img', 'pic', 'screenshot', 'wallpaper', 'avatar', 'icon'],
                'priority': 'organize'
            },
            'documents': {
                'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
                'keywords': ['report', 'doc', 'letter', 'resume', 'cv', 'notes', 'invoice', 'receipt'],
                'priority': 'archive'
            },
            'spreadsheets': {
                'extensions': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
                'keywords': ['data', 'sheet', 'budget', 'finance', 'expense', 'tracking'],
                'priority': 'archive'
            },
            'presentations': {
                'extensions': ['.ppt', '.pptx', '.key', '.odp'],
                'keywords': ['presentation', 'slides', 'deck'],
                'priority': 'archive'
            },
            'videos': {
                'extensions': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
                'keywords': ['video', 'movie', 'clip', 'recording', 'screen'],
                'priority': 'organize'
            },
            'audio': {
                'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
                'keywords': ['audio', 'music', 'song', 'sound', 'podcast', 'voice'],
                'priority': 'organize'
            },
            'archives': {
                'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
                'keywords': ['archive', 'backup', 'compressed'],
                'priority': 'archive'
            },
            'code': {
                'extensions': ['.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs', '.php', '.rb', '.swift'],
                'keywords': ['src', 'source', 'code', 'script', 'main', 'test'],
                'priority': 'keep'
            },
            'web': {
                'extensions': ['.html', '.htm', '.css', '.scss', '.sass', '.less'],
                'keywords': ['web', 'site', 'page', 'index', 'style'],
                'priority': 'keep'
            },
            'config': {
                'extensions': ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.xml'],
                'keywords': ['config', 'settings', 'package', 'manifest'],
                'priority': 'keep'
            },
            'temporary': {
                'extensions': ['.tmp', '.temp', '.bak', '.old', '.cache', '.log', '.swp', '.swo', '~'],
                'keywords': ['temp', 'backup', 'copy', 'old', 'cache', 'log'],
                'priority': 'delete'
            },
            'installers': {
                'extensions': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage'],
                'keywords': ['setup', 'install', 'installer', 'download'],
                'priority': 'cleanup'
            },
            'databases': {
                'extensions': ['.db', '.sqlite', '.sql', '.mdb', '.accdb'],
                'keywords': ['database', 'data', 'backup'],
                'priority': 'keep'
            }
        }
    
    def analyze_files(self, file_list):
        """
        Sentinel Intelligence Analysis
        Uses advanced pattern recognition and semantic analysis
        
        Args:
            file_list: List of file paths or file info dicts
        
        Returns:
            dict: Analysis results with intelligent suggestions
        """
        if not file_list:
            return {"analysis": "No files to analyze.", "suggestions": []}
        
        # Prepare file information
        file_info = self._prepare_file_info(file_list)
        
        # Run Sentinel Intelligence Engine
        return self._sentinel_intelligence_analysis(file_info)
    
    def _prepare_file_info(self, file_list):
        """Prepare file information for AI analysis"""
        info = []
        
        for item in file_list[:50]:  # Limit to 50 files
            if isinstance(item, dict):
                file_path = item.get("path", "")
            else:
                file_path = item
            
            if os.path.exists(file_path):
                try:
                    stat = os.stat(file_path)
                    info.append({
                        "name": os.path.basename(file_path),
                        "path": file_path,
                        "size_mb": stat.st_size / (1024 * 1024),
                        "extension": os.path.splitext(file_path)[1]
                    })
                except:
                    continue
        
        return info
    
    
    def _sentinel_intelligence_analysis(self, file_info):
        """
        Advanced Sentinel Intelligence Engine
        Multi-layer analysis with pattern recognition and semantic understanding
        """
        if not file_info:
            return {"analysis": "No files to analyze.", "suggestions": []}
        
        analysis_parts = []
        suggestions = []
        
        # Layer 1: Statistical Analysis
        total_size = sum(f['size_mb'] for f in file_info)
        total_files = len(file_info)
        
        analysis_parts.append("⚔️ SENTINEL INTELLIGENCE REPORT ⚔️\n")
        analysis_parts.append(f"📊 Scanned: {total_files} files | Total: {total_size:.1f} MB\n")
        
        # Layer 2: Semantic Category Classification
        categorized = self._categorize_files(file_info)
        
        analysis_parts.append("🧠 INTELLIGENT CATEGORIZATION:")
        for category, files in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
            if files:
                cat_size = sum(f['size_mb'] for f in files)
                percentage = (len(files) / total_files) * 100
                analysis_parts.append(f"   • {category.title()}: {len(files)} files ({cat_size:.1f} MB) - {percentage:.0f}%")
        
        # Layer 3: Pattern Recognition
        patterns = self._detect_patterns(file_info)
        
        if patterns['duplicates']:
            analysis_parts.append(f"\n🔍 PATTERN DETECTION:")
            analysis_parts.append(f"   ⚠️ Detected {len(patterns['duplicates'])} potential duplicate patterns")
            
        if patterns['naming_chaos']:
            analysis_parts.append(f"   ⚠️ Inconsistent naming detected in {patterns['naming_chaos']} files")
        
        if patterns['old_files']:
            analysis_parts.append(f"   📅 Found {len(patterns['old_files'])} files older than 90 days")
        
        # Layer 4: Intelligent Recommendations
        analysis_parts.append("\n💡 INTELLIGENT RECOMMENDATIONS:")
        
        # Analyze category priorities
        priority_actions = self._generate_priority_actions(categorized, patterns)
        
        for idx, action in enumerate(priority_actions[:5], 1):
            confidence_icon = "🟢" if action['confidence'] > 80 else "🟡" if action['confidence'] > 50 else "🟠"
            analysis_parts.append(f"   {idx}. {confidence_icon} {action['description']} (Confidence: {action['confidence']}%)")
            suggestions.append(action)
        
        # Layer 5: Strategic Insights
        insights = self._generate_insights(categorized, patterns, total_size)
        if insights:
            analysis_parts.append("\n🎯 STRATEGIC INSIGHTS:")
            for insight in insights:
                analysis_parts.append(f"   • {insight}")
        
        analysis_parts.append("\n\n✨ Powered by: Sentinel Intelligence Engine (Self-Contained AI)")
        analysis_parts.append("   No external APIs • 100% Private • Running on your machine")
        
        return {
            "analysis": "\n".join(analysis_parts),
            "suggestions": suggestions
        }
    
    def _categorize_files(self, file_info):
        """Intelligent file categorization using extension and semantic analysis"""
        categorized = defaultdict(list)
        
        for file in file_info:
            ext = file['extension'].lower()
            name = file['name'].lower()
            
            # Multi-factor classification
            category = 'uncategorized'
            max_score = 0
            
            for cat_name, cat_data in self.file_categories.items():
                score = 0
                
                # Extension match (high weight)
                if ext in cat_data['extensions']:
                    score += 50
                
                # Keyword match in filename (medium weight)
                for keyword in cat_data['keywords']:
                    if keyword in name:
                        score += 20
                        break
                
                if score > max_score:
                    max_score = score
                    category = cat_name
            
            categorized[category].append(file)
        
        return categorized
    
    def _detect_patterns(self, file_info):
        """Advanced pattern detection in files"""
        patterns = {
            'duplicates': [],
            'naming_chaos': 0,
            'old_files': [],
            'large_files': [],
            'series': []
        }
        
        # Detect potential duplicates (similar names)
        names = [f['name'].lower() for f in file_info]
        name_counts = defaultdict(int)
        
        for name in names:
            # Remove numbers and common suffixes to find patterns
            base_name = re.sub(r'\d+|_copy|_\(\d+\)|\s-\scopy', '', name)
            name_counts[base_name] += 1
        
        patterns['duplicates'] = [name for name, count in name_counts.items() if count > 1]
        
        # Detect naming inconsistency
        has_camel = sum(1 for f in file_info if re.search(r'[a-z][A-Z]', f['name']))
        has_snake = sum(1 for f in file_info if '_' in f['name'])
        has_kebab = sum(1 for f in file_info if '-' in f['name'])
        
        if min(has_camel, has_snake, has_kebab) > 0 and max(has_camel, has_snake, has_kebab) > 5:
            patterns['naming_chaos'] = len(file_info)
        
        # Detect large files
        patterns['large_files'] = [f for f in file_info if f['size_mb'] > 100]
        
        # Detect file series (photo_1, photo_2, etc.)
        series_pattern = defaultdict(list)
        for f in file_info:
            base = re.sub(r'\d+', '#', f['name'])
            series_pattern[base].append(f)
        
        patterns['series'] = [files for files in series_pattern.values() if len(files) > 3]
        
        return patterns
    
    def _generate_priority_actions(self, categorized, patterns):
        """Generate prioritized action recommendations"""
        actions = []
        
        # Priority 1: Clean temporary files
        if 'temporary' in categorized and categorized['temporary']:
            temp_size = sum(f['size_mb'] for f in categorized['temporary'])
            actions.append({
                'action': 'cleanup',
                'description': f"Clean {len(categorized['temporary'])} temporary files to free {temp_size:.1f} MB",
                'confidence': 95,
                'files': categorized['temporary']
            })
        
        # Priority 2: Archive old installers
        if 'installers' in categorized and categorized['installers']:
            inst_size = sum(f['size_mb'] for f in categorized['installers'])
            actions.append({
                'action': 'archive',
                'description': f"Archive {len(categorized['installers'])} installer files ({inst_size:.1f} MB)",
                'confidence': 85,
                'files': categorized['installers']
            })
        
        # Priority 3: Organize media by type
        media_cats = ['images', 'videos', 'audio']
        total_media = sum(len(categorized.get(cat, [])) for cat in media_cats)
        
        if total_media > 20:
            actions.append({
                'action': 'organize',
                'description': f"Organize {total_media} media files into type-specific folders",
                'confidence': 90,
                'categories': media_cats
            })
        
        # Priority 4: Compress large files
        if patterns['large_files']:
            large_size = sum(f['size_mb'] for f in patterns['large_files'])
            actions.append({
                'action': 'compress',
                'description': f"Compress {len(patterns['large_files'])} large files ({large_size:.1f} MB) to save space",
                'confidence': 70,
                'files': patterns['large_files']
            })
        
        # Priority 5: Archive old documents
        if 'documents' in categorized and len(categorized['documents']) > 10:
            actions.append({
                'action': 'archive',
                'description': f"Archive {len(categorized['documents'])} document files for long-term storage",
                'confidence': 75,
                'files': categorized['documents']
            })
        
        # Priority 6: Organize by category
        total_cats = len([c for c in categorized if categorized[c]])
        if total_cats > 5:
            actions.append({
                'action': 'organize',
                'description': f"Create category-based folder structure for {total_cats} file types",
                'confidence': 85
            })
        
        return sorted(actions, key=lambda x: x['confidence'], reverse=True)
    
    def _generate_insights(self, categorized, patterns, total_size):
        """Generate strategic insights about the file collection"""
        insights = []
        
        # Space usage insight
        if total_size > 1000:
            insights.append(f"Large collection detected ({total_size:.1f} MB). Consider archiving or cloud storage.")
        
        # Category dominance
        largest_cat = max(categorized.items(), key=lambda x: len(x[1])) if categorized else None
        if largest_cat and len(largest_cat[1]) > len(categorized.get('uncategorized', [])) * 2:
            percentage = (len(largest_cat[1]) / sum(len(v) for v in categorized.values())) * 100
            insights.append(f"{largest_cat[0].title()} files dominate ({percentage:.0f}%) - specialized organization recommended")
        
        # Duplicate concern
        if len(patterns['duplicates']) > 5:
            insights.append(f"High duplicate pattern count suggests manual review needed")
        
        # Series detection
        if patterns['series']:
            insights.append(f"Detected {len(patterns['series'])} file series - consider grouping into subfolders")
        
        return insights
    
    def suggest_folder_structure(self, base_path, file_extensions):
        """Suggest intelligent folder structure based on file types"""
        # Group extensions by category
        structure = {}
        
        for ext in file_extensions:
            for cat_name, cat_data in self.file_categories.items():
                if ext in cat_data['extensions']:
                    if cat_name not in structure:
                        structure[cat_name] = []
                    structure[cat_name].append(ext)
                    break
        
        # Generate folder structure suggestion
        suggestion = f"Suggested structure for {base_path}:\n\n"
        for category, extensions in structure.items():
            suggestion += f"📁 {category.title()}/\n"
            suggestion += f"   Extensions: {', '.join(extensions)}\n\n"
        
        return suggestion
