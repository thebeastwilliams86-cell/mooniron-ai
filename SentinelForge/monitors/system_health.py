"""
System health monitoring for disk usage, fragmentation, and performance
"""

import psutil
import os
import platform
from datetime import datetime

class SystemHealthMonitor:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
    
    def get_disk_usage(self):
        """Get disk usage statistics for all partitions"""
        partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": usage.total / (1024**3),
                    "used_gb": usage.used / (1024**3),
                    "free_gb": usage.free / (1024**3),
                    "percent": usage.percent
                })
            except PermissionError:
                continue
        
        return disk_info
    
    def get_fragmentation_level(self, drive="C:"):
        """
        Get disk fragmentation level (Windows only)
        On Linux, returns 0 as fragmentation is less of an issue
        """
        if self.is_windows:
            try:
                import subprocess
                result = subprocess.run(
                    ['defrag', drive, '/A'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                # Parse defrag output for fragmentation percentage
                # This is a simplified version
                return self._parse_defrag_output(result.stdout)
            except Exception as e:
                return 0
        else:
            return 0
    
    def _parse_defrag_output(self, output):
        """Parse Windows defrag analysis output"""
        # Simplified parsing - in production would need more robust parsing
        for line in output.split('\n'):
            if 'fragmented' in line.lower():
                try:
                    # Extract percentage
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if '%' in part:
                            return float(part.replace('%', ''))
                except:
                    pass
        return 0
    
    def get_memory_usage(self):
        """Get current memory usage statistics"""
        mem = psutil.virtual_memory()
        return {
            "total_gb": mem.total / (1024**3),
            "available_gb": mem.available / (1024**3),
            "used_gb": mem.used / (1024**3),
            "percent": mem.percent
        }
    
    def get_cpu_usage(self, interval=1):
        """Get CPU usage percentage"""
        return psutil.cpu_percent(interval=interval)
    
    def get_system_uptime(self):
        """Get system uptime"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        return {
            "boot_time": boot_time,
            "uptime_seconds": uptime.total_seconds(),
            "uptime_days": uptime.days,
            "uptime_hours": uptime.seconds // 3600
        }
    
    def get_full_report(self):
        """Generate a comprehensive system health report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "disk_usage": self.get_disk_usage(),
            "memory": self.get_memory_usage(),
            "cpu_percent": self.get_cpu_usage(),
            "uptime": self.get_system_uptime(),
            "platform": platform.system(),
            "platform_version": platform.version()
        }
    
    def check_health_thresholds(self, disk_threshold=90, memory_threshold=85):
        """Check if system metrics exceed warning thresholds"""
        warnings = []
        
        # Check disk usage
        for disk in self.get_disk_usage():
            if disk["percent"] > disk_threshold:
                warnings.append(f"Disk {disk['mountpoint']} at {disk['percent']:.1f}% capacity")
        
        # Check memory
        mem = self.get_memory_usage()
        if mem["percent"] > memory_threshold:
            warnings.append(f"Memory usage at {mem['percent']:.1f}%")
        
        return warnings
