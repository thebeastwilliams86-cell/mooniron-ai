# Moon-Iron System Sentinel - Advanced Features Guide

## 🧠 Intelligence Systems

### 1. Learning Mode - Adaptive Intelligence
**Location**: `intelligence/learning.py`

The Sentinel learns from every action you take:

**What It Tracks:**
- Every action you perform (cleanup, organize, archive)
- Your acceptance/rejection of suggestions
- Preferred cleanup ages
- Favorite organization styles
- File type preferences

**How It Adapts:**
- Adjusts confidence scores based on your history
- Filters out suggestions you consistently reject
- Recommends actions you frequently use
- Predicts your next likely action

**Example Learning Cycle:**
```
1. Sentinel suggests cleanup of 30-day old files
2. You accept → Confidence increases to 95%
3. Next time, similar suggestions appear first
4. After 10 actions, Sentinel predicts you'll cleanup next
```

**Stats Tracked:**
- Total actions: How many times you've used each feature
- Files cleaned/organized/archived
- Space freed (in MB)
- Learning since date
- Favorite action with usage count

### 2. Predictive Cleanup - Anticipatory Intelligence
**Location**: `intelligence/predictor.py`

Predicts what you'll want to clean BEFORE you ask:

**Prediction Factors:**
1. **Age Analysis**: Compares file age to your preferences
2. **Extension Analysis**: Identifies temp files (.tmp, .bak, .old)
3. **Size Analysis**: Flags large unused files
4. **Naming Patterns**: Detects "copy", "old", "backup" in names
5. **Usage Patterns**: Tracks which files you typically clean

**Confidence Scoring:**
- Each factor contributes to overall confidence (0-100%)
- Multiple factors = higher confidence
- Sorted by confidence for best suggestions first

**Space Predictions:**
- Estimates days until disk is full
- Recommends proactive actions
- Urgency levels (high/medium/low)

### 3. Smart Scheduling - Idle Detection
**Location**: `intelligence/scheduler.py`

Runs tasks automatically when your system is idle:

**Idle Detection:**
- Monitors CPU usage (idle if <20%)
- Tracks disk I/O activity
- Waits for low-activity periods
- Typical idle windows: 2-6 AM, lunch hours

**Schedule Types:**
- **Idle**: Run when system is quiet
- **Daily**: Run at specific time each day
- **Weekly**: Run on specific day/time
- **Monthly**: Run on specific date

**Smart Features:**
- Never interrupts your work
- Automatically calculates next run time
- Tracks last execution
- Enable/disable individual tasks

### 4. File Relationship Detection
**Location**: `intelligence/relationships.py`

Understands how files relate to each other:

**Relationship Types:**

**a) Project Folders**
- Detects code repositories
- Identifies work projects
- Confidence scoring based on:
  - Number of code files
  - Presence of README
  - .gitignore file
  - package.json
  - Config files

**b) File Series**
- photo_1.jpg, photo_2.jpg, photo_3.jpg
- document_v1.doc, document_v2.doc
- Detects numbering patterns
- Identifies sequential vs non-sequential

**c) Backup Pairs**
- original.txt → original - copy.txt
- document.docx → document (1).docx
- Groups files with common base names
- Identifies original vs backups

**d) Related Media**
- Photos taken in same hour
- Videos from same event
- Groups by creation time
- Minimum 5 files per group

**e) Temporal Groups**
- Files from same month
- Batch downloads
- Project snapshots
- Minimum 10 files per period

## 🛠️ Automation Systems

### 5. Undo System - Complete Safety Net
**Location**: `automation/undo.py`

Full rollback capability for all operations:

**How It Works:**
1. Before any change, creates checkpoint
2. Backs up all affected files
3. Stores metadata about operation
4. Enables one-click undo

**Checkpoint Data:**
- Timestamp of operation
- Operation type and description
- List of all affected files
- Complete file backups
- Total size backed up

**Undo Capabilities:**
- Undo last operation
- Undo specific checkpoint by ID
- View complete history
- Restore any previous state

**Space Management:**
- Automatic cleanup of old backups (30+ days)
- Configurable retention period
- Space-efficient storage

**Usage:**
```python
# Before cleanup
checkpoint_id = undo.create_checkpoint(
    "cleanup",
    "Remove temp files",
    ["/path/to/file1.tmp", "/path/to/file2.bak"]
)

# If something goes wrong
undo.undo_checkpoint(checkpoint_id)
```

### 6. Custom Rules Engine - Your Organization, Your Way
**Location**: `automation/custom_rules.py`

Define exactly how YOU want files organized:

**Rule Structure:**
```json
{
  "name": "Screenshots to Screenshots folder",
  "conditions": [
    {"type": "filename_contains", "value": "screenshot"}
  ],
  "actions": [
    {"type": "move", "destination": "Screenshots"}
  ],
  "priority": 10
}
```

**Condition Types:**
- **filename_contains**: Check if filename contains text
- **filename_matches**: Wildcard pattern matching
- **extension_is**: Match specific file extension
- **size_mb**: Compare file size (>, <, =)
- **age_days**: Compare file age (>, <)
- **folder_contains**: Path contains specific folder
- **regex_match**: Advanced regex patterns

**Action Types:**
- **move**: Move to destination folder
- **archive**: Archive to specified location
- **cleanup**: Mark for cleanup
- **organize**: Organize by type

**Priority System:**
- Higher priority runs first
- Range: 0-100
- Default: 5
- Critical rules: 10+

**Default Rules Included:**
1. Screenshots → Screenshots folder
2. Old downloads (90+ days) → Archive

## 📊 How Everything Works Together

### Typical Workflow:

1. **You analyze a folder** →
   - Sentinel Intelligence Engine categorizes files
   - Learning Mode checks your historical preferences
   - Predictive Cleanup identifies likely targets
   - File Relationships detects patterns
   - Custom Rules apply your personal organization

2. **Sentinel suggests actions** →
   - Confidence scores adjusted by learning
   - Predictions sorted by likelihood
   - Rule-based actions included
   - Relationship-aware groupings

3. **You accept/reject** →
   - Learning Mode records your choice
   - Confidence scores update
   - Preferences adapt
   - Future suggestions improve

4. **Smart Scheduler activates** →
   - Waits for idle time
   - Runs approved tasks automatically
   - Creates checkpoints before changes
   - Enables undo if needed

## 🎯 Power User Features

### Confidence Calibration
- Each suggestion has confidence score
- Learning adjusts scores over time
- 95%+ = Almost certain you'll accept
- <30% = Probably won't suggest

### Pattern Recognition
- Detects duplicate naming patterns
- Identifies file series automatically
- Groups related projects
- Finds temporal relationships

### Predictive Actions
- "You'll probably want to cleanup next" (85% confidence)
- "Disk C: will be full in ~45 days"
- "Detected 12 file series for grouping"

### Complete Safety
- Every change creates checkpoint
- Full undo for all operations
- 30-day backup retention
- One-click restore

## 📈 Learning Stats

View what Sentinel has learned:
- Favorite actions with counts
- Total operations performed
- Space freed over time
- Preferred cleanup thresholds
- Prediction accuracy
- Next action prediction

## 🔮 Future Predictions

Sentinel can predict:
- What action you'll take next
- When you'll need cleanup
- Which files will be organized
- Space usage trends
- Days until disks fill

---

**All systems running locally. No external APIs. 100% private. Gets smarter every time you use it.**
