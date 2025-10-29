"""Main GUI window for the Moon-Iron System Sentinel"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os

from monitors.system_health import SystemHealthMonitor
from monitors.folder_watcher import FolderWatcher, FolderAnalyzer
from ai.analyzer import AIFileAnalyzer
from automation.tasks import AutomationTasks
from SentinelForge.ai.web_search import generate_response

class SentinelGUI:
    def __init__(self, root, config, logger):
        self.root = root
        self.config = config
        self.logger = logger
        self.root.title("Moon-Iron System Sentinel")
        self.root.geometry("900x700")

        self.health_monitor = SystemHealthMonitor()
        self.folder_analyzer = FolderAnalyzer(logger)
        self.ai_analyzer = AIFileAnalyzer(logger, config)
        self.automation = AutomationTasks(logger, config)
        self.folder_watcher = None

        self.setup_ui()
        self.update_system_health()
        self.auto_refresh()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_dashboard_tab()
        self.create_folder_monitor_tab()
        self.create_automation_tab()
        self.create_logs_tab()
        self.create_config_tab()

    def create_dashboard_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚔️ Dashboard")

        title = tk.Label(tab, text="System Sentinel Dashboard", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        health_frame = ttk.LabelFrame(tab, text="System Health", padding=10)
        health_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.health_text = scrolledtext.ScrolledText(health_frame, height=15, wrap=tk.WORD)
        self.health_text.pack(fill=tk.BOTH, expand=True)

        chat_frame = ttk.LabelFrame(tab, text="Sentinel Chat", padding=10)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=10, font=("Courier", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.insert(tk.END, "🌙 Sentinel: I await your query...\n\n")
        self.chat_display.config(state=tk.DISABLED)

        self.input_box = tk.Entry(chat_frame, width=80, font=("Courier", 12))
        self.input_box.pack(padx=10, pady=(0,10))
        self.input_box.bind("<Return>", lambda event: self.handle_input())

        self.send_button = tk.Button(chat_frame, text="Send", command=self.handle_input)
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

    def create_folder_monitor_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📁 Folder Monitor")

        list_frame = ttk.LabelFrame(tab, text="Monitored Folders", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.folder_listbox = tk.Listbox(list_frame, height=8)
        self.folder_listbox.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(btn_frame, text="➕ Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="➖ Remove Folder", command=self.remove_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔍 Analyze Selected", command=self.analyze_folder).pack(side=tk.LEFT, padx=5)

        results_frame = ttk.LabelFrame(tab, text="Analysis Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.analysis_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)

        self.update_folder_list()

    def create_automation_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🤖 Automation")

        cleanup_frame = ttk.LabelFrame(tab, text="File Cleanup", padding=10)
        cleanup_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(cleanup_frame, text="Clean files older than (days):").pack(side=tk.LEFT, padx=5)
        self.cleanup_days = tk.Entry(cleanup_frame, width=10)
        self.cleanup_days.insert(0, "30")
        self.cleanup_days.pack(side=tk.LEFT, padx=5)

        ttk.Button(cleanup_frame, text="🧹 Preview Cleanup", command=self.preview_cleanup).pack(side=tk.LEFT, padx=5)
        ttk.Button(cleanup_frame, text="✅ Execute Cleanup", command=self.execute_cleanup).pack(side=tk.LEFT, padx=5)

        archive_frame = ttk.LabelFrame(tab, text="Archive Old Files", padding=10)
        archive_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(archive_frame, text="📦 Archive Files", command=self.archive_files).pack(side=tk.LEFT, padx=5)

        ai_frame = ttk.LabelFrame(tab, text="AI Suggestions", padding=10)
        ai_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(ai_frame, text="🧠 Get AI Suggestions", command=self.get_ai_suggestions).pack(side=tk.LEFT, padx=5)

        defrag_frame = ttk.LabelFrame(tab, text="Defragmentation (Placeholder)", padding=10)
        defrag_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(defrag_frame, text="🧩 Run Defragment", command=lambda: self.automation_text.insert(tk.END, "🧩 Defragmentation started...\n")).pack(side=tk.LEFT, padx=5)

        results_frame = ttk.LabelFrame(tab, text="Automation Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.automation_text = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.automation_text.pack(fill=tk.BOTH, expand=True)

    def create_logs_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📜 Logs")

        self.logs_text = scrolledtext.ScrolledText(tab, height=25, wrap=tk.WORD)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update_logs()

    def create_config_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Config")

        frame = ttk.LabelFrame(tab, text="Configuration Settings", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="Scan Interval (sec):").grid(row=0, column=0, sticky="w")
        self.scan_interval = tk.Entry(frame, width=10)
        self.scan_interval.insert(0, str(self.config.get("scan_interval", 60)))
        self.scan_interval.grid(row=0, column=1)

        tk.Label(frame, text="Cleanup Threshold (GB):").grid(row=1, column=0, sticky="w")
        self.cleanup_threshold = tk.Entry(frame, width=10)
        self.cleanup_threshold.insert(0, str(self.config.get("auto_cleanup_threshold_gb", 1.0)))
        self.cleanup_threshold.grid(row=1, column=1)

        self.auto_actions_var = tk.BooleanVar(value=self.config.get("enable_auto_actions", False))
        tk.Checkbutton(frame, text="Enable Auto Actions", variable=self.auto_actions_var).grid(row=2, columnspan=2, sticky="w")

        tk.Label(frame, text="OpenAI Model:").grid(row=3, column=0, sticky="w")
        self.ai_model = tk.Entry(frame, width=20)
        self.ai_model.insert(0, self.config.get("openai_model", "gpt-4"))
        self.ai_model.grid(row=3, column=1)

        ttk.Button(frame, text="💾 Save Config", command=self.save_config).grid(row=4, columnspan=2, pady=10)

    def
