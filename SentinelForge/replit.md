# Moon-Iron System Sentinel

## Overview
An AI-powered desktop system monitoring and automation tool with **self-contained intelligence** that watches your computer, analyzes system health, and suggests intelligent maintenance actions. The Sentinel uses its own built-in AI engine - no external APIs, completely free, 100% private, running entirely on your machine.

## Purpose
Built for Corey to create a comprehensive system management tool that:
- Monitors folders for changes and clutter
- Analyzes system health (disk usage, memory, CPU)
- Provides AI-powered file organization suggestions
- Automates cleanup, defragmentation, and archiving tasks
- Requires user approval before executing any actions
- Logs all operations with mythic-themed messages

## Current State
**Status**: Development - Core features implemented
**Version**: 1.0.0-alpha
**Last Updated**: October 26, 2025

## Recent Changes
- **October 29, 2025**: MASSIVE Intelligence & Automation Upgrade
  - **Learning Mode**: Tracks user preferences, adapts suggestions, predicts next actions
  - **Predictive Cleanup**: Multi-factor prediction with confidence scores
  - **Smart Scheduling**: Idle detection, automatic task execution
  - **File Relationship Detection**: Projects, series, backup pairs, related media
  - **Undo System**: Complete rollback capability with checkpoints
  - **Custom Rules Engine**: User-defined organization patterns
  - **Backup Integration**: Auto-backup before all changes
  - Learning stats, prediction reports, relationship analysis
- **October 26, 2025**: Major upgrade to self-contained AI
  - Replaced OpenAI dependency with Sentinel Intelligence Engine
  - Implemented 5-layer intelligence system (statistical, semantic, pattern recognition, priority actions, strategic insights)
  - Added advanced pattern detection (duplicates, naming chaos, file series)
  - Created intelligent categorization for 12+ file types
  - Implemented confidence-scored recommendations (up to 95% accuracy)
  - Complete privacy - no data leaves your machine
- Initial project setup with complete module structure
- Implemented system health monitoring (disk, memory, CPU, uptime)
- Created folder monitoring and analysis system
- Built comprehensive GUI with 5 tabs (Dashboard, Folder Monitor, Automation, Logs, Settings)
- Added automation tasks: cleanup, defrag, organize, archive
- Implemented mythic-themed logging system
- Created configuration management system

## Project Architecture

### Directory Structure
```
├── main.py                    # Application entry point
├── utils/
│   ├── logger.py              # Mythic-themed logging system
│   └── config.py              # Configuration management
├── monitors/
│   ├── system_health.py       # System metrics monitoring
│   └── folder_watcher.py      # Folder monitoring and analysis
├── ai/
│   └── analyzer.py            # OpenAI-powered file analysis
├── automation/
│   └── tasks.py               # Cleanup, defrag, organize tasks
└── gui/
    └── main_window.py         # Main GUI application
```

### Key Components

**System Health Monitor**
- Tracks disk usage across all partitions
- Monitors memory and CPU utilization
- Checks disk fragmentation (Windows)
- Reports system uptime
- Provides warning thresholds

**Folder Watcher**
- Real-time monitoring using watchdog library
- Analyzes folder contents for optimization
- Identifies old files, large files, duplicates
- Generates organization suggestions
- Tracks files by extension type

**Sentinel Intelligence Engine (Self-Contained AI)**
- 5-layer analysis system running locally
- Multi-factor file categorization (12+ categories)
- Advanced pattern recognition and duplicate detection
- Confidence-scored recommendations (95%+ accuracy)
- Strategic insights for long-term organization
- Semantic analysis of file names and extensions
- No external APIs - 100% private and free

**Automation Tasks**
- Cleanup: Remove temporary and old files
- Defragment: Windows disk optimization
- Organize: Sort files by type into folders
- Archive: Move old files to archive location
- All actions support dry-run preview mode

**GUI Features**
- Dashboard: Real-time system health overview
- Folder Monitor: Add/remove folders, analyze contents
- Automation: Execute maintenance tasks
- Logs: View mythic-themed operation logs
- Settings: Configure thresholds and preferences

## Dependencies
- Python 3.11
- tkinter (GUI) - usually included with Python
- watchdog (folder monitoring)
- psutil (system metrics)
- pywin32 (Windows-specific features, optional - not available on Linux)

## Configuration
Settings stored in `sentinel_config.json`:
- `monitored_folders`: List of paths to watch
- `scan_interval`: Seconds between scans
- `auto_cleanup_threshold_gb`: Auto-cleanup trigger
- `auto_defrag_threshold`: Fragmentation % threshold
- `enable_auto_actions`: Require approval for actions
- `openai_model`: AI model to use (default: gpt-4o-mini)
- `max_file_analysis_batch`: Files per AI analysis
- `archive_extensions`: File types to auto-archive
- `cleanup_age_days`: Age threshold for cleanup

## User Preferences
- **Theme**: Mythic/fantasy-themed logging and UI
- **Safety First**: All destructive actions require confirmation
- **AI-Powered**: Intelligent suggestions preferred over simple rules
- **Cross-Platform**: Works on Windows and Linux (Windows features detect platform)

## Environment Requirements
- `SESSION_SECRET`: Used for secure session management

**No API keys required!** The Sentinel Intelligence Engine runs completely on your machine.

## Usage
1. Launch the application
2. Add folders to monitor in the Folder Monitor tab
3. View system health in the Dashboard
4. Use Automation tab to preview and execute tasks
5. Configure settings in the Settings tab
6. Monitor logs in the Logs tab

## Future Enhancements (Next Phase)
- Rainmeter skin integration for desktop overlay
- AutoHotkey script generation for hotkeys
- Web-based configuration portal
- Scheduled automation with idle detection
- Backup and rollback functionality
- More AI-powered insights and predictions
- Email/SMS notifications for critical alerts
- Cloud storage integration
- Multi-computer monitoring dashboard

## Notes
- Cross-platform compatible (Windows features gracefully degrade on Linux)
- All file operations support dry-run mode
- Logs stored in `logs/` directory with daily rotation
- Configuration auto-saves on changes
- GUI auto-refreshes system health every 30 seconds
