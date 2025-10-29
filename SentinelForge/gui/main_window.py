"""
Main GUI window for the Moon-Iron System Sentinel
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
from monitors.system_health import SystemHealthMonitor
from monitors.folder_watcher import FolderWatcher, FolderAnalyzer
from ai.analyzer import AIFileAnalyzer
from automation.tasks import AutomationTasks

class SentinelGUI:
    """Main application window"""
    import tkinter as tk
from tkinter import scrolledtext
from SentinelForge.ai.web_search import generate_response

class SentinelGUI:
    def __init__(self, root, config, logger):
        self.root = root
        self.config = config
        self.logger = logger
        self.root.title("Moon-Iron System Sentinel")

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Courier", 12))
        self.chat_display.pack(padx=10, pady=10)
        self.chat_display.insert(tk.END, "🌙 Sentinel: I await your query...\n\n")
        self.chat_display.config(state=tk.DISABLED)

        # Input box
        self.input_box = tk.Entry(root, width=80, font=("Courier", 12))
        self.input_box.pack(padx=10, pady=(0,10))
        self.input_box.bind("<Return>", lambda event: self.handle_input())

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.handle_input)
        self.send_button.pack(pady=(0,10))

    def handle_input(self):
        user_input = self.input_box.get()
        if not user_input.strip():
            return

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"🧍 You: {user_input}\n")
        response = generate_response(user_input)
        self.chat_display.insert(tk.END, f"🌙 Sentinel: {response}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        self.input_box.delete(0, tk.END)

    
    def __init__(self, root, config, logger):
        self.root = root
        self.config = config
        self.logger = logger
        
        self.root.title("Moon-Iron System Sentinel")
        self.root.geometry("900x700")
        
        # Initialize components
        self.health_monitor = SystemHealthMonitor()
        self.folder_analyzer = FolderAnalyzer(logger)
        self.ai_analyzer = AIFileAnalyzer(logger, config)
        self.automation = AutomationTasks(logger, config)
        self.folder_watcher = None
        
        # Setup GUI
        self.setup_ui()
        self.update_system_health()
        
        # Start auto-refresh
        self.auto_refresh()
    
    def setup_ui(self):
        """Create the user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_folder_monitor_tab()
        self.create_automation_tab()
        self.create_logs_tab()
        self.create_config_tab()
    
    def create_dashboard_tab(self):
        """Create system health dashboard"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚔️ Dashboard")
        
        # Title
        title = tk.Label(tab, text="System Sentinel Dashboard", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # System health frame
        health_frame = ttk.LabelFrame(tab, text="System Health", padding=10)
        health_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.health_text = scrolledtext.ScrolledText(health_frame, height=15, wrap=tk.WORD)
        self.health_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.update_system_health).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⚠️ Check Warnings", command=self.check_warnings).pack(side=tk.LEFT, padx=5)
    
    def create_folder_monitor_tab(self):
        """Create folder monitoring interface"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Folder Monitor")
        
        # Monitored folders list
        list_frame = ttk.LabelFrame(tab, text="Monitored Folders", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.folder_listbox = tk.Listbox(list_frame, height=8)
        self.folder_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Update folder list
        self.update_folder_list()
        
        # Buttons
        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="➕ Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="➖ Remove Folder", command=self.remove_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔍 Analyze Selected", command=self.analyze_folder).pack(side=tk.LEFT, padx=5)
        
        # Analysis results
        results_frame = ttk.LabelFrame(tab, text="Analysis Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.analysis_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
    
    def create_automation_tab(self):
        """Create automation controls"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🤖 Automation")
        
        # Cleanup section
        cleanup_frame = ttk.LabelFrame(tab, text="File Cleanup", padding=10)
        cleanup_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(cleanup_frame, text="Clean files older than (days):").pack(side=tk.LEFT, padx=5)
        self.cleanup_days = tk.Entry(cleanup_frame, width=10)
        self.cleanup_days.insert(0, "30")
        self.cleanup_days.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(cleanup_frame, text="🧹 Preview Cleanup", command=self.preview_cleanup).pack(side=tk.LEFT, padx=5)
        ttk.Button(cleanup_frame, text="✅ Execute Cleanup", command=self.execute_cleanup).pack(side=tk.LEFT, padx=5)
        
        # Defrag section
        defrag_frame = ttk.LabelFrame(tab, text="Disk Defragmentation", padding=10)
        defrag_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(defrag_frame, text="Drive:").pack(side=tk.LEFT, padx=5)
        self.drive_entry = tk.Entry(defrag_frame, width=5)
        self.drive_entry.insert(0, "C:")
        self.drive_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(defrag_frame, text="🗡️ Analyze Fragmentation", command=self.analyze_defrag).pack(side=tk.LEFT, padx=5)
        ttk.Button(defrag_frame, text="⚔️ Defragment", command=self.execute_defrag).pack(side=tk.LEFT, padx=5)
        
        # Organization section
        org_frame = ttk.LabelFrame(tab, text="File Organization", padding=10)
        org_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(org_frame, text="📊 Organize by Type", command=self.organize_by_type).pack(side=tk.LEFT, padx=5)
        ttk.Button(org_frame, text="📦 Archive Old Files", command=self.archive_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(org_frame, text="🧠 AI Suggestions", command=self.get_ai_suggestions).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = ttk.LabelFrame(tab, text="Automation Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.automation_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.automation_text.pack(fill=tk.BOTH, expand=True)
    
    def create_logs_tab(self):
        """Create logs viewer"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 Logs")
        
        # Logs display
        logs_frame = ttk.LabelFrame(tab, text="Sentinel Logs", padding=10)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20, wrap=tk.WORD, font=("Courier", 9))
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="🔄 Refresh Logs", command=self.update_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Clear Display", command=lambda: self.logs_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Load initial logs
        self.update_logs()
    
    def create_config_tab(self):
        """Create configuration interface"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Settings")
        
        # Configuration options
        config_frame = ttk.LabelFrame(tab, text="Configuration", padding=10)
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scan interval
        tk.Label(config_frame, text="Scan Interval (seconds):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.scan_interval = tk.Entry(config_frame, width=10)
        self.scan_interval.insert(0, str(self.config.get("scan_interval", 300)))
        self.scan_interval.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Auto cleanup threshold
        tk.Label(config_frame, text="Auto Cleanup Threshold (GB):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cleanup_threshold = tk.Entry(config_frame, width=10)
        self.cleanup_threshold.insert(0, str(self.config.get("auto_cleanup_threshold_gb", 5.0)))
        self.cleanup_threshold.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Enable auto actions
        self.auto_actions_var = tk.BooleanVar(value=self.config.get("enable_auto_actions", False))
        tk.Checkbutton(config_frame, text="Enable Auto Actions (requires approval)", variable=self.auto_actions_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # OpenAI model
        tk.Label(config_frame, text="AI Model:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.ai_model = tk.Entry(config_frame, width=20)
        self.ai_model.insert(0, self.config.get("openai_model", "gpt-4o-mini"))
        self.ai_model.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Save button
        ttk.Button(config_frame, text="💾 Save Configuration", command=self.save_config).grid(row=4, column=0, columnspan=2, pady=10)
    
    def update_system_health(self):
        """Update system health display"""
        self.health_text.delete(1.0, tk.END)
        self.health_text.insert(tk.END, "⚔️ THE SENTINEL'S VIGIL ⚔️\n\n", "title")
        
        report = self.health_monitor.get_full_report()
        
        # Disk usage
        self.health_text.insert(tk.END, "📊 DISK STATUS:\n", "header")
        for disk in report["disk_usage"]:
            status = "⚠️" if disk["percent"] > 80 else "✓"
            self.health_text.insert(tk.END, f"{status} {disk['mountpoint']}: {disk['percent']:.1f}% used ({disk['free_gb']:.1f} GB free)\n")
        
        # Memory
        self.health_text.insert(tk.END, "\n💾 MEMORY STATUS:\n", "header")
        mem = report["memory"]
        mem_status = "⚠️" if mem["percent"] > 80 else "✓"
        self.health_text.insert(tk.END, f"{mem_status} RAM: {mem['percent']:.1f}% used ({mem['available_gb']:.1f} GB available)\n")
        
        # CPU
        self.health_text.insert(tk.END, "\n⚡ CPU STATUS:\n", "header")
        cpu_status = "⚠️" if report["cpu_percent"] > 80 else "✓"
        self.health_text.insert(tk.END, f"{cpu_status} Usage: {report['cpu_percent']:.1f}%\n")
        
        # Uptime
        self.health_text.insert(tk.END, "\n⏱️ SYSTEM UPTIME:\n", "header")
        uptime = report["uptime"]
        self.health_text.insert(tk.END, f"The Sentinel has watched for {uptime['uptime_days']} days, {uptime['uptime_hours']} hours\n")
    
    def check_warnings(self):
        """Check for system warnings"""
        warnings = self.health_monitor.check_health_thresholds()
        
        if warnings:
            msg = "⚠️ THE SENTINEL WARNS:\n\n" + "\n".join(f"• {w}" for w in warnings)
            messagebox.showwarning("System Warnings", msg)
        else:
            messagebox.showinfo("System Status", "✓ All systems operating within normal parameters.\nThe realm is at peace.")
    
    def update_folder_list(self):
        """Update the monitored folders list"""
        self.folder_listbox.delete(0, tk.END)
        for folder in self.config.get("monitored_folders", []):
            self.folder_listbox.insert(tk.END, folder)
    
    def add_folder(self):
        """Add a folder to monitor"""
        folder = filedialog.askdirectory(title="Select Folder to Monitor")
        if folder:
            self.config.add_monitored_folder(folder)
            self.update_folder_list()
            self.logger.log_event(f"New watch established over {folder}", "SYSTEM")
    
    def remove_folder(self):
        """Remove selected folder from monitoring"""
        selection = self.folder_listbox.curselection()
        if selection:
            folder = self.folder_listbox.get(selection[0])
            self.config.remove_monitored_folder(folder)
            self.update_folder_list()
            self.logger.log_event(f"Watch removed from {folder}", "SYSTEM")
    
    def analyze_folder(self):
        """Analyze selected folder"""
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a folder to analyze.")
            return
        
        folder = self.folder_listbox.get(selection[0])
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, f"🔍 Analyzing {folder}...\n\n")
        
        def analyze():
            analysis = self.folder_analyzer.analyze_folder(folder)
            if analysis:
                self.display_analysis(analysis)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def display_analysis(self, analysis):
        """Display folder analysis results"""
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, f"📊 ANALYSIS: {analysis['path']}\n\n")
        self.analysis_text.insert(tk.END, f"Total Files: {analysis['total_files']}\n")
        self.analysis_text.insert(tk.END, f"Total Size: {analysis['total_size_mb']:.1f} MB\n\n")
        
        if analysis['suggestions']:
            self.analysis_text.insert(tk.END, "💡 SUGGESTIONS:\n")
            for suggestion in analysis['suggestions']:
                self.analysis_text.insert(tk.END, f"• {suggestion['message']}\n")
    
    def preview_cleanup(self):
        """Preview cleanup operation"""
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a folder to clean.")
            return
        
        folder = self.folder_listbox.get(selection[0])
        days = int(self.cleanup_days.get())
        
        results = self.automation.cleanup_temp_files(folder, age_days=days, dry_run=True)
        
        self.automation_text.delete(1.0, tk.END)
        self.automation_text.insert(tk.END, f"🧹 CLEANUP PREVIEW for {folder}\n\n")
        self.automation_text.insert(tk.END, f"Files to remove: {len(results['files_to_remove'])}\n")
        
        if results['files_to_remove']:
            total_size = sum(f['size_mb'] for f in results['files_to_remove'])
            self.automation_text.insert(tk.END, f"Space to free: {total_size:.1f} MB\n\n")
            self.automation_text.insert(tk.END, "Files:\n")
            for f in results['files_to_remove'][:20]:
                self.automation_text.insert(tk.END, f"• {os.path.basename(f['path'])} ({f['size_mb']:.1f} MB, {f['age_days']} days old)\n")
    
    def execute_cleanup(self):
        """Execute cleanup after confirmation"""
        if messagebox.askyesno("Confirm Cleanup", "Execute cleanup operation?\nThis will permanently remove files."):
            selection = self.folder_listbox.curselection()
            if not selection:
                return
            
            folder = self.folder_listbox.get(selection[0])
            days = int(self.cleanup_days.get())
            
            results = self.automation.cleanup_temp_files(folder, age_days=days, dry_run=False)
            
            self.automation_text.delete(1.0, tk.END)
            self.automation_text.insert(tk.END, "✅ CLEANUP COMPLETE\n\n")
            self.automation_text.insert(tk.END, f"Files removed: {results['files_removed']}\n")
            self.automation_text.insert(tk.END, f"Space freed: {results['space_freed_mb']:.1f} MB\n")
    
    def analyze_defrag(self):
        """Analyze disk fragmentation"""
        drive = self.drive_entry.get()
        results = self.automation.defragment_disk(drive, dry_run=True)
        
        self.automation_text.delete(1.0, tk.END)
        if "error" in results:
            self.automation_text.insert(tk.END, f"⚠️ {results['error']}\n")
        else:
            self.automation_text.insert(tk.END, f"🗡️ FRAGMENTATION ANALYSIS: {drive}\n\n")
            self.automation_text.insert(tk.END, results.get("output", "Analysis complete."))
    
    def execute_defrag(self):
        """Execute defragmentation"""
        if messagebox.askyesno("Confirm Defragmentation", "Reforge the Blade?\nThis may take several minutes."):
            drive = self.drive_entry.get()
            self.automation_text.delete(1.0, tk.END)
            self.automation_text.insert(tk.END, "⚔️ Reforging the Blade...\n\n")
            
            def defrag():
                results = self.automation.defragment_disk(drive, dry_run=False)
                self.root.after(0, lambda: self.show_defrag_results(results))
            
            threading.Thread(target=defrag, daemon=True).start()
    
    def show_defrag_results(self, results):
        """Show defragmentation results"""
        self.automation_text.delete(1.0, tk.END)
        if "error" in results:
            self.automation_text.insert(tk.END, f"⚠️ {results['error']}\n")
        else:
            self.automation_text.insert(tk.END, "✅ THE BLADE IS REFORGED\n\n")
            self.automation_text.insert(tk.END, results.get("output", "Defragmentation complete."))
    
    def organize_by_type(self):
        """Organize files by type"""
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a folder to organize.")
            return
        
        folder = self.folder_listbox.get(selection[0])
        
        if messagebox.askyesno("Confirm Organization", f"Organize files in {folder} by type?"):
            results = self.automation.organize_by_type(folder, dry_run=False)
            
            self.automation_text.delete(1.0, tk.END)
            self.automation_text.insert(tk.END, "📊 ORGANIZATION COMPLETE\n\n")
            self.automation_text.insert(tk.END, f"Files organized: {results['files_organized']}\n")
            if results['folders_created']:
                self.automation_text.insert(tk.END, f"Folders created: {', '.join(results['folders_created'])}\n")
    
    def archive_files(self):
        """Archive old files"""
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a folder.")
            return
        
        folder = self.folder_listbox.get(selection[0])
        archive_folder = filedialog.askdirectory(title="Select Archive Destination")
        
        if archive_folder:
            # Get old files
            analysis = self.folder_analyzer.analyze_folder(folder)
            if analysis and analysis['old_files']:
                files_to_archive = [f['path'] for f in analysis['old_files'][:50]]
                
                if messagebox.askyesno("Confirm Archive", f"Archive {len(files_to_archive)} old files?"):
                    results = self.automation.archive_files(files_to_archive, archive_folder, dry_run=False)
                    
                    self.automation_text.delete(1.0, tk.END)
                    self.automation_text.insert(tk.END, "📦 ARCHIVE COMPLETE\n\n")
                    self.automation_text.insert(tk.END, f"Files archived: {results['files_archived']}\n")
                    self.automation_text.insert(tk.END, f"Total size: {results['total_size_mb']:.1f} MB\n")
    
    def get_ai_suggestions(self):
        """Get AI-powered suggestions"""
        selection = self.folder_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a folder.")
            return
        
        folder = self.folder_listbox.get(selection[0])
        
        self.automation_text.delete(1.0, tk.END)
        self.automation_text.insert(tk.END, "🧠 Consulting the AI Oracle...\n\n")
        
        def get_suggestions():
            # Get file list
            files = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames[:50]:
                    files.append(os.path.join(root, filename))
            
            results = self.ai_analyzer.analyze_files(files)
            self.root.after(0, lambda: self.show_ai_suggestions(results))
        
        threading.Thread(target=get_suggestions, daemon=True).start()
    
    def show_ai_suggestions(self, results):
        """Display AI suggestions"""
        self.automation_text.delete(1.0, tk.END)
        
        if "error" in results:
            self.automation_text.insert(tk.END, f"⚠️ {results['error']}\n")
        else:
            self.automation_text.insert(tk.END, "🧠 AI ANALYSIS\n\n")
            self.automation_text.insert(tk.END, results.get("analysis", "No analysis available."))
    
    def save_config(self):
        """Save configuration"""
        self.config.set("scan_interval", int(self.scan_interval.get()))
        self.config.set("auto_cleanup_threshold_gb", float(self.cleanup_threshold.get()))
        self.config.set("enable_auto_actions", self.auto_actions_var.get())
        self.config.set("openai_model", self.ai_model.get())
        
        messagebox.showinfo("Configuration", "⚙️ Configuration saved successfully!")
        self.logger.log_event("Configuration updated", "SYSTEM")
    
    def update_logs(self):
        """Update logs display"""
        self.logs_text.delete(1.0, tk.END)
        logs = self.logger.get_recent_logs(100)
        for log in logs:
            self.logs_text.insert(tk.END, log)
    
    def auto_refresh(self):
        """Auto-refresh system health"""
        self.update_system_health()
        self.root.after(30000, self.auto_refresh)  # Refresh every 30 seconds
