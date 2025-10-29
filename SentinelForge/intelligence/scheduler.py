"""
Smart Scheduling - Runs tasks when system is idle
"""

import psutil
import time
from datetime import datetime, timedelta
from threading import Thread, Event
import json
import os

class SmartScheduler:
    """
    Intelligent task scheduler that detects system idle time
    and runs maintenance when it won't disturb the user
    """
    
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self.is_running = False
        self.stop_event = Event()
        self.scheduled_tasks = []
        self.load_schedule()
        
    def load_schedule(self):
        """Load scheduled tasks from config"""
        schedule_file = "sentinel_schedule.json"
        if os.path.exists(schedule_file):
            try:
                with open(schedule_file, 'r') as f:
                    self.scheduled_tasks = json.load(f)
            except:
                self.scheduled_tasks = []
    
    def save_schedule(self):
        """Save scheduled tasks"""
        with open("sentinel_schedule.json", 'w') as f:
            json.dump(self.scheduled_tasks, f, indent=2, default=str)
    
    def is_system_idle(self, idle_threshold_minutes=5):
        """
        Detect if system is idle based on CPU and disk activity
        
        Args:
            idle_threshold_minutes: Minutes of low activity to consider idle
        
        Returns:
            bool: True if system appears idle
        """
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 20:  # System is busy
            return False
        
        # Check disk I/O
        disk_io = psutil.disk_io_counters()
        time.sleep(2)
        disk_io_after = psutil.disk_io_counters()
        
        # Calculate I/O rate
        read_rate = (disk_io_after.read_bytes - disk_io.read_bytes) / 2  # bytes per second
        write_rate = (disk_io_after.write_bytes - disk_io.write_bytes) / 2
        
        # If heavy I/O, not idle
        if read_rate > 1_000_000 or write_rate > 1_000_000:  # 1 MB/s
            return False
        
        return True
    
    def get_idle_windows(self):
        """
        Identify typical idle windows based on time of day
        
        Returns:
            List of (start_hour, end_hour) tuples
        """
        return [
            (2, 6),   # Late night: 2 AM - 6 AM
            (12, 13), # Lunch time: 12 PM - 1 PM
        ]
    
    def is_preferred_time(self):
        """Check if current time is in a typical idle window"""
        current_hour = datetime.now().hour
        
        for start, end in self.get_idle_windows():
            if start <= current_hour < end:
                return True
        
        return False
    
    def add_task(self, task_type, task_config, schedule_type="idle", schedule_params=None):
        """
        Add a task to the schedule
        
        Args:
            task_type: Type of task (cleanup, defrag, organize, etc.)
            task_config: Configuration for the task
            schedule_type: When to run (idle, daily, weekly, monthly)
            schedule_params: Additional scheduling parameters
        """
        task = {
            "id": len(self.scheduled_tasks) + 1,
            "type": task_type,
            "config": task_config,
            "schedule_type": schedule_type,
            "schedule_params": schedule_params or {},
            "last_run": None,
            "next_run": self._calculate_next_run(schedule_type, schedule_params),
            "enabled": True
        }
        
        self.scheduled_tasks.append(task)
        self.save_schedule()
        self.logger.log_event(f"Task scheduled: {task_type}", "SYSTEM")
        
        return task["id"]
    
    def _calculate_next_run(self, schedule_type, params):
        """Calculate next run time for a task"""
        now = datetime.now()
        
        if schedule_type == "idle":
            # Run at next idle detection
            return now.isoformat()
        
        elif schedule_type == "daily":
            # Run daily at specified hour (default 2 AM)
            hour = params.get("hour", 2)
            next_run = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            return next_run.isoformat()
        
        elif schedule_type == "weekly":
            # Run weekly on specified day (default Sunday)
            target_day = params.get("day", 6)  # 6 = Sunday
            days_ahead = target_day - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(hour=params.get("hour", 2), minute=0, second=0)
            return next_run.isoformat()
        
        elif schedule_type == "monthly":
            # Run monthly on specified day
            target_day = params.get("day", 1)
            if now.day >= target_day:
                # Next month
                if now.month == 12:
                    next_run = now.replace(year=now.year+1, month=1, day=target_day)
                else:
                    next_run = now.replace(month=now.month+1, day=target_day)
            else:
                next_run = now.replace(day=target_day)
            next_run = next_run.replace(hour=params.get("hour", 2), minute=0, second=0)
            return next_run.isoformat()
        
        return now.isoformat()
    
    def check_due_tasks(self):
        """Check which tasks are due to run"""
        due_tasks = []
        now = datetime.now()
        
        for task in self.scheduled_tasks:
            if not task.get("enabled", True):
                continue
            
            next_run = datetime.fromisoformat(task["next_run"])
            
            if task["schedule_type"] == "idle":
                # Check if system is idle
                if self.is_system_idle():
                    due_tasks.append(task)
            
            elif now >= next_run:
                due_tasks.append(task)
        
        return due_tasks
    
    def run_task(self, task, executor_callback):
        """
        Execute a scheduled task
        
        Args:
            task: Task definition
            executor_callback: Function to call to execute the task
        """
        self.logger.log_event(f"Running scheduled task: {task['type']}", "SYSTEM")
        
        try:
            # Call the executor
            result = executor_callback(task['type'], task['config'])
            
            # Update task
            task["last_run"] = datetime.now().isoformat()
            task["next_run"] = self._calculate_next_run(
                task["schedule_type"],
                task.get("schedule_params", {})
            )
            
            self.save_schedule()
            
            return result
        
        except Exception as e:
            self.logger.log_event(f"Scheduled task failed: {str(e)}", "ERROR")
            return None
    
    def start_monitoring(self, executor_callback):
        """
        Start the scheduler monitoring thread
        
        Args:
            executor_callback: Function to call when tasks are due
        """
        if self.is_running:
            return
        
        self.is_running = True
        self.stop_event.clear()
        
        def monitor_loop():
            self.logger.log_event("Smart Scheduler activated", "SYSTEM")
            
            while not self.stop_event.is_set():
                # Check for due tasks every 5 minutes
                due_tasks = self.check_due_tasks()
                
                for task in due_tasks:
                    if self.stop_event.is_set():
                        break
                    self.run_task(task, executor_callback)
                
                # Wait 5 minutes before next check
                self.stop_event.wait(300)
            
            self.logger.log_event("Smart Scheduler deactivated", "SYSTEM")
        
        self.monitor_thread = Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop the scheduler"""
        if not self.is_running:
            return
        
        self.stop_event.set()
        self.is_running = False
    
    def get_schedule_summary(self):
        """Get a summary of scheduled tasks"""
        summary = {
            "total_tasks": len(self.scheduled_tasks),
            "enabled_tasks": len([t for t in self.scheduled_tasks if t.get("enabled", True)]),
            "tasks_by_type": {},
            "next_run": None
        }
        
        for task in self.scheduled_tasks:
            if not task.get("enabled", True):
                continue
            
            task_type = task["type"]
            summary["tasks_by_type"][task_type] = summary["tasks_by_type"].get(task_type, 0) + 1
            
            # Find earliest next run
            next_run = datetime.fromisoformat(task["next_run"])
            if summary["next_run"] is None or next_run < summary["next_run"]:
                summary["next_run"] = next_run
        
        return summary
