"""
Predictive Cleanup - Anticipates organization needs
"""

from datetime import datetime, timedelta
from collections import defaultdict
import os

class PredictiveAnalyzer:
    """
    Predicts what files user will want to organize/cleanup
    based on patterns and behavior
    """
    
    def __init__(self, logger, learning_system):
        self.logger = logger
        self.learning = learning_system
    
    def predict_cleanup_targets(self, file_info):
        """
        Predict which files user will want to clean up
        
        Args:
            file_info: List of file information dicts
        
        Returns:
            List of files predicted for cleanup with confidence scores
        """
        predictions = []
        
        # Get user's preferred cleanup age
        preferred_age = self.learning.get_preferred_cleanup_age()
        
        cutoff_date = datetime.now() - timedelta(days=preferred_age)
        
        for file in file_info:
            prediction = {
                "file": file,
                "actions": [],
                "overall_confidence": 0
            }
            
            factors = []
            
            # Factor 1: Age matches user preference
            if 'modified_time' in file:
                file_age_days = (datetime.now() - file['modified_time']).days
                if file_age_days >= preferred_age:
                    age_confidence = min(100, (file_age_days / preferred_age) * 50)
                    factors.append(("age", age_confidence))
                    prediction["actions"].append("cleanup")
            
            # Factor 2: Temporary file extension
            if file.get('extension') in ['.tmp', '.bak', '.old', '.cache']:
                factors.append(("temp_extension", 95))
                if "cleanup" not in prediction["actions"]:
                    prediction["actions"].append("cleanup")
            
            # Factor 3: Large file that was never used
            if file.get('size_mb', 0) > 100:
                if file_age_days > 60:
                    factors.append(("large_unused", 80))
                    if "archive" not in prediction["actions"]:
                        prediction["actions"].append("archive")
            
            # Factor 4: File naming patterns user has cleaned before
            filename_lower = file.get('name', '').lower()
            if any(word in filename_lower for word in ['copy', 'old', 'backup', 'temp']):
                factors.append(("naming_pattern", 75))
                if "cleanup" not in prediction["actions"]:
                    prediction["actions"].append("cleanup")
            
            # Calculate overall confidence
            if factors:
                prediction["overall_confidence"] = sum(c for _, c in factors) / len(factors)
                prediction["factors"] = factors
                predictions.append(prediction)
        
        # Sort by confidence
        return sorted(predictions, key=lambda x: x["overall_confidence"], reverse=True)
    
    def predict_organization_needs(self, folder_path, file_info):
        """
        Predict how user will want to organize files
        
        Args:
            folder_path: Path being analyzed
            file_info: File information
        
        Returns:
            Organization strategy prediction with confidence
        """
        # Get user's preferred organization style
        org_style = self.learning.memory["preferences"].get("organization_style", "by_type")
        
        # Analyze file distribution
        extensions = defaultdict(int)
        categories = defaultdict(int)
        
        for file in file_info:
            ext = file.get('extension', '')
            extensions[ext] += 1
        
        # Predict organization strategy
        strategy = {
            "method": org_style,
            "confidence": 85,
            "reasoning": []
        }
        
        # If many different file types, suggest organization
        if len(extensions) > 5:
            strategy["reasoning"].append("Multiple file types detected")
            strategy["confidence"] += 10
        
        # Check if this matches a pattern user has organized before
        if folder_path in self.learning.memory["preferences"].get("folder_patterns", {}):
            previous_style = self.learning.memory["preferences"]["folder_patterns"][folder_path]
            strategy["method"] = previous_style
            strategy["reasoning"].append(f"Previously organized as '{previous_style}'")
            strategy["confidence"] = 95
        
        return strategy
    
    def anticipate_space_issues(self, disk_usage):
        """
        Predict if user will run out of space soon
        
        Args:
            disk_usage: Current disk usage info
        
        Returns:
            Prediction with recommended actions
        """
        predictions = []
        
        for disk in disk_usage:
            if disk["percent"] > 80:
                # High usage - predict need for cleanup
                days_until_full = self._estimate_days_until_full(disk)
                
                if days_until_full < 30:
                    predictions.append({
                        "disk": disk["mountpoint"],
                        "urgency": "high",
                        "days_until_full": days_until_full,
                        "recommended_action": "cleanup",
                        "confidence": 90
                    })
                elif days_until_full < 90:
                    predictions.append({
                        "disk": disk["mountpoint"],
                        "urgency": "medium",
                        "days_until_full": days_until_full,
                        "recommended_action": "archive",
                        "confidence": 70
                    })
        
        return predictions
    
    def _estimate_days_until_full(self, disk):
        """
        Estimate days until disk is full based on usage patterns
        Simple linear estimation - could be made smarter with historical data
        """
        free_gb = disk["free_gb"]
        
        # Assume 1GB per week growth (conservative estimate)
        weekly_growth = 1.0
        weeks_until_full = free_gb / weekly_growth
        
        return int(weeks_until_full * 7)
    
    def generate_predictive_report(self, file_info, disk_usage):
        """Generate a predictive analysis report"""
        report = ["🔮 PREDICTIVE ANALYSIS 🔮\n"]
        
        # Predict cleanup targets
        cleanup_predictions = self.predict_cleanup_targets(file_info)
        high_confidence_cleanup = [p for p in cleanup_predictions if p["overall_confidence"] > 70]
        
        if high_confidence_cleanup:
            report.append(f"🧹 CLEANUP PREDICTIONS:")
            report.append(f"   • {len(high_confidence_cleanup)} files predicted for cleanup")
            for pred in high_confidence_cleanup[:5]:
                file = pred["file"]
                report.append(f"   • {file.get('name', 'Unknown')}: {pred['overall_confidence']:.0f}% confidence")
        
        # Space predictions
        space_predictions = self.anticipate_space_issues(disk_usage)
        if space_predictions:
            report.append(f"\n⚠️ SPACE PREDICTIONS:")
            for pred in space_predictions:
                report.append(f"   • {pred['disk']}: ~{pred['days_until_full']} days until full")
                report.append(f"     Recommended: {pred['recommended_action']} ({pred['urgency']} urgency)")
        
        # Next action prediction
        next_action, confidence = self.learning.predict_next_action()
        if next_action:
            report.append(f"\n🎯 NEXT ACTION PREDICTION:")
            report.append(f"   • Likely next: {next_action} ({confidence}% confidence)")
        
        return "\n".join(report)
