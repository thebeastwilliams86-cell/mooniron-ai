"""
Learning Mode - Sentinel Memory System
Tracks user preferences and adapts recommendations over time
"""

import json
import os
from datetime import datetime
from collections import defaultdict

class SentinelLearning:
    """
    Machine learning system that remembers user preferences
    and adapts suggestions based on behavior patterns
    """
    
    def __init__(self, logger, learning_file="sentinel_memory.json"):
        self.logger = logger
        self.learning_file = learning_file
        self.memory = self.load_memory()
        
    def load_memory(self):
        """Load the Sentinel's learned patterns"""
        if os.path.exists(self.learning_file):
            try:
                with open(self.learning_file, 'r') as f:
                    return json.load(f)
            except:
                return self._initialize_memory()
        return self._initialize_memory()
    
    def _initialize_memory(self):
        """Initialize learning memory structure"""
        return {
            "user_actions": [],
            "preferences": {
                "favorite_actions": defaultdict(int),
                "avoided_actions": defaultdict(int),
                "folder_patterns": {},
                "file_type_preferences": {},
                "cleanup_thresholds": {},
                "organization_style": "by_type"
            },
            "patterns": {
                "cleanup_frequency": 0,
                "organization_frequency": 0,
                "archive_frequency": 0,
                "avg_cleanup_age_days": 30,
                "preferred_times": []
            },
            "stats": {
                "total_actions": 0,
                "files_cleaned": 0,
                "files_organized": 0,
                "files_archived": 0,
                "space_freed_mb": 0,
                "learning_since": datetime.now().isoformat()
            }
        }
    
    def save_memory(self):
        """Persist learned patterns"""
        with open(self.learning_file, 'w') as f:
            json.dump(self.memory, f, indent=2, default=str)
    
    def record_action(self, action_type, details, accepted=True):
        """
        Record a user action for learning
        
        Args:
            action_type: Type of action (cleanup, organize, archive, etc.)
            details: Dict with action details
            accepted: Whether user accepted the suggestion
        """
        action_record = {
            "timestamp": datetime.now().isoformat(),
            "type": action_type,
            "accepted": accepted,
            "details": details
        }
        
        self.memory["user_actions"].append(action_record)
        
        # Update preferences
        if accepted:
            self.memory["preferences"]["favorite_actions"][action_type] = \
                self.memory["preferences"]["favorite_actions"].get(action_type, 0) + 1
            
            # Track patterns
            if action_type == "cleanup":
                self.memory["patterns"]["cleanup_frequency"] += 1
                if "age_days" in details:
                    # Update average cleanup threshold
                    current_avg = self.memory["patterns"]["avg_cleanup_age_days"]
                    new_avg = (current_avg + details["age_days"]) / 2
                    self.memory["patterns"]["avg_cleanup_age_days"] = new_avg
            
            elif action_type == "organize":
                self.memory["patterns"]["organization_frequency"] += 1
                if "style" in details:
                    self.memory["preferences"]["organization_style"] = details["style"]
            
            elif action_type == "archive":
                self.memory["patterns"]["archive_frequency"] += 1
        
        else:
            self.memory["preferences"]["avoided_actions"][action_type] = \
                self.memory["preferences"]["avoided_actions"].get(action_type, 0) + 1
        
        # Update stats
        self.memory["stats"]["total_actions"] += 1
        if "files_count" in details:
            stat_key = f"files_{action_type}d"
            if stat_key in self.memory["stats"]:
                self.memory["stats"][stat_key] += details["files_count"]
        
        if "space_freed" in details:
            self.memory["stats"]["space_freed_mb"] += details["space_freed"]
        
        # Keep only last 1000 actions
        if len(self.memory["user_actions"]) > 1000:
            self.memory["user_actions"] = self.memory["user_actions"][-1000:]
        
        self.save_memory()
        self.logger.log_event(f"Learning: Recorded {action_type} action", "SYSTEM")
    
    def get_preferred_cleanup_age(self):
        """Get user's preferred cleanup age based on history"""
        return int(self.memory["patterns"]["avg_cleanup_age_days"])
    
    def get_action_confidence(self, action_type):
        """
        Calculate confidence that user will accept this action
        
        Returns: Confidence score 0-100
        """
        favorites = self.memory["preferences"]["favorite_actions"].get(action_type, 0)
        avoided = self.memory["preferences"]["avoided_actions"].get(action_type, 0)
        total = favorites + avoided
        
        if total == 0:
            return 50  # Neutral confidence
        
        confidence = (favorites / total) * 100
        return min(100, max(0, confidence))
    
    def should_suggest_action(self, action_type):
        """Determine if we should suggest this action based on learning"""
        confidence = self.get_action_confidence(action_type)
        
        # Don't suggest if user consistently rejects it
        if confidence < 30:
            return False
        
        return True
    
    def get_personalized_suggestions(self, base_suggestions):
        """
        Adapt suggestions based on learned preferences
        
        Args:
            base_suggestions: List of AI-generated suggestions
        
        Returns:
            Filtered and prioritized suggestions
        """
        personalized = []
        
        for suggestion in base_suggestions:
            action_type = suggestion.get("action", "unknown")
            
            # Skip if user consistently rejects this action
            if not self.should_suggest_action(action_type):
                continue
            
            # Adjust confidence based on user history
            user_confidence = self.get_action_confidence(action_type)
            base_confidence = suggestion.get("confidence", 50)
            
            # Weighted average: 70% AI confidence, 30% user history
            adjusted_confidence = (base_confidence * 0.7) + (user_confidence * 0.3)
            suggestion["confidence"] = int(adjusted_confidence)
            suggestion["learned"] = True
            
            personalized.append(suggestion)
        
        # Sort by adjusted confidence
        return sorted(personalized, key=lambda x: x["confidence"], reverse=True)
    
    def predict_next_action(self):
        """
        Predict what the user might want to do next
        
        Returns: Predicted action type and confidence
        """
        # Analyze recent action patterns
        recent_actions = self.memory["user_actions"][-20:]
        
        if not recent_actions:
            return None, 0
        
        # Count action types in recent history
        action_counts = defaultdict(int)
        for action in recent_actions:
            if action.get("accepted", False):
                action_counts[action["type"]] += 1
        
        if not action_counts:
            return None, 0
        
        # Find most common action
        predicted_action = max(action_counts.items(), key=lambda x: x[1])
        
        # Calculate confidence based on frequency
        total_recent = len(recent_actions)
        confidence = (predicted_action[1] / total_recent) * 100
        
        return predicted_action[0], int(confidence)
    
    def get_learning_stats(self):
        """Get statistics about what the Sentinel has learned"""
        stats = self.memory["stats"].copy()
        
        # Add derived stats
        if stats["total_actions"] > 0:
            favorite_actions = self.memory["preferences"]["favorite_actions"]
            if favorite_actions:
                most_used = max(favorite_actions.items(), key=lambda x: x[1])
                stats["favorite_action"] = most_used[0]
                stats["favorite_count"] = most_used[1]
        
        stats["total_patterns"] = len(self.memory["user_actions"])
        stats["preferred_cleanup_age"] = self.get_preferred_cleanup_age()
        
        predicted_action, confidence = self.predict_next_action()
        if predicted_action:
            stats["predicted_next_action"] = predicted_action
            stats["prediction_confidence"] = confidence
        
        return stats
    
    def generate_learning_report(self):
        """Generate a human-readable learning report"""
        stats = self.get_learning_stats()
        
        report = ["⚔️ SENTINEL LEARNING REPORT ⚔️\n"]
        report.append(f"📚 Learning since: {stats.get('learning_since', 'Unknown')}")
        report.append(f"📊 Total actions observed: {stats['total_actions']}\n")
        
        report.append("🎯 YOUR PREFERENCES:")
        if stats.get("favorite_action"):
            report.append(f"   • Most used action: {stats['favorite_action']} ({stats['favorite_count']} times)")
        
        report.append(f"   • Preferred cleanup age: {stats['preferred_cleanup_age']} days")
        
        if stats.get("predicted_next_action"):
            report.append(f"\n🔮 PREDICTION:")
            report.append(f"   • Next likely action: {stats['predicted_next_action']}")
            report.append(f"   • Confidence: {stats['prediction_confidence']}%")
        
        report.append(f"\n📈 STATISTICS:")
        report.append(f"   • Files cleaned: {stats.get('files_cleaned', 0)}")
        report.append(f"   • Files organized: {stats.get('files_organized', 0)}")
        report.append(f"   • Files archived: {stats.get('files_archived', 0)}")
        report.append(f"   • Space freed: {stats.get('space_freed_mb', 0):.1f} MB")
        
        return "\n".join(report)
