"""
Custom Rules Engine - User-defined organization patterns
"""

import json
import os
import re
from datetime import datetime
from fnmatch import fnmatch

class CustomRulesEngine:
    """
    Allows users to define custom file organization rules
    """
    
    def __init__(self, logger, rules_file="sentinel_rules.json"):
        self.logger = logger
        self.rules_file = rules_file
        self.rules = []
        self.load_rules()
    
    def load_rules(self):
        """Load custom rules from file"""
        if os.path.exists(self.rules_file):
            try:
                with open(self.rules_file, 'r') as f:
                    self.rules = json.load(f)
            except:
                self.rules = []
        
        # Add default rules if none exist
        if not self.rules:
            self.rules = self._get_default_rules()
            self.save_rules()
    
    def _get_default_rules(self):
        """Get default rule templates"""
        return [
            {
                "id": "rule_1",
                "name": "Screenshots to Screenshots folder",
                "enabled": True,
                "conditions": [
                    {"type": "filename_contains", "value": "screenshot", "case_sensitive": False}
                ],
                "actions": [
                    {"type": "move", "destination": "Screenshots"}
                ],
                "priority": 10
            },
            {
                "id": "rule_2",
                "name": "Old downloads cleanup",
                "enabled": True,
                "conditions": [
                    {"type": "folder_contains", "value": "Downloads"},
                    {"type": "age_days", "operator": ">", "value": 90}
                ],
                "actions": [
                    {"type": "archive", "destination": "Old Downloads"}
                ],
                "priority": 5
            }
        ]
    
    def save_rules(self):
        """Save rules to file"""
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=2)
    
    def add_rule(self, name, conditions, actions, priority=5):
        """
        Add a new custom rule
        
        Args:
            name: Rule name
            conditions: List of condition dicts
            actions: List of action dicts
            priority: Rule priority (higher = runs first)
        
        Returns:
            rule_id: ID of created rule
        """
        rule_id = f"rule_{len(self.rules) + 1}"
        
        rule = {
            "id": rule_id,
            "name": name,
            "enabled": True,
            "conditions": conditions,
            "actions": actions,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "match_count": 0
        }
        
        self.rules.append(rule)
        self.save_rules()
        
        self.logger.log_event(f"Custom rule added: {name}", "SYSTEM")
        
        return rule_id
    
    def evaluate_conditions(self, file_info, conditions):
        """
        Check if file matches all conditions
        
        Args:
            file_info: File information dict
            conditions: List of conditions to check
        
        Returns:
            bool: True if all conditions match
        """
        for condition in conditions:
            condition_type = condition["type"]
            
            if condition_type == "filename_contains":
                filename = file_info.get("name", "").lower()
                value = condition["value"].lower() if not condition.get("case_sensitive", False) else condition["value"]
                if value not in filename:
                    return False
            
            elif condition_type == "filename_matches":
                filename = file_info.get("name", "")
                pattern = condition["value"]
                if not fnmatch(filename, pattern):
                    return False
            
            elif condition_type == "extension_is":
                ext = file_info.get("extension", "")
                if ext != condition["value"]:
                    return False
            
            elif condition_type == "size_mb":
                size_mb = file_info.get("size_mb", 0)
                operator = condition.get("operator", "=")
                value = condition["value"]
                
                if operator == ">":
                    if not (size_mb > value):
                        return False
                elif operator == "<":
                    if not (size_mb < value):
                        return False
                elif operator == "=":
                    if not (size_mb == value):
                        return False
            
            elif condition_type == "age_days":
                if "modified_time" not in file_info:
                    return False
                
                age_days = (datetime.now() - file_info["modified_time"]).days
                operator = condition.get("operator", ">")
                value = condition["value"]
                
                if operator == ">":
                    if not (age_days > value):
                        return False
                elif operator == "<":
                    if not (age_days < value):
                        return False
            
            elif condition_type == "folder_contains":
                path = file_info.get("path", "")
                if condition["value"] not in path:
                    return False
            
            elif condition_type == "regex_match":
                filename = file_info.get("name", "")
                pattern = condition["value"]
                if not re.search(pattern, filename):
                    return False
        
        return True
    
    def apply_rules(self, file_list):
        """
        Apply custom rules to a list of files
        
        Args:
            file_list: List of file information dicts
        
        Returns:
            Dict of actions to take for each file
        """
        file_actions = {}
        
        # Sort rules by priority
        sorted_rules = sorted(
            [r for r in self.rules if r.get("enabled", True)],
            key=lambda x: x.get("priority", 0),
            reverse=True
        )
        
        for file_info in file_list:
            file_path = file_info.get("path")
            
            # Check each rule
            for rule in sorted_rules:
                if self.evaluate_conditions(file_info, rule["conditions"]):
                    # Rule matches!
                    rule["match_count"] = rule.get("match_count", 0) + 1
                    
                    # Apply actions
                    if file_path not in file_actions:
                        file_actions[file_path] = []
                    
                    for action in rule["actions"]:
                        file_actions[file_path].append({
                            "rule_id": rule["id"],
                            "rule_name": rule["name"],
                            "action": action
                        })
                    
                    # If rule says to stop processing, break
                    if rule.get("stop_on_match", False):
                        break
        
        self.save_rules()  # Save updated match counts
        
        return file_actions
    
    def get_rule_by_id(self, rule_id):
        """Get a specific rule"""
        for rule in self.rules:
            if rule["id"] == rule_id:
                return rule
        return None
    
    def update_rule(self, rule_id, updates):
        """Update an existing rule"""
        for rule in self.rules:
            if rule["id"] == rule_id:
                rule.update(updates)
                self.save_rules()
                self.logger.log_event(f"Rule updated: {rule['name']}", "SYSTEM")
                return True
        return False
    
    def delete_rule(self, rule_id):
        """Delete a rule"""
        self.rules = [r for r in self.rules if r["id"] != rule_id]
        self.save_rules()
        self.logger.log_event(f"Rule deleted: {rule_id}", "SYSTEM")
    
    def toggle_rule(self, rule_id):
        """Enable/disable a rule"""
        for rule in self.rules:
            if rule["id"] == rule_id:
                rule["enabled"] = not rule.get("enabled", True)
                self.save_rules()
                return rule["enabled"]
        return None
    
    def get_rules_summary(self):
        """Get summary of all rules"""
        return {
            "total_rules": len(self.rules),
            "enabled_rules": len([r for r in self.rules if r.get("enabled", True)]),
            "total_matches": sum(r.get("match_count", 0) for r in self.rules),
            "rules": self.rules
        }
